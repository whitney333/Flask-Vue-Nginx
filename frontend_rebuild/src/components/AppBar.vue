<script setup>
import { useRoute, useRouter } from 'vue-router';

const route = useRoute()

</script>
<template>
    <v-app-bar :elevation="1" app :style="{ padding: '0px 20px' }">        
        <v-app-bar-title :style="{ fontSize: '1.5rem', fontWeight: 'bold'}">{{ route.name }}</v-app-bar-title>
        
        <template v-slot:append>
            <v-btn icon="mdi-heart"></v-btn>
            
            <v-btn icon="mdi-magnify"></v-btn>
            
            <v-btn icon="mdi-dots-vertical"></v-btn>
        </template>
    </v-app-bar>
</template>
