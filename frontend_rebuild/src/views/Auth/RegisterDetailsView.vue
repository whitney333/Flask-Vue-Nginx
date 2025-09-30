<script setup>
    import { reactive, ref, onMounted, watch } from 'vue';
    import mishkanLogo from '@/assets/mishkan-logo.svg'
    import { useRouter } from 'vue-router';
    import { currentProfile } from '@/libs/current-profile';
    import { getAuth, updateProfile } from 'firebase/auth';
    import { useUserStore } from "@/stores/user.js";
    import axios from '@/axios';

    const userStore = useUserStore()
    const valid = ref(false)
    const router = useRouter()
    const errorMsg = ref()
    const loadingBar = ref(false)
    const name = reactive({
        firstname: '',
        lastname: ''
    })
    const companyName = ref('')
    const selectedTenantId = ref(null)
    const companies = ref([])
    const artists = ref([])
    const selectedArtists = ref([])
    const { currentUser } = getAuth()

    const nameRules = ref([
        value => {
            if (value) return true
            return 'Name is required.'
        },
        value => {
            if (/^[A-Za-z]+$/.test(value)) return true
            return 'Name must be valid.'
        },
    ])

    // if(profile) {
    //     router.push("/dashboard")
    // }
    //
    // if (!currentUser) {
    //     router.push("/auth/login")
    // } else {
    //     name.firstname = currentUser?.displayName?.split(" ")[0]
    //     name.lastname = currentUser?.displayName?.split(" ")[1]
    // }

    const handleCreateAccount = async () => {
        if (!nameRules.value.every((rule) => rule(name.firstname) && rule(name.lastname))){
            return
        }

        try {
            const { currentUser } = getAuth()
            const fullName = `${name.firstname} ${name.lastname}`
            await updateProfile(currentUser, { 
                displayName: fullName, 
                // photoURL: "https://example.com/jane-q-user/profile.jpg"
            })

            const idToken = await currentUser.getIdToken();
            const userDetails = {
                firebaseId: currentUser.uid,
                name: fullName,
                tenant: selectedTenantId.value, // company id
                image_url: currentUser.photoURL,
                email: currentUser.email,
                followed_artist: selectedArtists.value,
                firebaseToken: idToken
            }

            // send register details to backend
            const res = await axios.post('/user/v1/auth/register', userDetails)
            // fetch current user data from backend
            // get data from /v1/auth/firebaseId
            const user_profile = await axios.get(`/user/v1/auth/${currentUser.uid}`)
            console.log("user profile: ", user_profile)
            userStore.setFollowedArtists(user_profile.data.data["followed_artist"])

            // console.log("store followedArtists after set:", userStore.followedArtists)
            // redirect to /dashboard
            router.push("/dashboard");
        } catch(error) {
            // An error occurred
            // ...
            console.error(error);

        }
        
    }

    // onMounted(async () => {
    //   try {
    //     const res = await axios.get("/user/v1/company")
    //
    //     companies.value = res.data.data || []
    //
    //   } catch (err) {
    //     console.error("Error fetching tenant companies:", err)
    //   }
    // })

    onMounted(async () => {
      const auth = getAuth()
      const currentUser = auth.currentUser

      if (!currentUser) {
        console.log("No currentUser, redirecting...")
        return router.push("/auth/login")
      }

      try {
        const profile = await currentProfile()
        if (profile) {
          console.log("Profile exists, redirecting dashboard...")
          return router.push("/dashboard")
        }
      } catch (err) {
        console.error("currentProfile error:", err)
      }

      // 初始化名字顯示
      name.firstname = currentUser?.displayName?.split(" ")[0] || ''
      name.lastname = currentUser?.displayName?.split(" ")[1] || ''

      try {
        const res = await axios.get("/user/v1/company")
        companies.value = res.data.data || []
      } catch (err) {
        console.error("Error fetching tenant companies:", err)
      }
    })

    const handleCompanyChange = async (tenantId) => {
      selectedTenantId.value = tenantId   // store tenant id
      console.log("selected tenantId:", selectedTenantId.value)

      // get artists
      const res = await axios.get(`/user/v1/artists/${tenantId}`)
      console.log("artists:", res.data.data)
    }

    watch(selectedTenantId, async (newTenantId) => {
      if (!newTenantId) {
        artists.value = []
        selectedArtists.value = []
        return
      }

      try {
        const res = await axios.get(`/user/v1/artists/${newTenantId}`)
        artists.value = res.data.data || []
        // reset value
        selectedArtists.value = []
      } catch (err) {
        console.error(err)
        artists.value = []
        selectedArtists.value = []
      }
    })


</script>

<template>
    <v-container
        fluid
        :class="['fill-height', 'align-start', 'bg-grey-lighten-4']">
        
        <v-card
            :loading="loadingBar"
            class="ma-auto pb-10 pt-5 w-full max-w-[400px]"
            rounded="xl"
        >
            <template v-slot:text>
                <div :class="['flex-column', 'd-flex','justify-center', 'align-center']">

                    <img :src='mishkanLogo' alt="Mishkan"/>
                    <span :class="['text-h5']">{{ $t('Tell us more about you')}}</span>
                    <br />
                    <v-form ref="form" v-model="valid" @submit.prevent class="mb-2 w-full">
                        <div :class="['flex-column', 'd-flex','justify-center', 'ga-3']">
                            <div>
                                <div class='d-flex ga-3'>
                                    <v-text-field
                                        v-model="name.firstname"
                                        :class="['mb-1', 'w-full']"
                                        :rules="nameRules"
                                        :label="$t('First Name')"
                                        type="text"
                                        variant="solo-filled"
                                        flat
                                        rounded="lg"
                                        required
                                    ></v-text-field>
                                    <v-text-field
                                        v-model="name.lastname"
                                        :class="['mb-1', 'w-full']"
                                        :rules="nameRules"
                                        :label="$t('Last Name')"
                                        type="text"
                                        variant="solo-filled"
                                        flat
                                        rounded="lg"
                                        required
                                    ></v-text-field>
                                </div>
                                <v-autocomplete
                                    v-model="companyName"
                                    :items="companies"
                                    item-title="tenant_name"
                                    item-value="tenant_id"
                                    :label="$t('Company Name')"
                                    variant="solo-filled"
                                    flat
                                    rounded="lg"
                                    required
                                    @update:modelValue="handleCompanyChange"
                                ></v-autocomplete>
                                <v-select
                                    v-model="selectedArtists"
                                    :items="artists"
                                    :item-title="item => `${item.artist_name} (${item.korean_name})`"
                                    item-value="artist_objId"
                                    label="Artists You liked to track"
                                    multiple
                                    chips
                                    required
                                    variant="solo-filled"
                                    flat
                                    rounded="lg"
                                >
                                  <!-- selected artists -->
                                  <template #item="{ item, props }">
                                    <v-list-item v-bind="props">
                                      <template #prepend>
                                        <v-avatar size="24">
                                          <img :src="item.raw.imageURL" alt="avatar"/>
                                        </v-avatar>
                                      </template>
                                    </v-list-item>
                                  </template>
                                  <!-- chips for chosen artists -->
                                  <template #selection="{ item }">
                                    <v-chip class="ma-1" rounded size="small">
                                      <v-avatar size="20" start>
                                        <img :src="item.raw.imageURL" alt="avatar"/>
                                      </v-avatar>
                                      {{ item.raw.artist_name }}
                                    </v-chip>
                                  </template>
                                </v-select>

                              <v-alert v-if="errorMsg" type="error" density="compact" variant="tonal"> {{ errorMsg }}</v-alert>
                            </div>
                            <!-- <br v-else="errorMsg"/> -->
                            <v-btn @click="handleCreateAccount" color="warning" block :disabled="loadingBar">{{ $t('Register') }}</v-btn>
                        </div>
                    </v-form>
                    </div>
            </template>
        </v-card>
    </v-container>
</template>

<style scoped>
    .v-messages .v-input__details{
        display: none;
    }
</style>