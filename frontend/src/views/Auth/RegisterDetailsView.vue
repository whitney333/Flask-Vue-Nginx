<script setup>
    import { reactive, ref } from 'vue';
    import mishkanLogo from '@/assets/mishkan-logo.svg'
    import { useRouter } from 'vue-router';
    import { currentProfile } from '@/libs/current-profile';
    import { getAuth, updateProfile } from 'firebase/auth';
    import axios from '@/axios';
    const valid = ref(false)
    const router = useRouter()
    const errorMsg = ref()
    const loadingBar = ref(false)
    const name = reactive({
        firstname: '',
        lastname: ''
    })
    const companyName = ref('')
    const artistName = ref('')

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

    const companyNameRules = ref([
        value => {
            if (value) return true
            return 'Name is required.'
        },
        value => {
            if (/^[A-Za-z1-9\s]+$/.test(value)) return true
            return 'Name must be valid.'
        },
    ])

    const artistNameRules = ref([
        value => {
            if (value) return true
            return 'Name is required.'
        }
    ])

    const { currentUser } = getAuth()
    const profile = await currentProfile()
    
    if(profile) {
        router.push("/dashboard")
    }
    
    if (!currentUser) {
        router.push("/auth/login")
    } else {
        name.firstname = currentUser?.displayName?.split(" ")[0]
        name.lastname = currentUser?.displayName?.split(" ")[1]
    }
    
    const handleCreateAccount = async () => {
        if (!nameRules.value.every((rule) => rule(name.firstname) && rule(name.lastname))){
            return
        }
        if (!companyNameRules.value.every((rule) => rule(companyName.value))){
            return
        }
        if (!artistNameRules.value.every((rule) => rule(artistName.value))){
            return
        }
        try {
            const { currentUser } = getAuth()
            const fullName = `${name.firstname} ${name.lastname}`
            await updateProfile(currentUser, { 
                displayName: fullName, 
                // photoURL: "https://example.com/jane-q-user/profile.jpg"
            })
            const userDetails = {
                firebaseId: currentUser.uid,
                name: fullName,
                companyName: companyName.value,
                artistName: artistName.value,
                imageUrl: currentUser.photoURL,
                email: currentUser.email
            }
            const res = await axios.post('/v1/auth/register', userDetails)

            router.push('/dashboard')

        } catch(error) {
            // An error occurred
            // ...
            console.error(error);
            
        }
        
    }






</script>

<template>
    <v-container
        fluid
        :class="['fill-height', 'align-start', 'bg-grey-lighten-4']">
        
        <v-card
            :loading="loadingBar"
            :class="['ma-auto', 'pb-10', 'pt-5']"
            :width="450"
            rounded="xl"
        >
            <template v-slot:text>
                <div :class="['flex-column', 'd-flex','justify-center', 'align-center']">

                    <img :src='mishkanLogo' alt="Mishkan"/>
                    <span :class="['text-h5']">{{ $t('Tell us more about you')}}</span>
                    <br />
                    <v-form ref="form" v-model="valid" @submit.prevent class="mb-2">
                        <div :class="['flex-column', 'd-flex','justify-center', 'ga-3']">
                            <div>
                                <div class='d-flex ga-3'>
                                    <v-text-field
                                        v-model="name.firstname"
                                        :class="['mb-1']"
                                        :width="150"
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
                                        :class="['mb-1']"
                                        :width="150"
                                        :rules="nameRules"
                                        :label="$t('Last Name')"
                                        type="text"
                                        variant="solo-filled"
                                        flat
                                        rounded="lg"
                                        required
                                    ></v-text-field>
                                </div>
                                <v-text-field
                                    v-model="companyName"
                                    :class="['mb-1']"
                                    :width="350"
                                    :rules="companyNameRules"
                                    :label="$t('Company Name')"
                                    type="text"
                                    variant="solo-filled"
                                    flat
                                    rounded="lg"
                                    required
                                ></v-text-field>
                                <v-text-field
                                    v-model="artistName"
                                    :class="['mb-1']"
                                    :width="350"
                                    :rules="artistNameRules"
                                    :label="$t('Artist Name')"
                                    type="text"
                                    variant="solo-filled"
                                    flat
                                    rounded="lg"
                                    required
                                ></v-text-field>
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