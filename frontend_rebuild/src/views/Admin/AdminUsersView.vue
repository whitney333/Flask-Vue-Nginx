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

onMounted(() => {
  fetchUsers();
});

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
          <th class="w-32 px-4 py-2 text-left">Followed Artists</th>
          <th class="w-32 px-4 py-2 text-left">Admin</th>
          <th class="w-32 px-4 py-2 text-left">Image</th>
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
          <td class="px-4 py-2">{{ u.followed_artist || '-' }}</td>
          <td class="px-4 py-2">{{ u.admin || '-' }}</td>
          <td class="px-4 py-2">
            <img
                v-if="u.image"
                :src="u.image"
                alt="artist"
                class="h-10 w-10 rounded object-cover"
            />
            <span v-else>-</span>
          </td>
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
