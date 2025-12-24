<script setup>
import { defineProps } from "vue"

const props = defineProps({
  data: Object
})

const platforms = [
  { key: "instagram", label: "Instagram" },
  { key: "spotify", label: "Spotify" },
  { key: "threads", label: "Threads" },
  { key: "tiktok", label: "TikTok" },
  { key: "youtube", label: "YouTube" }
]

const getBefore = (p, item) =>
  p === "threads"
    ? item?.before?.threads_follower ?? 0
    : item?.before?.follower ?? 0

const getAfter = (p, item) =>
  p === "threads"
    ? item?.after?.threads_follower ?? 0
    : item?.after?.follower ?? 0

</script>

<template>
 <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
    <div
      v-for="p in platforms"
      :key="p.key"
      class="bg-white rounded-xl p-4 shadow"
    >
      <p class="text-sm text-gray-500 mb-1">{{ p.label }}</p>

      <p class="text-xl font-semibold text-gray-800">
        +{{ data.followers_growth[p.key]?.growth?.toLocaleString() || 0 }}
      </p>

      <p class="text-xs text-gray-500 mt-1">
        {{ getBefore(p.key, data.followers_growth[p.key])?.toLocaleString() }}
        →
        {{ getAfter(p.key, data.followers_growth[p.key])?.toLocaleString() }}
      </p>

      <p
        class="text-sm mt-2"
        :class="
          data.followers_growth[p.key]?.percentage > 0
            ? 'text-green-600'
            : 'text-gray-400'
        "
      >
        {{ data.followers_growth[p.key]?.percentage ?? 0 }}%
      </p>
    </div>
  </div>
</template>

<style scoped>

</style>