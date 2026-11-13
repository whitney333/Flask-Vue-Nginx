<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const activeTab = computed(() => route.path)
</script>

<template>
  <v-container fluid>
    <v-tabs :model-value="activeTab">
      <v-tab to="/campaign/">
        Online Campaigns
      </v-tab>

      <v-tab to="/campaign/offline-event">
        Offline Event
      </v-tab>
    </v-tabs>

    <router-view />
  </v-container>
</template>

<style scoped>

</style>
