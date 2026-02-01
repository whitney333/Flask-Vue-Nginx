<script setup>
import { onMounted, ref, watch } from "vue";
import { useArtistStore } from "@/stores/artist.js";
import { useUserStore } from "@/stores/user.js";
import axios from '@/axios';
import { useRouter } from 'vue-router';
import { DollarSign, Globe, Share2, Box, Blocks } from 'lucide-vue-next';
import CampaignPercentCard from "@/views/Campaign/components/Campaign_PercentCard.vue";
import campaignJSON from './json/campaignViewDetails.json'
import CampaignDataTable from "@/views/Campaign/components/Campaign_DataTable.vue";
import CampaignColumnCard from "@/views/Campaign/components/Campaign_ColumnCard.vue";
import * as XLSX from 'xlsx'


const infoOpen = ref(false)
const router = useRouter()
const artistStore = useArtistStore()
const userStore = useUserStore()
const campaigns = ref([])
const showCancelDialog = ref(false)
const showPerformanceDialog = ref(false)
const selectedPerformanceCampaign = ref(null)
const targetCampaignId = ref(null)
const dialog = ref(false)
const selectedCampaign = ref(null)
const loadingBar = ref(true)
const campaignDetail = ref([])
const campaignChartCountryData = ref([])
const campaignChartRegionData = ref([])
const campaignChartPlatformData = ref([])
const dialogData = ref([])
const showTooltip = ref(false)

// Taiwan', 'Hong Kong', 'Japan', 'South Korea', 'Thailand', 'Vietnam', 'Philippines', 'Indonesia', 'United States', 'Canada', 'Brazil', 'Mexico', 'United Kingdom', 'Germany', 'France', 'Spain', 'Italy', 'Australia']
// make up some posts
// const posts = [
//     { id: 1, title: 'Post 1', description: 'Description 1', platform: 'tiktok', countries: ['Taiwan', 'Hong Kong', 'Japan'], budget: 'US$50 - US$500' },
// ];

// open detail dialog
const openDialog = (campaign) => {
  // console.log("openDialog got id:", campaign);
  selectedCampaign.value = campaign
  dialog.value = true
}

// open cancel dialog
const openCancelDialog = (campaignId) => {
  // console.log("openCancelDialog got id:", campaignId);
  targetCampaignId.value = campaignId
  showCancelDialog.value = true
};

// soft delete campaign
const confirmCancel = async () => {
  // console.log("confirmCancel got id:", targetCampaignId.value);
  try {
    if (!targetCampaignId.value) {
      console.error("No campaign ID found")
      return
    }

    const res = await axios.patch(
        `/campaign/v1/cancel/${targetCampaignId.value}`,
        {status: "cancelled"},
        {headers: {
            Authorization:  `Bearer ${userStore.firebaseToken}`,
            "Content-Type": "application/json"
          }}
    )
    // console.log(res.data)
    //change status to cancelled
    const campaign = campaigns.value.find(
        (c) => c.campaign_id === targetCampaignId.value
    );
    if (campaign) campaign.status = "cancelled";
    showCancelDialog.value = false
    alert("Campaign cancelled successfully!")
  } catch (err) {
    console.error(err)
  }
};


// get user's all campaign
const getAllCampaign = async () => {
  try {
    const res = await axios.get(
        "/campaign/v1/read",
        {headers: {
            "Authorization": `Bearer ${userStore.firebaseToken}`,
            "Content-Type": "application/json"
        }}
    )

    campaigns.value = res.data.data
    // console.log("all cp: ", campaigns.value)
  } catch (err) {
    console.error("Error loading campaigns:", err)
  }
}

// get single campaign performance
const getSingleCampaignPerformance = async () => {
  try {
    const res = await axios.get(
        `/campaign/v1/${selectedCampaign?.campaign_id}`,
        {headers: {
            "Authorization": `Bearer ${userStore.firebaseToken}`,
            "Content-Type": "application/json"
          }}
    )
  } catch (err) {
    console.error("Error loading campaigns:", err)
  }
}

onMounted(() => {
  getAllCampaign();
})

const formatDate = (dateStr) => {
  if (!dateStr) return ""
  const d = new Date(dateStr)
  return d.toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  })
}

const truncateText = (text, length = 20) => {
  if (!text) return ""
  return text.length > length ? text.slice(0, length) + "..." : text
}

const getStatusColor = (status) => {
  switch (status) {
    case 'submitted':
      return 'blue';
    case 'approved':
      return 'green';
    case 'cancelled':
      return 'red';
    default:
      return 'grey';
  }
};

const openPerformanceDialog = (campaign) => {
  // console.log("Open performance for:", campaign)
  selectedCampaign.value = campaign
  showPerformanceDialog.value = true
}

const closePerformanceDialog = () => {
  showPerformanceDialog.value = false
  selectedPerformanceCampaign.value = null
}

watch(showPerformanceDialog, async (newVal) => {
  if (newVal && selectedCampaign.value) {
    try {
      const response = await axios.get(
          `/campaign/v1/detail/${selectedCampaign.value.campaign_id}`,
          {
          headers: {
            "Authorization": `Bearer ${userStore.firebaseToken}`,
            "Content-Type": "application/json"
          }
        }
      );
      dialogData.value = response.data.data;
      campaignDetail.value = response.data.data.post;
      campaignChartCountryData.value = response.data.data.total_country;
      campaignChartRegionData.value = response.data.data.total_region;
      campaignChartPlatformData.value = response.data.data.total_platform;
      // console.log("cd: ", campaignDetail.value)
    } catch (error) {
      console.error(error);
    }
  }
});

const parseEngagement = (value) => {
  if (!value) return 0
  return Number(String(value).replace('%', '')) || 0
}

const calculateSummary = (posts) => {
  if (!posts.length) {
    return {
      total_reach: 0,
      total_reaction: 0,
      total_cost: 0,
      avg_engagement: '0.00%',
      weighted_avg_engagement: '0.00%',
      cpr: 0,
      cpe: 0
    }
  }

  let totalReach = 0
  let totalReaction = 0
  let totalCost = 0
  let engagementSum = 0
  let weightedEngagementSum = 0

  posts.forEach(p => {
    const reach = Number(p.reach) || 0
    const reaction = Number(p.reaction) || 0
    const cost = Number(p.cost) || 0
    const engagement = parseEngagement(p.engagement)

    totalReach += reach
    totalReaction += reaction
    totalCost += cost

    engagementSum += engagement
    weightedEngagementSum += engagement * reach
  })

  const avgEngagement = engagementSum / posts.length
  const weightedAvgEngagement =
      totalReach > 0
          ? weightedEngagementSum / totalReach
          : 0

  const cpr = totalReach > 0 ? totalCost / totalReach : 0
  const cpe = totalReaction > 0 ? totalCost / totalReaction : 0

  return {
    total_reach: totalReach,
    total_reaction: totalReaction,
    total_cost: totalCost,
    avg_engagement: `${avgEngagement.toFixed(2)}%`,
    weighted_avg_engagement: `${weightedAvgEngagement.toFixed(2)}%`,
    cpr: cpr.toFixed(4),
    cpe: cpe.toFixed(4)
  }
}

const exportDialogData = () => {
  const campaign =
      dialogData.value?.data ?? dialogData.value

  if (!campaign) {
    console.error('No campaign data')
    return
  }

  const posts = campaign.post || []
  const summary = calculateSummary(posts)

  /* =========================
   * Sheet 1：Summary
   * ========================= */
  const summarySheetData = [
    {
      campaign_id: campaign.campaign_id,
      artist_en_name: campaign.artist_en_name,
      artist_kr_name: campaign.artist_kr_name,
      total_reach: summary.total_reach,
      total_reaction: summary.total_reaction,
      total_cost: summary.total_cost,
      avg_engagement: summary.avg_engagement,
      weighted_avg_engagement: summary.weighted_avg_engagement,
      cpr: summary.cpr,
      cpe: summary.cpe
    },
    // break line
    {},
    // ===== Total region =====
    {section: "Total Region"},
    ...campaignChartRegionData.value.map(c => ({
      name: c.name,
      count: c.count
    })),
    // break line
    {},
    // ===== Total country =====
    {section: "Total Country"},
    ...campaignChartCountryData.value.map(c => ({
      name: c.name,
      count: c.count
    })),
    // break line
    {},
    // ===== Total platform =====
    {section: "Total Platform"},
    ...campaignChartPlatformData.value.map(p => ({
      name: p.name,
      count: p.count
    }))
  ]

  const summarySheet = XLSX.utils.json_to_sheet(summarySheetData)

  // bold headers
  const range = XLSX.utils.decode_range(summarySheet['!ref'])
  for (let C = range.s.c; C <= range.e.c; ++C) {
    const cellAddress = XLSX.utils.encode_cell({ r: 0, c: C })
    if (!summarySheet[cellAddress]) continue
    summarySheet[cellAddress].s = {
      font: { bold: true }
    }
  }

  /* =========================
   * Sheet 2：POSTS
   * ========================= */
  const postSheetData = posts.map(post => {
    const reach = Number(post.reach) || 0
    const reaction = Number(post.reaction) || 0
    const cost = Number(post.cost) || 0

    return {
      campaign_id: campaign.campaign_id,
      artist_en_name: campaign.artist_en_name,
      artist_kr_name: campaign.artist_kr_name,
      post_platform: post.platform,
      kol_account: post.kol_account,
      target_country: post.target_country,
      post_type: post.type,
      post_created_at: post.post_created_at,

      reach: reach,
      reaction: reaction,
      engagement: post.engagement,

      latest_view: post.latest_view,
      one_hour_view: post.one_hour_view,
      twentyfour_hour_view: post.twentyfour_hour_view,

      cost: cost,
      cost_per_view: post.cost_per_view,
      cost_per_reach: post.cost_per_reach,


      post_url: post.url,
      used_hashtag: post.used_hashtag?.join(' | ')
    }
  })

  const postSheet = XLSX.utils.json_to_sheet(postSheetData)

  /* =========================
   * combine sheets to workbook
   * ========================= */
  const workbook = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(workbook, summarySheet, 'Summary')
  XLSX.utils.book_append_sheet(workbook, postSheet, 'Posts')

  /* =========================
   * Download
   * ========================= */
  XLSX.writeFile(
      workbook,
      `Campaign_${campaign.campaign_id}_SummaryReport.xlsx`
  )
}

</script>

<template>
  <v-container
      fluid
      class="fill-height bg-grey-lighten-4 py-6"
  >
    <v-card
        flat
        class="bg-grey-lighten-4 w-full mx-auto mb-6 px-4"
        max-width="1200"
    >
      <div class="flex items-center gap-3">
        <!-- Create Post Button -->
        <button @click="() => router.push('/campaign/posts/create')"
            class="bg-black text-white text-sm px-4 py-2 rounded-md
            hover:bg-gray-800 transition-colors"
        >
          Create Post
        </button>

        <!-- info icon -->
        <div class="relative flex items-center"
            @mouseenter="showTooltip = true"
            @mouseleave="showTooltip = false"
        >
          <i class="mdi mdi-information text-xl text-gray-400 cursor-help
             hover:text-blue-500 transition-colors"
          ></i>

          <transition name="fade">
            <div v-if="showTooltip"
                class="absolute left-full top-0 ml-3 mt-1
                 w-96 p-4 bg-white border border-gray-200
                 rounded-lg shadow-xl z-[9999]"
            >
              <p class="text-xs leading-relaxed text-gray-600">
                You can create a campaign on this page.
                Once submitted, the status will show as 'submitted'.
                After approval by the admin, the status will change to 'approved'.
                The day after the campaign begins, we will update the related analysis.
                You can view the analysis by clicking the icon next to the status chips.
              </p>

              <div class="absolute right-full top-3
                    border-8 border-transparent border-r-white"
              ></div>
            </div>
          </transition>
        </div>
      </div>

      <v-card-text class="mt-4">
        <!-- loading condition -->
        <div v-if="loading" class="flex justify-center items-center py-20">
          <v-progress-circular indeterminate color="black" size="48"/>
        </div>
        <!-- if data exists -->
        <template v-if="campaigns && campaigns.length > 0">
          <v-row dense>
            <v-col
                v-for="campaign in campaigns"
                :key="campaign.campaign_id"
                cols="12" md="6"
            >
              <v-card class="rounded-xl p-6 h-full">
                <v-card-item>
                  <v-card-title class="text-base sm:text-lg font-semibold">
                    {{ $t('campaign.campaign') }}: {{ campaign.campaign_id }}
                  </v-card-title>
                  <v-card-subtitle class="text-xs sm:text-sm text-gray-600">
                    {{ $t('campaign.created_at') }}: {{ formatDate(campaign.created_at) }}
                  </v-card-subtitle>
                </v-card-item>

                <v-card-text>
                  <div class="flex items-center gap-2 mb-4 overflow-x-auto no-scrollbar">
                    <v-chip
                        :color="campaign.status === 'submitted' ? 'blue' : 'grey lighten-2'"
                        dark
                        size="small"
                        class="text-[10px] sm:text-xs md:text-sm px-2 sm:px-3 py-1 sm:py-2 whitespace-nowrap"
                    >
                      {{ $t('campaign.submitted') }}
                    </v-chip>
                    <v-chip
                        :color="campaign.status === 'approved' ? 'green' : 'grey lighten-2'"
                        dark
                        size="small"
                        class="text-[10px] sm:text-xs md:text-sm px-2 sm:px-3 py-1 sm:py-2 whitespace-nowrap"
                    >
                      {{ $t('campaign.approved') }}
                    </v-chip>
                    <v-chip
                        :color="campaign.status === 'cancelled' ? 'red' : 'grey lighten-2'"
                        dark
                        size="small"
                        class="text-[10px] sm:text-xs md:text-sm px-2 sm:px-3 py-1 sm:py-2 whitespace-nowrap"
                    >
                      {{ $t('campaign.cancelled') }}
                    </v-chip>
                    <!-- only when campaign is approved will show this icon  -->
                    <v-icon
                        v-if="campaign.status === 'approved'"
                        icon="mdi-chart-line"
                        class="ml-2 text-green-500 cursor-pointer"
                        @click="openPerformanceDialog(campaign)"
                    />
                    <!-- Performance Dialog -->
                    <v-dialog v-model="showPerformanceDialog" max-width="800px" transition="dialog-bottom-transition">
                      <v-card class="flex flex-col max-h-[90vh]" v-show="showPerformanceDialog">
                        <!-- Header -->
                        <div
                            class="bg-gradient-to-r from-gray-800 via-gray-700 to-gray-600 text-white p-5 flex items-center justify-between">
                          <div>
                            <h2 class="text-xl font-semibold">{{ selectedCampaign?.campaign_id }} Campaign
                              Performance</h2>
                            <p class="text-sm opacity-90">{{ selectedCampaign?.artist_en_name }}
                              ({{ selectedCampaign?.artist_kr_name }})</p>
                          </div>
                          <!-- Right actions -->
                          <div class="flex items-center gap-2">
                            <!-- Export Button -->
                            <v-btn
                                size="small"
                                color="white"
                                variant="outlined"
                                rounded
                                @click="exportDialogData"
                            >
                              {{ $t('export') }}
                            </v-btn>

                            <!-- Status -->
                            <v-chip color="blue-lighten-3" text-color="black" size="small">
                              {{ selectedCampaign?.status }}
                            </v-chip>
                          </div>
                        </div>

                        <v-card-text class="p-4 flex-1">
                          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                            <CampaignPercentCard
                                :value="{
                              title: campaignJSON.campaignPlatformPercentage.title,
                              tooltipText: campaignJSON.campaignPlatformPercentage.tooltipText,
                              colors: ['#4E56C0', '#9B5DE0', '#D78FEE', '#FDCFFA', '#FDAAAA', '#F8F7BA']
                            }"
                                :campaignId="selectedCampaign?.campaign_id"
                                :campaignData="campaignChartPlatformData"
                            />
                            <CampaignPercentCard
                                :value="{
                              title: campaignJSON.campaignRegionPercentage.title,
                              tooltipText: campaignJSON.campaignRegionPercentage.tooltipText,
                              colors: ['#4E56C0', '#9B5DE0', '#D78FEE', '#FDCFFA', '#FDAAAA', '#F8F7BA']
                            }"
                                :campaignId="selectedCampaign?.campaign_id"
                                :campaignData="campaignChartRegionData"
                            />
                            <CampaignPercentCard
                                :value="{
                                title: campaignJSON.campaignCountryPercentage.title,
                                tooltipText: campaignJSON.campaignCountryPercentage.tooltipText,
                                colors: campaignJSON.campaignCountryPercentage.colors
                                }"
                                :campaignId="selectedCampaign?.campaign_id"
                                :campaignData="campaignChartCountryData"
                            />
                            <CampaignColumnCard
                                :campaignId="selectedCampaign?.campaign_id"
                                :campaignData="campaignDetail"
                            />
                          </div>
                          <div class="grid grid-cols-1 md:grid-cols-1 gap-4">
                            <CampaignDataTable
                                :campaignId="selectedCampaign?.campaign_id"
                            />
                          </div>
                        </v-card-text>

                        <v-card-actions>
                          <v-spacer/>
                          <v-btn color="grey" variant="text" @click="closePerformanceDialog">
                            {{ $t('campaign.close') }}
                          </v-btn>
                        </v-card-actions>
                      </v-card>
                    </v-dialog>
                  </div>
                  <div class="flex flex-col gap-4">
                    <!-- Artist -->
                    <div class="flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-2">
                      <div class="flex items-center gap-2">
                        <Box class="w-4 h-4 text-gray-500"/>
                        <span class="font-medium">{{ $t('campaign.artist') }}:</span>
                      </div>
                      <span class="break-words">{{ campaign.artist_en_name }}</span>
                    </div>

                    <!-- Platform -->
                    <div class="flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-2">
                      <div class="flex items-center  gap-2">
                        <Blocks class="w-4 h-4 text-gray-500"/>
                        <span class="font-medium">{{ $t('campaign.platforms') }}:</span>
                      </div>
                      <span class="break-words whitespace-pre-wrap">{{ campaign.platform.join(', ') }}</span>
                    </div>

                    <!-- Region -->
                    <div class="flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-2">
                      <div class="flex items-center gap-2">
                        <Globe class="w-4 h-4 text-gray-500"/>
                        <span class="font-medium">{{ $t('campaign.regions') }}:</span>
                      </div>
                      <span class="break-words whitespace-pre-wrap">{{
                          campaign.region.join(', ')
                        }}</span>
                    </div>

                    <!-- Budget -->
                    <div class="flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-2">
                      <div class="flex items-center gap-2">
                        <DollarSign class="w-4 h-4 text-gray-500"/>
                        <span class="font-medium">{{ $t('campaign.budget') }}:</span>
                      </div>
                      <span class="break-words">{{ campaign.budget }}</span>
                    </div>
                  </div>
                </v-card-text>

                <v-card-actions>
                  <!-- open view details dialog  -->
                  <v-btn
                      @click="openDialog(campaign)"
                      color="black"
                  >
                    {{ $t('campaign.view_details') }}
                  </v-btn>
                  <v-dialog v-model="dialog" max-width="700px" transition="dialog-bottom-transition">
                    <v-card class="rounded-2xl shadow-lg overflow-hidden">

                      <!-- Header -->
                      <div
                          class="bg-gradient-to-r from-gray-800 via-gray-700 to-gray-600 text-white p-5 flex items-center justify-between">
                        <div>
                          <h2 class="text-xl font-semibold">{{ selectedCampaign?.artist_en_name }}</h2>
                          <p class="text-sm opacity-90">{{ selectedCampaign?.artist_kr_name }}</p>
                        </div>
                        <v-chip color="blue-lighten-3" text-color="black" size="small">
                          {{ selectedCampaign?.status }}
                        </v-chip>
                      </div>

                      <!-- Body -->
                      <v-card-text class="bg-[#F9F9F9] p-6">
                        <div class="grid grid-cols-2 gap-4">
                          <div>
                            <p class="text-gray-500 text-sm">{{ $t('campaign.platform') }}</p>
                            <p class="font-medium">{{ selectedCampaign?.platform.join(', ') }}</p>
                          </div>
                          <div>
                            <p class="text-gray-500 text-sm">{{ $t('campaign.regions') }}</p>
                            <p class="font-medium">{{ selectedCampaign?.region.join(', ') }}</p>
                          </div>
                          <div>
                            <p class="text-gray-500 text-sm">{{ $t('campaign.budget') }}</p>
                            <p class="font-medium">{{ selectedCampaign?.budget }}</p>
                          </div>
                          <div>
                            <p class="text-gray-500 text-sm">{{ $t('campaign.created_at') }}</p>
                            <p class="font-medium">{{ new Date(selectedCampaign?.created_at).toLocaleString() }}</p>
                          </div>
                        </div>

                        <v-divider class="my-4"></v-divider>

                        <!-- Description-->
                        <div class="mb-2">
                          <p class="text-gray-500 text-sm mb-1">{{ $t('campaign.description') }}</p>
                          <p class="text-base leading-relaxed">
                            {{ selectedCampaign?.info?.description || 'No description provided.' }}
                          </p>
                        </div>
                        <!-- Hashtag -->
                        <div class="mb-2">
                          <p class="text-gray-500 text-sm mb-1">{{ $t('campaign.hashtags') }}</p>
                          <div v-if="selectedCampaign?.info?.hashtag?.length" class="flex flex-wrap gap-2">
                            <v-chip
                                v-for="(tag, index) in selectedCampaign.info.hashtag"
                                :key="index"
                                color="blue-darken-2"
                                text-color="white"
                                size="small"
                            >
                              #{{ tag }}
                            </v-chip>
                          </div>
                          <p v-else class="text-gray-400 text-sm italic">No hashtags provided.</p>
                        </div>
                        <!-- URL -->
                        <div class="mb-2">
                          <p class="text-gray-500 text-sm mb-1">{{ $t('campaign.url') }}</p>
                          <div v-if="selectedCampaign?.info?.url">
                            <a
                                :href="selectedCampaign.info.url"
                                target="_blank"
                                class="text-blue-600 hover:underline break-all"
                            >
                              {{ selectedCampaign.info.url }}
                            </a>
                          </div>
                          <p v-else class="text-gray-400 text-sm italic">No URL provided.</p>
                        </div>
                      </v-card-text>

                      <!-- Footer -->
                      <v-card-actions class="justify-end bg-gray-50 px-6 py-4">
                        <v-btn text color="black" @click="dialog = false">{{ $t('campaign.close') }}</v-btn>
                      </v-card-actions>

                    </v-card>
                  </v-dialog>
                  <!-- open cancel dialog -->
                  <v-btn
                      @click="openCancelDialog(campaign.campaign_id)"
                      color="red"
                      variant="outlined"
                      :disabled="['approved', 'cancelled'].includes(campaign.status)"
                  >
                    {{ $t('campaign.cancel') }}
                  </v-btn>
                  <v-dialog v-model="showCancelDialog" max-width="400">
                    <v-card>
                      <v-card-title class="text-lg font-semibold">Confirm Cancel</v-card-title>
                      <v-card-text>
                        Are you sure you want to cancel this campaign?
                      </v-card-text>
                      <v-card-actions class="justify-end">
                        <v-btn
                            color="grey"
                            text
                            @click="showCancelDialog = false"
                        >
                          No
                        </v-btn>
                        <v-btn
                            color="red"
                            variant="flat"
                            @click="confirmCancel(campaign.campaign_id)"
                        >
                          Yes, Cancel
                        </v-btn>
                      </v-card-actions>
                    </v-card>
                  </v-dialog>
                </v-card-actions>
              </v-card>
            </v-col>
          </v-row>
        </template>
        <!-- if no data -->
        <template v-else>
          <div class="flex flex-col items-center justify-center py-20 text-gray-500">
            <v-icon size="64" color="grey-lighten-1">
              mdi-clipboard-text-off-outline
            </v-icon>
            <p class="mt-4 text-lg font-medium">
              {{ $t('campaign.no_campaigns') }}
            </p>
            <p class="text-sm text-gray-400">
              {{ $t('campaign.no_campaigns_hint') }}
            </p>
            <v-btn
                class="mt-6"
                color="black"
                @click="() => router.push('/campaign/posts/create')"
            >
              {{ $t('campaign.create_first_campaign') }}
            </v-btn>
          </div>
        </template>
      </v-card-text>
    </v-card>
  </v-container>
</template>


<style>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
</style>
