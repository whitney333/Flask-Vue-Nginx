<script setup>
import { useUserStore } from "@/stores/user.js";
import { computed, ref, onMounted } from "vue"
import { getAuth } from "firebase/auth"
import { useAuthStore } from "@/stores/auth.js";

const userStore = useUserStore()
const authStore = useAuthStore()
const defaultAvatar = "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-dist/user-circle-96.png"

const isPremium = computed(() => userStore.isPremium)
const selectedPlan = ref("monthly")
const planLabel = computed(() => {
  if (userStore.plan === "free") return "Free Plan"
  if (userStore.plan === "monthly") return "Premium Monthly"
  if (userStore.plan === "yearly") return "Premium Yearly"
  return "Premium"
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

  const idToken = await user.getIdToken(true)

  const res = await fetch("/api/stripe/checkout-session", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${idToken}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({plan: selectedPlan.value})
  })
  const data = await res.json()
  if (data.checkout_url) {
    window.location.href = data.checkout_url
  } else {
    alert("Failed to open Stripe checkout")
  }
}

const manageSubscription = async () => {
  const res = await fetch("/api/stripe/customer-portal", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${authStore.idToken}`,
      "Content-Type": "application/json"
    }
  })

  if (!res.ok) {
    console.error(await res.text())
    alert("Failed to open portal")
    return
  }

  const data = await res.json()
  window.location.href = data.url
}

onMounted(async () => {
  await userStore.fetchMe()
})
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
        <span
            v-if="isPremium && expiredDate"
            class="text-sm text-gray-500"
        >
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

        <!-- Plan selector -->
        <div class="grid grid-cols-2 gap-4 mb-6">
          <!-- Monthly -->
          <button
              @click="selectedPlan = 'monthly'"
              :class="selectedPlan === 'monthly'
          ? 'border-indigo-600 bg-white ring-2 ring-indigo-600'
          : 'border-gray-300 bg-white hover:border-gray-400'"
              class="border rounded-lg p-4 text-left transition"
          >
            <p class="text-sm font-medium text-gray-900">Monthly</p>
            <p class="mt-1 text-2xl font-semibold text-gray-900">$10</p>
            <p class="text-xs text-gray-500 mt-1">Billed monthly</p>
          </button>

          <!-- Yearly -->
          <button
              @click="selectedPlan = 'yearly'"
              :class="selectedPlan === 'yearly'
          ? 'border-indigo-600 bg-white ring-2 ring-indigo-600'
          : 'border-gray-300 bg-white hover:border-gray-400'"
              class="border rounded-lg p-4 text-left relative transition"
          >
        <span
            class="absolute top-2 right-2 text-xs bg-indigo-600 text-white px-2 py-0.5 rounded-full"
        >
          Save 8%
        </span>
            <p class="text-sm font-medium text-gray-900">Yearly</p>
            <p class="mt-1 text-2xl font-semibold text-gray-900">$110</p>
            <p class="text-xs text-gray-500 mt-1">Billed yearly</p>
          </button>
        </div>

        <!-- Features -->
        <ul class="text-sm text-gray-600 space-y-1 mb-6">
          <li>• Full campaign analytics</li>
          <li>• Historical data access</li>
          <li>• Unlimited artist tracking</li>
        </ul>

        <!-- CTA -->
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
            :key="artist.id"
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