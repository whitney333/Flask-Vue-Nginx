<script setup>
import {ref, onMounted, computed, watch} from 'vue'
import { getAuth, getIdToken } from "firebase/auth"
import axios from '@/axios'
import { useArtistStore } from "@/stores/artist.js";
import { useUserStore } from "@/stores/user.js";
import CampaignLineChart from "@/views/Campaign/components/Campaign_LineChart.vue";
import CampaignKpiCard from "@/views/Campaign/components/Campaign_KpiCard.vue"
import CampaignPlatformGrowthCard from "@/views/Campaign/components/Campaign_PlatformGrowthCard.vue"
import MiniKpiCard from "@/views/Campaign/components/Campaign_MiniKpiCard.vue"
import * as XLSX from "xlsx"


const auth = getAuth()
const artistStore = useArtistStore()
const userStore = useUserStore()
const data = ref(null)
const miniKpiData = ref({
  fastest_growing_city: {},
  new_market: {},
  top_city: {}
})
const audienceData = ref({
  cities: []
})
const artistName = ref(null)
const loading = ref(true)
const selectedArtist = ref(null)
const selectedCampaign = ref(null)
const campaignOptions = ref([])
const showTooltip = ref(false)
const campaignAnalyticsView = ref(null)


// get followed artists list
const artistOptions = computed(() => {
  return (userStore.followedArtists || []).map(a => ({
    id: a.id,
    name: `${a.english_name} (${a.korean_name})`
  }))
})

// selected artist > list all campaigns of artist
watch(selectedArtist, async (artistId) => {
  selectedCampaign.value = null
  data.value = null

  if (!artistId) {
    campaignOptions.value = []
    return
  }

  const user = auth.currentUser
  if (!user) {
    console.error("Firebase user not logged in")
    return
  }
  try {
    const token = await getIdToken(user)

    const res = await axios.get("/campaign/v1/list", {
      headers: {
        Authorization: `Bearer ${token}`
      },
      params: {artist_id: artistId}
    })

    campaignOptions.value = res.data.data.map(c => ({
      id: c.campaign_name,
      obj_id: c.id,
      approved_at: c.approved_at
    }))

    if (campaignOptions.value.length === 1) {
      selectedCampaign.value = campaignOptions.value[0].obj_id
    }
  } catch (err) {
    console.error("Error fetching campaigns:", err)
  }
})
// console.log("artist_id: ", selectedArtist.value)
// console.log("campaign: ", selectedCampaign.value)
// selected campaign > load follower growth
watch(selectedCampaign, async (campaignId) => {
  data.value = null
  miniKpiData.value = null

  if (!campaignId) return
  try {
    const res = await axios.get(
        `/campaign/v1/${campaignId}/follower-growth`
    )

    data.value = res.data.data
    const spotifyId = data.value.spotify_id
    const start = data.value.period.start.split("T")[0]

    artistName.value = data.value.artist

    if (spotifyId && start) {
      await getMiniKpi(spotifyId, start)
    }

  } catch (err) {
    console.error("Fetch follower growth failed:", err)
  }
})

// default: display the first artist
watch(artistOptions, (list) => {
  if (list.length === 1) {
    selectedArtist.value = list[0].id
  }
}, { immediate: true })

const getMiniKpi = async (artist_id, start) => {
  try {
    const res = await axios.get(
        `/spotify/v1/top-city/growth`,
        {
          headers: {
            "Authorization": `Bearer ${userStore.firebaseToken}`,
            "Content-Type": "application/json"
          },
          params: {
            artist_id,
            start
          }
        }
    )
    // console.log("hh: ", res)
    if (res.data.status === "success") {
      miniKpiData.value = res.data.data.kpi
      audienceData.value = res.data.data.chart
    //   console.log(miniKpiData.value)
    } else {
      console.error("API Error:", res.data)
    }
  } catch (err) {
      console.error("Fetch KPI failed:", err)
  }
}

const getApprovedDate = (campaignId) => {
  const campaign = campaignOptions.value.find(c => c.id === campaignId);
  if (!campaign || !campaign.approved_at) return ""

  return campaign.approved_at.split("T")[0];
};

const flattenObject = (obj, parentKey = "", result = {}) => {
  for (const key in obj) {
    if (!Object.prototype.hasOwnProperty.call(obj, key)) continue

    const newKey = parentKey ? `${parentKey}.${key}` : key
    const value = obj[key]

    if (
      value &&
      typeof value === "object" &&
      !Array.isArray(value)
    ) {
      flattenObject(value, newKey, result)
    } else {
      result[newKey] = value
    }
  }
  return result
}

const exportData = () => {
  if (!data.value || !audienceData.value?.cities?.length) return

  const {campaign_id, period, followers_growth} = data.value

  /* =========================
   * Sheet 1：Artist
   * ========================= */
  const artistSheetData = [
    {artist: artistName.value}
  ]
  const artistSheet = XLSX.utils.json_to_sheet(artistSheetData)

  /* =========================
   * Sheet 2：Campaign Follower Growth
   * ========================= */
  const campaignGrowthData = []

  Object.entries(followers_growth).forEach(([platform, result]) => {
    if (!result) return

    const before =
        result.before?.follower ?? result.before?.threads_follower ?? 0
    const after =
        result.after?.follower ?? result.after?.threads_follower ?? 0

    campaignGrowthData.push({
      campaign_id,
      period_start: period.start.split("T")[0],
      period_end: period.end.split("T")[0],
      platform,
      before,
      after,
      growth: result.growth ?? 0,
      percentage: result.percentage ?? 0
    })
  })

  const campaignSheet = XLSX.utils.json_to_sheet(campaignGrowthData)

  /* =========================
   * Sheet 3：Audience Cities Growth
   * ========================= */
  const audienceCitiesData = audienceData.value.cities.map(city => ({
    city: city.city,
    country: city.country,
    before: city.before ?? 0,
    after: city.after ?? 0,
    growth_pct: city.growth_pct ?? ""
  }))

  const audienceSheet = XLSX.utils.json_to_sheet(audienceCitiesData)

  /* =========================
   * combine to one workbook
   * ========================= */
  const workbook = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(workbook, artistSheet, "Artist")
  XLSX.utils.book_append_sheet(workbook, campaignSheet, "Follower Growth")
  XLSX.utils.book_append_sheet(workbook, audienceSheet, "Audience Cities")

  /* =========================
   * Download Excel
   * ========================= */
  XLSX.writeFile(
      workbook,
      `Campaign_${campaign_id}_Report.xlsx`
  )
}

</script>

<template>
  <div class="p-6 bg-gray-50 min-h-screen">

   <!-- Filter -->
    <div class="flex flex-wrap gap-4 mb-6 items-end">
      <!-- Artist -->
      <div class="w-64 flex flex-col">
        <label class="text-sm font-medium text-gray-700 mb-1">
          {{ $t('campaign.artist') }}
        </label>
        <div class="relative">
          <select
              v-model="selectedArtist"
              class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm
                 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="" disabled selected hidden>
              Select Artist
            </option>
            <option
                v-for="a in artistOptions"
                :key="a.id"
                :value="a.id"
            >
              {{ a.name }}
            </option>
          </select>
          <!-- icon -->
          <span class="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-gray-500">
            <i class="mdi mdi-menu-down text-xl"></i>
          </span>
        </div>
      </div>

      <!-- Campaign -->
      <div class="w-64 flex flex-col">
        <label class="text-sm font-medium text-gray-700 mb-1">
          {{ $t('campaign.campaign') }}
        </label>
        <div class="relative">
          <select
              v-model="selectedCampaign"
              :disabled="!selectedArtist"
              class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm
                 focus:outline-none focus:ring-2 focus:ring-indigo-500
                 disabled:bg-gray-100"
          >
            <option value="" disabled selected hidden>
              Select Campaign
            </option>
            <option
                v-for="c in campaignOptions"
                :key="c.id"
                :value="c.id"
            >
              {{ c.id }}
            </option>
          </select>
           <!-- approved date on the right -->
          <span
              v-if="selectedCampaign"
              class="absolute right-10 top-1/2 -translate-y-1/2 text-gray-500 text-sm"
          >
            {{ getApprovedDate(selectedCampaign) }}
          </span>
          <!-- icon -->
          <span class="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-gray-500">
            <i class="mdi mdi-menu-down text-xl"></i>
          </span>
        </div>
      </div>

      <!-- inform the campaign report duration -->
      <div class="w-64 flex flex-col relative">
        <label class="text-sm font-medium text-gray-700 mb-1">&nbsp;</label>

        <div class="flex items-center justify-start">
          <div class="relative flex items-center"
              @mouseenter="showTooltip = true"
              @mouseleave="showTooltip = false"
          >
            <i class="mdi mdi-information text-xl text-gray-400 cursor-help hover:text-blue-500 transition-colors"></i>

            <transition name="fade">
              <div v-if="showTooltip"
                  class="absolute left-full top-1/2 -translate-y-1/2 ml-3 w-64 p-3 bg-white border border-gray-200 rounded-lg shadow-xl z-[9999]"
              >
                <p class="text-xs leading-relaxed text-gray-600">
                  To evaluate campaign performance, we track your followers and listeners across major platforms from
                  two weeks before to two weeks after the campaign.
                </p>
                <div class="absolute right-full top-1/2 -translate-y-1/2 border-8 border-transparent border-r-white"></div>
              </div>
            </transition>
          </div>
        </div>
      </div>

      <!-- export button  -->
      <div class="w-40 flex-1 flex justify-end">
        <button
            @click="exportData"
            class="bg-indigo-500 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 transition duration-200"
        >
          {{ $t('export') }}
        </button>
      </div>
    </div>

    <!-- KPI -->
    <CampaignKpiCard
        v-if="data"
        :data="data"
    />

    <!-- Chart -->
    <div class="bg-white rounded-md shadow p-4 mb-6">
      <h3 class="text-base font-semibold text-gray-800 mb-3">
        {{ $t('campaign.follower_growth_trend_before_after_campaign') }}
      </h3>
      <CampaignLineChart
        v-if="data"
        :data="data"
      />
      <div
        v-else-if="selectedCampaign"
        class="text-gray-400 text-sm text-center py-16"
      >
        {{ $t('campaign.loading_campaign')}}...
      </div>
      <div
        v-else
        class="text-gray-400 text-sm text-center py-16"
      >
        {{ $t('campaign.please_select') }}
      </div>
    </div>

    <!-- Platform Cards -->
    <div class="mb-6">
      <CampaignPlatformGrowthCard v-if="data" :data="data" />
    </div>
    <!-- TODO ADD AUDIENCE CHANGE -->
    <!-- Audience change  -->

    <!-- mini kpi cards of spotify top city/region -->
    <MiniKpiCard :kpi="miniKpiData" />
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>