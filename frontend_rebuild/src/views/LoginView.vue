<script setup>
    import { ref } from 'vue';
    import mishkanLogo from '@/assets/mishkan-logo.svg'
    import { FacebookAuthProvider, getAuth, GoogleAuthProvider, signInWithEmailAndPassword, signInWithPopup } from 'firebase/auth';
    import { useRouter } from 'vue-router';
    const valid = ref(false)
    const email = ref('')
    const password = ref('')
    const router = useRouter()
    const errorMsg = ref()
    const loadingBar = ref(false)
    const onRemeberMe = ref(false)

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
            console.log("//before sign in: ",auth.currentUser);
            const data = await signInWithEmailAndPassword(auth , email.value, password.value)
            console.log("Successfully Login!");
            console.log("//after sign in: ", auth.currentUser);
            router.push('/dashboard')
            
        } catch (e) {
            console.error(e);
            switch(e.code) {
                case "auth/invalid-email":
                    errorMsg.value = "Invalid email"
                    break;
                case "auth/user-not-found":
                    errorMsg.value = "No account with that email was found";
                    break;
                case "auth/wrong-password":
                    errorMsg.value = "Incorrect password";
                    break
                default:
                    errorMsg.value = "Email or password was incorrect"
                    break
            }
        } finally {
            loadingBar.value = false
        }
    }
    const handleGoogleLogin = async () => {       
        const provider = new GoogleAuthProvider()
        try {
            const result = await signInWithPopup(getAuth(), provider)
            console.log(result.user);
            if (result.user.metadata.createdAt === result.user.metadata.lastLoginAt) {
                console.log("/// LoginView - New created Account!");
            }
            router.push("/dashboard")
        } catch(e) {
            console.error(e);
        }
    }

    const handleFacebookLogin = async () => {       
        const provider = new FacebookAuthProvider()
        try {
            const result = await signInWithPopup(getAuth(), provider)
            console.log(result.user);
            router.push("/dashboard")
        } catch(e) {
            console.error(e);
        }
        
    }
    const handleRegister = () => {
        router.push('/auth/register')
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
                    <span :class="['text-h5']">{{ $t('Log in')}}</span>
                    <br />
                    <v-form ref="form" v-model="valid" @submit.prevent class="mb-2">
                        <div :class="['flex-column', 'd-flex','justify-center', 'ga-3']">
                            <div>
                            <v-text-field
                                v-model="email"
                                :class="['mb-1']"
                                :width="350"
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
                                :class="['mb-1']"
                                :width="350"
                                :rules="passwordRules"
                                type="password"
                                :label="$t('Password')"
                                variant="solo-filled"
                                flat
                                rounded="lg"
                                required
                            ></v-text-field>
                            <v-checkbox
                                v-model="onRemeberMe"
                                focused
                                class="mt-n2 mb-1"
                                hide-details
                                variant="solo"
                                density="compact"
                                :label="$t('Remember me')" />
                            <v-alert v-if="errorMsg" type="error" density="compact" variant="tonal"> {{ errorMsg }}</v-alert>
                            </div>
                            <!-- <br v-else="errorMsg"/> -->
                            <v-btn @click="handleLogin" color="warning" block :disabled="loadingBar">{{ $t('Login') }}</v-btn>
                            <v-divider :class="['my-4']">
                                <span style="color: #757575;">{{ $t('or continue with') }}</span>
                            </v-divider>
                        </div>
                    </v-form>
                        <div class="d-flex justify-space-around ga-3">
                            <v-btn size="large" color="#DB4437" :width="170" prepend-icon="mdi-google" variant="outlined" class="px-auto text-none" @click="handleGoogleLogin" type="submit">Google</v-btn>
                            <v-btn size="large" color="#1877F2" :width="170" prepend-icon="mdi-facebook" variant="outlined" class="px-auto text-none" @click="handleFacebookLogin" type="submit">Facebook</v-btn>
                        </div>
                        <br />
                        <div class="d-flex flex-row align-center justify-center">
                            <span class="text-caption inline">{{ $t("Don't have an account?") }}</span>
                            <v-btn @click="handleRegister" color="#FF6F00" class="text-caption inline" slim density="compact" variant="plain">
                                <span class="font-weight-bold">Sign up</span>
                                </v-btn>
                        </div>
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