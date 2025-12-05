<script setup>
import {ref, onMounted, watch, computed} from "vue";
import axios from "axios";
import {useUserStore} from "@/stores/user.js";
import StatusChip from "@/components/StatusChip.vue"

// dropdown list options
const tenantOptions = ref([])
const threadsOption = [true, false]
const pronounsOption = ["C", "F", "M"]
const typeOptions = ["Actor", "Musician"]
const nationOptions = ["Canada", "Hong Kong", "Japan", "Mainland China", "South Korea", "Taiwan", "Thailand", "United States"]
const currentYear = new Date().getFullYear()
const debutYears = Array.from({ length: currentYear - 1950 + 1 }, (_, i) => 1950 + i)

const profileImageFile = ref(null);
const artists = ref([]);
const loading = ref(false);
const userStore = useUserStore();
const showDialog = ref(false);
const datePickerMenu = ref(false);
// pagination
const page = ref(1); // current page
const limit = ref(10); // per page limit
const total = ref(0); // total page
const totalPages = computed(() => Math.ceil(total.value / limit.value));

// edit artist info
const showEditDialog = ref(false);
const selectedArtist = ref([]);
const detailLoading = ref(false);
const editSection = ref({
  basic: false,
  sns: false,
  music: false
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

// add new tenant
const showAddTenantDialog = ref(false);
const newTenantName = ref("");

// add new artist
const showAddDialog = ref(false);
const birthMenu = ref(false);
const birthPicker = ref(null);
const birthText = ref("");

const setBirth = async (val) => {
  birthText.value = new Date(val).toISOString()
  birthMenu.value = false
};

const newArtist = ref({
  artist_id: "",
  english_name: "",
  korean_name: "",
  debut_year: "",
  nation: "",
  pronouns: "",
  type: [],
  birth: null,
  fandom: "",
  belong_group: [],
  instagram_id: "",
  instagram_user: "",
  threads: "",
  youtube_id: "",
  tiktok_id: "",
  spotify_id: "",
  melon_id: "",
  genie_id: "",
  apple_id: "",
  bilibili_id: "",
  weibo_id: "",
  tenant_id: "",
  image_url: ""
});

// fetch all artist
const fetchArtists = async () => {
  loading.value = true;
  try {
    const res = await axios.get(
        `/api/admin/v1/artists`, {
          params: {
            page: page.value,
            limit: limit.value,
            name: filters.value.english_name,
            type: filters.value.type,
            pronouns: filters.value.pronouns,
            debut_year: filters.value.debut_year
          }
        }
    )
    artists.value = res.data.data;
    total.value = res.data.total;
    // console.log("res: ", res.data.data)

  } catch (err) {
    console.error("Error fetching artists:", err);
  } finally {
    loading.value = false;
  }
};

// artist types: chips color style
const typeClass = (t) => {
  switch (t.toLowerCase()) {
    case "actor":
      return "bg-purple-100 text-purple-800"
    case "musician":
      return "bg-blue-100 text-blue-800"
    default:
      return "bg-gray-100 text-gray-700"
  }
}

// add new artist
const addArtist = async () => {
  loading.value = true;
  try {
    const token = userStore.firebaseToken
    const res = await axios.post(
        `/api/admin/v1/artists`,
        newArtist.value, {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          }
        }
    )
    showMessage("Artist added successfully.", "success");
    this.showAddDialog = false;
  } catch (err) {
    if (err.response?.status === 409) {
      showMessage("Artist already exists. Please check artist name, company, pronouns and types.", "error")
    } else if (err.response?.status === 400) {
      showMessage("Please input artist name.", "warning")
    } else {
      showMessage("Server error. Please try again later.", "error")
    }
  } finally {
    loading.value = false
  }
}

// if tenant not exists, add new tenant
const addTenant = async () => {
  try {

  } catch (err) {

  }
}

// view specific artist
const viewArtistDetail = async (artistId) => {
  console.log("Clicked row:", artistId);
  showDialog.value = true;
  detailLoading.value = true;
  selectedArtist.value = {};

  try {
    const token = userStore.firebaseToken
    const res = await axios.get(
        `/api/admin/v1/artists/${artistId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
    );

    selectedArtist.value = res.data.data || {};
  } catch (err) {
    console.error("Fetch artist details failed:", err);
  } finally {
    loading.value = false;
  }
}

// preprocess none value to null
const normalizeValue = (value) => {
  if (value === "" || value === undefined) return null
  if (value === null) return null
  return value
}

// update artist
const updateArtist = async (section, artistId) => {
  try {
    const token = userStore.firebaseToken
    let payload = {}

    //basic info
    if (section === "basic") {
      payload = {
        id: selectedArtist.value.id,
        artist_id: Number(selectedArtist.value.artist_id),
        tenant_id: selectedArtist.value.tenant_id,
        english_name: selectedArtist.value.artist_en_name,
        korean_name: selectedArtist.value.artist_kr_name,
        debut_year: Number(selectedArtist.value.debut ),
        type: selectedArtist.value.type,
        nation: selectedArtist.value.nation,
        pronouns: selectedArtist.value.pronouns,
        fandom: selectedArtist.value.fandom,
        birth: formattedBirth.value,
        image_url: selectedArtist.value.image
      }
    }

    //sns info
    if (section === "sns") {
      payload = {
        id: selectedArtist.value.id,
        instagram_id: selectedArtist.value.instagram_id || null,
        instagram_user: selectedArtist.value.instagram_user || null,
        threads: selectedArtist.value.threads != null ? selectedArtist.value.threads : false,
        tiktok_id: selectedArtist.value.tiktok_id || null,
        bilibili_id: normalizeValue(selectedArtist.value.bilibili_id),
        weibo_id: normalizeValue(selectedArtist.value.weibo_id)
      }
    }

    //music info
    if (section === "music") {
      payload = {
        id: selectedArtist.value.id,
        youtube_id: selectedArtist.value.youtube_id,
        spotify_id: selectedArtist.value.spotify_id,
        apple_id: selectedArtist.value.apple_id,
        melon_id: selectedArtist.value.melon_id,
        genie_id: selectedArtist.value.genie_id
      }
    }
    console.log("payload: ", payload)
    const res = await axios.patch(
        `/api/admin/v1/artists/${artistId}/update`,
        payload, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
    );

    console.log("revise: ", res.data)
  } catch (err) {
    console.error("Update failed:", err);
  }
}

const startEdit = (section) => {
  editSection.value[section] = true;
};

const saveSection = async (section) => {
  try {
    const artistId = selectedArtist.value.id;
    // console.log("artistId: ", artistId)
    await updateArtist(section, artistId);
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

// open update dialog
const uploadImage = async () => {
  if (!selectedArtist.value || !selectedArtist.value.artist_id) {
    alert("Please add the artist first, then upload the profile image")
    return
  }

  if (!profileImageFile.value) {
    alert("Please choose image")
    return
  }

  const formData = new FormData()
  formData.append("file", profileImageFile.value)
  formData.append("artist_id", selectedArtist.value.artist_id || "")
  formData.append("artist_name", selectedArtist.value.artist_en_name|| "")

  // console.log(selectedArtist.value.artist_id)
  // console.log("artist_name", selectedArtist.value.artist_en_name)

  try {
    const token = userStore.firebaseToken
    const res = await axios.post(
      "/api/admin/v1/artists/upload/image",
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: `Bearer ${token}`
        }
      }
    )

    selectedArtist.image = res.data.url
    profileImageFile.value = null
  } catch (err) {
    console.error(err)
    alert("Upload failed")
  }
}

const getTenantName = (tenantId) => {
  const tenant = tenantOptions.value.find(t => t.id === tenantId);
  return tenant ? tenant.tenant_name : '';
};

// get tenantList
const getTenantDropDownList = async () => {
  loading.value = true;
  try {
    const token = userStore.firebaseToken
    const res = await axios.get(
        `/api/admin/v1/tenants/list`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
    )
    tenantOptions.value = res.data.data;
    // console.log("to: ", tenantOptions.value)
  } catch (err) {
    console.error("Error fetching tenant list:", err);
  } finally {
    loading.value = false;
  }
}

// get belong group list
const getBelongGroupList = async () => {
  try {

  } catch (err) {

  } finally {

  }
}

const formatDate = (date) => {
  if (!date) return "-";
  const d = new Date(date);
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(
    d.getDate()
  ).padStart(2, "0")}`;
};

// formatted birth date
const formattedBirth = computed({
  get() {
    const birth = selectedArtist.value.birth;
    if (!birth) return "";

    const date = birth instanceof Date ? birth : new Date(birth);

    // get local date to prevent UTC time flow
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");

    return `${year}-${month}-${day}`;
  },
  set(val) {
    selectedArtist.value.birth = val ? new Date(val) : null;
  }
});

// filters
const filters = ref({
  english_name: "",
  type: "",
  pronouns: "",
  debut_year: ""
});

const onFilterChange = () => {
  page.value = 1;
  fetchArtists()
};

const resetFilters = () => {
  filters.value.english_name = "";
  filters.value.type = "";
  filters.value.pronouns = "";
  filters.value.debut_year = "";
  page.value = 1
  fetchArtists()
}

onMounted(() => {
  fetchArtists();
  getTenantDropDownList();
});

watch([page, limit], () => {
  fetchArtists();
});

watch(() => selectedArtist.value.tenant_id, (newId) => {
  const tenant = tenantOptions.value.find(t => t.id === newId)
  selectedArtist.value.tenant_name = tenant ? tenant.tenant_name : ''
})

</script>

<template>
  <div class="p-6 bg-gray-50 min-h-screen">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-semibold text-gray-800">All Artists</h2>
      <!-- open Dialog -->
      <button
          @click="showAddDialog = true"
          class="flex items-center gap-2 bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"
             stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/>
        </svg>
        Add Artist
      </button>
    </div>
    <!-- open dialog: add new artist -->
    <v-dialog v-model="showAddDialog" max-width="500px">
      <v-card>
        <v-card-title class="text-h6">Add New Artist</v-card-title>

        <v-card-text>
          <!-- Basic Info  -->
          <div class="flex items-center gap-3">
            <h3 class="text-lg font-semibold">Basic Info</h3>
          </div>
          <v-row dense>
            <v-col cols="12" md="6">
              <v-text-field
                  label="English Name"
                  v-model="newArtist.english_name"
                  variant="underlined"
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                  label="Korean Name"
                  v-model="newArtist.korean_name"
                  variant="underlined"
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-select
                  label="Debut Year"
                  v-model="newArtist.debut_year"
                  variant="underlined"
                  :items="debutYears"
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-select
                  label="Type"
                  v-model="newArtist.type"
                  variant="underlined"
                  :items="typeOptions"
                  multiple
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-menu
                  v-model="birthMenu"
                  :close-on-content-click="false"
                  transition="scale-transition"
                  offset-y
                  max-width="290px"
                  min-width="290px"
              >
                <template #activator="{ props }">
                  <v-text-field
                      v-model="birthText"
                      label="Birth"
                      variant="underlined"
                      readonly
                      v-bind="props"
                      v-on="props.on"
                  />
                </template>
                <v-date-picker
                    v-model="birthPicker"
                    @update:model-value="setBirth"
                    no-title
                    color="primary"
                    scrollable
                    :max="new Date().toISOString().substr(0, 10)"
                />
              </v-menu>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                  label="Fandom"
                  v-model="newArtist.fandom"
                  variant="underlined"
              />
            </v-col>
            <v-col cols="9">
              <v-select
                  v-model="newArtist.tenant_id"
                  :items="tenantOptions"
                  label="Company"
                  variant="underlined"
                  item-title="tenant_name"
                  item-value="id"
              />
            </v-col>
            <v-col cols="3" class="d-flex">
              <v-btn color="primary"
                     @click="showAddTenantDialog = true"
                     small>
                + Add
              </v-btn>
            </v-col>
            <v-col cols="12" md="6">
              <v-select
                  label="Nation"
                  v-model="newArtist.nation"
                  variant="underlined"
                  :items="nationOptions"
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-select
                  label="Pronouns"
                  v-model="newArtist.pronouns"
                  variant="underlined"
                  :items="pronounsOption"
              />
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>

          <!-- SNS Info -->
          <div class="flex items-center gap-3">
            <h3 class="text-lg font-semibold">SNS Accounts</h3>
          </div>
          <v-row dense>
            <v-col cols="12" md="6">
              <v-text-field
                  label="Instagram ID"
                  v-model="newArtist.instagram_id"
                  variant="underlined"
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                  label="Instagram User Name"
                  v-model="newArtist.instagram_user"
                  variant="underlined"
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-select
                  label="Threads"
                  v-model="newArtist.threads"
                  variant="underlined"
                  :items="threadsOption"
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                  label="TikTok ID"
                  v-model="newArtist.tiktok_id"
                  variant="underlined"
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                  label="Bilibili ID"
                  v-model="newArtist.bilibili_id"
                  variant="underlined"
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                  label="Weibo ID"
                  v-model="newArtist.weibo_id"
                  variant="underlined"
              />
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>

          <!-- Music Info -->
          <div class="flex items-center gap-3">
            <h3 class="text-lg font-semibold">
              Music
            </h3>
          </div>
          <v-row dense>
            <v-col cols="12" md="6">
              <v-text-field
                  label="YouTube ID"
                  v-model="newArtist.youtube_id"
                  variant="underlined"
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                  label="Spotify ID"
                  v-model="newArtist.spotify_id"
                  variant="underlined"
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                  label="Apple ID"
                  v-model="newArtist.apple_id"
                  variant="underlined"
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                  label="Melon ID"
                  v-model="newArtist.melon_id"
                  variant="underlined"
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                  label="Genie ID"
                  v-model="newArtist.genie_id"
                  variant="underlined"
              />
            </v-col>
          </v-row>
        </v-card-text>

        <v-card-actions class="justify-end">
          <v-btn variant="text"
                 @click="showAddDialog = false">
            Cancel
          </v-btn>
          <v-btn
              color="indigo"
              class="text-white"
              @click="addArtist"
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

     <!-- Filters -->
    <!--TODO FILTER: COMPANY-->
    <div class="flex flex-wrap gap-4 mb-4 items-end">
      <!-- Search artist name -->
      <div class="w-64 flex flex-col">
        <label class="text-sm font-medium text-gray-700 mb-1">Artist Name</label>
        <div class="relative">
          <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-gray-500">
            <i class="mdi mdi-magnify"></i>
          </span>
          <input
              v-model="filters.english_name"
              type="text"
              class="w-full border border-gray-300 rounded-md pl-10 pr-3 py-2 text-sm
               focus:outline-none focus:ring-2 focus:ring-indigo-500"
              placeholder="Search artist..."
          />
        </div>
      </div>

      <!-- Type filter -->
      <div class="w-32 flex flex-col">
        <label class="text-sm font-medium text-gray-700 mb-1">Type</label>
        <div class="relative">
          <select
              v-model="filters.type"
              class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm
              focus:outline-none focus:ring-2 focus:ring-indigo-500"
              :class="filters.type === '' ? 'text-gray-400' : 'text-gray-700'"
          >
            <!-- placeholder -->
            <option value="" disabled selected hidden>Select Type</option>
            <option value="Musician">Musician</option>
            <option value="Actor">Actor</option>
          </select>
          <!-- icon -->
          <span class="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-gray-500">
            <i class="mdi mdi-menu-down text-xl"></i>
          </span>
        </div>
      </div>

      <!-- Pronouns filter -->
      <div class="w-32 flex flex-col">
        <label class="text-sm font-medium text-gray-700 mb-1">Pronouns</label>
        <div class="relative">
          <select
              v-model="filters.pronouns"
              class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm
             focus:outline-none focus:ring-2 focus:ring-indigo-500"
              :class="filters.pronouns === '' ? 'text-gray-400' : 'text-gray-700'"
          >
            <!-- placeholder -->
            <option value="" disabled selected hidden>C/F/M</option>
            <option value="C">Group</option>
            <option value="F">Female</option>
            <option value="M">Male</option>
          </select>
          <!-- icon -->
          <span class="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-gray-500">
            <i class="mdi mdi-menu-down text-xl"></i>
          </span>
        </div>
      </div>

      <!-- Debut year filter -->
      <div class="w-32 flex flex-col">
        <label class="text-sm font-medium text-gray-700 mb-1">Debut Year</label>
        <div class="relative">
          <select
              v-model="filters.debut_year"
              class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm
              focus:outline-none focus:ring-2 focus:ring-indigo-500"
              :class="filters.debut_year === '' ? 'text-gray-400' : 'text-gray-700'"
          >
            <!-- placeholder -->
            <option value="" disabled selected hidden>Select Year</option>
            <option
                v-for="year in debutYears"
                :key="year"
                :value="year"
            >
              {{ year }}
            </option>
          </select>
          <!-- dropdown icon -->
          <span class="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-gray-500">
            <i class="mdi mdi-menu-down text-xl"></i>
          </span>
        </div>
      </div>

      <!-- Reset button -->
      <button
          class="h-[42px] px-4 text-sm border rounded-md hover:bg-gray-100 transition"
          @click="resetFilters"
      >
        Reset
      </button>

      <!-- Submit button -->
      <button
          class="h-[42px] px-4 text-sm rounded-md bg-indigo-600 text-white
           hover:bg-indigo-700 transition"
          @click="onFilterChange"
      >
        Submit
      </button>
    </div>

    <!-- Table -->
    <div class="overflow-x-auto bg-white rounded-lg shadow">
      <table class="min-w-full text-sm text-gray-700">
        <thead class="bg-gray-100 text-left text-gray-600 uppercase text-xs">
        <tr>
          <th class="w-32 px-4 py-2 text-left">Artist Id</th>
          <th class="w-32 px-4 py-2 text-left">Image</th>
          <th class="w-32 px-4 py-2 text-left">EN Name</th>
          <th class="w-32 px-4 py-2 text-left">KR Name</th>
          <th class="w-32 px-4 py-2 text-left">Debut Year</th>
          <th class="w-32 px-4 py-2 text-left">Birth</th>
          <th class="w-32 px-4 py-2 text-left">Belong Tenant</th>
          <th class="w-32 px-4 py-2 text-left">Pronouns</th>
          <th class="w-32 px-4 py-2 text-left">Type</th>
          <th class="w-32 px-4 py-2 text-left">Actions</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="a in artists"
            :key="a.artist_id"
            class="border-t hover:bg-gray-50 transition">
          <td class="px-4 py-2 font-mono">{{ a.artist_id || '-' }}</td>
          <td class="px-4 py-2">
            <img
                v-if="a.image"
                :src="a.image"
                alt="artist"
                class="h-10 w-10 rounded object-cover"
            />
            <span v-else>-</span>
          </td>
          <td class="px-4 py-2">{{ a.artist_en_name || '-' }}</td>
          <td class="px-4 py-2">{{ a.artist_kr_name || '-' }}</td>
          <td class="px-4 py-2">{{ a.debut || '-' }}</td>
          <td class="px-4 py-2">{{ formatDate(a.birth) || '-' }}</td>
          <td class="px-4 py-2">{{ a.belong_tenant || '-' }}</td>
          <td class="px-4 py-2">{{ a.pronouns || '-' }}</td>
          <td class="px-4 py-2 capitalize">
            <div v-if="a.type && a.type.length" class="flex flex-wrap gap-1">
              <span
                  v-for="t in a.type"
                  :key="t"
                  class="px-2 py-1 rounded text-xs font-medium"
                  :class="typeClass(t)"
              >
                {{ t }}
              </span>
            </div>
            <span v-else>-</span>
          </td>
          <td class="px-4 py-2 flex gap-2">
            <button
                @click.stop="viewArtistDetail(a.id)"
                class="px-2 py-1 rounded text-xs font-medium cursor-pointer border border-green-600 text-green-600 hover:bg-green-50 transition"
            >
              Update
            </button>
          </td>
        </tr>
        <tr v-if="!loading && artists.length === 0">
          <td colspan="6" class="text-center text-gray-500 py-6">No artists found</td>
        </tr>
        </tbody>
      </table>
    </div>

    <!-- Artist Details Dialog -->
    <v-dialog v-model="showDialog" max-width="800px">
      <v-card>
        <v-card-title class="text-h6 flex justify-between items-center">
          Artist Details
        </v-card-title>

        <v-card-text>
          <v-skeleton-loader v-if="dialogLoading" type="card"/>

          <div v-else class="space-y-8">
            <!-- Basic Info Section -->
            <div>
              <div class="flex justify-between items-center mb-2">
                <!-- Title -->
                <div class="flex items-center gap-3">
                  <h3 class="text-lg font-semibold">Basic Info</h3>
                  <StatusChip :edit="editSection.basic"/>
                </div>
                <!-- StatusChip & edit icon -->
                <div class="flex gap-2">
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
              </div>
              <!-- Basic Info Content -->
              <div>
                <v-row dense>
                  <v-col cols="12" md="6">
                    <v-text-field
                        v-model="selectedArtist.artist_id"
                        label="Artist ID"
                        variant="underlined"
                        :readonly="!editSection.basic"
                    />
                  </v-col>
                  <v-col cols="12" md="6">
                    <template v-if="!editSection.basic">
                      <!-- View Mode -->
                      <v-text-field
                          v-model="selectedArtist.tenant_name"
                          label="Company"
                          variant="underlined"
                          :readonly="!editSection.basic"
                      />
                    </template>
                    <template v-else>
                      <!-- Edit Mode -->
                      <v-select
                          v-model="selectedArtist.tenant_id"
                          :items="tenantOptions"
                          label="Company"
                          variant="underlined"
                          dense
                          item-title="tenant_name"
                          item-value="id"
                      />
                    </template>
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field
                        v-model="selectedArtist.artist_en_name"
                        label="English Name"
                        variant="underlined"
                        :readonly="!editSection.basic"
                    />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field
                        v-model="selectedArtist.artist_kr_name"
                        label="Korean Name"
                        variant="underlined"
                        :readonly="!editSection.basic"
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-select
                        v-model="selectedArtist.debut"
                        :items="debutYears"
                        label="Debut Year"
                        variant="underlined"
                        :readonly="!editSection.basic"
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-select
                        v-model="selectedArtist.type"
                        :items="typeOptions"
                        label="Type"
                        multiple
                        variant="underlined"
                        :readonly="!editSection.basic"
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-select
                        v-model="selectedArtist.nation"
                        :items="nationOptions"
                        label="Nation"
                        variant="underlined"
                        :readonly="!editSection.basic"
                    />
                  </v-col>
                  <v-col cols="12" md="3">
                    <v-tooltip location="top" open-delay="300">
                      <template #activator="{ props }">
                        <v-select
                            v-model="selectedArtist.pronouns"
                            :items="pronounsOption"
                            label="Pronouns"
                            variant="underlined"
                            v-bind="props"
                            :readonly="!editSection.basic"
                        />
                      </template>
                      <span>C for groups, F for female, M for male</span>
                    </v-tooltip>
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-menu v-model="datePickerMenu"
                            :close-on-content-click="false"
                            transition="scale-transition"
                            offset-y>
                      <template #activator="{ props }">
                        <v-text-field
                            v-model="formattedBirth"
                            label="Birth"
                            :readonly="!editSection.basic"
                            variant="underlined"
                            v-bind="editSection.basic ? props : {}"
                            v-on="editSection.basic ? props.on : {}"
                        />
                      </template>
                      <v-date-picker
                          v-model="selectedArtist.birth"
                          :return-value.sync="selectedArtist.birth"
                          type="date"
                          @input="datePickerMenu = false"
                          no-title
                          color="primary"
                          scrollable
                          :max="new Date().toISOString().substr(0, 10)"
                      />
                    </v-menu>
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field
                        v-model="selectedArtist.fandom"
                        label="Fandom"
                        variant="underlined"
                        :readonly="!editSection.basic"
                    />
                  </v-col>
                  <v-col cols="12" md="12">
                    <template v-if="!editSection.basic">
                      <!-- View Mode -->
                      <v-text-field
                          v-model="selectedArtist.image"
                          label="Profile Image"
                          variant="underlined"
                          readonly
                      />
                    </template>
                    <template v-else>
                      <!-- Edit Mode -->
                      <div class="d-flex align-center gap-2">
                        <v-text-field
                            v-model="selectedArtist.image"
                            label="Profile Image URL"
                            variant="underlined"
                        />
                        <!-- Local File -->
                        <v-file-input
                            v-model="profileImageFile"
                            accept="image/*"
                            label="Choose Image"
                            prepend-icon="mdi-image"
                            density="comfortable"
                            :multiple="false"
                            show-size
                            class="flex-1"
                        />

                        <!-- Upload Btn -->
                        <v-btn
                            color="indigo"
                            @click="uploadImage"
                            :disabled="!profileImageFile"
                        >
                          Upload
                        </v-btn>
                      </div>
                    </template>
                  </v-col>
                </v-row>
              </div>
            </div>

            <!-- SNS Section -->
            <div>
              <div class="flex justify-between items-center mb-2">
                <!-- Title -->
                <div class="flex items-center gap-3">
                  <h3 class="text-lg font-semibold">SNS Info</h3>
                  <StatusChip :edit="editSection.sns"/>
                </div>
                <!-- StatusChip & edit icon -->
                <div class="flex gap-2">
                  <v-btn
                      icon
                      variant="text"
                      @click="startEdit('sns')"
                      v-if="!editSection.sns"
                  >
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>

                  <div v-if="editSection.sns" class="flex gap-2">
                    <v-btn size="small" color="success" @click="saveSection('sns')">Save</v-btn>
                    <v-btn size="small" color="error" @click="cancelSection('sns')">Cancel</v-btn>
                  </div>
                </div>
              </div>

              <!-- SNS Info Content -->
              <div>
                <v-row dense>
                  <v-col cols="12" md="6">
                    <v-text-field
                        v-model="selectedArtist.instagram_id"
                        label="Instagram ID"
                        variant="underlined"
                        :readonly="!editSection.sns"
                    />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field
                        v-model="selectedArtist.instagram_user"
                        label="Instagram User Name"
                        variant="underlined"
                        :readonly="!editSection.sns"
                    />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-select
                        v-model="selectedArtist.threads"
                        :items="threadsOption"
                        label="Threads"
                        variant="underlined"
                        :readonly="!editSection.sns"
                    />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field
                        v-model="selectedArtist.tiktok_id"
                        label="Tiktok ID"
                        variant="underlined"
                        :readonly="!editSection.sns"
                    />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field
                        v-model="selectedArtist.bilibili_id"
                        label="Bilibili ID"
                        variant="underlined"
                        :readonly="!editSection.sns"
                    />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field
                        v-model="selectedArtist.weibo_id"
                        label="Weibo ID"
                        variant="underlined"
                        :readonly="!editSection.sns"
                    />
                  </v-col>
                </v-row>
              </div>
            </div>

            <!-- Music Section -->
            <div>
              <div class="flex justify-between items-center mb-2">
                <!-- Title -->
                <div class="flex items-center gap-3">
                  <h3 class="text-lg font-semibold">Music Info</h3>
                  <StatusChip :edit="editSection.music"/>
                </div>
                <!-- StatusChip & edit icon -->
                <div class="flex gap-2">
                  <v-btn
                      icon
                      variant="text"
                      @click="startEdit('music')"
                      v-if="!editSection.music"
                  >
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>

                  <div v-if="editSection.music" class="flex gap-2">
                    <v-btn size="small" color="success" @click="saveSection('music')">Save</v-btn>
                    <v-btn size="small" color="error" @click="cancelSection('music')">Cancel</v-btn>
                  </div>
                </div>
              </div>
              <!-- Music Info Content -->
              <div>
                <v-row dense>
                  <v-col cols="12" md="6">
                    <v-text-field
                        v-model="selectedArtist.youtube_id"
                        label="YouTube ID"
                        variant="underlined"
                        :readonly="!editSection.music"
                    />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field
                        v-model="selectedArtist.spotify_id"
                        label="Spotify ID"
                        variant="underlined"
                        :readonly="!editSection.music"
                    />
                  </v-col>
                   <v-col cols="12" md="6">
                    <v-text-field
                        v-model="selectedArtist.apple_id"
                        label="Apple ID"
                        variant="underlined"
                        :readonly="!editSection.music"
                    />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field
                        v-model="selectedArtist.melon_id"
                        label="Melon ID"
                        variant="underlined"
                        :readonly="!editSection.music"
                    />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field
                        v-model="selectedArtist.genie_id"
                        label="Genie ID"
                        variant="underlined"
                        :readonly="!editSection.music"
                    />
                  </v-col>
                </v-row>
              </div>
            </div>
          </div>

        </v-card-text>
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

</style>