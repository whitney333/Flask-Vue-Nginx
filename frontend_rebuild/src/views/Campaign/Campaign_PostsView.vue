<script setup>
import router from '@/router';
// Taiwan', 'Hong Kong', 'Japan', 'South Korea', 'Thailand', 'Vietnam', 'Philippines', 'Indonesia', 'United States', 'Canada', 'Brazil', 'Mexico', 'United Kingdom', 'Germany', 'France', 'Spain', 'Italy', 'Australia']
// make up some posts
const posts = [
    { id: 1, title: 'Post 1', description: 'Description 1', platform: 'tiktok', countries: ['Taiwan', 'Hong Kong', 'Japan'], budget: 'US$50 - US$500' },
];

</script>

<template>
    <v-container
        fluid
        :class="['fill-height', 'align-start', 'bg-grey-lighten-4']">
        <v-container
        >

            <v-card
            flat
            class="bg-grey-lighten-4 w-full"> 
                <template v-slot:title>
                    <div class="flex w-full">
                        <span class="text-h4 w-full">{{ $t('Posts') }}</span>
                        <v-btn @click="() => router.push('/campaign/posts/create')" color="black">Create Post</v-btn>
                    </div>
                </template>
                <v-card-text class="mt-4">
                    <v-card
                        v-for="post in posts"
                        :key="post.id"
                        class="rounded-xl p-2"
                    >
                    <v-card-item>
                        <v-card-title>{{ post.title }}</v-card-title>
                        <v-card-subtitle>{{ post.description }}</v-card-subtitle>
                        <v-card-subtitle>{{ post.platform }}</v-card-subtitle>
                        <v-card-subtitle>{{ post.countries.join(', ') }}</v-card-subtitle>
                        <v-card-subtitle>{{ post.budget }}</v-card-subtitle>
                    </v-card-item>
                    <v-card-text>

                    </v-card-text>
                    <v-card-actions>
                        <v-btn @click="() => router.push('/campaign/posts/edit')" color="black">Edit</v-btn>
                        <v-btn @click="() => router.push('/campaign/posts/delete')" color="black">Delete</v-btn>
                    </v-card-actions>

                    
                    </v-card>
                </v-card-text>
            </v-card>
        </v-container>
    </v-container>
</template>
