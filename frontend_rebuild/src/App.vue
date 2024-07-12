<template>
    <v-div class="flex">
        <Nav />
        <RouterView />
    </v-div>
    
</template>

<script setup>
import { RouterView } from 'vue-router';
import Nav from './components/Nav.vue'
</script>


<style scoped>
</style>
