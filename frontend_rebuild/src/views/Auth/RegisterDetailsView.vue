<script setup>
    import { computed, reactive, ref, onMounted, watch } from 'vue';
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
    const selectedTenantId = ref(null)
    const companies = ref([])
    const artistOptions = ref([])
    const selectedArtistId = ref(null)
    const loadingArtists = ref(false)
    const { currentUser } = getAuth()
    const followLimit = 1
    // add pagination var
    const page = ref(1)
    const hasMore = ref(true)
    const isLoadingMore = ref(false)
    // const selectedArtist = computed(() => {
    //   return artistOptions.value.find((artist) => artist.artist_objId === selectedArtistId.value) || null
    // })

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

    const artistDropdownOpen = ref(false)
    const artistSearch = ref('')

    const selectedArtist = computed(() => {
      return artistOptions.value.find(
          artist => artist.artist_objId === selectedArtistId.value
      )
    })

    const selectArtist = (artist) => {
      selectedArtistId.value = artist.artist_objId
      artistDropdownOpen.value = false
      artistSearch.value = ''
    }

    const toggleArtistDropdown = () => {
      if (loadingArtists.value) return

      artistDropdownOpen.value = !artistDropdownOpen.value
    }

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

        // validate followed artist
        if (!selectedArtist.value) {
          errorMsg.value = `You must select 1 artist.`
          return
        }

        if (!selectedArtist.value.tenant_id) {
          errorMsg.value = `Selected artist is missing tenant information.`
          return
        } else {
          errorMsg.value = null
        }

        selectedTenantId.value = selectedArtist.value.tenant_id

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
                tenant: selectedArtist.value.tenant_id,
                image_url: currentUser.photoURL,
                email: currentUser.email,
                followed_artist: [selectedArtist.value.artist_objId],
                firebaseToken: idToken,
                created_at: currentUser.metadata.creationTime,
                last_login_at: currentUser.metadata.lastSignInTime
            }

            // send register details to backend
            const res = await axios.post('/user/v1/auth/register', userDetails, {
              headers: {
                Authorization: `Bearer ${idToken}`
              }
            })
            // fetch current user data from backend
            // get data from /v1/auth/firebaseId
            const user_profile = await axios.get(`/user/v1/auth/${currentUser.uid}`, {
              headers: {
                Authorization: `Bearer ${idToken}`
              }
            })
            // console.log("user profile: ", user_profile)
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

      await loadArtistOptions()
    })


    const loadArtistOptions = async (isReset = false) => {
      // if reload, reset pagination condition and list
      if (isReset) {
        page.value = 1
        hasMore.value = true
        artistOptions.value = []
      }

      // prevent duplicate requesting
      if (!hasMore.value || isLoadingMore.value) return

      // 第一頁顯示全局 loading，後續分頁使用 isLoadingMore
      if (page.value === 1) {
        loadingArtists.value = true
      }
      isLoadingMore.value = true

      try {
        const res = await axios.get("/user/v1/artists/all", {
          params: {
            page: page.value,
            limit: 20,
            search: artistSearch.value.trim()
          }
        })

        const newArtists = res.data.data || []

        artistOptions.value = [...artistOptions.value, ...newArtists]

        if (newArtists.length < 20) {
          hasMore.value = false
        } else {
          page.value++
        }

        errorMsg.value = ""
      } catch (err) {
        console.error("Error fetching artists:", err)

        if (page.value === 1) {
          artistOptions.value = []
          selectedArtistId.value = null
          errorMsg.value = "Unable to load artists. Please try again."
        }
      } finally {
        loadingArtists.value = false
        isLoadingMore.value = false
      }
    }

    // listen to horizontal scroll event
    const handleScroll = (e) => {
      const {scrollLeft, clientWidth, scrollWidth} = e.target
      if (scrollWidth - (scrollLeft + clientWidth) < 100) {
        loadArtistOptions()
      }
    }

    // 💡 使用 debounce 避免輸入時頻繁觸發 API
    let searchTimer = null
    watch(artistSearch, () => {
      clearTimeout(searchTimer)
      searchTimer = setTimeout(() => {
        loadArtistOptions(true) // 輸入關鍵字時重置分頁並重新載入
      }, 300)
    })

    watch(selectedArtist, (artist) => {
      if (!artist) {
        selectedTenantId.value = null
        errorMsg.value = `You must select 1 artist.`
      } else {
        selectedTenantId.value = artist.tenant_id
        errorMsg.value = null
      }
    })

</script>

<template>
  <v-container
    fluid
    class="!flex !min-h-screen !items-start !justify-center !bg-gray-100 !p-3 sm:!p-4"
  >
    <v-card
      :loading="loadingBar"
      class="!mx-auto !mt-8 !w-full !max-w-[720px] !rounded-2xl !pb-10 !pt-6 !overflow-visible"
      elevation="0"
    >
      <template #text>
        <div
          class="flex w-full flex-col items-center justify-center px-1 sm:px-4"
        >
          <!-- Title -->
          <span
            class="text-lg font-semibold text-gray-800 sm:text-xl"
          >
            {{ $t('auth.fields.tell_us_more') }}
          </span>

          <v-form
            ref="form"
            v-model="valid"
            class="mb-2 mt-5 w-full sm:mt-6"
            @submit.prevent="handleCreateAccount"
          >
            <div class="flex flex-col gap-4">

              <!-- Name -->
              <!-- Desktop: horizontal -->
              <div class="hidden w-full gap-3 sm:flex">
                <v-text-field
                  v-model="name.firstname"
                  class="!w-full"
                  :rules="nameRules"
                  :label="$t('auth.fields.first_name')"
                  type="text"
                  variant="solo-filled"
                  flat
                  rounded="lg"
                  required
                />

                <v-text-field
                  v-model="name.lastname"
                  class="!w-full"
                  :rules="nameRules"
                  :label="$t('auth.fields.last_name')"
                  type="text"
                  variant="solo-filled"
                  flat
                  rounded="lg"
                  required
                />
              </div>

              <!-- Mobile: vertical -->
              <div class="flex w-full flex-col gap-3 sm:hidden">
                <v-text-field
                  v-model="name.firstname"
                  class="!w-full"
                  :rules="nameRules"
                  :label="$t('auth.fields.first_name')"
                  type="text"
                  variant="solo-filled"
                  flat
                  rounded="lg"
                  required
                />

                <v-text-field
                  v-model="name.lastname"
                  class="!w-full"
                  :rules="nameRules"
                  :label="$t('auth.fields.last_name')"
                  type="text"
                  variant="solo-filled"
                  flat
                  rounded="lg"
                  required
                />
              </div>

              <!-- Artist -->
              <div class="mt-2 w-full overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm">

                <!-- Search Area -->
                <div class="border-b border-gray-100 p-2.5 sm:p-3">
                  <div class="relative flex items-center">
                    <!-- Search icon (Left) -->
                    <svg
                        class="absolute left-3 h-4 w-4 text-gray-400"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                    >
                      <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="m21 21-4.35-4.35m0 0A7.5 7.5 0 1 0 6.05 6.05a7.5 7.5 0 0 0 10.6 10.6Z"
                      />
                    </svg>

                    <input
                        v-model="artistSearch"
                        :disabled="loadingArtists"
                        type="text"
                        placeholder="Search artist..."
                        class="h-10 w-full rounded-lg bg-gray-100 pl-9 pr-10 text-sm text-gray-800 outline-none transition focus:bg-gray-50 focus:ring-2 focus:ring-amber-400 disabled:cursor-not-allowed disabled:opacity-60"
                    />

                    <!-- Loading Spinner in Search Bar (Right) -->
                    <v-progress-circular
                        v-if="loadingArtists"
                        indeterminate
                        size="16"
                        width="2"
                        class="absolute right-3 text-amber-500"
                    />
                  </div>
                </div>

                <!-- Loading State: Skeleton Loader -->
                <div
                    v-if="loadingArtists"
                    class="flex w-full gap-2.5 overflow-hidden px-2.5 py-3 sm:gap-3 sm:px-3 sm:py-4"
                >
                  <!-- Skeleton Cards (顯示 4 個假卡片) -->
                  <div
                      v-for="n in 4"
                      :key="'skeleton-' + n"
                      class="flex shrink-0 animate-pulse flex-col items-center justify-center rounded-xl border border-gray-100 bg-gray-50 text-center h-[125px] w-[92px] p-2 sm:h-[145px] sm:w-[112px] sm:p-3"
                  >
                    <!-- Avatar Skeleton -->
                    <div class="h-14 w-14 rounded-full bg-gray-200 sm:h-16 sm:w-16"></div>
                    <!-- English Name Skeleton -->
                    <div class="mt-2 h-3 w-14 rounded bg-gray-200 sm:mt-3 sm:w-16"></div>
                    <!-- Korean Name Skeleton -->
                    <div class="mt-1.5 h-2 w-10 rounded bg-gray-200 sm:mt-2 sm:w-12"></div>
                  </div>
                </div>

                <!-- Loaded State: Actual Artist Horizontal List -->
                <template v-else>
                  <div
                      class="flex w-full gap-2.5 overflow-x-auto px-2.5 py-3 sm:gap-3 sm:px-3 sm:py-4"
                      style="scrollbar-width: thin; -webkit-overflow-scrolling: touch;"
                      @scroll="handleScroll"
                  >
                    <!-- Artist Card -->
                    <button
                        v-for="artist in artistOptions"
                        :key="artist.artist_objId"
                        type="button"
                        class="group flex shrink-0 flex-col items-center justify-center rounded-xl border bg-white text-center transition-all duration-200"
                        :class="[
                          'h-[125px] w-[92px] p-2',
                          'sm:h-[145px] sm:w-[112px] sm:p-3',
                          selectedArtistId === artist.artist_objId
                            ? 'border-amber-500 bg-amber-50 shadow-md'
                            : 'border-gray-200 hover:border-amber-400 hover:bg-amber-50 hover:shadow-sm'
                        ]"
                        @click="selectArtist(artist)"
                    >
                      <!-- Avatar -->
                      <div class="relative">
                        <img
                            :src="artist.imageURL"
                            alt="avatar"
                            class="h-14 w-14 rounded-full object-cover shadow-sm sm:h-16 sm:w-16"
                        />

                        <!-- Selected Indicator -->
                        <div
                            v-if="selectedArtistId === artist.artist_objId"
                            class="absolute -bottom-1 -right-1 flex h-5 w-5 items-center justify-center rounded-full bg-amber-500 text-white"
                        >
                          <svg
                              class="h-3 w-3"
                              fill="none"
                              stroke="currentColor"
                              viewBox="0 0 24 24"
                          >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="3"
                                d="m5 12 4 4L19 6"
                            />
                          </svg>
                        </div>
                      </div>

                      <!-- English Name -->
                      <div class="mt-1.5 w-full truncate text-[11px] font-semibold text-gray-800 sm:mt-2 sm:text-xs">
                        {{ artist.artist_name }}
                      </div>

                      <!-- Korean Name -->
                      <div class="mt-0.5 w-full truncate text-[10px] text-gray-400 sm:text-[11px]">
                        {{ artist.korean_name || '\u00A0' }}
                      </div>

                      <!-- Birth Year -->
                      <div
                          v-if="artist.birth_year"
                          class="mt-0.5 text-[9px] text-gray-400 sm:mt-1 sm:text-[10px]"
                      >
                        {{ artist.birth_year }}
                      </div>
                    </button>

                    <div
                        v-if="isLoadingMore"
                        class="flex h-[125px] w-[92px] shrink-0 items-center justify-center rounded-xl border border-dashed border-gray-200 sm:h-[145px] sm:w-[112px]"
                    >
                      <div class="h-5 w-5 animate-spin rounded-full border-2 border-amber-500 border-t-transparent">
                      </div>
                    </div>
                    <!-- No Result -->
                    <div
                        v-if="artistOptions.length === 0"
                        class="flex h-[125px] w-full min-w-full items-center justify-center text-sm text-gray-400 sm:h-[145px]"
                    >
                      No artists found
                    </div>
                  </div>

                  <!-- Scroll Hint -->
                  <div
                      v-if="artistOptions.length > 3"
                      class="border-t border-gray-100 px-3 py-2 text-center text-[9px] text-gray-400 sm:text-[10px]"
                  >
                    ← Swipe to explore more artists →
                  </div>
                </template>
              </div>

              <!-- Error -->
              <v-alert
                v-if="errorMsg"
                type="error"
                density="compact"
                variant="tonal"
                class="!mt-1 !rounded-lg"
              >
                {{ errorMsg }}
              </v-alert>

              <!-- Follow Limit -->
              <p class="!m-0 text-xs text-gray-500">
                {{ selectedArtistId ? 1 : 0 }}/{{ followLimit }}
                artist selected
              </p>


              <!-- Submit -->
              <v-btn
                type="submit"
                color="warning"
                block
                :disabled="loadingBar"
                class="!mt-2 !h-11 !rounded-lg !font-semibold !normal-case"
              >
                {{ $t('auth.register.title') }}
              </v-btn>

            </div>
          </v-form>

        </div>
      </template>
    </v-card>
  </v-container>
</template>

<style scoped>
.v-messages .v-input__details {
  display: none;
}
</style>
