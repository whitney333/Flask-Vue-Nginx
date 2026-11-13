<script setup>
import { computed } from 'vue'
import { ringDash } from '@/libs/shareReport.js'

const props = defineProps({
  percent: { type: Number, default: 0 },
})

const RADIUS = 52
const STROKE = 12
const SIZE = (RADIUS + STROKE / 2) * 2

const dash = computed(() => ringDash(props.percent, RADIUS))
</script>

<template>
  <div class="relative" :style="{ width: `${SIZE}px`, height: `${SIZE}px` }">
    <svg :width="SIZE" :height="SIZE" :viewBox="`0 0 ${SIZE} ${SIZE}`" class="-rotate-90" aria-hidden="true">
      <defs>
        <linearGradient id="share-ring-gradient" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#6366f1" />
          <stop offset="100%" stop-color="#a855f7" />
        </linearGradient>
      </defs>
      <circle :cx="SIZE / 2" :cy="SIZE / 2" :r="RADIUS" fill="none" stroke="#eef2ff" :stroke-width="STROKE" />
      <circle
          class="share-ring-arc"
          :cx="SIZE / 2" :cy="SIZE / 2" :r="RADIUS"
          fill="none"
          stroke="url(#share-ring-gradient)"
          :stroke-width="STROKE"
          stroke-linecap="round"
          :stroke-dasharray="dash.circumference"
          :stroke-dashoffset="dash.offset"
          :style="{ '--ring-from': dash.circumference }"
      />
    </svg>
    <span class="absolute inset-0 grid place-items-center text-2xl font-black tabular-nums tracking-tight">
      {{ Math.round(percent) }}%
    </span>
  </div>
</template>

<style scoped>
.share-ring-arc {
  animation: share-ring-draw 1s cubic-bezier(0.16, 1, 0.3, 1) both;
}
@keyframes share-ring-draw {
  from { stroke-dashoffset: var(--ring-from); }
}
@media (prefers-reduced-motion: reduce) {
  .share-ring-arc { animation: none; }
}
</style>
