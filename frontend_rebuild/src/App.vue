<template>
    <v-app class="font">
        <Drawer />
        <AppBar />
        <v-main>
            <RouterView />
        </v-main>
    </v-app>
</template>

<script setup>
import { RouterView } from 'vue-router';
import Drawer from './components/Drawer.vue';
import AppBar from './components/AppBar.vue';
</script>


<style scoped>
    .font {
        font-family: 'Cairo', sans-serif;
    }
</style>
