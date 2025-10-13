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
      :class="['fill-height', 'align-start', 'bg-grey-lighten-4']"
  >
    <v-row class="pa-4" dense>
      <!-- Card 1 -->
      <v-col cols="12" sm="6">
        <v-card class="pa-6 rounded-2xl shadow-sm">
          <template v-slot:title>
            <span class="text-h5 font-weight-bold">{{ $t('Report A') }}</span>
          </template>
          <v-card-text>
            {{ $t('Content for Report A goes here...') }}
          </v-card-text>
          <CampaignPercentCard value=""></CampaignPercentCard>
        </v-card>
      </v-col>

      <!-- Card 2 -->
      <v-col cols="12" sm="6">
        <v-card class="pa-6 rounded-2xl shadow-sm">
          <template v-slot:title>
            <span class="text-h5 font-weight-bold">{{ $t('Report B') }}</span>
          </template>
          <v-card-text>
            {{ $t('Content for Report B goes here...') }}
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Card 3 -->
      <v-col cols="12" sm="6">
        <v-card class="pa-6 rounded-2xl shadow-sm">
          <template v-slot:title>
            <span class="text-h5 font-weight-bold">{{ $t('Report C') }}</span>
          </template>
          <v-card-text>
            {{ $t('Content for Report C goes here...') }}
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Card 4 -->
      <v-col cols="12" sm="6">
        <v-card class="pa-6 rounded-2xl shadow-sm">
          <template v-slot:title>
            <span class="text-h5 font-weight-bold">{{ $t('Report D') }}</span>
          </template>
          <v-card-text>
            {{ $t('Content for Report D goes here...') }}
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
