<script setup>
    import { reactive, ref, computed } from 'vue';
    import axios from '@/axios';
    import mishkanLogo from '@/assets/mishkan-logo.svg'
    import { FacebookAuthProvider, getAuth, GoogleAuthProvider, createUserWithEmailAndPassword, signInWithPopup } from 'firebase/auth';
    import { useRouter } from 'vue-router';
    import { useUserStore } from "@/stores/user.js";
    const userStore = useUserStore()
    const valid = ref(false)
    const email = ref('')
    const password = ref('')
    const passwordConfirm = ref('')
    const showPassword = ref(false)
    const showConfirmedPassword = ref(false)
    const router = useRouter()
    const errorMsg = ref()
    const loadingBar = ref(false)
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
            if (/^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(value)) return true
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


    const confirmPasswordRules = computed(() => [
      v => !!v || 'Confirm Password is required.',
      v => v === password.value || 'Passwords do not match.'
    ])


    const handleRegister = async () => {
      if (!valid.value) return

      if (password.value !== passwordConfirm.value) {
        snackbarText.value = 'Passwords do not match.'
        snackbarColor.value = 'error'
        snackbar.value = true
        return
      }

        loadingBar.value = true
        try {
            // register on Firebase
            const auth = getAuth()
            const userCredential = await createUserWithEmailAndPassword(auth , email.value, password.value)

            const idToken = await userCredential.user.getIdToken()
            snackbarText.value = 'Registration successful! Redirecting to login...'
            snackbarColor.value = 'success'
            snackbar.value = true

            // signup successfully then redirect to /login
            await auth.signOut()
            setTimeout(() => {
              router.push("/auth/login")
            }, 2000)

        } catch (e) {
            snackbarText.value = err.message
            snackbarColor.value = 'error'
            snackbar.value = true
        } finally {
            loadingBar.value = false
        }
    }
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
          firebaseToken: idToken,
          admin: result.user.admin,
          created_at: result.user.metadata.creationTime,
          last_login_at: result.user.metadata.lastSignInTime
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
        const {exists, admin} = response.data
        userStore.admin = admin || false;

        // get followed artists list
        if (exists === true) {
          const getFollowedArtists = await axios.get("/user/v1/followed_artists", {
            headers: {
              Authorization: `Bearer ${idToken}`,
              timeout: 10000
            }
          });
          // store followed artist
          userStore.setFollowedArtists(getFollowedArtists.data.data || []);
          // console.log("Followed Artists in store:", userStore.followedArtists);
          // redirect to /dashboard

          snackbarText.value = 'Welcome back! Redirecting to dashboard...'
          snackbarColor.value = 'success'
          snackbar.value = true
          if (userStore.admin) {
                router.push("/admin");
              } else {
                router.push("/dashboard");
              }

        } else {
          // first time login > redirect to fill out company name & followed artists
          // console.log("First time login, redirecting to details...")
          snackbarText.value = 'Welcome to Mishkan!'
          snackbarColor.value = 'success'
          snackbar.value = true
          setTimeout(() => {
            router.push("/auth/register/details")
          }, 2000)
        }
      } catch (e) {
        console.error('Google login error: ', e);
        snackbarText.value = 'Login failed. Please check your credentials.'
        snackbarColor.value = 'error'
        snackbar.value = true
      }
    }

    const handleLogin = () => {
      setTimeout(() => {
        router.push('/auth/login')
      }, 1500)
    }


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
                    <span :class="['text-h5']">{{ $t('Create Account')}}</span>
                    <br />
                    <v-form ref="form" v-model="valid" @submit.prevent="handleRegister" class="w-full mb-2">
                        <div :class="['flex-column', 'd-flex','justify-center', 'ga-3']">
                            <div>
                                <v-text-field
                                    v-model="email"
                                    class="mb-1 w-full"
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
                                    class="mb-1 w-full"
                                    :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                                    :type="showPassword ? 'text' : 'password'"
                                    @click:append="showPassword = !showPassword"
                                    :rules="passwordRules"
                                    :label="$t('Password')"
                                    variant="solo-filled"
                                    flat
                                    rounded="lg"
                                    required
                                ></v-text-field>
                                <v-text-field
                                    v-model="passwordConfirm"
                                    class="mb-1 w-full"
                                    :rules="confirmPasswordRules"
                                    :append-icon="showConfirmedPassword ? 'mdi-eye' : 'mdi-eye-off'"
                                    :type="showConfirmedPassword ? 'text' : 'password'"
                                    @click:append="showConfirmedPassword = !showConfirmedPassword"
                                    :label="$t('Confirm Password')"
                                    variant="solo-filled"
                                    flat
                                    rounded="lg"
                                    required
                                ></v-text-field>
                                <v-alert v-if="errorMsg" type="error" density="compact" variant="tonal"> {{ errorMsg }}</v-alert>
                            </div>
                            <!-- <br v-else="errorMsg"/> -->
                            <v-btn type="submit" color="warning" block :disabled="loadingBar">{{ $t('Create Account') }}</v-btn>
                            <v-divider :class="['my-4']">
                                <span style="color: #757575;">{{ $t('or continue with') }}</span>
                            </v-divider>
                        </div>
                    </v-form>
                        <div class="d-flex justify-space-around ga-3 w-full">
                            <v-btn size="large" color="#DB4437" :width="170" prepend-icon="mdi-google" variant="outlined" class="px-auto text-none" @click="() => handleProviderLogin('Google')" type="submit">Google</v-btn>
<!--                            <v-btn size="large" color="#1877F2" :width="170" prepend-icon="mdi-facebook" variant="outlined" class="px-auto text-none" @click="() => handleProviderLogin('Facebook')" type="submit">Facebook</v-btn>-->
                        </div>
                        <br />
                        <div class="d-flex flex-row align-center justify-center">
                            <span class="text-caption inline">{{ $t("Already have an account?") }}</span>
                            <v-btn @click="handleLogin" color="#FF6F00" class="text-caption inline" slim density="compact" variant="plain">
                                <span class="font-weight-bold">Sign In</span>
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