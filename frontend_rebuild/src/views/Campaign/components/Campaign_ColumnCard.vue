<script setup>
import {ref, defineProps, computed} from "vue";
import {useUserStore} from "@/stores/user.js";
import getUnicodeFlagIcon from 'country-flag-icons/unicode'
import {countryNameToCode} from "@/libs/utils.js";


const props = defineProps({
  campaignId: {
    type: String,
    required: true,
  },
  campaignData: {
    type: Array,
    required: true,
    default: () => []
  }
});

const userStore = useUserStore()

// sorting
const sortKey = ref("cost_per_reach")
const sortAscend = ref(false)

// group by country, calculate average cost_per_reach
const groupData = computed(() => {
  const groups = {}

  props.campaignData.forEach(item => {
    const country = item.target_country || 'Unknown'

    const rawCostReach = (item.cost_per_reach || "").toString()
    const cleanCostReach = rawCostReach.replace(/[^0-9.\-]/g, "")  // 移除非數字字元
    const costReach = parseFloat(cleanCostReach)

    const rawCostView = (item.cost_per_view || "").toString()
    const cleanCostView = rawCostView.replace(/[^0-9.\-]/g, "")  // 移除非數字字元
    const costView = parseFloat(cleanCostView)

    if (!groups[country]) {
      groups[country] = {total_cpr: 0, total_cpv: 0, count: 0}
    }

    if (!isNaN(costReach)) {
      groups[country].total_cpr += costReach
    }
    if (!isNaN(costView)) {
      groups[country].total_cpv += costView
    }

    groups[country].count += 1

  })
  const arr = Object.entries(groups).map(([country, data]) => ({
    target_country: country,
    cost_per_reach: (data.total_cpr / data.count).toFixed(4),
    cost_per_view: (data.total_cpv / data.count).toFixed(4)
  }))

  // sort
  arr.sort((a, b) => {
    const aVal = parseFloat(a[sortKey.value])
    const bVal = parseFloat(b[sortKey.value])
    return sortAsc.value ? aVal - bVal : bVal - aVal
  })

  return arr
})

const toggleSort = (key) => {
  if (sortKey.value === key) {
    sortAsc.value = !sortAsc.value
  } else {
    sortKey.value = key
    sortAsc.value = false
  }
}

</script>

<template>
  <v-card :loading="loadingBar"
          class="flex flex-col items-center justify-center p-4"
          style="width: 100%;">
    <v-card-text
        class="flex items-center justify-center w-full p-0"
        style="padding: 0;"
    >
      <v-table
          height="300px"
          fixed-header
      >
        <thead>
        <tr>
          <th class="text-left">
            {{ $t('country') }}
          </th>
          <th class="text-left"
            @click="toggleSort('cost_per_reach')" style="cursor: pointer;"
          >
            {{ $t('campaign.cost_per_reach') }}
            <span v-if="sortKey==='cost_per_reach'">{{ sortAsc ? '▲' : '▼' }}</span>
          </th>
          <th class="text-left"
            @click="toggleSort('cost_per_view')" style="cursor: pointer;"
          >
            {{ $t('campaign.cost_per_view') }}
            <span v-if="sortKey==='cost_per_view'">{{ sortAsc ? '▲' : '▼' }}</span>
          </th>
        </tr>
        </thead>
        <tbody>
        <tr
            v-for="item in groupData"
            :key="item.target_country"
        >
          <td class="flex items-center gap-2">
            <img
                :src="`https://flagcdn.com/${countryNameToCode[item.target_country].toLowerCase()}.svg`"
                alt="flag"
                width="24"
            />
            {{ item.target_country }}
          </td>
          <td>{{ item.cost_per_reach }}</td>
          <td>{{ item.cost_per_view }}</td>
        </tr>
        </tbody>
      </v-table>
    </v-card-text>
  </v-card>
</template>

<style scoped>

</style>