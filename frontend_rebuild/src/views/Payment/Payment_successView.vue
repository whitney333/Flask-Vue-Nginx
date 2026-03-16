<script setup>
import { onMounted, ref } from "vue"
import { useUserStore } from "@/stores/user"
import { useRouter } from "vue-router"

const userStore = useUserStore()
const router = useRouter()

const loading = ref(true)
const retryCount = ref(0)
const MAX_RETRY = 10
const isPremium = computed(() => userStore.isPremium)

const pollUserStatus = async () => {
  await userStore.fetchMe()

  if (isPremium) {
    router.replace("/profile")
    return
  }

  retryCount.value++

  if (retryCount.value >= MAX_RETRY) {
    loading.value = false
    return
  }

  setTimeout(pollUserStatus, 1000)
}

onMounted(() => {
  pollUserStatus()
})

</script>

<template>
  <div class="min-h-screen flex items-center justify-center px-4">
    <div class="bg-white border rounded-lg p-8 max-w-md text-center">
      <template v-if="loading">
        <p class="text-gray-600 mb-3">
          Finalizing your subscription…
        </p>
        <p class="text-xs text-gray-400">
          This may take a few seconds
        </p>
      </template>

      <template v-else>
        <h2 class="text-lg font-semibold text-gray-900 mb-2">
          Subscription processing
        </h2>
        <p class="text-sm text-gray-600 mb-4">
          Your payment was successful, but activation is still in progress.
        </p>
        <button
            @click="pollUserStatus"
            class="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-2 rounded-md text-sm"
        >
          Refresh Status
        </button>
      </template>
    </div>
  </div>
</template>

<style scoped>

</style>