<script setup>
import { ref, onMounted } from 'vue'
import axios from '@/axios'
import CampaignPercentCard from '@/views/Campaign/components/Campaign_PercentCard.vue'

const loading = ref(true)
const countryData = ref(null)
const error = ref(null)

const fetchCountryData = async () => {
  loading.value = true
  try {

  } catch (err) {
    console.error(err)
    error.value = 'Failed to load data'
  } finally {
    loading.value = false
  }
}

</script>

<template>
   <v-container
    fluid
    class="bg-[#F5F5F5]"
   >

  </v-container>
</template>
