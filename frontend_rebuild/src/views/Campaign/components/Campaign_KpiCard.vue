<script setup>
import { computed, defineProps } from "vue"


const props = defineProps({
  data: {
    type: Object,
    required: true
  }
})

const platforms = ["instagram", "spotify", "threads", "tiktok", "youtube", "bilibili", "weibo"]

const summary = computed(() => {
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
  })
  const totalGrowth = totalAfter - totalBefore
  const percentage =
    totalBefore > 0 ? (totalGrowth / totalBefore) * 100 : 0

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
      <p class="text-sm text-gray-500">{{ $t('campaign.followers_before_campaign') }}</p>
      <p class="text-2xl font-semibold">
        {{ summary.totalBefore.toLocaleString() }}
      </p>
    </div>

    <!-- After -->
    <div class="bg-white rounded-xl p-4 shadow-sm">
      <p class="text-sm text-gray-500">{{ $t('campaign.followers_after_campaign') }}</p>
      <p class="text-2xl font-semibold">
        {{ summary.totalAfter.toLocaleString() }}
      </p>
    </div>

    <!-- Growth -->
    <div class="bg-white rounded-xl p-4 shadow-sm">
      <p class="text-sm text-gray-500">{{ $t('campaign.total_growth') }}</p>
      <p class="text-2xl font-semibold"
         :class="summary.totalGrowth > 0 ? 'text-green-600' : summary.totalGrowth < 0 ? 'text-red-600' : 'text-gray-400'"
      >
        {{ summary.totalGrowth > 0 ? '+' : summary.totalGrowth < 0 ? '−' : '' }}
        {{ Math.abs(summary.totalGrowth).toLocaleString() }}
      </p>
    </div>

    <!-- Percentage -->
    <div class="bg-white rounded-xl p-4 shadow-sm">
      <p class="text-sm text-gray-500">{{ $t('campaign.growth_rate') }}</p>
      <p class="text-2xl font-semibold"
         :class="summary.percentage > 0 ? 'text-green-600' : summary.percentage < 0 ? 'text-red-600' : 'text-gray-400'"
      >
        {{ summary.percentage > 0 ? '+' : summary.percentage < 0 ? '−' : '' }}
        {{ Math.abs(summary.percentage).toFixed(2) }}%
      </p>
    </div>
  </div>
</template>

<style scoped>

</style>