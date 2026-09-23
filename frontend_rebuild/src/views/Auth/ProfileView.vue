<script setup>
import { useUserStore } from "@/stores/user.js";
import { computed, ref, onMounted } from "vue"
import { getAuth } from "firebase/auth"
import axios from "@/axios";
import { useRouter } from "vue-router"; //
import { useI18n } from "vue-i18n"

const router = useRouter()
const { t, tm } = useI18n({ useScope: "global" })
const userStore = useUserStore()
const defaultAvatar = "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-dist/user-circle-96.png"

const isPremium = computed(() => userStore.isPremium)
const billingInterval = ref("monthly") // monthly/yearly

// Modal state & Pagination state
const showManageArtists = ref(false)
const artists = ref([])                // 所有 tenant 的 artist
const editingArtists = ref([])         // modal 中選中的 artist ids
const isSaving = ref(false)
const isLoadingArtists = ref(false)
const plan = ref("free")

const lockedArtistId = ref(null)

const page = ref(1)
const hasMore = ref(true)
const isLoadingMore = ref(false)

const searchQuery = ref("")
let searchDebounceTimer = null

// plan config
const PLANS = [
  {
    key: "starter",
    monthlyPrice: 10,
    yearlyPrice: 110,
  },
  {
    key: "standard",
    monthlyPrice: 70,
    yearlyPrice: 770,
  }
]
const currentPlanConfig = computed(() => {
  return PLANS.find(p => p.key === plan.value) || PLANS[0]
})
const currentPlanFeatures = computed(() => {
  const features = tm(`user.plans.${currentPlanConfig.value.key}.features`)
  return Array.isArray(features) ? features : []
})

const planName = computed(() => userStore.plan)

const planLabel = computed(() => {
  if (!isPremium.value) return t("user.free_plan")

  return `${t(`user.plans.${planName.value}.name`)} ${t(`user.${billingInterval.value}`)}`
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

//load artists
const loadArtists = async (isReset = false) => {
  if (isReset) {
    page.value = 1
    hasMore.value = true
    artists.value = []
  }

  if (!hasMore.value || isLoadingMore.value) return

  if (page.value === 1) {
    isLoadingArtists.value = true
  }
  isLoadingMore.value = true

  try {
    const res = await axios.get('/user/v1/artists/all', {
      params: {
        page: page.value,
        limit: 20,
        search: searchQuery.value.trim()
      }
    })
    const newArtists = res.data?.data || []

    artists.value = [...artists.value, ...newArtists]

    if (newArtists.length < 20) {
      hasMore.value = false
    } else {
      page.value++
    }
  } catch (err) {
    console.error('Failed to load artists:', err)
    if (page.value === 1) {
      alert("Failed to load artists")
    }
  } finally {
    isLoadingArtists.value = false
    isLoadingMore.value = false
  }
}

const handleSearchInput = () => {
  if (searchDebounceTimer) clearTimeout(searchDebounceTimer)
  searchDebounceTimer = setTimeout(() => {
    loadArtists(true)
  }, 300)
}

const handleScroll = (e) => {
  const { scrollTop, clientHeight, scrollHeight } = e.target
  if (scrollHeight - (scrollTop + clientHeight) < 50) {
    loadArtists()
  }
}

const getArtistId = (artist) => {
  if (!artist) return null
  if (typeof artist === "string") return artist
  return artist.artist_objId || artist.artistId || artist.artist_id || artist._id || artist.id || null
}

const normalizeArtistId = (artistOrId) => {
  const id = typeof artistOrId === "object" ? getArtistId(artistOrId) : artistOrId
  return id == null ? null : String(id)
}

const isOwnCompanyArtist = (artist) => {
  const artistTenant = artist?.tenant_id || artist?.tenant
  return artistTenant != null && userStore.tenant != null && String(artistTenant) === String(userStore.tenant)
}

const initializeLockedArtist = (currentFollowedArtists) => {
  if (lockedArtistId.value || !currentFollowedArtists.length) return

  const ownCompanyArtist = currentFollowedArtists.find(isOwnCompanyArtist)
  lockedArtistId.value = normalizeArtistId(ownCompanyArtist || currentFollowedArtists[0])
}

const closeManageArtists = () => {
  showManageArtists.value = false
}

// open modal
const openManageArtists = async () => {
  showManageArtists.value = true
  searchQuery.value = ""

  const currentFollowedArtists = userStore.followedArtists || []
  const currentFollowedIds = currentFollowedArtists
    .map(normalizeArtistId)
    .filter(Boolean)

  editingArtists.value = [...currentFollowedIds]

  if (!lockedArtistId.value && currentFollowedArtists.length > 0) {
    initializeLockedArtist(currentFollowedArtists)
  }

  await loadArtists(true)
}

// 更新方案上限 (N + M <= Limit)
const artistLimit = computed(() => {
  if (!userStore.isPremium) return 1
  if (userStore.plan === "standard") return 20
  if (userStore.plan === "starter") return 5
  return 1
})


const hasOwnArtist = computed(() => {
  return editingArtists.value.includes(lockedArtistId.value)
})

// check if the modal is locked（free / starter plan limit）
const isSelected = (artistId) => {
  const normalizedId = normalizeArtistId(artistId)
  return normalizedId != null && editingArtists.value.includes(normalizedId)
}

const isOnboardArtist = (artistId) => {
  return lockedArtistId.value != null && normalizeArtistId(artistId) === lockedArtistId.value
}

// check Add / Remove buttons are disable
const isRemoveDisabled = (artistId) => {
  return isOnboardArtist(artistId)
}

const isAddDisabled = (artistId) => {
  if (isSelected(artistId)) return true
  return editingArtists.value.length >= artistLimit.value
}

const toggleArtist = (artistId) => {
  const normalizedId = normalizeArtistId(artistId)
  if (!normalizedId) return

  const isAlreadySelected = isSelected(normalizedId)

  if (isAlreadySelected) {
    // 需求 1 & 防呆：若是 Onboard 藝人，直接阻擋不予移除
    if (isOnboardArtist(artistId)) return

    // 移除藝人
    editingArtists.value = editingArtists.value.filter(id => id !== normalizedId)
  } else {
    // 需求 2 & 3: 已選過的不能再選 + 超出人數上限不能再選
    if (editingArtists.value.length >= artistLimit.value) return

    // 新增藝人
    editingArtists.value.push(normalizedId)
  }
}


const saveArtists = async () => {
  // 檢查 N >= 1
  if (userStore.isPremium && !hasOwnArtist.value) {
    alert("Must follow at least 1 artist from your own company")
    return
  }

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
          {{ $t('user.expires') }} {{ expiredDate }}
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
          {{ $t('user.upgrade_to_premium') }}
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
              {{ $t(`user.plans.${p.key}.name`) }}
            </h4>
            <p class="mt-1 text-sm text-gray-500">
              {{ $t(`user.plans.${p.key}.description`) }}
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
            <p class="font-medium text-gray-900">{{ $t('user.monthly') }}</p>
            <p class="text-xs text-gray-500 mt-1">{{ $t('user.billed_monthly') }}</p>
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
              {{ $t('user.save_more') }}
            </span>
            <p class="font-medium text-gray-900">{{ $t('user.yearly') }}</p>
            <p class="text-xs text-gray-500 mt-1">{{ $t('user.billed_yearly') }}</p>
          </button>
        </div>

        <!-- ===== Features ===== -->
        <ul class="text-sm text-gray-600 space-y-1 mb-6">
          <li v-for="f in currentPlanFeatures" :key="f">
            • {{ f }}
          </li>
        </ul>

        <!-- ===== CTA ===== -->
        <button
          @click="upgrade"
          class="w-full px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-md text-sm font-medium"
        >
          {{ $t('user.upgrade_now') }}
        </button>
      </template>

      <!-- ===== PREMIUM USER ===== -->
      <template v-else>
        <h3 class="text-lg font-semibold text-gray-900 mb-1">
          {{ $t('user.your_subscription') }}
        </h3>
        <p class="text-sm text-gray-600 mb-4">
          {{ planLabel }} · Active
        </p>
        <button
          @click="manageSubscription"
          class="px-4 py-2 border border-indigo-600 text-indigo-600 hover:bg-indigo-50 rounded-md text-sm font-medium"
        >
          {{ $t('user.manage_subscription') }}
        </button>
      </template>
    </div>

    <!-- ===== Followed Artists ===== -->
    <div class="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
      <h3 class="text-lg font-semibold text-gray-900">
        {{ $t('user.followed_artists') }}
        <span class="ml-2 text-sm text-gray-500">
          ({{ userStore.followedArtists.length }} / {{ artistLimit }})
        </span>
      </h3>

      <button
          @click="openManageArtists"
          class="px-4 py-2 border border-indigo-600 text-indigo-600 hover:bg-indigo-50 rounded-md text-sm font-medium"
      >
        {{ $t('user.manage') }}
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
        {{ $t('user.no_followed_artists') }}
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
            {{ $t('user.manage_artists') }}
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

          <!-- Search Input Bar -->
          <div class="relative">
            <input
                v-model="searchQuery"
                @input="handleSearchInput"
                type="text"
                placeholder="Search artists..."
                class="w-full pl-9 pr-4 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            />
            <span class="absolute left-3 top-2.5 text-gray-400">
              🔍
            </span>
          </div>

          <!-- loading spinner -->
          <div v-if="isLoadingArtists && page === 1" class="flex justify-center py-8">
            <div class="w-8 h-8 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin"></div>
          </div>

          <!-- Artist List -->
          <div
              v-else
              ref="scrollContainer"
              @scroll="handleScroll"
              class="space-y-2 max-h-72 overflow-y-auto pr-1"
          >
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
                  <div class="flex items-center gap-2">
                    <p class="font-medium text-gray-900">
                      {{ artist.artist_name }}
                    </p>
                    <span
                        v-if="isOwnCompanyArtist(artist)"
                        class="text-xs px-2 py-0.5 rounded bg-indigo-100 text-indigo-700 font-medium"
                    >
                      {{ $t('user.in_house') }}
                    </span>
                    <span v-else
                        class="text-xs px-2 py-0.5 rounded bg-gray-100 text-gray-600">
                      {{ $t('user.external') }}
                    </span>
                  </div>
                  <p class="text-sm text-gray-500">
                    {{ artist.korean_name }}
                  </p>
                </div>
              </div>

              <button
                  @click="toggleArtist(artist.artist_objId)"
                  :disabled="isSelected(artist.artist_objId) ? isRemoveDisabled(artist.artist_objId) : isAddDisabled(artist.artist_objId)"
                  class="text-sm font-medium px-3 py-1.5 rounded-md transition"
                  :class="{
                    // 1. Onboard 藝人：鎖定不可點擊
                    'bg-gray-100 text-gray-400 cursor-not-allowed': isOnboardArtist(artist.artist_objId),

                    // 2. 一般已選藝人：可點擊 Remove
                    'bg-red-100 text-red-600 hover:bg-red-200': isSelected(artist.artist_objId) && !isOnboardArtist(artist.artist_objId),

                    // 3. 未選藝人 且 未達上限：可點擊 Add
                    'bg-indigo-600 text-white hover:bg-indigo-700': !isSelected(artist.artist_objId) && editingArtists.length < artistLimit,

                    // 4. 未選藝人 但 已達上限：禁用不可點擊
                    'bg-gray-200 text-gray-400 cursor-not-allowed': !isSelected(artist.artist_objId) && editingArtists.length >= artistLimit
                  }"
              >
                <template v-if="isOnboardArtist(artist.artist_objId)">
                    {{ $t('user.locked') }}
                </template>
                <template v-else-if="isSelected(artist.artist_objId)">
                  {{ $t('user.remove') }}
                </template>
                <template v-else>
                  {{ $t('user.add') }}
                </template>
              </button>
            </div>
            <!-- search if no data -->
            <p v-if="artists.length === 0 && !isLoadingArtists" class="text-center text-sm text-gray-500 py-6">
              {{ $t('user.no_artists_found') }}
            </p>
            <!-- loading spinner -->
            <div v-if="isLoadingMore" class="flex justify-center py-3">
              <div class="w-5 h-5 border-2 border-indigo-600 border-t-transparent rounded-full animate-spin"></div>
            </div>

            <p v-if="!hasMore && artists.length > 0" class="text-center text-xs text-gray-400 py-2">
              {{ $t('user.no_more_artists') }}
            </p>

          </div>

          <!-- Limit Warning -->
          <div
              v-if="editingArtists.length >= artistLimit"
              class="text-sm text-red-600 bg-red-50 border border-red-200 rounded-md px-3 py-2"
          >
            {{ $t('user.artist_limit_reached', artistLimit, {count: artistLimit}) }}
          </div>
        </div>

        <!-- Footer -->
        <div class="px-6 py-4 border-t flex justify-end gap-3">
          <button
              @click="closeManageArtists"
              class="px-4 py-2 text-sm rounded-md border border-gray-300 hover:bg-gray-50"
          >
            {{ $t('user.cancel') }}
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
