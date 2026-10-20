<script setup>
defineProps({
  metrics: {
    type: Object,
    required: true,
    default: () => ({
      ticketRevenue: 0,
      benefitRevenue: 0,
      totalRevenue: 0,
      ticketSellThrough: 0,
      benefitSellThrough: 0
    })
  }
});

// 數字千分位格式化
const formatNumber = (val) => {
  if (val === null || val === undefined || isNaN(val)) return "0";
  return Number(val).toLocaleString("en-US");
};
</script>

<template>
  <div class="bg-white rounded-xl shadow p-6 border border-gray-200">
    <h3 class="text-lg font-semibold text-gray-800 mb-4 pb-3 border-b border-gray-100">Event Summary</h3>

    <!-- 1 row 3 cards (grid-cols-1 sm:grid-cols-2 lg:grid-cols-3) -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">

      <!-- Card 1: Ticket Sales Revenue -->
      <div class="p-4 rounded-xl bg-gray-50 border border-gray-200 flex items-center gap-4">
        <!-- Icon: 淡灰底 + 黑色 -->
        <div class="p-3 bg-gray-100 text-black rounded-lg flex-shrink-0">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z" />
          </svg>
        </div>
        <div class="min-w-0">
          <!-- Title: text-sm (14px) -->
          <p class="text-sm font-medium text-gray-500 truncate">Ticket Sales Revenue</p>
          <!-- Metric Number: text-xl (20px) 或 text-2xl (24px) -->
          <p class="text-xl sm:text-2xl font-bold text-gray-900 mt-1 truncate">{{ formatNumber(metrics.ticketRevenue) }}</p>
        </div>
      </div>

      <!-- Card 2: Benefit Sales Revenue -->
      <div class="p-4 rounded-xl bg-gray-50 border border-gray-200 flex items-center gap-4">
        <div class="p-3 bg-gray-100 text-black rounded-lg flex-shrink-0">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
          </svg>
        </div>
        <div class="min-w-0">
          <p class="text-sm font-medium text-gray-500 truncate">Benefit Sales Revenue</p>
          <p class="text-xl sm:text-2xl font-bold text-gray-900 mt-1 truncate">{{ formatNumber(metrics.benefitRevenue) }}</p>
        </div>
      </div>

      <!-- Card 3: Total Sales Revenue -->
      <div class="p-4 rounded-xl bg-gray-50 border border-gray-200 flex items-center gap-4">
        <div class="p-3 bg-gray-100 text-black rounded-lg flex-shrink-0">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div class="min-w-0">
          <p class="text-sm font-medium text-gray-500 truncate">Total Sales Revenue</p>
          <p class="text-xl sm:text-2xl font-bold text-gray-900 mt-1 truncate">{{ formatNumber(metrics.totalRevenue) }}</p>
        </div>
      </div>

      <!-- Card 4: Ticket Sell-Through Rate -->
      <div class="p-4 rounded-xl bg-gray-50 border border-gray-200 flex items-center gap-4">
        <div class="p-3 bg-gray-100 text-black rounded-lg flex-shrink-0">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        </div>
        <div class="min-w-0">
          <p class="text-sm font-medium text-gray-500 truncate">Ticket Sell-Through</p>
          <p class="text-xl sm:text-2xl font-bold text-gray-900 mt-1 truncate">{{ metrics.ticketSellThrough }}%</p>
        </div>
      </div>

      <!-- Card 5: Benefit Sell-Through Rate -->
      <div class="p-4 rounded-xl bg-gray-50 border border-gray-200 flex items-center gap-4">
        <div class="p-3 bg-gray-100 text-black rounded-lg flex-shrink-0">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
          </svg>
        </div>
        <div class="min-w-0">
          <p class="text-sm font-medium text-gray-500 truncate">Benefit Sell-Through</p>
          <p class="text-xl sm:text-2xl font-bold text-gray-900 mt-1 truncate">{{ metrics.benefitSellThrough }}%</p>
        </div>
      </div>

    </div>
  </div>
</template>
