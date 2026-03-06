<script setup>
import {ref, watch} from 'vue'
import DB_TS_card from '@/views/Dashboard/components/DB_TS_card.vue'
import { useDisplay } from 'vuetify'

defineProps({
  graphItems: {
    type: Array,
    required: true
  }
})

const model = ref(null)
const { smAndDown } = useDisplay()
</script>

<template>
  <v-card flat class="bg-[#f8f7f2]">
    <!-- Title -->
    <template #title>
      <h2 class="text-2xl font-semibold tracking-tight">
        {{ $t('Top Statistics') }}
      </h2>
    </template>

    <!-- Content -->
    <template #text>
      <!--  Mobile: column layout -->
      <div
        v-if="smAndDown"
        class="flex flex-col items-center gap-4 px-2"
      >
        <DB_TS_card
          v-for="item in graphItems"
          :key="item.name"
          :value="item"
          class="w-full max-w-md rounded-xl shadow-sm"
        />
      </div>

      <!--  Desktop: slider -->
      <v-slide-group
        v-else
        show-arrows
        class="top-stats-slider px-4 py-2"
      >
        <v-slide-group-item
          v-for="item in graphItems"
          :key="item.name"
        >
          <DB_TS_card
            :value="item"
            class="mx-4"
          />
        </v-slide-group-item>
      </v-slide-group>
    </template>
  </v-card>
</template>

<style scoped>
:deep(.top-stats-slider .v-slide-group__container) {
  overflow-x: auto;
  overflow-y: visible;
  padding-top: 8px;
  padding-bottom: 12px;
}

:deep(.top-stats-slider .v-slide-group__content) {
  overflow: visible;
}
</style>

