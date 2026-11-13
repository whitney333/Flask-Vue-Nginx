<script setup>
defineProps({
  // 'original' | 'usd'
  modelValue: { type: String, default: 'original' },
  // e.g. 'HKD'; empty when the event mixes currencies
  originalCode: { type: String, default: '' },
  // 'idle' | 'loading' | 'ready' | 'error'
  ratesStatus: { type: String, default: 'idle' },
  // false when some item currency has no exchange rate
  canConvert: { type: Boolean, default: true },
})
const emit = defineEmits(['update:modelValue', 'retry'])

const OPTION =
  'rounded-full px-3.5 py-1.5 text-sm font-semibold transition focus-visible:outline focus-visible:outline-2 focus-visible:outline-indigo-600 disabled:cursor-not-allowed disabled:opacity-50'
const ACTIVE = 'bg-slate-900 text-white shadow-sm'
const IDLE = 'text-slate-600 hover:bg-white hover:text-slate-900'
</script>

<template>
  <div class="flex items-center gap-2">
    <div class="flex rounded-full bg-white/70 p-1 ring-1 ring-indigo-950/5 backdrop-blur-xl" role="group" aria-label="Currency">
      <button
          type="button"
          :class="[OPTION, modelValue === 'original' ? ACTIVE : IDLE]"
          :aria-pressed="modelValue === 'original'"
          @click="emit('update:modelValue', 'original')"
      >{{ originalCode || 'Original' }}</button>
      <button
          type="button"
          :class="[OPTION, modelValue === 'usd' ? ACTIVE : IDLE]"
          :aria-pressed="modelValue === 'usd'"
          :disabled="ratesStatus === 'loading' || (ratesStatus === 'ready' && !canConvert)"
          :title="ratesStatus === 'ready' && !canConvert ? 'No exchange rate for this currency' : 'Show amounts in US dollars'"
          @click="ratesStatus === 'error' ? emit('retry') : emit('update:modelValue', 'usd')"
      >USD</button>
    </div>
  </div>
</template>
