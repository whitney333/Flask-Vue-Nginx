<script setup>
import { computed, defineProps } from "vue"


const props = defineProps({
  data: {
    type: Object,
    required: true
  }
})

const platforms = ["instagram", "spotify", "threads", "tiktok", "youtube"]

const summary = computed(() => {
  let totalGrowth = 0
  let totalBefore = 0
  let totalAfter = 0

  platforms.forEach(p => {
    const item = props.data.followers_growth[p]
    if (!item) return

    const before =
      p === "threads"
        ? item.before?.threads_follower ?? 0
        : item.before?.follower ?? 0

    const after =
      p === "threads"
        ? item.after?.threads_follower ?? 0
        : item.after?.follower ?? 0

    totalBefore += before
    totalAfter += after
    totalGrowth += item.growth ?? 0
  })

  const percentage =
    totalBefore > 0
      ? ((totalGrowth / totalBefore) * 100).toFixed(2)
      : 0

  return {
    totalBefore,
    totalAfter,
    totalGrowth,
    percentage
  }
})

</script>

<template>
<div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
    <!-- Before -->
    <div class="bg-white rounded-xl p-4 shadow-sm">
      <p class="text-sm text-gray-500">Before Followers</p>
      <p class="text-2xl font-semibold">
        {{ summary.totalBefore.toLocaleString() }}
      </p>
    </div>

    <!-- After -->
    <div class="bg-white rounded-xl p-4 shadow-sm">
      <p class="text-sm text-gray-500">After Followers</p>
      <p class="text-2xl font-semibold">
        {{ summary.totalAfter.toLocaleString() }}
      </p>
    </div>

    <!-- Growth -->
    <div class="bg-white rounded-xl p-4 shadow-sm">
      <p class="text-sm text-gray-500">Total Growth</p>
      <p class="text-2xl font-semibold text-green-600">
        +{{ summary.totalGrowth.toLocaleString() }}
      </p>
    </div>

    <!-- Percentage -->
    <div class="bg-white rounded-xl p-4 shadow-sm">
      <p class="text-sm text-gray-500">Growth Rate</p>
      <p class="text-2xl font-semibold text-indigo-600">
        {{ summary.percentage }}%
      </p>
    </div>
  </div>
</template>

<style scoped>

</style>