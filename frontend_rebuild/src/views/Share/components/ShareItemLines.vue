<script setup>
import { computed } from 'vue'
import { formatMoney } from '@/libs/eventMetrics.js'
import { SERIES } from '../shareTheme.js'

const props = defineProps({
  // ticket_items of one type from the public report
  items: { type: Array, default: () => [] },
  // 'ticket' (indigo) or 'benefit' (amber)
  tone: { type: String, default: 'ticket' },
})

const count = (value) => (Number(value) || 0).toLocaleString('en-US')
// one decimal, matching the tile badges (e.g. 94.3%)
const rate = (item) => Math.round(Math.min(100, Math.max(0, Number(item.sell_through_rate) || 0)) * 10) / 10
const isSoldOut = (item) => rate(item) >= 100
const series = computed(() => SERIES[props.tone] || SERIES.ticket)
</script>

<template>
  <ul class="mt-4 space-y-4">
    <li v-for="(item, index) in items" :key="`${item.name}-${index}`">
      <div class="flex items-start justify-between gap-3">
        <div class="min-w-0">
          <p class="flex items-center gap-2">
            <span class="truncate font-semibold">{{ item.name }}</span>
            <span
                v-if="isSoldOut(item)"
                class="shrink-0 rounded-full bg-emerald-50 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide text-emerald-700 ring-1 ring-emerald-600/20"
            >Sold out</span>
          </p>
          <p class="text-xs text-slate-500">{{ formatMoney(item.price, item.currency) }} each</p>
        </div>
        <p class="shrink-0 text-right font-bold tabular-nums">{{ formatMoney(item.revenue, item.currency) }}</p>
      </div>
      <div
          class="mt-2 h-2 overflow-hidden rounded-full"
          :class="series.track"
          role="progressbar"
          :aria-valuenow="rate(item)"
          aria-valuemin="0"
          aria-valuemax="100"
          :aria-label="`${item.name} sold`"
      >
        <div
            class="share-grow h-full rounded-full"
            :class="series.fill"
            :style="{ width: `${rate(item)}%` }"
        ></div>
      </div>
      <p class="mt-1.5 flex justify-between text-xs text-slate-500 tabular-nums">
        <span>{{ count(item.net_sold) }} / {{ count(item.total_quantity) }} sold<template v-if="item.refund"> · {{ count(item.refund) }} refunded</template></span>
        <span class="font-semibold text-slate-700">{{ rate(item) }}%</span>
      </p>
    </li>
  </ul>
</template>
