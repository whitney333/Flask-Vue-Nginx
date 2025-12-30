<script setup>
import { defineProps } from "vue"
import youtubeIcon from "@/assets/icons/youtube.svg"
import tiktokIcon from "@/assets/icons/tiktok.svg"
import instagramIcon from "@/assets/icons/instagram.svg"
import bilibiliIcon from "@/assets/icons/bilibili.svg"
import threadsIcon from "@/assets/icons/threads.svg"
import spotifyIcon from "@/assets/icons/spotify.svg"

const props = defineProps({
  data: Object
})

const platforms = [
  { key: "instagram", label: "Instagram" },
  { key: "spotify", label: "Spotify" },
  { key: "threads", label: "Threads" },
  { key: "tiktok", label: "Tiktok" },
  { key: "youtube", label: "Youtube" },
  { key: "bilibili", label: "Bilibili"}
]

const platformIconMap = {
  instagram: instagramIcon,
  spotify: spotifyIcon,
  threads: threadsIcon,
  tiktok: tiktokIcon,
  bilibili: bilibiliIcon,
  youtube: youtubeIcon
}

const getBefore = (p, item) =>
  p === "threads"
    ? item?.before?.threads_follower ?? 0
    : item?.before?.follower ?? 0

const getAfter = (p, item) =>
  p === "threads"
    ? item?.after?.threads_follower ?? 0
    : item?.after?.follower ?? 0

const getGrowth = (p, item) => {
  const before = getBefore(p, item)
  const after = getAfter(p, item)
  return after - before
}

const getPercentage = (p, item) => {
  const before = getBefore(p, item)
  const growth = getGrowth(p, item)
  return before > 0 ? (growth / before) * 100 : 0
}

</script>

<template>
 <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
    <div
      v-for="p in platforms"
      :key="p.key"
      class="bg-white rounded-xl p-4 shadow"
    >
      <div class="flex items-center gap-2 mb-1">
        <img
            :src="platformIconMap[p.key]"
            :alt="p.label"
            class="w-4 h-4"
        />
        <p class="text-sm text-gray-500 mb-1">{{ $t(`sns.${p.label}`) }}</p>
      </div>
      <p class="text-xl font-semibold text-gray-800"
        :class="
        getGrowth(p.key, data.followers_growth[p.key]) > 0
          ? 'text-green-600'
          : getGrowth(p.key, data.followers_growth[p.key]) < 0
            ? 'text-red-600'
            : 'text-gray-400'
        "
      >
        {{ getGrowth(p.key, data.followers_growth[p.key]) > 0 ? '+' : getGrowth(p.key, data.followers_growth[p.key]) < 0 ? '−' : '' }}
        {{ Math.abs(getGrowth(p.key, data.followers_growth[p.key])).toLocaleString() }}
      </p>

      <p class="text-xs text-gray-500 mt-1">
        {{ getBefore(p.key, data.followers_growth[p.key])?.toLocaleString() }}
        →
        {{ getAfter(p.key, data.followers_growth[p.key])?.toLocaleString() }}
      </p>

      <p
        class="text-sm mt-2"
        :class="
        getPercentage(p.key, data.followers_growth[p.key]) > 0
          ? 'text-green-600'
          : getPercentage(p.key, data.followers_growth[p.key]) < 0
            ? 'text-red-600'
            : 'text-gray-400'
        "
      >
        {{ getPercentage(p.key, data.followers_growth[p.key]) > 0 ? '+' : getPercentage(p.key, data.followers_growth[p.key]) < 0 ? '−' : '' }}
        {{ Math.abs(getPercentage(p.key, data.followers_growth[p.key])).toFixed(2) }}%
      </p>
    </div>
  </div>
</template>

<style scoped>

</style>