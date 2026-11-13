import { ref } from 'vue'
import { fetchUsdRates } from '@/libs/currencyConversion.js'

/**
 * Today's USD exchange rates, fetched once per page visit and used as-is.
 * @returns {{ rates: import('vue').Ref<Record<string, number> | null>, updatedAt: import('vue').Ref<string | null>,
 *   status: import('vue').Ref<'idle' | 'loading' | 'ready' | 'error'>, load: () => Promise<boolean> }}
 */
export function useUsdRates() {
  const rates = ref(null)
  const updatedAt = ref(null)
  const status = ref('idle')

  const load = async () => {
    if (status.value === 'loading') return false
    if (status.value === 'ready') return true
    status.value = 'loading'
    try {
      const result = await fetchUsdRates()
      rates.value = result.rates
      updatedAt.value = result.updatedAt
      status.value = 'ready'
      return true
    } catch (error) {
      // The page still works in its original currency; the USD option shows as unavailable.
      console.warn(error.message)
      status.value = 'error'
      return false
    }
  }

  return { rates, updatedAt, status, load }
}
