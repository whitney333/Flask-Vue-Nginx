<script setup>
import {ref, onMounted, watch, computed} from "vue";
import axios from "axios";
import {useUserStore} from "@/stores/user.js";
import {indexToCountry} from "@/libs/utils.js";


const campaigns = ref([]);
const loading = ref(false);

const selectedStatus = ref("");
const statusOptions = ["submitted", "approved", "cancelled"];
const postStatusOptions = ["New", "In progress", "Under review", "Published", "Suspended", "Paused"];
const postTypeOptions = ["Posts", "Reels/ Videos", "Stories"]
const userStore = useUserStore()
// selection
const budgetSelection = ["Less than US$100", "US$100 - US$1,000", "US$1,000 - US$5,000", "US$5,000 - US$10,000", "More than US$10,000"]
const countrySelection = []
const platformSelection = ["Instagram", "Tiktok", "Youtube", "Rednote", "Bilibili"]
const regionSelection = ["Asia", "North America", "South America", "Europe", "Oceania"]
// pagination
const page = ref(1); // current page
const limit = ref(10); // per page limit
const total = ref(0); // total page
const totalPages = computed(() => Math.ceil(total.value / limit.value));
// edit campaign
const showDialog = ref(false);
const selectedCampaign = ref([]);
const detailLoading = ref(false);
const editSection = ref({
  basic: false,
  performance: false,
  posts: false
});
// add campaign
const showAddDialog = ref(false);
const newCampaign = ref({
  user_id: "",
  status: "",
  artist_en_name: "",
  artist_kr_name: "",
  budget: "",
  target_region: [],
  target_platform: []
});
// alert message
const snackbar = ref({
  show: false,
  message: "",
  color: "info"
});
const showMessage = (msg, color = "info") => {
  snackbar.value.message = msg;
  snackbar.value.color = color;
  snackbar.value.show = true;
};

const fetchCampaigns = async () => {
  loading.value = true;
  try {
    const res = await axios.get(
        `/api/admin/v1/campaigns?page=${page.value}&limit=${limit.value}`,
    )
    campaigns.value = res.data.data;
    total.value = res.data.total;
    // console.log("res: ", res.data)

  } catch (err) {
    console.error("Error fetching campaigns:", err);
  } finally {
    loading.value = false;
  }
};

// approve campaign
const approveCampaign = async (campaignId) => {
  try {
    const token = userStore.firebaseToken
    await axios.patch(`/api/admin/v1/campaigns/${campaignId}/approve`,
        {}, {
          headers: {Authorization: `Bearer ${token}`}
        });
    fetchCampaigns();
  } catch (err) {
    console.error("Approve failed:", err);
  }
}

// cancel campaign
const cancelCampaign = async (campaignId) => {
  try {
    const token = userStore.firebaseToken;
    await axios.patch(`/api/admin/v1/campaigns/${campaignId}/cancel`,
        {}, {
          headers: {Authorization: `Bearer ${token}`}
        })
    fetchCampaigns();
  } catch (err) {
    console.error("Cancel failed:", err);
  }
}

const openDialog = (campaign) => {
  editingCampaign.value = {...campaign};
  showDialog.value = true;
};

// view specific campaign
const viewCampaignDetail = async (campaignId) => {
  console.log("Clicked row:", campaignId);
  showDialog.value = true;
  detailLoading.value = true;
  selectedCampaign.value = {};

  try {
    const token = userStore.firebaseToken
    const res = await axios.get(
        `/api/admin/v1/campaigns/${campaignId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
    );

    selectedCampaign.value = res.data.data || {};

    if (!Array.isArray(selectedCampaign.value.actual_region)) {
      selectedCampaign.value.actual_region = [];
    }
    if (!Array.isArray(selectedCampaign.value.actual_country)) {
      selectedCampaign.value.actual_country = [];
    }
    if (!Array.isArray(selectedCampaign.value.actual_platform)) {
      selectedCampaign.value.actual_platform = [];
    }
  } catch (err) {
    console.error("Fetch campaign details failed:", err);
  } finally {
    loading.value = false;
  }
}

// add campaign
const addCampaign = async () => {
  try {

  } catch (err) {

  }
}

// update campaign
const updateCampaign = async (section, campaignId) => {
  try {
    const token = userStore.firebaseToken
    let payload = {}

    if (section === "basic") {
      //basic info
      payload = {
        user_target_region: selectedCampaign.value.user_target_region,
        budget: selectedCampaign.value.budget,
        user_target_platform: selectedCampaign.value.user_target_platform,
        user_post_info: {
          title: selectedCampaign.value.user_post_info.title,
          description: selectedCampaign.value.user_post_info.description,
          hashtag: selectedCampaign.value.user_post_info.hashtag,
          url: selectedCampaign.value.user_post_info.url,
        }
      };
    }
    //performance info
    if (section === "performance") {
      payload = {
        actual_region: selectedCampaign.value.actual_region,
        actual_country: selectedCampaign.value.actual_country,
        actual_platform: selectedCampaign.value.actual_platform
      };
    }
    //posts info
    if (section === "posts") {
      payload = {
        post: selectedCampaign.value.post.map(p => ({
          kol_account: p.kol_account,
          post_created_at: new Date(p.post_created_at).toISOString(),
          status: p.status,
          artist: p.artist,
          content: p.content,
          type: p.type,
          platform: p.platform,
          target_country: p.target_country,
          reach: p.reach,
          reaction: p.reaction,
          engagement: p.engagement,
          hashtag_reach: p.hashtag_reach,
          one_hour_view: p.one_hour_view,
          twentyfour_hour_view: p.twentyfour_hour_view,
          latest_view: p.latest_view,
          cost: p.cost,
          cost_per_reach: p.cost_per_reach,
          cost_per_view: p.cost_per_view,
          url: p.url,
          used_hashtag: p.used_hashtag,
          notes: p.notes
        }))
      }
    }

    console.log("payload: ", payload)
    // console.log(typeof(payload))
    const res = await axios.patch(
        `/api/admin/v1/campaigns/${campaignId}/update`,
        payload, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
    );
    // console.log("revise: ", res.data)
  } catch (err) {
    console.error("Update failed:", err);
  }
}

const startEdit = (section) => {
  editSection.value[section] = true;
};

const saveSection = async (section) => {
  try {
    const campaignId = selectedCampaign.value.campaign_id;
    await updateCampaign(section, campaignId);
    editSection.value[section] = false;
    console.log(`${section} saved`);
  } catch (err) {
    console.error("Save failed", err);
  }
};

const cancelSection = (section) => {
  // TODO: restore backup
  editSection.value[section] = false;
};

// Performance section: add new region
const addRegion = (index) => {
  const regionList = selectedCampaign.value.actual_region || [];

  regionList.splice(index + 1, 0, {
    name: '',
    count: 0,
  });

  // reassign
  selectedCampaign.value.actual_region = [...regionList];
}

// Performance section: add new country
const addCountry = (index) => {
  const countryList = selectedCampaign.value.actual_country || [];

  countryList.splice(index + 1, 0, {
    name: '',
    count: 0,
  });

  // reassign
  selectedCampaign.value.actual_country = [...countryList];
}

// Performance section: add new platform
const addPlatform = (index) => {
  const platformList = selectedCampaign.value.actual_platform || [];

  platformList.splice(index + 1, 0, {
    name: '',
    count: 0,
  });

  // reassign
  selectedCampaign.value.actual_platform = [...platformList];
}

const closeDialog = () => {
  showDialog.value = false;
};

const formatDate = (date) => {
  if (!date) return "-";
  return new Date(date).toLocaleString();
};

onMounted(fetchCampaigns);

watch([page, limit], () => {
  fetchCampaigns();
});

</script>

<template>
  <div class="p-6 bg-gray-50 min-h-screen">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-semibold text-gray-800">All Campaigns</h2>
      <!-- open Dialog -->
      <button
          @click="showAddDialog = true"
          class="flex items-center gap-2 bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"
             stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/>
        </svg>
        Add New Campaign
      </button>
    </div>

    <!-- Filters -->
    <div class="flex flex-wrap gap-4 mb-6">
      <div>
        <label class="text-sm text-gray-600 block mb-1">Status</label>
        <select
            v-model="selectedStatus"
            class="border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
        >
          <option value="">All</option>
          <option v-for="s in statusOptions" :key="s" :value="s">{{ s }}</option>
        </select>
      </div>

      <button
          @click="fetchCampaigns"
          class="self-end bg-gray-800 text-white px-4 py-2 rounded-lg hover:bg-gray-900 transition"
      >
        Apply Filter
      </button>
    </div>

    <!-- open dialog: add new campaign -->
    <v-dialog v-model="showAddDialog" max-width="500px">
      <v-card>
        <v-card-title class="text-h6">Add New Campaign</v-card-title>

        <v-card-text>
          <v-text-field
              label="User ID"
              v-model="newCampaign.user_id"
              variant="underlined"
          ></v-text-field>
          <v-text-field
              label="Artist EN Name"
              v-model="newCampaign.artist_en_name"
              variant="underlined"
          ></v-text-field>
          <v-select
              label="Status"
              :items="statusOptions"
              v-model="newCampaign.status"
              variant="underlined"
          ></v-select>
          <v-select
              label="Target Region"
              :items="regionSelection"
              v-model="newCampaign.target_region"
              variant="underlined"
          ></v-select>
          <v-select
              label="Target Platform"
              :items="platformSelection"
              v-model="newCampaign.target_platform"
              variant="underlined"
          ></v-select>
          <v-select
              label="Budget"
              :items="budgetSelection"
              v-model="newCampaign.budget"
              variant="underlined"
          ></v-select>
        </v-card-text>

        <v-card-actions class="justify-end">
          <v-btn variant="text" @click="showAddDialog = false">Cancel</v-btn>

          <v-btn
              color="indigo"
              class="text-white"
              @click="addCampaign"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- Snackbar -->
    <v-snackbar
        v-model="snackbar.show"
        :color="snackbar.color"
        timeout="1500"
        location="top">
      {{ snackbar.message }}
    </v-snackbar>

    <!-- Table -->
    <div class="overflow-x-auto bg-white rounded-lg shadow">
      <table class="min-w-full text-sm text-gray-700">
        <thead class="bg-gray-100 text-left text-gray-600 uppercase text-xs">
        <tr>
          <th class="px-6 py-3">Campaign ID</th>
          <th class="px-6 py-3">Status</th>
          <th class="px-6 py-3">Created At</th>
          <th class="px-6 py-3">Approved At</th>
          <th class="px-6 py-3">Cancelled At</th>
          <th class="px-6 py-3">User Name</th>
          <th class="px-6 py-3">User Email</th>
          <th class="px-6 py-3">Actions</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="c in campaigns"
            :key="c.campaign_id"
            @click="viewCampaignDetail(c.campaign_id)"
            class="border-t hover:bg-gray-50 transition">
          <td class="px-6 py-3 font-mono">{{ c.campaign_id }}</td>
          <td class="px-6 py-3 capitalize">
              <span
                  class="px-2 py-1 rounded text-xs font-medium"
                  :class="{
                  'bg-green-100 text-green-800': c.status === 'approved',
                  'bg-blue-100 text-blue-800': c.status === 'submitted',
                  'bg-red-100 text-red-800': c.status === 'cancelled'
                }"
              >
                {{ c.status }}
              </span>
          </td>
          <td class="px-6 py-3">{{ formatDate(c.created_at) }}</td>
          <td class="px-6 py-3">{{ formatDate(c.approved_at) }}</td>
          <td class="px-6 py-3">{{ formatDate(c.cancelled_at) }}</td>
          <td class="px-6 py-3">{{ c.user_name || '-' }}</td>
          <td class="px-6 py-3">{{ c.user_email || '-' }}</td>
          <td class="px-6 py-3 flex gap-2">
            <button
                v-if="c.status !== 'approved'"
                @click="approveCampaign(c.campaign_id)"
                class="px-2 py-1 rounded text-xs font-medium cursor-pointer border border-green-600 text-green-600 hover:bg-green-50 transition"
            >
              Approve
            </button>
            <button
                v-if="c.status !== 'cancelled'"
                @click="cancelCampaign(c.campaign_id)"
                class="px-2 py-1 rounded text-xs font-medium cursor-pointer border border-red-600 text-red-600 hover:bg-red-50 transition"
            >
              Cancel
            </button>
          </td>
        </tr>
        <tr v-if="!loading && campaigns.length === 0">
          <td colspan="6" class="text-center text-gray-500 py-6">No campaigns found</td>
        </tr>
        </tbody>
      </table>
    </div>

    <!-- Campaign Details Dialog -->
    <v-dialog v-model="showDialog" max-width="800px">
      <v-card>
        <v-card-title class="text-h6 flex justify-between items-center">
          Campaign Details
          <v-chip
              :color="editSection.basic ? 'indigo' : 'grey'"
              text-color="white"
              size="small"
          >
            {{ editSection.basic ? 'Edit Mode' : 'View Mode' }}
          </v-chip>
        </v-card-title>

        <v-card-text>
          <v-skeleton-loader v-if="dialogLoading" type="card"/>

          <div v-else class="space-y-8">
            <!-- Basic Info Section -->
            <div>
              <div class="flex justify-between items-center mb-2">
                <h3 class="text-lg font-semibold">Basic Info</h3>
                <v-btn
                    icon
                    variant="text"
                    @click="startEdit('basic')"
                    v-if="!editSection.basic"
                >
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>

                <div v-if="editSection.basic" class="flex gap-2">
                  <v-btn size="small" color="success" @click="saveSection('basic')">Save</v-btn>
                  <v-btn size="small" color="error" @click="cancelSection('basic')">Cancel</v-btn>
                </div>
              </div>

              <!-- Basic Info Content -->
              <div>
                <v-row dense>
                  <v-col cols="12" md="6">
                    <v-text-field
                        v-model="selectedCampaign.campaign_id"
                        label="Campaign ID"
                        variant="underlined"
                        readonly
                    />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field
                        v-model="selectedCampaign.status"
                        label="Status"
                        variant="underlined"
                        readonly
                    />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field
                        v-model="selectedCampaign.created_at"
                        label="Created At"
                        variant="underlined"
                        readonly
                    />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field
                        v-model="selectedCampaign.user_id"
                        label="User ID"
                        variant="underlined"
                        readonly
                    />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field
                        v-model="selectedCampaign.artist_en_name"
                        label="Artist Name"
                        variant="underlined"
                        readonly
                    />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field
                        v-model="selectedCampaign.artist_kr_name"
                        label="Artist Name"
                        variant="underlined"
                        readonly
                    />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-select
                        v-model="selectedCampaign.budget"
                        :items="budgetSelection"
                        label="Budget"
                        variant="underlined"
                        :readonly="!editSection.basic"
                    />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-select
                        v-model="selectedCampaign.user_target_region"
                        :items="indexToCountry"
                        label="Target Region"
                        variant="underlined"
                        multiple
                        :readonly="!editSection.basic"
                    />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-select
                        v-model="selectedCampaign.user_target_platform"
                        :items="platformSelection"
                        label="Target Platform"
                        variant="underlined"
                        multiple
                        :readonly="!editSection.basic"
                    />
                  </v-col>
                  <v-col cols="12">
                    <v-textarea
                        v-model="selectedCampaign.user_post_info.title"
                        :placeholder="selectedCampaign.user_post_info.title ? '' : 'None'"
                        label="User Post Title"
                        rows="1"
                        variant="underlined"
                    />
                    <v-textarea
                        v-model="selectedCampaign.user_post_info.description"
                        :placeholder="selectedCampaign.user_post_info.description ? '' : 'None'"
                        label="User Post Description"
                        rows="1"
                        variant="underlined"
                    />
                    <v-textarea
                        v-model="selectedCampaign.user_post_info.url"
                        :placeholder="selectedCampaign.user_post_info.url ? '' : 'None'"
                        label="User Provided Link"
                        rows="1"
                        variant="underlined"
                    />
                    <v-combobox
                        v-model="selectedCampaign.user_post_info.hashtag"
                        label="User Requested Hashtags"
                        multiple
                        chips
                        small-chips
                        variant="underlined"
                        placeholder="None"
                        :closable-chips="editSection.basic"
                        :readonly="!editSection.basic"
                        class="hashtag-combobox"
                    />
                  </v-col>
                </v-row>
              </div>
            </div>

            <!-- Performance Section -->
            <div>
              <div class="flex justify-between items-center mb-2">
                <h3 class="text-lg font-semibold">Performance</h3>
                <v-btn
                    icon
                    variant="text"
                    @click="startEdit('performance')"
                    v-if="!editSection.performance"
                >
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>

                <div v-if="editSection.performance" class="flex gap-2">
                  <v-btn size="small" color="success" @click="saveSection('performance')">
                    Save
                  </v-btn>
                  <v-btn size="small" color="error" @click="cancelSection('performance')">
                    Cancel
                  </v-btn>
                </div>
              </div>

              <!-- Performance Info Content -->
              <div>
                <v-row dense>
                  <!-- Performance - Region View Mode -->
                  <v-col cols="12">
                    <div v-if="!editSection.performance">
                      <div class="text-subtitle-2 font-weight-medium mb-1">Region</div>
                      <v-chip-group multiple>
                        <v-chip
                            v-for="region in selectedCampaign.actual_region"
                            :key="region.name"
                            color="blue"
                            variant="tonal"
                            :ripple="false"
                            class="pointer-events-none"
                        >
                          {{ region.name }} ({{ region.count }})
                        </v-chip>
                      </v-chip-group>
                    </div>
                    <!-- Performance - Region Edit Mode -->
                    <div v-else>
                      <v-row v-for="(p, index) in selectedCampaign.actual_region || []" :key="index" align="center">
                        <v-col cols="5">
                          <v-select
                              v-model="p.name"
                              :items="regionSelection"
                              label="Region Name"
                              variant="underlined"
                              dense
                          />
                        </v-col>
                        <v-col cols="5">
                          <v-text-field
                              v-model.number="p.count"
                              label="Count"
                              type="number"
                              variant="underlined"
                              dense
                              min="0"
                          />
                        </v-col>

                        <v-col cols="2" class="text-center">
                          <v-btn
                              icon="mdi-plus"
                              color="blue"
                              variant="text"
                              @click="addRegion(index)"
                          ></v-btn>
                          <v-btn
                              icon="mdi-delete"
                              color="red"
                              variant="text"
                              @click="selectedCampaign.actual_region.splice(index, 1)"
                          ></v-btn>
                        </v-col>
                      </v-row>
                    </div>
                  </v-col>
                  <!-- Performance - Country View Mode -->
                  <v-col cols="12">
                    <div v-if="!editSection.performance">
                      <div class="text-subtitle-2 font-weight-medium mb-1">Country</div>
                      <v-chip-group multiple>
                        <v-chip
                            v-for="country in selectedCampaign.actual_country"
                            :key="country.name"
                            color="blue"
                            variant="tonal"
                            :ripple="false"
                            class="pointer-events-none"
                        >
                          {{ country.name }} ({{ country.count }})
                        </v-chip>
                      </v-chip-group>
                    </div>
                    <!-- Performance - Country Edit Mode -->
                    <div v-else>
                      <v-row v-for="(p, index) in selectedCampaign.actual_country" :key="index" align="center">
                        <v-col cols="5">
                          <v-select
                              v-model="p.name"
                              :items="indexToCountry"
                              label="Country Name"
                              variant="underlined"
                              dense
                          />
                        </v-col>
                        <v-col cols="5">
                          <v-text-field
                              v-model.number="p.count"
                              label="Count"
                              type="number"
                              variant="underlined"
                              dense
                              min="0"
                          />
                        </v-col>

                        <v-col cols="2" class="text-center">
                          <v-btn
                              icon="mdi-plus"
                              color="blue"
                              variant="text"
                              @click="addCountry(index)"
                          ></v-btn>
                          <v-btn
                              icon="mdi-delete"
                              color="red"
                              variant="text"
                              @click="selectedCampaign.actual_country.splice(index, 1)"
                          ></v-btn>
                        </v-col>
                      </v-row>

                    </div>
                  </v-col>
                  <!-- Performance - Platform View Mode -->
                  <v-col cols="12">
                    <div v-if="!editSection.performance">
                      <div class="text-subtitle-2 font-weight-medium mb-1">Platform</div>
                      <v-chip-group multiple>
                        <v-chip
                            v-for="platform in selectedCampaign.actual_platform"
                            :key="platform.name"
                            color="blue"
                            variant="tonal"
                            :ripple="false"
                            class="pointer-events-none"
                        >
                          {{ platform.name }} ({{ platform.count }})
                        </v-chip>
                      </v-chip-group>
                    </div>
                    <!-- Performance - Platform Edit Mode -->
                    <div v-else>
                      <v-row v-for="(p, index) in selectedCampaign.actual_platform" :key="index" align="center">
                        <v-col cols="5">
                          <v-select
                              v-model="p.name"
                              :items="platformSelection"
                              label="Platform Name"
                              variant="underlined"
                              dense
                          />
                        </v-col>
                        <v-col cols="5">
                          <v-text-field
                              v-model.number="p.count"
                              label="Count"
                              type="number"
                              variant="underlined"
                              dense
                              min="0"
                          />
                        </v-col>

                        <v-col cols="2" class="text-center">
                          <v-btn
                              icon="mdi-plus"
                              color="blue"
                              variant="text"
                              @click="addPlatform(index)"
                          ></v-btn>
                          <v-btn
                              icon="mdi-delete"
                              color="red"
                              variant="text"
                              @click="selectedCampaign.actual_platform.splice(index, 1)"
                          ></v-btn>
                        </v-col>
                      </v-row>

                    </div>
                  </v-col>
                </v-row>
              </div>
            </div>

            <!-- Posts Section -->
            <div>
              <div class="flex justify-between items-center mb-2">
                <h3 class="text-lg font-semibold">Posts</h3>

                <v-btn
                    icon
                    variant="text"
                    @click="startEdit('posts')"
                    v-if="!editSection.posts"
                >
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>

                <div v-if="editSection.posts" class="flex gap-2">
                  <v-btn size="small" color="success" @click="saveSection('posts')">Save</v-btn>
                  <v-btn size="small" color="error" @click="cancelSection('posts')">Cancel</v-btn>
                </div>
              </div>

              <!-- Posts info -->
              <div>
                <v-row>
                  <v-col
                      v-for="(p, index) in selectedCampaign.post || []"
                      :key="index"
                      cols="12"
                  >
                    <v-card class="pa-4 rounded-xl elevation-2 w-100 bg-grey-lighten-4">
                      <!-- Card Title -->
                      <v-card-title class="text-h6 font-weight-bold pb-1 rounded-lg px-4 py-3">
                        Post {{ index + 1 }}
                      </v-card-title>

                      <v-divider class="mb-3"></v-divider>
                      <v-row>
                        <v-col cols="6">
                          <v-text-field
                              v-model="p.kol_account"
                              label="KOL"
                              variant="underlined"
                              :readonly="!editSection.posts"
                          />
                        </v-col>

                        <v-col cols="6">
                          <v-select
                              v-model="p.status"
                              :items="postStatusOptions"
                              label="Status"
                              variant="underlined"
                              :readonly="!editSection.posts"
                          />
                        </v-col>

                        <v-col cols="6">
                          <v-text-field
                              v-model="p.artist"
                              label="Artist"
                              variant="underlined"
                              :readonly="!editSection.posts"
                          />
                        </v-col>

                        <v-col cols="6">
                          <v-text-field
                              v-model="p.content"
                              label="Content"
                              variant="underlined"
                              :readonly="!editSection.posts"
                          />
                        </v-col>

                        <v-col cols="6">
                          <v-text-field
                              v-model="p.post_created_at"
                              label="Created at"
                              variant="underlined"
                              :readonly="!editSection.posts"
                          />
                        </v-col>

                        <v-col cols="6">
                          <v-select
                              v-model="p.type"
                              :items="postTypeOptions"
                              label="Type"
                              variant="underlined"
                              :readonly="!editSection.posts"
                          />
                        </v-col>

                        <v-col cols="6">
                          <v-select
                              v-model="p.platform"
                              :items="platformSelection"
                              label="Platform"
                              variant="underlined"
                              :readonly="!editSection.posts"
                          />
                        </v-col>

                        <v-col cols="6">
                          <v-select
                              v-model="p.target_country"
                              :items="indexToCountry"
                              label="Country"
                              variant="underlined"
                              :readonly="!editSection.posts"
                          />
                        </v-col>

                        <!-- Reach Count -->
                        <v-col cols="3">
                          <v-text-field
                              v-model="p.reach"
                              label="Reach"
                              variant="underlined"
                              :readonly="!editSection.posts"
                          />
                        </v-col>
                        <v-col cols="3">
                          <v-text-field
                              v-model="p.reaction"
                              label="Reaction"
                              variant="underlined"
                              :readonly="!editSection.posts"
                          />
                        </v-col>
                        <v-col cols="3">
                          <v-text-field
                              v-model="p.engagement"
                              label="Engagement"
                              variant="underlined"
                              :readonly="!editSection.posts"
                          />
                        </v-col>
                        <v-col cols="3">
                          <v-text-field
                              v-model="p.hashtag_reach"
                              label="Hashtag Reach"
                              variant="underlined"
                              :readonly="!editSection.posts"
                          />
                        </v-col>

                        <!-- View Count -->
                        <v-col cols="4">
                          <v-text-field
                              v-model="p.one_hour_view"
                              label="1hr View"
                              variant="underlined"
                              :readonly="!editSection.posts"
                          />
                        </v-col>
                        <v-col cols="4">
                          <v-text-field
                              v-model="p.twentyfour_hour_view"
                              label="24hr View"
                              variant="underlined"
                              :readonly="!editSection.posts"
                          />
                        </v-col>
                        <v-col cols="4">
                          <v-text-field
                              v-model="p.latest_view"
                              label="Latest View"
                              variant="underlined"
                              :readonly="!editSection.posts"
                          />
                        </v-col>

                        <!-- Cost Count -->
                        <v-col cols="4">
                          <v-text-field
                              v-model="p.cost"
                              label="Cost"
                              variant="underlined"
                              :readonly="!editSection.posts"
                          />
                        </v-col>
                        <v-col cols="4">
                          <v-text-field
                              v-model="p.cost_per_reach"
                              label="Cost per Reach"
                              variant="underlined"
                              :readonly="!editSection.posts"
                          />
                        </v-col>
                        <v-col cols="4">
                          <v-text-field
                              v-model="p.cost_per_view"
                              label="Cost per View"
                              variant="underlined"
                              :readonly="!editSection.posts"
                          />
                        </v-col>
                        <!-- Link -->
                        <v-col cols="12">
                          <v-text-field
                              v-model="p.url"
                              label="Link"
                              variant="underlined"
                              :readonly="!editSection.posts"
                          />
                        </v-col>
                        <!-- Used hashtag -->
                        <v-col cols="12">
                          <v-combobox
                              v-model="p.used_hashtag"
                              label="Used Hashtags"
                              multiple
                              chips
                              small-chips
                              variant="underlined"
                              placeholder="None"
                              :closable-chips="editSection.posts"
                              :readonly="!editSection.posts"
                              class="hashtag-combobox"
                          />
                        </v-col>
                        <!-- Notes -->
                        <v-col cols="12">
                          <v-text-field
                              v-model="p.notes"
                              label="Notes"
                              variant="underlined"
                              :readonly="!editSection.posts"
                          />
                        </v-col>
                      </v-row>
                    </v-card>
                  </v-col>
                </v-row>
              </div>
            </div>
          </div>
        </v-card-text>

        <v-card-actions class="justify-end">
          <v-btn text @click="closeDialog">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>


    <!-- Pagination -->
    <div class="flex justify-between items-center mt-4 flex-wrap gap-2">
      <!-- per page limit -->
      <div class="flex items-center gap-2">
        <span class="text-sm text-gray-600">Rows per page:</span>
        <select v-model="limit" class="border border-gray-300 rounded px-2 py-1">
          <option v-for="n in [5, 10, 20, 50]" :key="n" :value="n">{{ n }}</option>
        </select>
      </div>

      <!-- pagination -->
      <div class="flex items-center gap-2">
        <button @click="page = 1" :disabled="page === 1"
                class="px-3 py-1 rounded border hover:bg-gray-100 disabled:opacity-50">« First
        </button>
        <button @click="page = page - 1" :disabled="page === 1"
                class="px-3 py-1 rounded border hover:bg-gray-100 disabled:opacity-50">‹ Prev
        </button>

        <span class="text-sm text-gray-600">Page {{ page }} of {{ totalPages }}</span>

        <button @click="page = page + 1" :disabled="page === totalPages"
                class="px-3 py-1 rounded border hover:bg-gray-100 disabled:opacity-50">Next ›
        </button>
        <button @click="page = totalPages" :disabled="page === totalPages"
                class="px-3 py-1 rounded border hover:bg-gray-100 disabled:opacity-50">Last »
        </button>
      </div>
      <!-- Loading -->
      <div v-if="loading" class="text-center py-6 text-gray-500">Loading...</div>
    </div>

  </div>
</template>

<style scoped>
.hashtag-combobox.v-input--readonly .v-chip {
  background-color: #e0e0e0;
  color: #555;
  cursor: default;
}
</style>