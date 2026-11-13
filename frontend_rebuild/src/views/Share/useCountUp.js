import { onBeforeUnmount, ref, watch } from 'vue'
import { countUpValue } from '@/libs/shareReport.js'

const DEFAULT_DURATION_MS = 900

const prefersReducedMotion = () =>
  typeof window !== 'undefined' && window.matchMedia?.('(prefers-reduced-motion: reduce)').matches

/**
 * Animates a number from 0 up to the source value whenever the source changes.
 * Jumps straight to the value when the viewer prefers reduced motion.
 * @param {import('vue').Ref<number>} source
 * @param {number} [durationMs]
 * @returns {import('vue').Ref<number>}
 */
export function useCountUp(source, durationMs = DEFAULT_DURATION_MS) {
  const display = ref(0)
  let frame = 0

  const run = (target) => {
    cancelAnimationFrame(frame)
    if (prefersReducedMotion() || !target) {
      display.value = Number(target) || 0
      return
    }
    const start = performance.now()
    const step = (now) => {
      const progress = (now - start) / durationMs
      display.value = countUpValue(target, progress)
      if (progress < 1) frame = requestAnimationFrame(step)
    }
    frame = requestAnimationFrame(step)
  }

  watch(source, run, { immediate: true })
  onBeforeUnmount(() => cancelAnimationFrame(frame))

  return display
}
