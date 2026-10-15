<script setup>
import {computed, onMounted, ref, watch} from "vue";
import {useRouter} from "vue-router";
import axios from "@/axios";
import {indexToCountry} from "@/libs/utils.js";

const router = useRouter();

const events = ref([]);
const artistOptions = ref([]);
const loading = ref(false);

const showAddDialog = ref(false);
const deleteDialog = ref(false);
const selectedDeleteEvent = ref(null);

const page = ref(1);
const limit = ref(10);
const total = ref(0);
const totalPages = computed(() => Math.max(Math.ceil(total.value / limit.value), 1));

const typeOptions = ["Concert", "Fan Meeting", "Festival", "Showcase", "Award Show", "Other"];

const filters = ref({
  search: ""
});

const emptyEvent = () => ({
  event_name: "",
  type: "",
  artist_id: "",
  event_date: "",
  session: "",
  held_country: "",
  held_city: "",
  venue: "",
  organizer: "",
  ticket_release: "",
  ticket_close: ""
});

const newEvent = ref(emptyEvent());

const snackbar = ref({
  show: false,
  message: "",
  color: "info"
});

const showMessage = (message, color = "info") => {
  snackbar.value = {
    show: true,
    message,
    color
  };
};

const formatDate = (date) => {
  if (!date) return "-";
  const d = new Date(date);
  if (Number.isNaN(d.getTime())) return "-";
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
};

const formatBirthDate = (date) => {
  if (!date) return "-";
  return formatDate(date);
};

const getArtistLabel = (artist) => {
  if (!artist || typeof artist !== "object") return "";
  const englishName = artist.artist_en_name || artist.artist_id || "";
  const koreanName = artist.artist_kr_name || "";
  return koreanName ? `${englishName} (${koreanName})` : englishName;
};

const buildPayload = (event) => ({
  event_name: event.event_name,
  type: event.type,
  artist_id: event.artist_id,
  event_date: event.event_date,
  session: event.session,
  held_country: event.held_country,
  held_city: event.held_city,
  venue: event.venue,
  organizer: event.organizer,
  ticket_release: event.ticket_release,
  ticket_close: event.ticket_close
});

const fetchEvents = async () => {
  loading.value = true;
  try {
    const res = await axios.get("/admin/v1/events", {
      params: {
        page: page.value,
        limit: limit.value,
        search: filters.value.search.trim()
      }
    });
    events.value = Array.isArray(res.data?.data) ? res.data.data : [];
    total.value = res.data?.total || 0;
  } catch (err) {
    console.error("Error fetching offline events:", err);
    showMessage("Failed to fetch events.", "error");
  } finally {
    loading.value = false;
  }
};

const fetchArtistOptions = async () => {
  try {
    const res = await axios.get("/admin/v1/artists/list");
    artistOptions.value = Array.isArray(res.data?.data) ? res.data.data : [];
  } catch (err) {
    console.error("Error fetching artist list:", err);
    artistOptions.value = [];
  }
};

const addEvent = async () => {
  loading.value = true;
  try {
    await axios.post("/admin/v1/events", buildPayload(newEvent.value), {
      headers: {"Content-Type": "application/json"}
    });
    showMessage("Event added successfully.", "success");
    showAddDialog.value = false;
    newEvent.value = emptyEvent();
    page.value = 1;
    await fetchEvents();
  } catch (err) {
    console.error("Add event failed:", err);
    showMessage(err.response?.data?.error || "Failed to add event.", "error");
  } finally {
    loading.value = false;
  }
};

const goToEventDetail = (eventId) => {
  router.push(`/admin/events/${eventId}`);
};

const openDeleteDialog = (event) => {
  selectedDeleteEvent.value = event;
  deleteDialog.value = true;
};

const deleteEvent = async () => {
  if (!selectedDeleteEvent.value) return;

  loading.value = true;
  try {
    await axios.delete(`/admin/v1/events/${selectedDeleteEvent.value.id}`);
    showMessage("Event deleted successfully.", "success");
    deleteDialog.value = false;
    selectedDeleteEvent.value = null;
    await fetchEvents();
  } catch (err) {
    console.error("Delete event failed:", err);
    showMessage("Failed to delete event.", "error");
  } finally {
    loading.value = false;
  }
};

const onFilterChange = () => {
  page.value = 1;
  fetchEvents();
};

const resetFilters = () => {
  filters.value.search = "";
  page.value = 1;
  fetchEvents();
};

const onPageChange = (newPage) => {
  page.value = Math.min(Math.max(newPage, 1), totalPages.value);
};

onMounted(() => {
  fetchEvents();
  fetchArtistOptions();
});

watch([page, limit], () => {
  fetchEvents();
});
</script>

<template>
  <div class="p-6 bg-gray-50 min-h-screen">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-semibold text-gray-800">Offline Events</h2>
      <button
          @click="showAddDialog = true"
          class="flex items-center gap-2 bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/>
        </svg>
        Add Event
      </button>
    </div>

    <div class="flex flex-wrap gap-4 mb-4 items-end">
      <div class="w-80 flex flex-col">
        <label class="text-sm font-medium text-gray-700 mb-1">Search</label>
        <div class="relative">
          <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-gray-500">
            <i class="mdi mdi-magnify"></i>
          </span>
          <input
              v-model="filters.search"
              type="text"
              class="w-full border border-gray-300 rounded-md pl-10 pr-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              placeholder="Event, artist, city, venue..."
              @keyup.enter="onFilterChange"/>
        </div>
      </div>
      <button class="h-[42px] px-4 text-sm border rounded-md hover:bg-gray-100 transition" @click="resetFilters">Reset</button>
      <button class="h-[42px] px-4 text-sm rounded-md bg-gray-800 text-white hover:bg-gray-900 transition" @click="onFilterChange">Submit</button>
    </div>

    <!-- Add Dialog -->
    <v-dialog v-model="showAddDialog" max-width="800px">
      <v-card>
        <v-card-title class="text-h6">Add Offline Event</v-card-title>
        <v-card-text>
          <v-row dense>
            <v-col cols="12" md="6">
              <v-text-field v-model="newEvent.event_name" label="Event Name" variant="underlined"/>
            </v-col>
            <v-col cols="12" md="6">
              <v-select v-model="newEvent.type" :items="typeOptions" label="Type" variant="underlined"/>
            </v-col>
            <v-col cols="12">
              <v-autocomplete
                  v-model="newEvent.artist_id"
                  :items="artistOptions"
                  :item-title="getArtistLabel"
                  item-value="id"
                  label="Artist"
                  clearable
                  variant="underlined">
                <template #item="{ props, item }">
                  <v-list-item v-bind="props" :title="undefined" :subtitle="undefined">
                    <template #prepend>
                      <v-avatar size="32">
                        <v-img v-if="item.raw.image" :src="item.raw.image" alt=""/>
                        <v-icon v-else>mdi-account</v-icon>
                      </v-avatar>
                    </template>
                    <v-list-item-title>{{ getArtistLabel(item.raw) }}</v-list-item-title>
                    <v-list-item-subtitle>Birth: {{ formatBirthDate(item.raw.birth) }}</v-list-item-subtitle>
                  </v-list-item>
                </template>
                <template #selection="{ item }">
                  <div class="flex items-center gap-2 min-w-0">
                    <v-avatar size="24">
                      <v-img v-if="item.raw.image" :src="item.raw.image" alt=""/>
                      <v-icon v-else size="16">mdi-account</v-icon>
                    </v-avatar>
                    <span class="truncate">{{ getArtistLabel(item.raw) }}</span>
                  </div>
                </template>
              </v-autocomplete>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                  v-model="newEvent.event_date"
                  label="Show Date"
                  type="date"
                  variant="underlined"/>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                  v-model="newEvent.session"
                  label="Show Session"
                  type="time"
                  variant="underlined"/>
            </v-col>
            <v-col cols="12" md="6">
              <v-select
                  v-model="newEvent.held_country"
                  :items="indexToCountry"
                  label="Country"
                  variant="underlined"/>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                  v-model="newEvent.held_city"
                  label="City"
                  variant="underlined"/>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                  v-model="newEvent.venue"
                  label="Venue"
                  variant="underlined"/>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                  v-model="newEvent.organizer"
                  label="Organizer"
                  variant="underlined"/>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                  v-model="newEvent.ticket_release"
                  label="Ticket Release"
                  type="datetime-local"
                  variant="underlined"/>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                  v-model="newEvent.ticket_close"
                  label="Ticket Close"
                  type="datetime-local"
                  variant="underlined"/>
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
              :loading="loading"
              @click="addEvent">
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar v-model="snackbar.show" :color="snackbar.color" timeout="1500" location="top">
      {{ snackbar.message }}
    </v-snackbar>

    <!-- Events Table -->
    <div class="overflow-x-auto bg-white rounded-lg shadow">
      <table class="min-w-full text-sm text-gray-700">
        <thead class="bg-gray-100 text-left text-gray-600 uppercase text-xs">
        <tr>
          <th class="px-6 py-3">Event ID</th>
          <th class="px-6 py-3">Event Name</th>
          <th class="px-6 py-3">Show Date</th>
          <th class="px-6 py-3">Show Session</th>
          <th class="px-6 py-3">Artist Name</th>
          <th class="px-6 py-3">Country</th>
          <th class="px-6 py-3">City</th>
          <th class="px-6 py-3">Venue</th>
          <th class="px-6 py-3">Organizer</th>
          <th class="px-6 py-3">Actions</th>
        </tr>
        </thead>
        <tbody>
        <tr
            v-for="event in events"
            :key="event.id"
            @click="goToEventDetail(event.id)"
            class="border-t hover:bg-gray-50 transition cursor-pointer">
          <td class="px-6 py-3 font-mono">{{ event.event_id }}</td>
          <td class="px-6 py-3">{{ event.event_name }}</td>
          <td class="px-6 py-3">{{ formatDate(event.event_date) }}</td>
          <td class="px-6 py-3">{{ event.session || '-' }}</td>
          <td class="px-6 py-3">{{ event.artist_name || '-' }}</td>
          <td class="px-6 py-3">{{ event.held_country || '-' }}</td>
          <td class="px-6 py-3">{{ event.held_city || '-' }}</td>
          <td class="px-6 py-3">{{ event.venue || '-' }}</td>
          <td class="px-6 py-3">{{ event.organizer || '-' }}</td>
          <td class="px-6 py-3">
            <div class="flex gap-2">
              <button
                  @click.stop="openDeleteDialog(event)"
                  class="px-2 py-1 rounded text-xs font-medium cursor-pointer border border-red-600 text-red-600 hover:bg-red-50 transition">
                Delete
              </button>
            </div>
          </td>
        </tr>
        <tr v-if="!loading && events.length === 0">
          <td colspan="10" class="text-center text-gray-500 py-6">No events found</td>
        </tr>
        </tbody>
      </table>
    </div>

    <!-- Delete Dialog -->
    <v-dialog v-model="deleteDialog" max-width="420px">
      <v-card>
        <v-card-title class="text-h6">Delete Event</v-card-title>
        <v-card-text>
          Delete {{ selectedDeleteEvent?.event_name || 'this event' }}?
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn variant="text" @click="deleteDialog = false">Cancel</v-btn>
          <v-btn color="error" :loading="loading" @click="deleteEvent">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Pagination -->
    <div class="flex justify-between items-center mt-4 flex-wrap gap-2">
      <div class="flex items-center gap-2">
        <span class="text-sm text-gray-600">Rows per page:</span>
        <select v-model="limit" class="border border-gray-300 rounded px-2 py-1">
          <option v-for="n in [10, 20, 50]" :key="n" :value="n">{{ n }}</option>
        </select>
      </div>
      <div class="flex items-center gap-2">
        <button @click="onPageChange(1)" :disabled="page === 1" class="px-3 py-1 rounded border hover:bg-gray-100 disabled:opacity-50">First</button>
        <button @click="onPageChange(page - 1)" :disabled="page === 1" class="px-3 py-1 rounded border hover:bg-gray-100 disabled:opacity-50">Prev</button>
        <span class="text-sm text-gray-600">Page {{ page }} of {{ totalPages }}</span>
        <button @click="onPageChange(page + 1)" :disabled="page === totalPages" class="px-3 py-1 rounded border hover:bg-gray-100 disabled:opacity-50">Next</button>
        <button @click="onPageChange(totalPages)" :disabled="page === totalPages" class="px-3 py-1 rounded border hover:bg-gray-100 disabled:opacity-50">Last</button>
      </div>
      <div v-if="loading" class="text-center py-2 text-gray-500">Loading...</div>
    </div>
  </div>
</template>

<style scoped>

</style>
