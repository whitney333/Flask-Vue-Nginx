<script setup>

</script>

<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-50 p-4">
    <div class="relative text-8xl mb-6 animate-bounce-slow">
      🚀
    </div>
    <h1 class="text-5xl font-bold tracking-widest">COMING SOON</h1>
    <!-- Title -->
<!--    <h1 class="text-4xl font-bold mb-4 text-gray-800 text-center">Coming Soon</h1>-->

    <!-- Subtitle -->
    <p class="mt-3 text-gray-400 text-lg">
      This feature is under development. Stay tuned for updates!
    </p>
    <p class="mt-3 text-gray-400 text-lg">
      We’re launching something exciting!
    </p>
    <!-- Optional button to go back -->
    <router-link
        to="/dashboard"
        class="mt-3 px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition"
    >
      Back to Dashboard
    </router-link>
  </div>
</template>

<style scoped>
@keyframes bounce-slow {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}
.animate-bounce-slow {
  animation: bounce-slow 2s infinite ease-in-out;
}
</style>