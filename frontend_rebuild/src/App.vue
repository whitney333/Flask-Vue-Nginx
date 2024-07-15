<template>
    <v-app >
        <Drawer />
        <AppBar />
        <v-main>
            <v-container>
                <RouterView />
            </v-container>
        </v-main>
    </v-app>
</template>

<script setup>
import { RouterView } from 'vue-router';
import Drawer from './components/Drawer.vue';
import AppBar from './components/AppBar.vue';
</script>


<style scoped>
</style>
