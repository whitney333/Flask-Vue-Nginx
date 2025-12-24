<script setup>
import {ref, defineProps, computed} from "vue";
import {useUserStore} from "@/stores/user.js";
import getUnicodeFlagIcon from 'country-flag-icons/unicode'
import {countryNameToCode} from "@/libs/utils.js";

const platforms = ["instagram", "spotify", "threads", "tiktok", "youtube"]
const props = defineProps({
  data: Object
})

const formatNumFunc = (value) => {
  if (value === null || value === undefined) return '0'

  const abs = Math.abs(value)
  if (abs < 1000) return value.toLocaleString()
  if (abs < 1_000_000) return (value / 1000).toFixed(1) + 'K'
  if (abs < 1_000_000_000) return (value / 1_000_000).toFixed(1) + 'M'
  return (value / 1_000_000_000).toFixed(1) + 'B'
}


const series = computed(() => {
  const before = { name: "Before", data: [] }
  const after = { name: "After", data: [] }

  platforms.forEach(p => {
    const item = props.data.followers_growth[p]

    const beforeValue =
      p === "threads"
        ? item?.before?.threads_follower ?? 0
        : item?.before?.follower ?? 0

    const afterValue =
      p === "threads"
        ? item?.after?.threads_follower ?? 0
        : item?.after?.follower ?? 0

    before.data.push(beforeValue)
    after.data.push(afterValue)
  })

  return [before, after]
})

const options = {
  chart: {
    type: "bar"
  },
  colors: ['#8acaee', '#277bec'],
  xaxis: {
    categories: ["Instagram", "Spotify", "Threads", "TikTok", "YouTube"]
  },
  yaxis: {
    labels: {
      formatter: formatNumFunc,
      style: {
        fontSize: '12px',
        fontWeight: 'bold',
        fontFamily: 'Cairo, sans-serif',
      }
    }
  },
  tooltip: {
    y: {
      formatter: v => v?.toLocaleString()
    }
  }
}


</script>

<template>
 <apexchart
    type="bar"
    height="320"
    :options="options"
    :series="series"
  />
</template>

<style scoped>

</style>