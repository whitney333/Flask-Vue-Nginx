/**
 * Live USD conversion for the public share page.
 * Rates: ExchangeRate-API open access (no key, daily updates, attribution required).
 * Pure helpers plus one fetch with an injectable fetch implementation; inputs are never mutated.
 */

export const RATES_URL = 'https://open.er-api.com/v6/latest/USD'
export const RATES_ATTRIBUTION_URL = 'https://www.exchangerate-api.com'

const FETCH_TIMEOUT_MS = 8000
// Trims floating-point noise (e.g. 200.00000000000003) while keeping sub-cent precision.
const PRECISION = 1e6
const RATE_DECIMALS = 2

const isPositiveNumber = (value) => typeof value === 'number' && Number.isFinite(value) && value > 0

/**
 * @param {unknown} payload raw API response
 * @returns {{ rates: Record<string, number>, updatedAt: string | null } | null} units of each currency per 1 USD
 */
export function parseUsdRates(payload) {
  if (!payload || payload.result !== 'success' || payload.base_code !== 'USD') return null
  if (!payload.rates || typeof payload.rates !== 'object') return null

  const rates = Object.fromEntries(
    Object.entries(payload.rates).filter(([, value]) => isPositiveNumber(value))
  )
  const updated = new Date(payload.time_last_update_utc)
  return { rates, updatedAt: Number.isNaN(updated.getTime()) ? null : updated.toISOString() }
}

/** @param {number} amount @param {string} currency @param {Record<string, number> | null} rates @returns {number | null} */
export function toUsd(amount, currency, rates) {
  if (currency === 'USD') return Number(amount) || 0
  const rate = rates?.[currency]
  if (!isPositiveNumber(rate)) return null
  return Math.round(((Number(amount) || 0) / rate) * PRECISION) / PRECISION
}

/** @param {Array<{ ticket_items?: Array<{ currency?: string }> }>} snapshots @param {Record<string, number> | null} rates */
export function canConvertToUsd(snapshots, rates) {
  if (!rates) return false
  return snapshots.every((snapshot) =>
    (snapshot.ticket_items || []).every((item) => toUsd(0, item.currency, rates) !== null)
  )
}

/**
 * @template {{ ticket_items?: Array<object> }} S
 * @param {S} snapshot @param {Record<string, number>} rates
 * @returns {S} a copy whose item prices and revenue are in USD
 */
export function convertSnapshotToUsd(snapshot, rates) {
  return {
    ...snapshot,
    ticket_items: (snapshot.ticket_items || []).map((item) => ({
      ...item,
      price: toUsd(item.price, item.currency, rates),
      revenue: toUsd(item.revenue, item.currency, rates),
      currency: 'USD',
    })),
  }
}

/** @param {string} currency @param {Record<string, number> | null} rates @returns {string} e.g. '1 USD = 7.84 HKD' */
export function rateLabel(currency, rates) {
  const rate = rates?.[currency]
  return isPositiveNumber(rate) ? `1 USD = ${rate.toFixed(RATE_DECIMALS)} ${currency}` : ''
}

/**
 * @param {typeof fetch} [fetchImpl]
 * @returns {Promise<{ rates: Record<string, number>, updatedAt: string | null }>}
 */
export async function fetchUsdRates(fetchImpl = globalThis.fetch) {
  const controller = typeof AbortController === 'undefined' ? null : new AbortController()
  const timer = controller ? setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS) : null
  try {
    const response = await fetchImpl(RATES_URL, controller ? { signal: controller.signal } : undefined)
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    const parsed = parseUsdRates(await response.json())
    if (!parsed) throw new Error('Unexpected response')
    return parsed
  } catch (error) {
    throw new Error(`Could not load today's exchange rate (${error.message})`)
  } finally {
    if (timer) clearTimeout(timer)
  }
}
