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
      benefitSellThrough: 0,
      salesVelocity: '0.0 / hr',
      ticketRemaining: 0,
      benefitRemaining: 0,
      ticketRefundRate: 0,
      benefitRefundRate: 0
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
  <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between border-b border-gray-100 pb-4">
      <div>
        <h3 class="text-lg font-bold text-gray-900 tracking-tight">Event Summary</h3>
        <p class="text-xs text-gray-400 mt-0.5">Real-time overview based on selected snapshot</p>
      </div>
      <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-100">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
        Active Snapshot
      </span>
    </div>

    <!-- 1. Hero KPI Section (三大核心亮點卡片) -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">

      <!-- Total Revenue (主卡片) -->
      <div class="p-5 rounded-xl bg-gray-900 text-white shadow-sm flex flex-col justify-between relative overflow-hidden group">
        <div class="absolute -right-4 -bottom-4 w-24 h-24 bg-white/5 rounded-full blur-2xl group-hover:bg-white/10 transition"></div>
        <div class="flex items-center justify-between">
          <span class="text-xs font-medium text-gray-400 uppercase tracking-wider">Total Revenue</span>
          <div class="p-2 bg-white/10 rounded-lg text-white">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        </div>
        <div class="mt-4">
          <div class="text-2xl sm:text-3xl font-extrabold tracking-tight text-white">
            {{ formatNumber(metrics.totalRevenue) }}
          </div>
          <span class="text-[11px] text-gray-400 mt-1 block">Ticket + Benefit Net Revenue</span>
        </div>
      </div>

      <!-- Ticket Sell-Through -->
      <div class="p-5 rounded-xl bg-gray-50 border border-gray-100 flex flex-col justify-between hover:border-gray-200 transition">
        <div class="flex items-center justify-between">
          <span class="text-xs font-medium text-gray-500 uppercase tracking-wider">Ticket Sell-Through</span>
          <div class="p-2 bg-white rounded-lg text-gray-700 shadow-sm border border-gray-100">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
        </div>
        <div class="mt-4">
          <div class="text-2xl sm:text-3xl font-bold text-gray-900 tracking-tight">
            {{ metrics.ticketSellThrough }}<span class="text-lg font-normal text-gray-400 ml-0.5">%</span>
          </div>
          <!-- 進度條 -->
          <div class="w-full bg-gray-200 h-1.5 rounded-full mt-2.5 overflow-hidden">
            <div class="bg-gray-900 h-full rounded-full transition-all duration-500" :style="{ width: `${Math.min(100, metrics.ticketSellThrough)}%` }"></div>
          </div>
        </div>
      </div>

      <!-- Sales Velocity -->
      <div class="p-5 rounded-xl bg-gray-50 border border-gray-100 flex flex-col justify-between hover:border-gray-200 transition">
        <div class="flex items-center justify-between">
          <span class="text-xs font-medium text-gray-500 uppercase tracking-wider">Sales Velocity</span>
          <div class="p-2 bg-white rounded-lg text-gray-700 shadow-sm border border-gray-100">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
        </div>
        <div class="mt-4">
          <div class="text-2xl sm:text-3xl font-bold text-gray-900 tracking-tight">
            {{ metrics.salesVelocity }}
          </div>
          <span class="text-[11px] text-gray-400 mt-1 block">Net sold difference per hour</span>
        </div>
      </div>

    </div>

    <!-- 2. Breakdown Grid Section (細項拆解 2x3 或 3x2 排版) -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 pt-2">

      <!-- Ticket Revenue -->
      <div class="p-4 rounded-xl border border-gray-100 bg-white hover:shadow-sm transition flex items-center justify-between">
        <div>
          <span class="text-xs font-medium text-gray-400 block mb-1">Ticket Revenue</span>
          <span class="text-lg font-bold text-gray-800">{{ formatNumber(metrics.ticketRevenue) }}</span>
        </div>
        <span class="px-2 py-1 bg-gray-100 text-gray-600 text-[10px] font-semibold rounded-md">Ticket</span>
      </div>

      <!-- Benefit Revenue -->
      <div class="p-4 rounded-xl border border-gray-100 bg-white hover:shadow-sm transition flex items-center justify-between">
        <div>
          <span class="text-xs font-medium text-gray-400 block mb-1">Benefit Revenue</span>
          <span class="text-lg font-bold text-gray-800">{{ formatNumber(metrics.benefitRevenue) }}</span>
        </div>
        <span class="px-2 py-1 bg-gray-100 text-gray-600 text-[10px] font-semibold rounded-md">Benefit</span>
      </div>

      <!-- Benefit Sell-Through -->
      <div class="p-4 rounded-xl border border-gray-100 bg-white hover:shadow-sm transition flex items-center justify-between">
        <div>
          <span class="text-xs font-medium text-gray-400 block mb-1">Benefit Sell-Through</span>
          <span class="text-lg font-bold text-gray-800">{{ metrics.benefitSellThrough }}%</span>
        </div>
        <span class="px-2 py-1 bg-gray-100 text-gray-600 text-[10px] font-semibold rounded-md">Rate</span>
      </div>

      <!-- Remaining Tickets -->
      <div class="p-4 rounded-xl border border-gray-100 bg-white hover:shadow-sm transition flex items-center justify-between">
        <div>
          <span class="text-xs font-medium text-gray-400 block mb-1">Remaining Tickets</span>
          <span class="text-lg font-bold text-gray-800">{{ formatNumber(metrics.ticketRemaining) }}</span>
        </div>
        <span class="px-2 py-1 bg-amber-50 text-amber-700 border border-amber-100 text-[10px] font-semibold rounded-md">Inventory</span>
      </div>

      <!-- Remaining Benefits -->
      <div class="p-4 rounded-xl border border-gray-100 bg-white hover:shadow-sm transition flex items-center justify-between">
        <div>
          <span class="text-xs font-medium text-gray-400 block mb-1">Remaining Benefits</span>
          <span class="text-lg font-bold text-gray-800">{{ formatNumber(metrics.benefitRemaining) }}</span>
        </div>
        <span class="px-2 py-1 bg-amber-50 text-amber-700 border border-amber-100 text-[10px] font-semibold rounded-md">Inventory</span>
      </div>

      <!-- Refund Rates (合併或呈現退款狀況) -->
      <div class="p-4 rounded-xl border border-gray-100 bg-white hover:shadow-sm transition flex items-center justify-between">
        <div>
          <span class="text-xs font-medium text-gray-400 block mb-1">Refund Rates (Ticket / Benefit)</span>
          <div class="flex items-center gap-2">
            <span class="text-base font-bold text-gray-800">{{ metrics.ticketRefundRate }}%</span>
            <span class="text-gray-300">/</span>
            <span class="text-base font-bold text-gray-800">{{ metrics.benefitRefundRate }}%</span>
          </div>
        </div>
        <span class="px-2 py-1 bg-rose-50 text-rose-600 border border-rose-100 text-[10px] font-semibold rounded-md">Refund</span>
      </div>

    </div>
  </div>
</template>
