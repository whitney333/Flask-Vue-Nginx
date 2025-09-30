<script setup>
    import { RouterView, useRouter } from 'vue-router';
    import { useDisplay } from 'vuetify';
    import Drawer from './components/Drawer.vue';
    import AppBar from './components/AppBar.vue';
    import { getAuth, onAuthStateChanged, signOut } from 'firebase/auth';
    import { onMounted, ref } from 'vue';
    import { useArtistStore } from "@/stores/artist.js";
    import { useUserStore } from "@/stores/user.js";

    const display = useDisplay()

    const userStore = useUserStore()
    const artistStore = useArtistStore()

    const router = useRouter()
    const isLoggedIn = ref(false)
    // desktop version default is true; mobile version will control by hamburger menu
    const drawer = ref(true)

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
            userStore.reset()
            artistStore.reset()
            router.push("/auth/login")
            console.log("Logout success!");
            console.log("artist: ", artistStore)
            console.log("user: ", userStore)
            
        } catch(e) {
            console.error("Sign-out error: ", e);
        }
    }

    function toggleDrawer() {
      drawer.value = !drawer.value
    }

</script>

<template>
  <v-app class="font">
      <Drawer
          v-if="isLoggedIn"
          v-model="drawer"
      />
      <AppBar :isLoggedIn="isLoggedIn"
              :handleSignOut="handleSignOut"
              :drawer="drawer"
              @toggle-drawer="toggleDrawer"
      />
      <v-main>
        <RouterView/>
      </v-main>
    </v-app>
</template>

<style scoped>
    .font {
        font-family: 'Cairo', sans-serif;
    }
</style>
