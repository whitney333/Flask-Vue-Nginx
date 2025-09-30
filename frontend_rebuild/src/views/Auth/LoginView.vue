<script setup>
    import { ref } from 'vue';
    import axios from '@/axios';
    import mishkanLogo from '@/assets/mishkan-logo.svg'
    import { FacebookAuthProvider, getAuth, GoogleAuthProvider, signInWithEmailAndPassword, signInWithPopup,   setPersistence,
             browserLocalPersistence, browserSessionPersistence } from 'firebase/auth';
    import { useRouter } from 'vue-router';
    import { useUserStore } from "@/stores/user.js";
    const valid = ref(false)
    const email = ref('')
    const password = ref('')
    const router = useRouter()

    const userStore = useUserStore()
    const errorMsg = ref()
    const loadingBar = ref(false)
    const onRememberMe = ref(false)

     // Snackbar
    const snackbar = ref(false)
    const snackbarText = ref('')
    const snackbarColor = ref('success')

    const emailRules = ref([
        value => {
            if (value) return true
            return 'E-mail is required.'
        },
        value => {
            if (/.+@.+\..+/.test(value)) return true
            return 'E-mail must be valid.'
        },
    ])
    const passwordRules = ref([
        value => {
            if (value) return true
            return 'Password is required.'
        },
        value => {
            if (value?.length >= 6) return true

            return 'Password must be at least 6 characters.'
        },

    ])

    const handleLogin = async () => {
        loadingBar.value = true
        try {
            const auth = getAuth()
            const result = await signInWithEmailAndPassword(auth , email.value, password.value)
            const idToken = await result.user.getIdToken();

            // set up login time persistence
            await setPersistence(
                auth,
                onRememberMe.value ? browserLocalPersistence : browserSessionPersistence
            )
            console.log(result.user)
            // store to userStore
            userStore.setUser({
              firebase_id: result.user.uid,
              email: result.user.email,
              name: result.user.displayName,
              photo: result.user.photoURL,
              firebaseToken: idToken
            })

          // POST firebase_id to check if user exists
          const response = await axios.post(
              "/user/v1/auth/check",
              {firebase_id: result.user.uid},
              {
                headers: {
                  Authorization: `Bearer ${idToken}`
                }
              }
          );

          // const token = response.data;
          // if data exists then return
          const {exists} = response.data

          // get followed artists list
          if (exists === true) {
            const getFollowedArtists = await axios.get(
                "/user/v1/followed_artists",
                {headers: {
                Authorization: `Bearer ${idToken}`,
              },
              timeout: 10000
            });
            // store followed artist
            userStore.setFollowedArtists(getFollowedArtists.data.data || []);
            // console.log("Followed Artists in store:", userStore.followedArtists);
            // redirect to /dashboard

            snackbarText.value = 'Welcome back! Redirecting to dashboard...'
            snackbarColor.value = 'success'
            snackbar.value = true
            setTimeout(() => {
              router.push("/dashboard")
            }, 2000)
          } else {
            // first time login > redirect to fill out company name & followed artists
            console.log("First time login, redirecting to details...")

            snackbarText.value = 'Welcome to Mishkan! Monitor the artists more easily, and promote overseas efficiently!'
            snackbarColor.value = 'success'
            snackbar.value = true
            setTimeout(() => {
              router.push("/auth/register/details")
            }, 2000)
          }
        } catch (err) {
            console.error(err);
            snackbarText.value = 'Login failed. Please check your credentials.'
            snackbarColor.value = 'error'
            snackbar.value = true
        } finally {
            loadingBar.value = false
        }
    }

    // Third Party login
    const handleProviderLogin = async (providerName) => {       
        let provider = null
        switch (providerName){
            case "Google":
                provider = new GoogleAuthProvider()
                break;
            case "Facebook":
                provider = new FacebookAuthProvider()
                break;
        }

        try {
            const result = await signInWithPopup(getAuth(), provider)
            // console.log(result.user);
            const idToken = await result.user.getIdToken();

            // store to userStore
            userStore.setUser({
              firebase_id: result.user.uid,
              email: result.user.email,
              name: result.user.displayName,
              photo: result.user.photoURL,
              firebaseToken: idToken
            })

            // POST firebase_id to check if user exists
            const response = await axios.post(
                "/user/v1/auth/check",
                {firebase_id: result.user.uid},
                {headers: {
                        Authorization: `Bearer ${idToken}`
                }}
            );
            // const token = response.data;
            // if data exists then return
            const { exists } = response.data
            console.log("resp: ", response.data)

            // get followed artists list
            if (exists === true) {
              const getFollowedArtists = await axios.get(
                  "/user/v1/followed_artists",
                  {headers: {
                     Authorization: `Bearer ${idToken}`,
                  }}
              );

              // store followed artist
              userStore.setFollowedArtists(getFollowedArtists.data.data || []);
              console.log("Followed Artists in store:", userStore.followedArtists);
              // redirect to /dashboard
              router.push("/dashboard");
            } else {
              // first time login > redirect to fill out company name & followed artists
              console.log("First time login, redirecting to details...")
              router.push("/auth/register/details")
            }
        } catch(e) {
            console.error('Google login error: ', e);
        }
    }

    const handleRegister = () => {
        router.push('/auth/register')
    }

</script>

<template>
    <v-container
        fluid
        class='fill-height align-start bg-grey-lighten-4'>

        <v-card
            :loading="loadingBar"
            class="ma-auto pb-10 pt-5 w-full max-w-[400px]"
            :width="450"
            rounded="xl"
        >
            <template v-slot:text>
                <div class='flex-col flex justify-center align-center'>

                    <img :src='mishkanLogo' alt="Mishkan"/>
                    <span class='text-h5'>{{ $t('Log in')}}</span>
                    <br />
                    <v-form ref="form" v-model="valid" @submit.prevent="handleLogin" class="w-full px-4">
                        <div class='flex-col flex justify-center ga-3'>
                            <div>
                            <v-text-field
                                v-model="email"
                                class='mb-1 w-full'
                                :rules="emailRules"
                                :label="$t('Email')"
                                type="text"
                                variant="solo-filled"
                                flat
                                rounded="lg"
                                required
                            ></v-text-field>
                            <v-text-field
                                v-model="password"
                                class='mb-1 w-full'
                                :rules="passwordRules"
                                type="password"
                                :label="$t('Password')"
                                variant="solo-filled"
                                flat
                                rounded="lg"
                                required
                            ></v-text-field>
<!--                            <v-checkbox-->
<!--                                v-model="onRememberMe"-->
<!--                                focused-->
<!--                                class="mt-n2 mb-1"-->
<!--                                hide-details-->
<!--                                variant="solo"-->
<!--                                density="compact"-->
<!--                                :label="$t('Remember me')" />-->
                            <v-alert v-if="errorMsg" type="error" density="compact" variant="tonal"> {{ errorMsg }}</v-alert>
                            </div>
                            <!-- <br v-else="errorMsg"/> -->
                            <v-btn type="submit" color="warning" block :disabled="loadingBar">{{ $t('Login') }}</v-btn>
                            <v-divider class='my-4'>
                                <span style="color: #757575;">{{ $t('or continue with') }}</span>
                            </v-divider>
                        </div>
                    </v-form>
                        <div class="flex justify-space-around ga-3">
                            <v-btn size="large" color="#DB4437" :width="170" prepend-icon="mdi-google" variant="outlined" class="px-auto text-none" @click="() => handleProviderLogin('Google')" type="submit">Google</v-btn>
<!--                            <v-btn size="large" color="#1877F2" :width="170" prepend-icon="mdi-facebook" variant="outlined" class="px-auto text-none" @click="() => handleProviderLogin('Facebook')" type="submit">Facebook</v-btn>-->

                        </div>
                        <br />
                        <div class="flex flex-row align-center justify-center">
                            <span class="text-caption inline">{{ $t("Don't have an account?") }}</span>
                            <v-btn @click="handleRegister" color="#FF6F00" class="text-caption inline" slim density="compact" variant="plain">
                                <span class="font-weight-bold">Sign up</span>
                            </v-btn>
                        </div>
                    </div>
            </template>
        </v-card>
      <!-- Snackbar -->
      <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="1500" location="top">
        {{ snackbarText }}
      </v-snackbar>
    </v-container>
</template>

<style scoped>
    .v-messages .v-input__details{
        display: none;
    }
</style>