<template>
    <v-div class="flex">
        <Drawer />
        <RouterView />
    </v-div>
    
</template>

<script setup>
import { RouterView } from 'vue-router';
import Drawer from './components/Drawer.vue';
</script>


<style scoped>
</style>
