<script setup>
import { useUserStore } from "@/stores/user.js";
import { computed } from "vue"

const userStore = useUserStore()
const defaultAvatar = "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-dist/user-circle-96.png"

const isPremium = computed(() => userStore.is_premium)

const planLabel = computed(() => {
  if (userStore.plan === "free") return "Free Plan"
  if (userStore.plan === "monthly") return "Premium Monthly"
  if (userStore.plan === "yearly") return "Premium Yearly"
  return "Premium"
})

const upgrade = async () => {
  const res = await fetch("/api/stripe/checkout-session", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${userStore.firebaseToken}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ plan: "monthly" })
  })
  const data = await res.json()
  window.location.href = data.checkout_url
}

const manageSubscription = async () => {
  const res = await fetch("/api/stripe/customer-portal")
  const data = await res.json()
  window.location.href = data.url
}

</script>


<template>
  <div class="max-w-3xl mx-auto px-4 py-8 space-y-6">

    <!-- ===== User Info ===== -->
    <div class="bg-white border border-gray-200 rounded-lg p-6 flex items-center gap-4">
      <div
          class="w-16 h-16 rounded-full bg-indigo-600 text-white flex items-center justify-center text-xl font-semibold"
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
      </div>
    </div>

    <!-- ===== Plan / Upgrade ===== -->
    <div
        class="border rounded-lg p-6"
        :class="isPremium ? 'bg-white border-gray-200' : 'bg-indigo-50 border-indigo-200'"
    >
      <template v-if="!isPremium">
        <h3 class="text-lg font-semibold text-gray-900 mb-2">
          Upgrade to Premium
        </h3>
        <ul class="text-sm text-gray-600 space-y-1 mb-4">
          <li>• Full Campaign analytics access</li>
          <li>• Historical data insights</li>
        </ul>
        <button
            @click="upgrade"
            class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-md text-sm font-medium"
        >
          Upgrade Now
        </button>
      </template>

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
    <div class="bg-white border border-gray-200 rounded-lg">
      <div class="px-6 py-4 border-b border-gray-200">
        <h3 class="text-lg font-semibold text-gray-900">
          Followed Artists
        </h3>
      </div>

      <ul class="divide-y">
        <li
            v-for="artist in (
            isPremium
              ? userStore.followedArtists
              : userStore.followedArtists.slice(0, 3)
          )"
            :key="artist.artist_id"
            class="px-6 py-4 flex items-center gap-4"
        >
          <img
              :src="artist.image"
              class="w-10 h-10 rounded-full object-cover"
          />

          <div>
            <p class="font-medium text-gray-900">
              {{ artist.english_name }}
            </p>
            <p class="text-sm text-gray-500">
              {{ artist.korean_name }}
            </p>
          </div>
        </li>

        <li
            v-if="!userStore.followedArtists || userStore.followedArtists.length === 0"
            class="px-6 py-4 text-sm text-gray-500"
        >
          No followed artists
        </li>
      </ul>
    </div>

  </div>
</template>

<style scoped>

</style>