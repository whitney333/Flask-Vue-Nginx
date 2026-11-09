<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const activeTab = computed(() => route.path)
</script>

<template>
  <v-container fluid>
    <v-tabs :model-value="activeTab">
      <v-tab to="/admin/campaigns/online">
        Online Campaigns
      </v-tab>

      <v-tab to="/admin/campaigns/offline">
        Offline Event
      </v-tab>
    </v-tabs>

    <router-view />
  </v-container>
</template>

<style scoped>

</style>