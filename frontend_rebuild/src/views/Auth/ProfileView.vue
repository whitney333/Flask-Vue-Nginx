<script setup>
import { useUserStore } from "@/stores/user.js";
import { computed } from "vue"

const userStore = useUserStore()
const defaultAvatar = "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-dist/user-circle-96.png"


</script>


<template>
 <v-container class="py-6">
  <v-row justify="center">
    <v-col cols="12" md="8">
      <v-card elevation="0" rounded="sm" class="mt-4 bg-white border border-gray-200">
        <v-row class="mt-4" align="center">
          <v-col
            cols="12"
            md="3"
            class="flex items-center justify-center md:justify-start"
          >
            <v-avatar size="64">
              <v-img :src="userStore.photo || defaultAvatar" alt="Profile"/>
            </v-avatar>
          </v-col>

          <v-col
            cols="12"
            md="9"
            class="flex flex-col items-center md:items-start justify-center"
          >
            <h2 class="mb-1 text-center md:text-left text-gray-900">{{ userStore.name }}</h2>
            <p class="text-gray-500 text-center md:text-left">{{ userStore.email }}</p>
          </v-col>
        </v-row>

        <v-divider class="my-2"/>

        <v-card-title class="text-gray-700 text-lg font-medium">Followed Artists</v-card-title>
        <v-list dense>
          <v-list-item
            v-for="artist in userStore.followedArtists"
            :key="artist.artist_id"
            :prepend-avatar="artist.image"
          >
            <v-list-item-title class="text-body-1 font-medium text-gray-900">
              {{ artist.english_name }}
            </v-list-item-title>
            <v-list-item-subtitle class="text-gray-500">
              {{ artist.korean_name }}
            </v-list-item-subtitle>
          </v-list-item>
          <v-list-item v-if="!userStore.followedArtists || userStore.followedArtists.length === 0">
            <v-list-item-title class="text-gray-500">No followed artists</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-card>
    </v-col>
  </v-row>
</v-container>
</template>

<style scoped>

</style>