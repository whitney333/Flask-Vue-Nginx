<script setup>
import {ref, onMounted, watch, computed} from "vue";
import axios from "axios";
import {useUserStore} from "@/stores/user.js";


const tenants = ref([]);
const loading = ref(false);
const userStore = useUserStore();
const statusOptions = ["active", "suspended", "closed"];
// pagination
const page = ref(1); // current page
const limit = ref(10); // per page limit
const total = ref(0); // total page
const totalPages = computed(() => Math.ceil(total.value / limit.value));
// edit tenant
const editMode = ref(false)
const dialogLoading = ref(false)
const updateDialog = ref(false);
const showUpdateDialog = ref(false);
const selectedTenant = ref({
  tenant_id: null,
  tenant_name: "",
  website: "",
  email: "",
  status: ""
});
const detailLoading = ref(false);
// cancel tenant
const deleteDialog = ref(false)
const selectedTenantId = ref(null)
const selectedTenantName = ref('')
// add new tenant
const showDialog = ref(false);
const newTenant = ref({
  tenant_name: "",
  website: "",
  email: ""
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

// fetch all tenants
const fetchTenants = async () => {
  loading.value = true;
  try {
    const res = await axios.get(
        `/api/admin/v1/tenants`, {
          params: {
            page: page.value,
            limit: limit.value,
            tenant_name: filters.value.name,
            status: filters.value.status
          }
        }
    )
    tenants.value = res.data.data;
    total.value = res.data.total;
    // console.log("res: ", res)

  } catch (err) {
    console.error("Error fetching tenants:", err);
  } finally {
    loading.value = false;
  }
};

// update specific tenant
const openUpdateDialog = async (tenantId) => {
  console.log("Clicked row:", tenantId);
  detailLoading.value = true;
  selectedTenant.value = {};

  try {
    const token = userStore.firebaseToken
    const res = await axios.get(
        `/api/admin/v1/tenants/${tenantId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
    );

    selectedTenant.value = res.data.data || {};
    showUpdateDialog.value = true
  } catch (err) {
    console.error("Fetch tenant details failed:", err);
  } finally {
    detailLoading.value = false;
  }
}

// close dialog
const closeDialog = () => {
  showUpdateDialog.value = false
  editMode.value = false
}

// submit updated tenant details
const submitUpdateTenant = async () => {
  try {
    // console.log(selectedTenant.value)
    const token = userStore.firebaseToken
    const res = await axios.put(
        `/api/admin/v1/tenants/${selectedTenant.value.tenant_id}/update`,
        {tenant_name: selectedTenant.value.tenant_name,
              website: selectedTenant.value.website,
              email: selectedTenant.value.email,
              status: selectedTenant.value.status},
        {headers: {
              Authorization: `Bearer ${token}`
          }}
    )

    showUpdateDialog.value = false
    editMode.value = false
    fetchTenants()
  } catch (err) {
    console.error(err)
    alert("Failed to update tenant")
  }
}

// add new tenant
const addTenant = async () => {
  loading.value = true;
  try {
    const token = userStore.firebaseToken
    const res = await axios.post(
        `/api/admin/v1/tenants`,
        {
          tenant_name: newTenant.value.tenant_name,
          website: newTenant.value.website,
          email: newTenant.value.email
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          }
        }
    )

    // clear value when post success
    newTenant.value.tenant_name = "";
    newTenant.value.website = "";
    newTenant.value.email = "";

    // close dialog
    showDialog.value = false;

    // load all tenants again
    fetchTenants();

    showMessage("Tenant created successfully.", "success")
  } catch (err) {
    if (err.response?.status === 409) {
      showMessage("Tenant already exists. Please check tenant name, email and website.", "error")
    } else if (err.response?.status === 400) {
      showMessage("Please input tenant name.", "warning")
    } else {
      showMessage("Server error. Please try again later.", "error")
    }
  } finally {
    loading.value = false
  }
}

// open delete dialog
const openDeleteDialog = (tenantId) => {
  selectedTenantId.value = tenantId.tenant_id;
  selectedTenantName.value = tenantId.tenant_name;
  deleteDialog.value = true;
}

// cancel tenant
const confirmCancelTenant = async () => {
  try {
    const token = userStore.firebaseToken;
    await axios.patch(`/api/admin/v1/tenants/${selectedTenantId.value}/cancel`,
        {}, {
          headers: {Authorization: `Bearer ${token}`}
        })
    deleteDialog.value = false;
    fetchTenants();
  } catch (err) {
    console.error("Cancel failed:", err);
  }
}

const formatDate = (date) => {
  if (!date) return "-";
  return new Date(date).toLocaleString();
};

// filters
const filters = ref({
  name: "",
  status: "",
});

const onFilterChange = () => {
  page.value = 1;
  fetchTenants();
};

const resetFilters = () => {
  filters.value.name = "";
  filters.value.status = "";
  page.value = 1
  fetchTenants()
}

onMounted(fetchTenants);

watch([page, limit], () => {
  fetchTenants();
});

</script>

<template>
  <div class="p-6 bg-gray-50 min-h-screen">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-semibold text-gray-800">All Tenants</h2>
      <!-- open Dialog -->
      <button
          @click="showDialog = true"
          class="flex items-center gap-2 bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"
             stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/>
        </svg>
        Add New Tenant
      </button>
    </div>
    <!-- Filter -->
    <div class="flex flex-wrap gap-4 mb-4 items-end">
      <!-- Search tenant name -->
      <div class="w-64 flex flex-col">
        <label class="text-sm font-medium text-gray-700 mb-1">Tenant Name</label>
        <div class="relative">
          <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-gray-500">
            <i class="mdi mdi-magnify"></i>
          </span>
          <input
              v-model="filters.name"
              type="text"
              class="w-full border border-gray-300 rounded-md pl-10 pr-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              placeholder="Search name..."
          />
        </div>
      </div>

      <!-- Status filter -->
      <div class="w-40 flex flex-col">
        <label class="text-sm font-medium text-gray-700 mb-1">Status</label>
        <div class="relative">
          <select
              v-model="filters.status"
              class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              :class="filters.status === '' ? 'text-gray-400' : 'text-gray-700'"
          >
             <!-- placeholder -->
            <option value="" disabled selected hidden>Select Status</option>
            <option value="">All</option>
            <option value="active">Active</option>
            <option value="suspended">Suspended</option>
            <option value="closed">Closed</option>
          </select>
          <!-- icon -->
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
          class="h-[42px] px-4 text-sm rounded-md bg-gray-800 text-white hover:bg-gray-900 transition"
          @click="onFilterChange"
      >
        Submit
      </button>
    </div>
    <!-- open dialog: add new tenant -->
    <v-dialog v-model="showDialog" max-width="500px">
      <v-card>
        <v-card-title class="text-h6">Add New Tenant</v-card-title>

        <v-card-text>
          <v-text-field
              label="Tenant Name"
              v-model="newTenant.tenant_name"
              variant="underlined"
          ></v-text-field>
          <v-text-field
              label="Website"
              v-model="newTenant.website"
              variant="underlined"
          ></v-text-field>
          <v-text-field
              label="Email"
              v-model="newTenant.email"
              variant="underlined"
          ></v-text-field>
        </v-card-text>

        <v-card-actions class="justify-end">
          <v-btn variant="text" @click="showDialog = false">Cancel</v-btn>

          <v-btn
              color="indigo"
              class="text-white"
              @click="addTenant"
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
          <th class="w-32 px-4 py-2 text-left">Tenant Number</th>
          <th class="w-32 px-4 py-2 text-left">Tenant Name</th>
          <th class="w-32 px-4 py-2 text-left">Status</th>
          <th class="w-32 px-4 py-2 text-left">Website</th>
          <th class="w-32 px-4 py-2 text-left">Email</th>
          <th class="w-32 px-4 py-2 text-left">Created At</th>
          <th class="w-32 px-4 py-2 text-left">Updated At</th>
          <th class="w-32 px-4 py-2 text-left">Closed At</th>
          <th class="w-32 px-4 py-2 text-left">Actions</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="t in tenants"
            :key="t.tenant_id"
            class="border-t hover:bg-gray-50 transition">
          <td class="px-4 py-2 font-mono">{{ t.tenant_number || '-' }}</td>
          <td class="px-4 py-2">{{ t.tenant_name || '-' }}</td>
          <td class="px-4 py-2 capitalize">
              <span
                  class="px-2 py-1 rounded text-xs font-medium"
                  :class="{
                  'bg-green-100 text-green-800': t.status === 'active',
                  'bg-orange-100 text-orange-800': t.status === 'suspended',
                  'bg-red-100 text-red-800': t.status === 'closed'
                }"
              >
                {{ t.status || '-' }}
              </span>
          </td>
          <td class="px-4 py-2">{{ t.website || '-' }}</td>
          <td class="px-4 py-2">{{ t.email || '-' }}</td>
          <td class="px-4 py-2">{{ formatDate(t.created_at) }}</td>
          <td class="px-4 py-2">{{ t.updated_at ? formatDate(t.updated_at) : '-' }}</td>
          <td class="px-4 py-2">{{ t.closed_at ? formatDate(t.closed_at) : '-' }}</td>
          <td class="px-4 py-2 flex gap-2">
            <button
                @click.stop="openUpdateDialog(t.tenant_id)"
                class="px-2 py-1 rounded text-xs font-medium cursor-pointer border border-green-600 text-green-600 hover:bg-green-50 transition"
            >
              Update
            </button>
            <button
                @click.stop="openDeleteDialog(t)"
                class="px-2 py-1 rounded text-xs font-medium cursor-pointer border border-red-600 text-red-600 hover:bg-red-50 transition"
            >
              Close
            </button>
          </td>
        </tr>
        <tr v-if="!loading && tenants.length === 0">
          <td colspan="6" class="text-center text-gray-500 py-6">No tenants found</td>
        </tr>
        </tbody>
      </table>
    </div>
    <!-- Confirm cancel tenant dialog -->
    <v-dialog v-model="deleteDialog" persistent max-width="400">
      <v-card>
        <v-card-title class="text-h6">Delete Confirmation</v-card-title>
        <v-card-text>
          Are you sure you want to delete <b>{{ selectedTenantName }}</b>?
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn @click="deleteDialog = false">Cancel</v-btn>
          <v-btn color="red" @click="confirmCancelTenant">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- Update tenant details dialog -->
    <v-dialog v-model="showUpdateDialog" max-width="500px">
      <v-card>
        <v-card-title class="text-h6 flex justify-between items-center">
          Tenant Details
          <v-chip
              :color="editMode ? 'indigo' : 'grey'"
              text-color="white"
              size="small"
          >
            {{ editMode ? 'Edit Mode' : 'View Mode' }}
          </v-chip>
        </v-card-title>

        <v-card-text>
          <v-skeleton-loader v-if="dialogLoading" type="card"/>
          <div v-else class="space-y-4">
            <!-- Edit Icon -->
            <div class="flex justify-end">
              <v-btn icon
                     variant="text"
                     @click="editMode = true"
                     v-if="!editMode">
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
            </div>

            <!--  tenant form  -->
            <v-text-field
                label="Tenant Name"
                v-model="selectedTenant.tenant_name"
                variant="underlined"
                :readonly="!editMode"
                :class="editMode ? 'bg-indigo-50' : ''"
            ></v-text-field>
            <v-select
                label="Status"
                :items="statusOptions"
                v-model="selectedTenant.status"
                variant="underlined"
                :readonly="!editMode"
                :class="editMode ? 'bg-indigo-50' : ''"
            ></v-select>
            <v-text-field
                label="Website"
                v-model="selectedTenant.website"
                variant="underlined"
                :readonly="!editMode"
                :class="editMode ? 'bg-indigo-50' : ''"
            ></v-text-field>
            <v-text-field
                label="Email"
                v-model="selectedTenant.email"
                variant="underlined"
                :readonly="!editMode"
                :class="editMode ? 'bg-indigo-50' : ''"
            ></v-text-field>
          </div>
        </v-card-text>

        <v-card-actions class="justify-end">
          <v-btn variant="text" @click="closeDialog">
            Cancel
          </v-btn>
          <v-btn
              color="green"
              class="text-white"
              @click="submitUpdateTenant"
              :disabled="!editMode"
          >
            Save
          </v-btn>
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

</style>