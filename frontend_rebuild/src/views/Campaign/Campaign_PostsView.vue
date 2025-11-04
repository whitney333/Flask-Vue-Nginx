<script setup>
import { onMounted, ref } from "vue";
import { useArtistStore } from "@/stores/artist.js";
import { useUserStore } from "@/stores/user.js";
import axios from '@/axios';
import { useRouter } from 'vue-router';
import { DollarSign, Globe, Share2, Box, Blocks } from 'lucide-vue-next';
import CampaignPercentCard from "@/views/Campaign/components/Campaign_PercentCard.vue";
import campaignJSON from './json/campaignViewDetails.json'
import CampaignDataTable from "@/views/Campaign/components/Campaign_DataTable.vue";


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
    console.log("cp: ", res)
    console.log("cp1 :", res.data.data)
  } catch (err) {
    console.error("Error loading campaigns:", err)
  }
}

onMounted(() => {
  getAllCampaign()
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
  console.log("Open performance for:", campaign)
  selectedCampaign.value = campaign
  showPerformanceDialog.value = true
  //
}

const closePerformanceDialog = () => {
  showPerformanceDialog.value = false
  selectedPerformanceCampaign.value = null
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
      <template v-slot:title>
        <div class="flex w-full items-center justify-between">
            <span class="text-h4">{{ $t('campaign.post') }}</span>
            <v-btn @click="() => router.push('/campaign/posts/create')" color="black">Create Post</v-btn>
        </div>
      </template>
      <v-card-text class="mt-4">
        <!-- loading condition -->
        <div v-if="loading" class="flex justify-center items-center py-20">
          <v-progress-circular indeterminate color="black" size="48"/>
        </div>
        <!-- if data exists -->
        <template v-else-if="campaigns && campaigns.length > 0">
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
                      <v-card class="flex flex-col max-h-[90vh]">
                        <!-- Header -->
                        <div
                            class="bg-gradient-to-r from-gray-800 via-gray-700 to-gray-600 text-white p-5 flex items-center justify-between">
                          <div>
                            <h2 class="text-xl font-semibold">{{ selectedCampaign?.campaign_id }} Campaign
                              Performance</h2>
                            <p class="text-sm opacity-90">{{ selectedCampaign?.artist_en_name }}
                              ({{ selectedCampaign?.artist_kr_name }})</p>
                          </div>
                          <v-chip color="blue-lighten-3" text-color="black" size="small">
                            {{ selectedCampaign?.status }}
                          </v-chip>
                        </div>

                        <v-card-text class="p-4 flex-1">
                          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                            <CampaignPercentCard
                                :value="{
                              fetchURL: campaignJSON.campaignPlatformPercentage.fetchURL,
                              fetchFollowerType: campaignJSON.campaignPlatformPercentage.followerDataType,
                              title: campaignJSON.campaignPlatformPercentage.title,
                              tooltipText: campaignJSON.campaignPlatformPercentage.tooltipText,
                              colors: ['#4E56C0', '#9B5DE0', '#D78FEE', '#FDCFFA', '#FDAAAA', '#F8F7BA']
                            }"
                                :campaignId="selectedCampaign?.campaign_id"
                            />
                            <CampaignPercentCard
                                :value="{
                              fetchURL: campaignJSON.campaignRegionPercentage.fetchURL,
                              fetchFollowerType: campaignJSON.campaignRegionPercentage.followerDataType,
                              title: campaignJSON.campaignRegionPercentage.title,
                              tooltipText: campaignJSON.campaignRegionPercentage.tooltipText,
                              colors: ['#4E56C0', '#9B5DE0', '#D78FEE', '#FDCFFA', '#FDAAAA', '#F8F7BA']
                            }"
                                :campaignId="selectedCampaign?.campaign_id"
                            />
                            <CampaignPercentCard
                                :value="{
                              fetchURL: campaignJSON.campaignCountryPercentage.fetchURL,
                              fetchFollowerType: campaignJSON.campaignCountryPercentage.followerDataType,
                              title: campaignJSON.campaignCountryPercentage.title,
                              tooltipText: campaignJSON.campaignCountryPercentage.tooltipText,
                              colors: ['#4E56C0', '#9B5DE0', '#D78FEE', '#FDCFFA', '#FDAAAA', '#F8F7BA']
                            }"
                                :campaignId="selectedCampaign?.campaign_id"
                            />
                            <CampaignPercentCard
                                :value="{
                              fetchURL: campaignJSON.campaignCountryPercentage.fetchURL,
                              fetchFollowerType: campaignJSON.campaignCountryPercentage.followerDataType,
                              title: campaignJSON.campaignCountryPercentage.title,
                              tooltipText: campaignJSON.campaignCountryPercentage.tooltipText,
                              colors: ['#4E56C0', '#9B5DE0', '#D78FEE', '#FDCFFA', '#FDAAAA', '#F8F7BA']
                            }"
                                :campaignId="selectedCampaign?.campaign_id"
                            />
                          </div>
                          <div class="grid grid-cols-1 md:grid-cols-1 gap-4">
                            <CampaignDataTable :campaignId="selectedCampaign?.campaign_id"/>
                          </div>
                        </v-card-text>

                        <v-card-actions>
                          <v-spacer/>
                          <v-btn color="grey" variant="text" @click="closePerformanceDialog">
                            Close
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
                    View Details
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
                            <p class="text-gray-500 text-sm">Platform</p>
                            <p class="font-medium">{{ selectedCampaign?.platform.join(', ') }}</p>
                          </div>
                          <div>
                            <p class="text-gray-500 text-sm">Region</p>
                            <p class="font-medium">{{ selectedCampaign?.region.join(', ') }}</p>
                          </div>
                          <div>
                            <p class="text-gray-500 text-sm">Budget</p>
                            <p class="font-medium">{{ selectedCampaign?.budget }}</p>
                          </div>
                          <div>
                            <p class="text-gray-500 text-sm">Created At</p>
                            <p class="font-medium">{{ new Date(selectedCampaign?.created_at).toLocaleString() }}</p>
                          </div>
                        </div>

                        <v-divider class="my-4"></v-divider>

                        <!-- Description-->
                        <div class="mb-2">
                          <p class="text-gray-500 text-sm mb-1">Description</p>
                          <p class="text-base leading-relaxed">
                            {{ selectedCampaign?.info?.description || 'No description provided.' }}
                          </p>
                        </div>
                        <!-- Hashtag -->
                        <div class="mb-2">
                          <p class="text-gray-500 text-sm mb-1">Hashtags</p>
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
                          <p class="text-gray-500 text-sm mb-1">URL</p>
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
                        <v-btn text color="black" @click="dialog = false">Close</v-btn>
                      </v-card-actions>

                    </v-card>
                  </v-dialog>
                  <!-- open cancel dialog -->
                  <v-btn
                      @click="openCancelDialog(campaign.campaign_id)"
                      color="red"
                      variant="outlined"
                  >
                    Cancel
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
