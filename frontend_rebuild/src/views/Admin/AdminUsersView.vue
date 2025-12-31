<script setup>
import {ref, onMounted, watch, computed} from "vue";
import axios from "axios";
import {useUserStore} from "@/stores/user.js";
import {indexToCountry} from "@/libs/utils.js";
import StatusChip from "@/components/StatusChip.vue"


const users = ref([]);
const userStore = useUserStore();
const loading = ref(false);

// pagination
const page = ref(1); // current page
const limit = ref(10); // per page limit
const total = ref(0); // total page
const totalPages = computed(() => Math.ceil(total.value / limit.value));

const showAddDialog = ref(false);

// dropdown list options
const adminOptions = [true, false]
const artistOptions = []
const filteredArtists = []
const tenantOptions = ref([])
const artists = ref([])
const selectedArtists = ref([])
const newUser = ref({
  name: "",
  email: "",
  admin: "",
  tenant: null,
  followed_artist: []
})

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

// get all users
const fetchUsers = async () => {
  loading.value = true;
  try {
    const res = await axios.get(
        `/api/admin/v1/users`, {
          params: {
            page: page.value,
            limit: limit.value,
          }
        }
    )
    users.value = res.data.data;
    total.value = res.data.total;
    // console.log("res: ", res.data.data)

  } catch (err) {
    console.error("Error fetching users:", err);
  } finally {
    loading.value = false;
  }
}

// view single user
const viewUserDetail = async () => {
  try {

  } catch (err) {

  }
}

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

//
const handleCompanyChange = async (tenantId) => {
  selectedTenantId.value = tenantId   // store tenant id
  console.log("selected tenantId:", selectedTenantId.value)

  // get artists
  const res = await axios.get(`/user/v1/artists/${tenantId}`)
  console.log("artists:", res.data.data)
}

// add new user
const addUser = async () => {
  loading.value = true;
  try {
    const token = userStore.firebaseToken
    const res = await axios.post(
      `/api/admin/v1/users`,
          newUser.value, {
        headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          }
        }
    )

     console.log("user: ", newUser.value)
    showMessage("User added successfully.", "success");
    // close dialog
    showAddDialog.value = false;

  } catch (err) {

  } finally {
    loading.value = false;
  }
}

// company name filter
const companyFilter = (item, queryText, itemText) => {
  if (!itemText) return false;

  const text = itemText.toString().toLowerCase();
  const query = queryText.toString().toLowerCase();

  return text.includes(query);
};

onMounted(() => {
  fetchUsers();
  getTenantDropDownList();
});

watch(
    () => newUser.value.tenant,
    async (newTenantId) => {
      if (!newTenantId) {
        artists.value = []
        selectedArtists.value = []
        newUser.value.followed_artist = []
        return
      }

      try {
        const res = await axios.get(`/api/user/v1/artists/${newTenantId}`)
        artists.value = res.data.data || []

        // renew options of v-select
        selectedArtists.value = artists.value.map(a => ({
          id: a.artist_objId,
          name: `${a.artist_name} (${a.korean_name || ""})`
        }))

        // clean artist
        newUser.value.followed_artist = []
      } catch (err) {
        console.error(err)
        artists.value = []
        selectedArtists.value = []
        newUser.value.followed_artist = []
      }
    }
)

watch([page, limit], () => {
  fetchUsers();
});

</script>

<template>
  <div class="p-6 bg-gray-50 min-h-screen">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-semibold text-gray-800">All Users</h2>
      <!-- open Dialog -->
      <button
          @click="showAddDialog = true"
          class="flex items-center gap-2 bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"
             stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/>
        </svg>
        Add User
      </button>
    </div>
    <!-- open dialog: add new user -->
    <v-dialog v-model="showAddDialog" max-width="500px">
      <v-card>
        <v-card-title class="text-h6">Add New User</v-card-title>

        <v-card-text>
          <!-- User Info  -->
          <div class="flex items-center gap-3">
            <h3 class="text-lg font-semibold">User Info</h3>
          </div>
          <v-row dense>
            <v-col cols="12" md="6">
              <v-text-field
                  label="User Name"
                  v-model="newUser.name"
                  variant="underlined"
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                  label="Email"
                  v-model="newUser.email"
                  variant="underlined"
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-select
                  label="Company"
                  v-model="newUser.tenant"
                  :items="tenantOptions"
                  variant="underlined"
                  item-title="tenant_name"
                  item-value="id"
                  :filter="companyFilter"
                  :search="true"
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-select
                  label="is Admin"
                  v-model="newUser.admin"
                  :items="adminOptions"
                  variant="underlined"
              />
            </v-col>
            <!-- only display artists belong to selected company -->
            <v-col cols="12" md="12">
              <v-select
                  label="Followed Artists"
                  v-model="newUser.followed_artist"
                  :items="selectedArtists"
                  item-title="name"
                  item-value="id"
                  variant="underlined"
                  multiple
                  :disabled="!newUser.tenant"
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
              @click="addUser"
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Table -->
    <div class="overflow-x-auto bg-white rounded-lg shadow">
      <table class="min-w-full text-sm text-gray-700">
        <thead class="bg-gray-100 text-left text-gray-600 uppercase text-xs">
        <tr>
          <th class="w-32 px-4 py-2 text-left">User Id</th>
          <th class="w-32 px-4 py-2 text-left">Created At</th>
          <th class="w-32 px-4 py-2 text-left">User Name</th>
          <th class="w-32 px-4 py-2 text-left">Email</th>
          <th class="w-32 px-4 py-2 text-left">Belong Tenant</th>
          <th class="w-32 px-4 py-2 text-left">Admin</th>
          <th class="w-32 px-4 py-2 text-left">Actions</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="u in users"
            :key="u.email"
            class="border-t hover:bg-gray-50 transition">
          <td class="px-4 py-2 font-mono">{{ u.user_id || '-' }}</td>
          <td class="px-4 py-2">{{ u.created_at || '-' }}</td>
          <td class="px-4 py-2">{{ u.name || '-' }}</td>
          <td class="px-4 py-2">{{ u.email || '-' }}</td>
          <td class="px-4 py-2">{{ u.tenant || '-' }}</td>
          <td class="px-4 py-2">{{ u.admin || '-' }}</td>
          <td class="px-4 py-2 flex gap-2">
            <button
                @click.stop="viewUserDetail(u.user_id)"
                class="px-2 py-1 rounded text-xs font-medium cursor-pointer border border-green-600 text-green-600 hover:bg-green-50 transition"
            >
              Update
            </button>
          </td>
        </tr>
        <tr v-if="!loading && users.length === 0">
          <td colspan="6" class="text-center text-gray-500 py-6">No artists found</td>
        </tr>
        </tbody>
      </table>
    </div>

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
