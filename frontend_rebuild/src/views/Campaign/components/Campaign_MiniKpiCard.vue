<script setup>
import { computed } from "vue";
import { defineProps } from "vue";

const props = defineProps({
  kpi: {
    type: Object,
    required: true,
  },
  unit: {
    type: String,
    default: "listeners",
  },
});

const kpiData = computed(() => ({
  fastest: {
    title: "Fastest Growing City/Region",
    ...props.kpi.fastest_growing_city,
  },
  newMarket: {
    title: "New Market",
    ...props.kpi.new_market,
  },
  top: {
    title: "Top City/Region",
    ...props.kpi.top_city,
  },
}));

</script>

<template>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
    <div
        v-for="(item, key) in kpiData"
        :key="key"
        class="p-4 bg-white shadow-md rounded-xl flex flex-col justify-between"
    >
      <!-- title -->
      <h3 class="text-sm text-gray-500 uppercase">{{ item.title }}</h3>

      <!-- city & country -->
      <p class="text-xl font-bold mt-2">
        {{ item.city }}, {{ item.country }}
      </p>

      <!-- Before → After -->
      <p class="text-lg mt-1">
        {{ item.before }} → {{ item.after }} {{ unit }}
      </p>

      <!-- growth percentage -->
      <p
          v-if="item.growth_pct !== null"
          :class="[
          'mt-2 font-semibold',
          item.growth_pct > 0 ? 'text-green-600' : 'text-red-600'
        ]"
      >
        {{ item.growth_pct > 0 ? '+' : '' }}{{ item.growth_pct }}%
      </p>

      <!-- New Market -->
      <p v-else class="mt-2 text-gray-400 font-semibold">New Market</p>
    </div>
  </div>
</template>

<style scoped>

</style>