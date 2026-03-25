<script setup>
import {ref, onMounted, watch, computed} from "vue";
import axios from "@/axios";
import StatusChip from "@/components/StatusChip.vue"
import {getAuth} from "firebase/auth";

// dropdown list options
const typeOptions = ["Drama", "Movie", "Variety Show"]
const countryOptions = ["South Korea", "United States", "Japan", "China", "Other"]
const languageOptions = ["Korean", "English", "Japanese", "Chinese", "Other"]
const genreOptions = ["Action", "Romance", "Comedy", "Thriller", "Horror", "Fantasy", "Historical", "Slice of Life", "Mystery"]
const currentYear = new Date().getFullYear()
const broadcastYears = Array.from({ length: currentYear - 1950 + 1 }, (_, i) => 1950 + i)
const broadcastDays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
const streamingOptions = ["Netflix", "Amazon Prime", "Hulu", "Disney+", "Apple TV+", "Other"]
const premiereOptions = ["Local", "OTT"]

const thumbnailFile = ref(null);
const dramas = ref([]);
const loading = ref(false);
const showDialog = ref(false);
const datePickerMenu = ref(false);
const artistOptions = ref([]);

// pagination
const page = ref(1); // current page
const limit = ref(10); // per page limit
const total = ref(0); // total count
const totalPages = computed(() => Math.ceil(total.value / limit.value));

// edit drama info
const showEditDialog = ref(false);
const selectedDrama = ref({});
const detailLoading = ref(false);
const editSection = ref({
  basic: false,
  broadcast: false,
  cast: false
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

// change drama status
const deleteDialog = ref(false);
const selectedDramaId = ref(null);
const selectedDramaName = ref("");

// add new drama
const showAddDialog = ref(false);
const onAirMenu = ref(false);
const onAirPicker = ref(null);
const onAirText = ref(""); 
const finaleMenu = ref(false);
const finalePicker = ref(null);
const finaleText = ref("");
const broadcastTimeMenu = ref(false);
const newDrama = ref({
  drama_id: "",
  // drama name
  name: "",
  name_in_korean: "",
  genre: [],
  type: "Drama",
  // datetime
  onair_date: "",
  finale: "",
  broadcast_year: currentYear,
  broadcast_day: [],
  broadcast_time: "",
  // series
  episode: "",
  special_episode: "",
  // production
  director: [],
  screenwriter: [],
  production: [],
  // OTT or local
  premiere_channel: [],
  streaming: [],
  country: "",
  language: "",
  thumbnail: "",
  // artists who are in the drama
  starring: [],
});

const setOnAirDate = (value) => {
  if (!value) return

  let formatted = ""
  if (typeof value === "string") {
    formatted = value.substring(0, 10)
  } else if (value instanceof Date) {
    const year = value.getFullYear()
    const month = String(value.getMonth() + 1).padStart(2, "0")
    const day = String(value.getDate()).padStart(2, "0")
    formatted = `${year}-${month}-${day}`
  }
  
  onAirText.value = formatted
  newDrama.value.onair_date = formatted
  onAirMenu.value = false
  // Also update onAirPicker for consistency if it's a Date object
  onAirPicker.value = value instanceof Date ? value : new Date(value)
}

const setFinaleDate = (value) => {
  if (!value) return

  let formatted = ""
  if (typeof value === "string") {
    formatted = value.substring(0, 10)
  } else if (value instanceof Date) {
    const year = value.getFullYear()
    const month = String(value.getMonth() + 1).padStart(2, "0")
    const day = String(value.getDate()).padStart(2, "0")
    formatted = `${year}-${month}-${day}`
  }
  
  finaleText.value = formatted
  newDrama.value.finale = formatted
  finaleMenu.value = false
  // Also update finalePicker for consistency
  finalePicker.value = value instanceof Date ? value : new Date(value)
}

// fetch all dramas
const fetchDramas = async () => {
  loading.value = true;
  try {
    const res = await axios.get(
        `/admin/v1/dramas`, {
          params: {
            page: page.value,
            limit: limit.value,
            name: filters.value.name,
            type: filters.value.type,
            broadcast_year: filters.value.broadcast_year
          }
        }
    )
    dramas.value = res.data.data;
    total.value = res.data.total;
  } catch (err) {
    console.error("Error fetching dramas:", err);
  } finally {
    loading.value = false;
  }
};

const fetchArtistOptions = async () => {
  try {
    const res = await axios.get(
        `/admin/v1/artists/list`,
        {}
    )
    artistOptions.value = Array.isArray(res.data?.data) ? res.data.data : []
  } catch (err) {
    console.error("Error fetching artist list:", err)
    artistOptions.value = []
  }
};

const typeClass = (t) => {
  switch (t.toLowerCase()) {
    case "drama":
      return "bg-purple-100 text-purple-800"
    case "movie":
      return "bg-blue-100 text-blue-800"
    default:
      return "bg-gray-100 text-gray-700"
  }
}

const addDrama = async () => {
  loading.value = true;
  const auth = getAuth()
  const user = auth.currentUser
  if (!user) {
    showMessage("Please login first.", "error")
    loading.value = false
    return
  }
  try {
    const normalizedStarring = Array.isArray(newDrama.value.starring)
      ? newDrama.value.starring.map(v => String(v || "").trim()).filter(Boolean)
      : []

    const normalizeChipField = (val) => {
      if (Array.isArray(val)) {
        return val.map(v => String(v).trim()).filter(Boolean).join(", ")
      }
      return val ? String(val).trim() : ""
    }

    const payload = {
      ...newDrama.value,
      director: normalizeChipField(newDrama.value.director),
      production: normalizeChipField(newDrama.value.production),
      screenwriter: normalizeChipField(newDrama.value.screenwriter),
      starring: normalizedStarring
    }

    await axios.post(
        `/admin/v1/dramas`,
        payload, {
          headers: {
            "Content-Type": "application/json",
          }
        }
    )
    showMessage("Drama added successfully.", "success");
    showAddDialog.value = false;
    onAirText.value = ""
    finaleText.value = ""
    newDrama.value = {
      broadcast_year: currentYear,
      type: "Drama",
      genre: [],
      starring: [],
      broadcast_day: [],
      premiere_channel: [],
      streaming: [],
    }
    fetchDramas();
  } catch (err) {
    if (err.response?.status === 409) {
      showMessage("Drama already exists.", "error")
    } else {
      showMessage("Server error.", "error")
    }
  } finally {
    loading.value = false
  }
}

const viewDramaDetail = async (id) => {
  showDialog.value = true;
  detailLoading.value = true;
  selectedDrama.value = {};
  editSection.value = {
    basic: false,
    broadcast: false,
    cast: false
  };

  try {
    const res = await axios.get(
        `/admin/v1/dramas/${id}`,
        {}
    );
    const data = res.data.data || {};
    selectedDrama.value = {
      ...data,
      genre: Array.isArray(data.genre) ? data.genre : [],
      broadcast_day: Array.isArray(data.broadcast_day) ? data.broadcast_day : [],
      premiere_channel: Array.isArray(data.premiere_channel) ? data.premiere_channel : [],
      streaming: Array.isArray(data.streaming) ? data.streaming : [],
      director: Array.isArray(data.director) ? data.director : [],
      production: Array.isArray(data.production) ? data.production : [],
      screenwriter: Array.isArray(data.screenwriter) ? data.screenwriter : [],
      starring: Array.isArray(data.starring) ? data.starring : []
    };

    onAirPicker.value = data.onair_date ? new Date(data.onair_date) : null
    finalePicker.value = data.finale ? new Date(data.finale) : null
  } catch (err) {
    console.error("Fetch drama details failed:", err);
  } finally {
    detailLoading.value = false;
  }
}

const updateDrama = async (section, dramaId) => {
  try {
    const normalizeChipField = (val) => {
      if (Array.isArray(val)) {
        return val.map(v => String(v).trim()).filter(Boolean).join(", ")
      }
      return val ? String(val).trim() : ""
    }

    const normalizedStarring = Array.isArray(selectedDrama.value.starring)
      ? selectedDrama.value.starring.map(v => String(v || "").trim()).filter(Boolean)
      : []

    let payload = {
      ...selectedDrama.value,
      director: normalizeChipField(selectedDrama.value.director),
      production: normalizeChipField(selectedDrama.value.production),
      screenwriter: normalizeChipField(selectedDrama.value.screenwriter),
      starring: normalizedStarring
    }
    
    const res = await axios.patch(
        `/admin/v1/dramas/${dramaId}`,
        payload, {
          headers: {}
        }
    );
    fetchDramas();
  } catch (err) {
    console.error("Update failed:", err);
  }
}

const startEdit = (section) => {
  editSection.value[section] = true;
};

const saveSection = async (section) => {
  try {
    const dramaId = selectedDrama.value.id;
    await updateDrama(section, dramaId);
    editSection.value[section] = false;
  } catch (err) {
    console.error("Save failed", err);
  }
};

const cancelSection = (section) => {
  editSection.value[section] = false;
  // Reload drama to reset changes
  viewDramaDetail(selectedDrama.value.id);
};

const uploadThumbnail = async () => {
  if (!selectedDrama.value || !selectedDrama.value.drama_id) {
    alert("Please add drama first")
    return
  }
  if (!thumbnailFile.value) {
    alert("Please choose image")
    return
  }

  const formData = new FormData()
  formData.append("file", thumbnailFile.value)
  formData.append("drama_id", selectedDrama.value.drama_id)

  try {
    const res = await axios.post(
      "/admin/v1/dramas/upload/thumbnail",
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      }
    )
    selectedDrama.value.thumbnail = res.data.url
    thumbnailFile.value = null
  } catch (err) {
    console.error(err)
    alert("Upload failed")
  }
}

const confirmChangeStatus = async () => {
  try {
    await axios.patch(`/admin/v1/dramas/${selectedDramaId.value}/status`,
        {}, {})
    deleteDialog.value = false;
    fetchDramas();
  } catch (err) {
    console.error("Status change failed:", err);
  }
}

const formatDate = (date) => {
  if (!date) return "-";
  const d = new Date(date);
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
};

const formatBirthDate = (date) => {
  if (!date) return "-"
  const d = new Date(date)
  if (Number.isNaN(d.getTime())) return "-"
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`
};

const formattedOnAirDate = computed({
  get() {
    const d = selectedDrama.value.onair_date;
    if (!d) return "";
    const date = new Date(d);
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`;
  },
  set(val) {
    selectedDrama.value.onair_date = val;
  }
});

const filters = ref({
  name: "",
  type: "",
  broadcast_year: ""
});

const onFilterChange = () => {
  page.value = 1;
  fetchDramas()
};

const resetFilters = () => {
  filters.value.name = "";
  filters.value.type = "";
  filters.value.broadcast_year = "";
  page.value = 1
  fetchDramas()
}

const onPageChange = (newPage) => {
  page.value = newPage;
}

onMounted(() => {
  fetchDramas();
  fetchArtistOptions();
});

watch([page, limit], () => {
  fetchDramas();
});
</script>

<template>
  <div class="p-6 bg-gray-50 min-h-screen">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-semibold text-gray-800">All Dramas</h2>
      <button
          @click="showAddDialog = true"
          class="flex items-center gap-2 bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/>
        </svg>
        Add Drama
      </button>
    </div>

    <!-- Add New Drama Dialog -->
    <v-dialog v-model="showAddDialog" max-width="800px">
      <v-card>
        <v-card-title class="text-h6">
          Add New Drama
        </v-card-title>
        <v-card-text>
          <!-- drama basic info  -->
          <div class="flex items-center gap-3">
            <h3 class="text-lg font-semibold">Basic Info</h3>
          </div>
          <v-row dense>
            <v-col cols="12" md="6">
              <v-text-field
                  label="Drama ID (Auto-generated)"
                  v-model="newDrama.drama_id"
                  variant="underlined"
                  readonly
                  hint="Will be generated on save"
                  persistent-hint/>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                  label="Drama Seq (Auto-generated)"
                  v-model="newDrama.drama_seq"
                  variant="underlined"
                  readonly
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                  label="Name (EN)"
                  v-model="newDrama.name"
                  variant="underlined"/>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                  label="Name (KR)"
                  v-model="newDrama.name_in_korean"
                  variant="underlined"/>
            </v-col>
            <v-col cols="12" md="6">
              <v-select
                  label="Type"
                  v-model="newDrama.type"
                  :items="typeOptions"
                  variant="underlined"/>
            </v-col>
            <v-col cols="12" md="6">
              <v-select
                  label="Genre"
                  v-model="newDrama.genre"
                  :items="genreOptions"
                  multiple
                  variant="underlined"/>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                  label="Episodes"
                  v-model="newDrama.episode"
                  variant="underlined"/>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                  label="Special Episodes"
                  v-model="newDrama.special_episode"
                  variant="underlined"/>
            </v-col>
            <v-col cols="12" md="6">
              <v-select
                  label="Country"
                  v-model="newDrama.country"
                  :items="countryOptions"
                  variant="underlined"/>
            </v-col>
            <v-col cols="12" md="6">
              <v-select
                  label="Language"
                  v-model="newDrama.language"
                  :items="languageOptions"
                  variant="underlined"/>
            </v-col>
            <v-col cols="12">
              <v-autocomplete
                  label="Starring"
                  v-model="newDrama.starring"
                  :items="artistOptions"
                  :item-title="item => `${item.artist_en_name || item.artist_id} (${item.artist_kr_name || ''})`"
                  item-value="id"
                  multiple
                  chips
                  clearable
                  variant="underlined"
                  hint="Select artists"
                  persistent-hint>
                <template #item="{ props, item }">
                  <v-list-item v-bind="props" :title="undefined" :subtitle="undefined">
                    <template #prepend>
                      <v-avatar size="32">
                        <v-img :src="item.raw.image" alt="" />
                      </v-avatar>
                    </template>
                    <v-list-item-title>{{ `${item.raw.artist_en_name || item.raw.artist_id} (${item.raw.artist_kr_name || ''})` }}</v-list-item-title>
                    <v-list-item-subtitle>Birth: {{ formatBirthDate(item.raw.birth) }}</v-list-item-subtitle>
                  </v-list-item>
                </template>
                <template #selection="{ item }">
                  <v-chip size="small" class="ma-1" label>
                    {{ `${item.raw.artist_en_name || item.raw.artist_id} (${item.raw.artist_kr_name || ''})` }}
                  </v-chip>
                </template>
              </v-autocomplete>
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>

          <!-- broadcast info -->
          <div class="flex items-center gap-3">
            <h3 class="text-lg font-semibold">Broadcast Info</h3>
          </div>

          <v-row dense>
            <v-col cols="12" md="4">
              <v-select
                  label="Broadcast Year"
                  v-model="newDrama.broadcast_year"
                  :items="broadcastYears"
                  variant="underlined"/>
            </v-col>
            <v-col cols="12" md="4">
              <v-select
                  label="Broadcast Day"
                  v-model="newDrama.broadcast_day"
                  :items="broadcastDays"
                  multiple
                  variant="underlined"/>
            </v-col>
            <v-col cols="12" md="4">
              <v-menu
                  v-model="broadcastTimeMenu"
                  :close-on-content-click="false"
                  transition="scale-transition"
                  offset-y>
                <template #activator="{ props }">
                  <v-text-field
                      v-model="newDrama.broadcast_time"
                      label="Broadcast Time"
                      variant="underlined"
                      readonly
                      v-bind="props"
                      hint="e.g. 21:00"
                      persistent-hint/>
                </template>
                <v-list>
                  <v-list-item>
                    <input
                        type="time"
                        v-model="newDrama.broadcast_time"
                        class="p-2 border rounded"
                        @change="broadcastTimeMenu = false"
                    />
                  </v-list-item>
                </v-list>
              </v-menu>
            </v-col>
            <v-col cols="12" md="6">
              <v-menu v-model="onAirMenu"
                      :close-on-content-click="false"
                      transition="scale-transition"
                      offset-y>
                <template #activator="{ props }">
                  <v-text-field
                      v-model="onAirText"
                      label="On-Air Date"
                      variant="underlined"
                      readonly
                      v-bind="props"/>
                </template>
                <v-date-picker
                    v-model="onAirPicker"
                    @update:model-value="setOnAirDate"
                    no-title color="primary"/>
              </v-menu>
            </v-col>
            <v-col cols="12" md="6">
              <v-menu
                  v-model="finaleMenu"
                  :close-on-content-click="false"
                  transition="scale-transition"
                  offset-y>
                <template #activator="{ props }">
                  <v-text-field
                      v-model="finaleText"
                      label="Finale Date"
                      variant="underlined"
                      readonly
                      v-bind="props"/>
                </template>
                <v-date-picker
                    v-model="finalePicker"
                    @update:model-value="setFinaleDate"
                    no-title
                    color="primary"/>
              </v-menu>
            </v-col>
            <v-col cols="12" md="6">
              <v-select
                  label="Premiere Channel"
                  v-model="newDrama.premiere_channel"
                  :items="premiereOptions"
                  multiple
                  variant="underlined"/>
            </v-col>
            <v-col cols="12" md="6">
              <v-select
                  label="Streaming"
                  v-model="newDrama.streaming"
                  :items="streamingOptions"
                  multiple
                  variant="underlined"/>
            </v-col>
          </v-row>

          <v-divider class="my-4"></v-divider>

          <!-- production info -->
          <div class="flex items-center gap-3">
            <h3 class="text-lg font-semibold">Production Info</h3>
          </div>

          <v-row dense>
            <v-col cols="12">
              <v-combobox
                  label="Director"
                  v-model="newDrama.director"
                  multiple
                  chips
                  clearable
                  variant="underlined"
                  hint="Press Enter to add"
                  persistent-hint/>
            </v-col>
            <v-col cols="12">
              <v-combobox
                  label="Production"
                  v-model="newDrama.production"
                  multiple
                  chips
                  clearable
                  variant="underlined"
                  hint="Press Enter to add"
                  persistent-hint/>
            </v-col>
            <v-col cols="12">
              <v-combobox
                  label="Screenwriter"
                  v-model="newDrama.screenwriter"
                  multiple
                  chips
                  clearable
                  variant="underlined"
                  hint="Press Enter to add"
                  persistent-hint/>
            </v-col>
          </v-row>

        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn
              variant="text"
              @click="showAddDialog = false">
            Cancel
          </v-btn>
          <v-btn
              color="indigo"
              class="text-white"
              @click="addDrama">
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Snackbar -->
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="1500" location="top">
      {{ snackbar.message }}
    </v-snackbar>

    <!-- Filters -->
    <div class="flex flex-wrap gap-4 mb-4 items-end">
      <div class="w-64 flex flex-col">
        <label class="text-sm font-medium text-gray-700 mb-1">Drama Name</label>
        <div class="relative">
          <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-gray-500">
            <i class="mdi mdi-magnify"></i>
          </span>
          <input v-model="filters.name" type="text" class="w-full border border-gray-300 rounded-md pl-10 pr-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="Search drama..." />
        </div>
      </div>
      <div class="w-32 flex flex-col">
        <label class="text-sm font-medium text-gray-700 mb-1">Type</label>
        <select v-model="filters.type" class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
          <option value="">All</option>
          <option v-for="opt in typeOptions" :key="opt" :value="opt">{{ opt }}</option>
        </select>
      </div>
      <div class="w-32 flex flex-col">
        <label class="text-sm font-medium text-gray-700 mb-1">Year</label>
        <select v-model="filters.broadcast_year" class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
          <option value="">All</option>
          <option v-for="year in broadcastYears" :key="year" :value="year">{{ year }}</option>
        </select>
      </div>
      <button class="h-[42px] px-4 text-sm border rounded-md hover:bg-gray-100 transition" @click="resetFilters">Reset</button>
      <button class="h-[42px] px-4 text-sm rounded-md bg-gray-800 text-white hover:bg-gray-900 transition" @click="onFilterChange">Submit</button>
    </div>

    <!-- Table -->
    <div class="overflow-x-auto bg-white rounded-lg shadow">
      <table class="min-w-full text-sm text-gray-700">
        <thead class="bg-gray-100 text-left text-gray-600 uppercase text-xs">
          <tr>
            <th class="px-4 py-2">ID</th>
            <th class="px-4 py-2">Thumbnail</th>
            <th class="px-4 py-2">Name (EN)</th>
            <th class="px-4 py-2">Name (KR)</th>
            <th class="px-4 py-2">Year</th>
            <th class="px-4 py-2">Type</th>
            <th class="px-4 py-2">Status</th>
            <th class="px-4 py-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="d in dramas" :key="d.drama_id" class="border-t hover:bg-gray-50 transition">
            <td class="px-4 py-2 font-mono">{{ d.drama_id }}</td>
            <td class="px-4 py-2">
              <img v-if="d.thumbnail" :src="d.thumbnail" class="h-10 w-16 object-cover rounded" />
              <span v-else>-</span>
            </td>
            <td class="px-4 py-2">{{ d.name }}</td>
            <td class="px-4 py-2">{{ d.name_in_korean }}</td>
            <td class="px-4 py-2">{{ d.broadcast_year }}</td>
            <td class="px-4 py-2">
              <span class="px-2 py-1 rounded text-xs font-medium" :class="typeClass(d.type || '')">{{ d.type }}</span>
            </td>
            <td class="px-4 py-2">
              <v-chip size="x-small" :color="d.finale ? 'success' : 'warning'" variant="flat">
                {{ d.finale ? 'Completed' : 'On Air' }}
              </v-chip>
            </td>
            <td class="px-4 py-2 flex gap-2">
              <button @click="viewDramaDetail(d.id)" class="px-2 py-1 rounded text-xs font-medium border border-green-600 text-green-600 hover:bg-green-50">Update</button>
            </td>
          </tr>
          <tr v-if="!loading && dramas.length === 0">
            <td colspan="8" class="text-center text-gray-500 py-6">No dramas found</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Drama Details Dialog -->
    <v-dialog v-model="showDialog" max-width="800px">
      <v-card>
        <v-card-title class="text-h6">
          Drama Details
        </v-card-title>
        <v-card-text>
          <v-skeleton-loader v-if="detailLoading" type="card"/>
          <div v-else class="mt-4">
            <!-- Part 1: Basic Info -->
            <div class="flex justify-between items-center mb-2">
              <h3 class="text-lg font-semibold">Basic Info</h3>
              <div class="flex gap-2">
                <v-btn icon variant="text" @click="startEdit('basic')" v-if="!editSection.basic">
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
                <div v-if="editSection.basic" class="flex gap-2">
                  <v-btn size="small" color="success" @click="saveSection('basic')">Save</v-btn>
                  <v-btn size="small" color="error" @click="cancelSection('basic')">Cancel</v-btn>
                </div>
              </div>
            </div>
            <v-row dense>
              <v-col cols="12" md="6">
                <v-text-field v-model="selectedDrama.drama_id" label="Drama ID" variant="underlined" readonly />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field v-model="selectedDrama.drama_sequence" label="Drama Seq" variant="underlined" :readonly="!editSection.basic" />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field v-model="selectedDrama.name" label="Name (EN)" variant="underlined" :readonly="!editSection.basic" />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field v-model="selectedDrama.name_in_korean" label="Name (KR)" variant="underlined" :readonly="!editSection.basic" />
              </v-col>
              <v-col cols="12" md="6">
                <v-select v-model="selectedDrama.type" :items="typeOptions" label="Type" variant="underlined" :disabled="!editSection.basic" />
              </v-col>
              <v-col cols="12" md="6">
                <v-select v-model="selectedDrama.genre" :items="genreOptions" multiple label="Genre" variant="underlined" :disabled="!editSection.basic" />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field v-model="selectedDrama.episode" label="Episodes" variant="underlined" :readonly="!editSection.basic" />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field v-model="selectedDrama.special_episode" label="Special Episodes" variant="underlined" :readonly="!editSection.basic" />
              </v-col>
              <v-col cols="12" md="6">
                <v-select v-model="selectedDrama.country" :items="countryOptions" label="Country" variant="underlined" :disabled="!editSection.basic" />
              </v-col>
              <v-col cols="12" md="6">
                <v-select v-model="selectedDrama.language" :items="languageOptions" label="Language" variant="underlined" :disabled="!editSection.basic" />
              </v-col>
              <v-col cols="12">
                <v-autocomplete
                    label="Starring"
                    v-model="selectedDrama.starring"
                    :items="artistOptions"
                    :item-title="item => `${item.artist_en_name || item.artist_id} (${item.artist_kr_name || ''})`"
                    item-value="id"
                    multiple
                    chips
                    clearable
                    variant="underlined"
                    :disabled="!editSection.basic"
                    hint="Select artists"
                    persistent-hint>
                  <template #item="{ props, item }">
                  <v-list-item v-bind="props" :title="undefined" :subtitle="undefined">
                      <template #prepend>
                        <v-avatar size="32">
                          <v-img :src="item.raw.image" alt="" />
                        </v-avatar>
                      </template>
                      <v-list-item-title>{{ `${item.raw.artist_en_name || item.raw.artist_id} (${item.raw.artist_kr_name || ''})` }}</v-list-item-title>
                      <v-list-item-subtitle>Birth: {{ formatBirthDate(item.raw.birth) }}</v-list-item-subtitle>
                    </v-list-item>
                  </template>
                  <template #selection="{ item }">
                    <v-chip size="small" class="ma-1" label>
                      {{ `${item.raw.artist_en_name || item.raw.artist_id} (${item.raw.artist_kr_name || ''})` }}
                    </v-chip>
                  </template>
                </v-autocomplete>
              </v-col>
              <v-col cols="12">
                <div class="d-flex align-center gap-2">
                  <v-text-field v-model="selectedDrama.thumbnail" label="Thumbnail URL" variant="underlined" :readonly="!editSection.basic" />
                  <v-file-input v-if="editSection.basic" v-model="thumbnailFile" accept="image/*" label="Upload" prepend-icon="mdi-image" density="comfortable" hide-details />
                  <v-btn v-if="editSection.basic" color="indigo" @click="uploadThumbnail" :disabled="!thumbnailFile">Upload</v-btn>
                </div>
              </v-col>
            </v-row>

            <v-divider class="my-4"></v-divider>

            <!-- Part 2: Broadcast Info -->
            <div class="flex justify-between items-center mb-2">
              <h3 class="text-lg font-semibold">Broadcast Info</h3>
              <div class="flex gap-2">
                <v-btn icon variant="text" @click="startEdit('broadcast')" v-if="!editSection.broadcast">
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
                <div v-if="editSection.broadcast" class="flex gap-2">
                  <v-btn size="small" color="success" @click="saveSection('broadcast')">Save</v-btn>
                  <v-btn size="small" color="error" @click="cancelSection('broadcast')">Cancel</v-btn>
                </div>
              </div>
            </div>
            <v-row dense>
              <v-col cols="12" md="4">
                <v-select v-model="selectedDrama.broadcast_year" :items="broadcastYears" label="Year" variant="underlined" :disabled="!editSection.broadcast" />
              </v-col>
              <v-col cols="12" md="4">
                <v-select v-model="selectedDrama.broadcast_day" :items="broadcastDays" multiple label="Day" variant="underlined" :disabled="!editSection.broadcast" />
              </v-col>
              <v-col cols="12" md="4">
                <v-menu
                    v-model="broadcastTimeMenu"
                    :close-on-content-click="false"
                    :disabled="!editSection.broadcast"
                    transition="scale-transition"
                    offset-y>
                  <template #activator="{ props }">
                    <v-text-field
                        v-model="selectedDrama.broadcast_time"
                        label="Time"
                        variant="underlined"
                        readonly
                        v-bind="editSection.broadcast ? props : {}" />
                  </template>
                  <v-list>
                    <v-list-item>
                      <input
                          type="time"
                          v-model="selectedDrama.broadcast_time"
                          class="p-2 border rounded"
                          :disabled="!editSection.broadcast"
                          @change="broadcastTimeMenu = false"
                      />
                    </v-list-item>
                  </v-list>
                </v-menu>
              </v-col>
              <v-col cols="12" md="6">
                <v-menu v-model="onAirMenu" :close-on-content-click="false" :disabled="!editSection.broadcast" transition="scale-transition" offset-y>
                  <template #activator="{ props }">
                    <v-text-field
                        :model-value="formatDate(selectedDrama.onair_date)"
                        label="On-Air Date"
                        variant="underlined"
                        readonly
                        v-bind="editSection.broadcast ? props : {}" />
                  </template>
                  <v-date-picker
                      v-model="onAirPicker"
                      @update:model-value="val => { selectedDrama.onair_date = val; onAirMenu = false; }"
                      no-title color="primary" />
                </v-menu>
              </v-col>
              <v-col cols="12" md="6">
                <v-menu v-model="finaleMenu" :close-on-content-click="false" :disabled="!editSection.broadcast" transition="scale-transition" offset-y>
                  <template #activator="{ props }">
                    <v-text-field
                        :model-value="formatDate(selectedDrama.finale)"
                        label="Finale Date"
                        variant="underlined"
                        readonly
                        v-bind="editSection.broadcast ? props : {}" />
                  </template>
                  <v-date-picker
                      v-model="finalePicker"
                      @update:model-value="val => { selectedDrama.finale = val; finaleMenu = false; }"
                      no-title color="primary" />
                </v-menu>
              </v-col>
              <v-col cols="12" md="6">
                <v-select v-model="selectedDrama.premiere_channel" :items="premiereOptions" multiple label="Premiere Channel" variant="underlined" :disabled="!editSection.broadcast" />
              </v-col>
              <v-col cols="12" md="6">
                <v-select v-model="selectedDrama.streaming" :items="streamingOptions" multiple label="Streaming" variant="underlined" :disabled="!editSection.broadcast" />
              </v-col>
            </v-row>

            <v-divider class="my-4"></v-divider>

            <!-- Part 3: Production Info -->
            <div class="flex justify-between items-center mb-2">
              <h3 class="text-lg font-semibold">Production Info</h3>
              <div class="flex gap-2">
                <v-btn icon variant="text" @click="startEdit('cast')" v-if="!editSection.cast">
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
                <div v-if="editSection.cast" class="flex gap-2">
                  <v-btn size="small" color="success" @click="saveSection('cast')">Save</v-btn>
                  <v-btn size="small" color="error" @click="cancelSection('cast')">Cancel</v-btn>
                </div>
              </div>
            </div>
            <v-row dense>
              <v-col cols="12">
                <v-combobox
                    label="Director"
                    v-model="selectedDrama.director"
                    multiple
                    chips
                    clearable
                    variant="underlined"
                    :disabled="!editSection.cast"
                    hint="Press Enter to add"
                    persistent-hint/>
              </v-col>
              <v-col cols="12">
                <v-combobox
                    label="Production"
                    v-model="selectedDrama.production"
                    multiple
                    chips
                    clearable
                    variant="underlined"
                    :disabled="!editSection.cast"
                    hint="Press Enter to add"
                    persistent-hint/>
              </v-col>
              <v-col cols="12">
                <v-combobox
                    label="Screenwriter"
                    v-model="selectedDrama.screenwriter"
                    multiple
                    chips
                    clearable
                    variant="underlined"
                    :disabled="!editSection.cast"
                    hint="Press Enter to add"
                    persistent-hint/>
              </v-col>
            </v-row>
          </div>
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn variant="text" @click="showDialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Pagination -->
    <div class="flex justify-between items-center mt-4">
      <div class="flex items-center gap-2">
        <span class="text-sm text-gray-600">Rows per page:</span>
        <select v-model="limit" class="border border-gray-300 rounded px-2 py-1">
          <option v-for="n in [10, 20, 50]" :key="n" :value="n">{{ n }}</option>
        </select>
      </div>
      <div class="flex items-center gap-2">
        <button @click="onPageChange(1)" :disabled="page === 1" class="px-3 py-1 rounded border disabled:opacity-50">First</button>
        <button @click="onPageChange(page - 1)" :disabled="page === 1" class="px-3 py-1 rounded border disabled:opacity-50">Prev</button>
        <span class="text-sm text-gray-600">Page {{ page }} of {{ totalPages }}</span>
        <button @click="onPageChange(page + 1)" :disabled="page === totalPages" class="px-3 py-1 rounded border disabled:opacity-50">Next</button>
        <button @click="onPageChange(totalPages)" :disabled="page === totalPages" class="px-3 py-1 rounded border disabled:opacity-50">Last</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>
