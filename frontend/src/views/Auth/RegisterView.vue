<script setup>
    import { reactive, ref } from 'vue';
    import mishkanLogo from '@/assets/mishkan-logo.svg'
    import { FacebookAuthProvider, getAuth, GoogleAuthProvider, createUserWithEmailAndPassword, signInWithPopup } from 'firebase/auth';
    import { useRouter } from 'vue-router';
    const valid = ref(false)
    const email = ref('')
    const password = ref('')
    const passwordConfirm = ref('')
    const router = useRouter()
    const errorMsg = ref()
    const loadingBar = ref(false)

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

    const handleRegister = async () => {
        loadingBar.value = true
        try {
            if (password.value !== passwordConfirm.value) {
                errorMsg.value = "Passwords do not match."
                return
            }
            
            const auth = getAuth()
            const data = await createUserWithEmailAndPassword(auth , email.value, password.value)
            
        } catch (e) {
            console.error(e);
            switch(e.code) {
                case "auth/email-already-exists	":
                    errorMsg.value = "Email already exist"
                    break;
                default:
                    errorMsg.value = "Email or password was incorrect"
                    break
            }
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
            if (result.user.metadata.createdAt === result.user.metadata.lastLoginAt) {
                router.push("/auth/register/details")
            } else {
                router.push("/dashboard")
            }
            router.push("/dashboard")
        } catch(e) {
            console.error(e);
        }
    }

    const handleLogin = () => {
        router.push('/auth/login')
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
                    <span :class="['text-h5']">{{ $t('Create Account')}}</span>
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
                                <v-text-field
                                    v-model="passwordConfirm"
                                    :class="['mb-1']"
                                    :width="350"
                                    :rules="passwordRules"
                                    type="password"
                                    :label="$t('Confirm Password')"
                                    variant="solo-filled"
                                    flat
                                    rounded="lg"
                                    required
                                ></v-text-field>
                                <v-alert v-if="errorMsg" type="error" density="compact" variant="tonal"> {{ errorMsg }}</v-alert>
                            </div>
                            <!-- <br v-else="errorMsg"/> -->
                            <v-btn @click="handleRegister" color="warning" block :disabled="loadingBar">{{ $t('Create Account') }}</v-btn>
                            <v-divider :class="['my-4']">
                                <span style="color: #757575;">{{ $t('or continue with') }}</span>
                            </v-divider>
                        </div>
                    </v-form>
                        <div class="d-flex justify-space-around ga-3">
                            <v-btn size="large" color="#DB4437" :width="170" prepend-icon="mdi-google" variant="outlined" class="px-auto text-none" @click="() => handleProviderLogin('Google')" type="submit">Google</v-btn>
                            <v-btn size="large" color="#1877F2" :width="170" prepend-icon="mdi-facebook" variant="outlined" class="px-auto text-none" @click="() => handleProviderLogin('Facebook')" type="submit">Facebook</v-btn>
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
    </v-container>
</template>

<style scoped>
    .v-messages .v-input__details{
        display: none;
    }
</style>