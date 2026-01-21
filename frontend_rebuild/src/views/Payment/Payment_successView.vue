<script setup>
import { onMounted, ref } from "vue"
import { useUserStore } from "@/stores/user"
import { useRouter } from "vue-router"

const userStore = useUserStore()
const router = useRouter()

const loading = ref(true)

onMounted(async () => {
  await userStore.fetchMe()
  loading.value = false
})

</script>

<template>
  <div class="min-h-screen flex items-center justify-center px-4">
    <div class="bg-white border border-gray-200 rounded-lg p-8 max-w-md text-center">
      <template v-if="loading">
        <p class="text-gray-600">Finalizing your subscription…</p>
      </template>

      <template v-else>
        <div class="text-indigo-600 text-4xl mb-3">🎉</div>
        <h2 class="text-xl font-semibold text-gray-900 mb-2">
          Payment Successful
        </h2>
        <p class="text-sm text-gray-600 mb-6">
          Your Premium subscription is now active.
        </p>

        <button
            @click="router.push('/dashboard')"
            class="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-2 rounded-md text-sm"
        >
          Go to Dashboard
        </button>
      </template>
    </div>
  </div>
</template>

<style scoped>

</style>