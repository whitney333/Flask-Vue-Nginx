<script setup>
    import { RouterView, useRouter } from 'vue-router';
    import Drawer from './components/Drawer.vue';
    import AppBar from './components/AppBar.vue';
    import { getAuth, onAuthStateChanged, signOut } from 'firebase/auth';
    import { onMounted, ref } from 'vue';
    import "@/style.css"

    const router = useRouter()
    const isLoggedIn = ref(false)
    let auth
    onMounted(() => {
        auth = getAuth()
        onAuthStateChanged(auth, (user) => {
            if (user) {
                isLoggedIn.value = true
            } else {
                isLoggedIn.value = false
            }
        }, (error) => {
            console.error("Error in onAuthStateChanged:", error); // Error handling
        })
    })

    const handleSignOut = async () => {        
        try {
            await signOut(auth)
            router.push("/auth/login")
            console.log("Logout success!");
            
        } catch(e) {
            console.error("Sign-out error: ", e);
        }
    }
</script>

<template>
    <v-app class="font">
        <Drawer v-if="isLoggedIn" />
        <AppBar :isLoggedIn="isLoggedIn" :handleSignOut="handleSignOut" />
        <v-main>
            <RouterView />
        </v-main>
    </v-app>
</template>

<style scoped>
    .font {
        font-family: 'Cairo', sans-serif;
    }
</style>
