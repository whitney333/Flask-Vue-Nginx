<script setup>
import {ref, onMounted, watch, computed} from "vue";
import axios from "axios";
import {useUserStore} from "@/stores/user.js";
import StatusChip from "@/components/StatusChip.vue"

// dropdown list options
const typeOptions = ["Drama", "Movie", "Variety Show"]
const genreOptions = ["Action", "Romance", "Comedy", "Thriller", "Horror", "Fantasy", "Historical", "Slice of Life", "Mystery"]
const currentYear = new Date().getFullYear()
const broadcastYears = Array.from({ length: currentYear - 1950 + 1 }, (_, i) => 1950 + i)

const thumbnailFile = ref(null);
const dramas = ref([]);
const loading = ref(false);
const userStore = useUserStore();
const showDialog = ref(false);
const datePickerMenu = ref(false);

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
const newDrama = ref({
  drama_id: "",
  name: "",
  name_in_korean: "",
  broadcast_year: currentYear,
  country: "",
  episode: "",
  genre: [],
  type: "Drama",
  language: "",
  onair_date: "",
  broadcast_day: "",
  broadcast_time: "",
  thumbnail: ""
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
}

// fetch all dramas
const fetchDramas = async () => {
  loading.value = true;
  try {
    const res = await axios.get(
        `/api/admin/v1/dramas`, {
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
  try {
    const token = userStore.firebaseToken
    await axios.post(
        `/api/admin/v1/dramas`,
        newDrama.value, {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          }
        }
    )
    showMessage("Drama added successfully.", "success");
    showAddDialog.value = false;
    onAirText.value = ""
    newDrama.value = { broadcast_year: currentYear, type: "Drama" }
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

  try {
    const token = userStore.firebaseToken
    const res = await axios.get(
        `/api/admin/v1/dramas/${id}`,
        {
          headers: { Authorization: `Bearer ${token}` }
        }
    );
    selectedDrama.value = res.data.data || {};
  } catch (err) {
    console.error("Fetch drama details failed:", err);
  } finally {
    detailLoading.value = false;
  }
}

const updateDrama = async (section, dramaId) => {
  try {
    const token = userStore.firebaseToken
    let payload = { ...selectedDrama.value }
    
    const res = await axios.patch(
        `/api/admin/v1/dramas/${dramaId}`,
        payload, {
          headers: { Authorization: `Bearer ${token}` }
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
    const token = userStore.firebaseToken
    const res = await axios.post(
      "/api/admin/v1/dramas/upload/thumbnail",
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: `Bearer ${token}`
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

const openChangeStatusDialog = (drama) => {
  selectedDramaId.value = drama.id;
  selectedDramaName.value = drama.name;
  deleteDialog.value = true;
}

const confirmChangeStatus = async () => {
  try {
    const token = userStore.firebaseToken;
    await axios.patch(`/api/admin/v1/dramas/${selectedDramaId.value}/status`,
        {}, {
          headers: {Authorization: `Bearer ${token}`}
        })
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

onMounted(() => {
  fetchDramas();
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
    <v-dialog v-model="showAddDialog" max-width="600px">
      <v-card>
        <v-card-title class="text-h6">Add New Drama</v-card-title>
        <v-card-text>
          <v-row dense>
            <v-col cols="12" md="6">
              <v-text-field label="Drama ID" v-model="newDrama.drama_id" variant="underlined" />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field label="Name (EN)" v-model="newDrama.name" variant="underlined" />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field label="Name (KR)" v-model="newDrama.name_in_korean" variant="underlined" />
            </v-col>
            <v-col cols="12" md="6">
              <v-select label="Type" v-model="newDrama.type" :items="typeOptions" variant="underlined" />
            </v-col>
            <v-col cols="12" md="6">
              <v-select label="Broadcast Year" v-model="newDrama.broadcast_year" :items="broadcastYears" variant="underlined" />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field label="Country" v-model="newDrama.country" variant="underlined" />
            </v-col>
             <v-col cols="12" md="6">
              <v-text-field label="Episodes" v-model="newDrama.episode" variant="underlined" />
            </v-col>
            <v-col cols="12" md="6">
              <v-select label="Genre" v-model="newDrama.genre" :items="genreOptions" multiple variant="underlined" />
            </v-col>
            <v-col cols="12" md="6">
              <v-menu v-model="onAirMenu" :close-on-content-click="false" transition="scale-transition" offset-y>
                <template #activator="{ props }">
                  <v-text-field v-model="onAirText" label="On-Air Date" variant="underlined" readonly v-bind="props" />
                </template>
                <v-date-picker v-model="onAirPicker" @update:model-value="setOnAirDate" no-title color="primary" />
              </v-menu>
            </v-col>
             <v-col cols="12" md="6">
              <v-text-field label="Language" v-model="newDrama.language" variant="underlined" />
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn variant="text" @click="showAddDialog = false">Cancel</v-btn>
          <v-btn color="indigo" class="text-white" @click="addDrama">Save</v-btn>
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
            <td class="px-4 py-2 flex gap-2">
              <button @click="viewDramaDetail(d.id)" class="px-2 py-1 rounded text-xs font-medium border border-green-600 text-green-600 hover:bg-green-50">Update</button>
              <button @click="openChangeStatusDialog(d)" class="px-2 py-1 rounded text-xs font-medium border border-red-600 text-red-600 hover:bg-red-50">Status</button>
            </td>
          </tr>
          <tr v-if="!loading && dramas.length === 0">
            <td colspan="7" class="text-center text-gray-500 py-6">No dramas found</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Drama Details Dialog -->
    <v-dialog v-model="showDialog" max-width="800px">
      <v-card>
        <v-card-title class="text-h6">Drama Details</v-card-title>
        <v-card-text>
          <v-skeleton-loader v-if="detailLoading" type="card"/>
          <div v-else class="space-y-6">
            <div>
              <div class="flex justify-between items-center mb-2">
                <div class="flex items-center gap-3">
                  <h3 class="text-lg font-semibold">Basic Info</h3>
                  <StatusChip :edit="editSection.basic"/>
                </div>
                <div class="flex gap-2">
                  <v-btn icon variant="text" @click="startEdit('basic')" v-if="!editSection.basic"><v-icon>mdi-pencil</v-icon></v-btn>
                  <div v-if="editSection.basic" class="flex gap-2">
                    <v-btn size="small" color="success" @click="saveSection('basic')">Save</v-btn>
                    <v-btn size="small" color="error" @click="cancelSection('basic')">Cancel</v-btn>
                  </div>
                </div>
              </div>
              <v-row dense>
                <v-col cols="12" md="6">
                  <v-text-field v-model="selectedDrama.drama_id" label="Drama ID" variant="underlined" :readonly="!editSection.basic" />
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field v-model="selectedDrama.name" label="Name (EN)" variant="underlined" :readonly="!editSection.basic" />
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field v-model="selectedDrama.name_in_korean" label="Name (KR)" variant="underlined" :readonly="!editSection.basic" />
                </v-col>
                <v-col cols="12" md="6">
                  <v-select v-model="selectedDrama.type" :items="typeOptions" label="Type" variant="underlined" :readonly="!editSection.basic" />
                </v-col>
                <v-col cols="12" md="6">
                  <v-select v-model="selectedDrama.broadcast_year" :items="broadcastYears" label="Year" variant="underlined" :readonly="!editSection.basic" />
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field v-model="selectedDrama.country" label="Country" variant="underlined" :readonly="!editSection.basic" />
                </v-col>
                <v-col cols="12" md="6">
                   <v-menu v-model="datePickerMenu" :close-on-content-click="false" transition="scale-transition" offset-y>
                    <template #activator="{ props }">
                      <v-text-field v-model="formattedOnAirDate" label="On-Air Date" variant="underlined" readonly v-bind="editSection.basic ? props : {}" />
                    </template>
                    <v-date-picker v-model="selectedDrama.onair_date" no-title color="primary" />
                  </v-menu>
                </v-col>
                <v-col cols="12">
                   <div class="d-flex align-center gap-2">
                    <v-text-field v-model="selectedDrama.thumbnail" label="Thumbnail URL" variant="underlined" :readonly="!editSection.basic" />
                    <v-file-input v-if="editSection.basic" v-model="thumbnailFile" accept="image/*" label="Upload" prepend-icon="mdi-image" density="comfortable" hide-details />
                    <v-btn v-if="editSection.basic" color="indigo" @click="uploadThumbnail" :disabled="!thumbnailFile">Upload</v-btn>
                  </div>
                </v-col>
              </v-row>
            </div>
          </div>
        </v-card-text>
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
        <button @click="page--" :disabled="page === 1" class="px-3 py-1 rounded border disabled:opacity-50">Prev</button>
        <span class="text-sm text-gray-600">Page {{ page }} of {{ totalPages }}</span>
        <button @click="page++" :disabled="page === totalPages" class="px-3 py-1 rounded border disabled:opacity-50">Next</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>
