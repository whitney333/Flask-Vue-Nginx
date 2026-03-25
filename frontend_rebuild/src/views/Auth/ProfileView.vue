<script setup>
import { useUserStore } from "@/stores/user.js";
import { computed, ref, onMounted } from "vue"
import { getAuth } from "firebase/auth"
import axios from "@/axios";

const userStore = useUserStore()
const defaultAvatar = "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-dist/user-circle-96.png"

const isPremium = computed(() => userStore.isPremium)
const billingInterval = ref("monthly") // monthly/yearly

// Modal state
const showManageArtists = ref(false)
const artists = ref([])                // 所有 tenant 的 artist
const editingArtists = ref([])         // modal 中選中的 artist ids
const isSaving = ref(false)
const isLoadingArtists = ref(false)
const plan = ref("free")

// plan config
const PLANS = [
  {
    key: "starter",
    name: "Starter",
    monthlyPrice: 10,
    yearlyPrice: 110,
    features: [
      "Artist online presence data aggregation",
      "Campaign performance tracking",
      "Campaign analytics",
      "1 artist",
    ]
  },
  {
    key: "standard",
    name: "Standard",
    monthlyPrice: 70,
    yearlyPrice: 770,
    features: [
      "Artist online presence data aggregation",
      "Campaign performance tracking",
      "Campaign analytics",
      "up to 10 artists",
    ]
  }
]
const currentPlanConfig = computed(() => {
  return PLANS.find(p => p.key === plan.value) || PLANS[0]
})

const planName = computed(() => userStore.plan)

const planLabel = computed(() => {
  if (!isPremium.value) return "Free Plan"

  return `${planName.value === "starter" ? "Starter" : "Standard"} ${
    billingInterval.value === "yearly" ? "Yearly" : "Monthly"
  }`
})

const expiredDate = computed(() => {
  if (!userStore.expiredAt) return ""
  return new Date(userStore.expiredAt).toLocaleDateString(
    undefined,
    { year: "numeric", month: "short", day: "numeric" }
  )
})

const upgrade = async () => {
  const auth = getAuth()
  const user = auth.currentUser

  if (!user) {
    alert("Not logged in")
    return
  }

  const res = await axios.post("/stripe/checkout-session", {
    plan: plan.value,
    billing_interval: billingInterval.value
  })
  const data = res.data
  if (data.checkout_url) {
    window.location.href = data.checkout_url
  } else {
    alert("Failed to open Stripe checkout")
  }
}

//subscription status
const manageSubscription = async () => {
  try {
    const res = await axios.post("/stripe/customer-portal", {})
    const data = res.data
    window.location.href = data.url
  } catch (err) {
    console.error(err)
    alert("Failed to open portal")
  }
}

onMounted(async () => {
  await userStore.fetchMe()
  plan.value = userStore.plan || "free"
})

const goUpgrade = () => {
  router.push("/billing") // or stripe checkout
}


// 打開 modal
const openManageArtists = async () => {
  showManageArtists.value = true
  isLoadingArtists.value = true

  // 初始化已選 artist
  editingArtists.value = userStore.followedArtists.map(a => a.artist_id)

  try {
    const res = await axios.get(`/user/v1/artists/${userStore.tenant}`)
    const data = res.data
    artists.value = data.data || []
  } catch (err) {
    console.error(err)
    alert("Failed to load artists")
  } finally {
    isLoadingArtists.value = false
  }
}

const closeManageArtists = () => {
  showManageArtists.value = false
}

// 方案上限
const artistLimit = computed(() => {
  if (!userStore.isPremium) return 1
  if (userStore.plan === "standard") return 10
  return 1 // starter
})

// 判斷 modal 是否鎖住（free / starter 限制）
const isPlanLocked = computed(() => {
  return !userStore.isPremium || userStore.plan === "starter"
})

const isSelected = (artistId) => {
  return editingArtists.value.includes(artistId)
}

// 判斷 Add / Remove 按鈕是否 disable
const isAddDisabled = (artistId) => {
  const selectedCount = editingArtists.value.length
  const isAlreadySelected = isSelected(artistId)

  // ❌ Remove：不能刪到 0（至少要 1 位）
  if (isAlreadySelected && selectedCount <= 1) {
    return true
  }

  // ❌ Add：Free / Starter 不能新增
  if (!isAlreadySelected && isPlanLocked.value) {
    return true
  }

  // ❌ Add：Standard 超過上限
  if (!isAlreadySelected && selectedCount >= artistLimit.value) {
    return true
  }

  return false
}

const toggleArtist = (artistId) => {
  if (isSelected(artistId)) {
    if (editingArtists.value.length <= 1) return
    editingArtists.value = editingArtists.value.filter(id => id !== artistId)
  } else {
    if (editingArtists.value.length >= artistLimit.value) return
    editingArtists.value.push(artistId)
  }
}

// 儲存
const saveArtists = async () => {
  isSaving.value = true
  try {
    await axios.put("/user/v1/followed_artists", {
      artist_ids: editingArtists.value
    })

    await userStore.fetchMe()
    showManageArtists.value = false

  } catch (err) {
    console.error(err)
    alert("Failed to update artists")
  } finally {
    isSaving.value = false
  }
}


</script>


<template>
  <div class="max-w-3xl mx-auto px-4 py-8 space-y-6">

    <!-- ===== User Info ===== -->
    <div class="bg-white border border-gray-200 rounded-lg p-6 flex items-center gap-4">
      <div
        class="w-16 h-16 rounded-full bg-gray-200 text-white flex items-center justify-center text-xl font-semibold"
      >
        <img
          v-if="userStore.photo"
          :src="userStore.photo"
          class="w-full h-full rounded-full object-cover"
        />
        <span v-else>
          {{ userStore.name?.charAt(0).toUpperCase() || "U" }}
        </span>
      </div>

      <div class="flex-1">
        <h2 class="text-lg font-semibold text-gray-900">
          {{ userStore.name }}
        </h2>
        <p class="text-sm text-gray-500">
          {{ userStore.email }}
        </p>

        <span
          class="inline-block mt-2 px-2 py-1 text-xs font-medium rounded-full"
          :class="isPremium
            ? 'bg-indigo-100 text-indigo-700'
            : 'bg-gray-100 text-gray-600'"
        >
          {{ planLabel }}
        </span>

        <span v-if="isPremium && expiredDate" class="ml-2 text-sm text-gray-500">
          Expires: {{ expiredDate }}
        </span>
      </div>
    </div>

    <!-- ===== Plan / Upgrade ===== -->
    <div
      class="border rounded-lg p-6"
      :class="isPremium ? 'bg-white border-gray-200' : 'bg-indigo-50 border-indigo-200'"
    >

      <!-- ===== FREE USER ===== -->
      <template v-if="!isPremium">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          Upgrade to Premium
        </h3>

        <!-- ===== Plan Tier Selector ===== -->
        <div class="grid grid-cols-2 gap-4 mb-6">
          <button
            v-for="p in PLANS"
            :key="p.key"
            @click="plan = p.key"
            :class="plan === p.key
              ? 'border-indigo-600 ring-2 ring-indigo-600'
              : 'border-gray-300 hover:border-gray-400'"
            class="border rounded-lg p-4 bg-white text-left transition"
          >
            <h4 class="text-lg font-semibold text-gray-900">
              {{ p.name }}
            </h4>
            <p class="mt-1 text-sm text-gray-500">
              {{ p.description }}
            </p>

            <p class="mt-3 text-xl font-semibold text-gray-900">
              {{ billingInterval === 'monthly'
                ? `$${p.monthlyPrice} / month`
                : `$${p.yearlyPrice} / year`
              }}
            </p>
          </button>
        </div>

        <!-- ===== Billing Interval Selector ===== -->
        <div class="grid grid-cols-2 gap-4 mb-6">
          <button
            @click="billingInterval = 'monthly'"
            :class="billingInterval === 'monthly'
              ? 'border-indigo-600 ring-2 ring-indigo-600'
              : 'border-gray-300 hover:border-gray-400'"
            class="border rounded-lg p-4 bg-white transition"
          >
            <p class="font-medium text-gray-900">Monthly</p>
            <p class="text-xs text-gray-500 mt-1">Billed monthly</p>
          </button>

          <button
            @click="billingInterval = 'yearly'"
            :class="billingInterval === 'yearly'
              ? 'border-indigo-600 ring-2 ring-indigo-600'
              : 'border-gray-300 hover:border-gray-400'"
            class="border rounded-lg p-4 bg-white relative transition"
          >
            <span
              class="absolute top-2 right-2 text-xs bg-indigo-600 text-white px-2 py-0.5 rounded-full"
            >
              Save more
            </span>
            <p class="font-medium text-gray-900">Yearly</p>
            <p class="text-xs text-gray-500 mt-1">Billed yearly</p>
          </button>
        </div>

        <!-- ===== Features ===== -->
        <ul class="text-sm text-gray-600 space-y-1 mb-6">
          <li v-for="f in currentPlanConfig.features" :key="f">
            • {{ f }}
          </li>
        </ul>

        <!-- ===== CTA ===== -->
        <button
          @click="upgrade"
          class="w-full px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-md text-sm font-medium"
        >
          Upgrade Now
        </button>
      </template>

      <!-- ===== PREMIUM USER ===== -->
      <template v-else>
        <h3 class="text-lg font-semibold text-gray-900 mb-1">
          Your Subscription
        </h3>
        <p class="text-sm text-gray-600 mb-4">
          {{ planLabel }} · Active
        </p>
        <button
          @click="manageSubscription"
          class="px-4 py-2 border border-indigo-600 text-indigo-600 hover:bg-indigo-50 rounded-md text-sm font-medium"
        >
          Manage Subscription
        </button>
      </template>
    </div>

    <!-- ===== Followed Artists ===== -->
    <div class="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
      <h3 class="text-lg font-semibold text-gray-900">
        Followed Artists
        <span class="ml-2 text-sm text-gray-500">
          ({{ userStore.followedArtists.length }} / {{ artistLimit }})
        </span>
      </h3>

      <button
          @click="openManageArtists"
          class="px-4 py-2 border border-indigo-600 text-indigo-600 hover:bg-indigo-50 rounded-md text-sm font-medium"
      >
        Manage
      </button>
    </div>

    <ul class="divide-y">
      <li
          v-for="artist in userStore.followedArtists"
          :key="artist.id"
          class="px-6 py-4 flex items-center gap-4"
      >
        <img
            :src="artist.image"
            class="w-10 h-10 rounded-full object-cover"
        />
        <div class="flex-1">
          <p class="font-medium text-gray-900">
            {{ artist.english_name }}
          </p>
          <p class="text-sm text-gray-500">
            {{ artist.korean_name }}
          </p>
        </div>

      </li>

      <li
          v-if="!userStore.followedArtists?.length"
          class="px-6 py-4 text-sm text-gray-500"
      >
        No followed artists
      </li>
    </ul>
    <!-- ===== Manage Artists Modal ===== -->
    <div
        v-if="showManageArtists"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/40"
    >
      <div class="w-full max-w-lg bg-white rounded-xl shadow-xl">

        <!-- Header -->
        <div class="px-6 py-4 border-b flex items-center justify-between">
          <h3 class="text-lg font-semibold text-gray-900">
            Manage Artists
            <span class="ml-2 text-sm text-gray-500">
          ({{ editingArtists.length }} / {{ artistLimit }})
        </span>
          </h3>

          <button
              @click="closeManageArtists"
              class="text-gray-400 hover:text-gray-600"
          >
            ✕
          </button>
        </div>

        <!-- Body -->
        <div class="px-6 py-4 space-y-4">

          <!-- Artist List -->
          <div class="space-y-2 max-h-72 overflow-y-auto">
            <div
                v-for="artist in artists"
                :key="artist.artist_objId"
                class="flex items-center justify-between p-3 border rounded-lg"
                :class="isSelected(artist.artist_objId)
            ? 'border-indigo-600 bg-indigo-50'
            : 'border-gray-200'"
            >
              <div class="flex items-center gap-3">
                <img
                    :src="artist.imageURL"
                    class="w-10 h-10 rounded-full object-cover"
                />
                <div>
                  <p class="font-medium text-gray-900">
                    {{ artist.artist_name }}
                  </p>
                  <p class="text-sm text-gray-500">
                    {{ artist.korean_name }}
                  </p>
                </div>
              </div>

              <button
                  @click="toggleArtist(artist.artist_objId)"
                  :disabled="isAddDisabled(artist.artist_objId)"
                  class="text-sm font-medium px-3 py-1.5 rounded-md"
                  :class="isSelected(artist.artist_objId)
              ? 'bg-red-100 text-red-600 hover:bg-red-200'
              : 'bg-indigo-600 text-white hover:bg-indigo-700 disabled:bg-gray-300'"
              >
                {{ isSelected(artist.artist_objId) ? "Remove" : "Add" }}
              </button>
            </div>
          </div>

          <!-- Limit Warning -->
          <div
              v-if="editingArtists.length >= artistLimit"
              class="text-sm text-red-600 bg-red-50 border border-red-200 rounded-md px-3 py-2"
          >
            Your current plan allows up to {{ artistLimit }} artist<span v-if="artistLimit > 1">s</span>.
            <span v-if="artistLimit === 1">
              Upgrade to Standard to follow more.
            </span>
          </div>

        </div>

        <!-- Footer -->
        <div class="px-6 py-4 border-t flex justify-end gap-3">
          <button
              @click="closeManageArtists"
              class="px-4 py-2 text-sm rounded-md border border-gray-300 hover:bg-gray-50"
          >
            Cancel
          </button>

          <button
              @click="saveArtists"
              :disabled="isSaving"
              class="px-4 py-2 text-sm rounded-md bg-indigo-600 text-white hover:bg-indigo-700 disabled:opacity-50"
          >
            {{ isSaving ? "Saving..." : "Save" }}
          </button>
        </div>

    </div>
  </div>
  </div>
</template>


<style scoped>

</style>
