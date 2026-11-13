/**
 * Derived figures for the public artist share page (bento layout).
 * Pure functions: no Vue, no I/O, inputs are never mutated.
 */

const GENDERS = Object.freeze([
  { key: 'female', label: 'Female' },
  { key: 'male', label: 'Male' },
  { key: 'other', label: 'Other' },
  { key: 'unknown', label: 'Unknown' },
])

const AGE_BUCKETS = Object.freeze([
  { key: 'age_10s', label: '10s' },
  { key: 'age_20s', label: '20s' },
  { key: 'age_30s', label: '30s' },
  { key: 'age_40s', label: '40s' },
  { key: 'age_50_plus', label: '50+' },
])

const toNumber = (value) => Number(value) || 0
const sum = (values) => values.reduce((acc, value) => acc + value, 0)
const roundTo1 = (value) => Math.round(value * 10) / 10

/**
 * @param {number} ticketRevenue @param {number} benefitRevenue
 * @returns {{ ticketPct: number, benefitPct: number }} whole-number shares summing to 100
 */
export function revenueSplit(ticketRevenue, benefitRevenue) {
  const total = toNumber(ticketRevenue) + toNumber(benefitRevenue)
  if (total <= 0) return { ticketPct: 0, benefitPct: 0 }
  const ticketPct = Math.round((toNumber(ticketRevenue) / total) * 100)
  return { ticketPct, benefitPct: 100 - ticketPct }
}

/**
 * @param {Array<{ net_sold?: number, total_quantity?: number }>} items
 * @returns {{ sold: number, total: number, percent: number }}
 */
export function overallSold(items = []) {
  const sold = sum(items.map((item) => toNumber(item.net_sold)))
  const total = sum(items.map((item) => toNumber(item.total_quantity)))
  return { sold, total, percent: total > 0 ? roundTo1((sold / total) * 100) : 0 }
}

/**
 * @param {Array<{ name?: string, revenue?: number }>} items
 * @returns {{ name: string, revenue: number, share: number } | null}
 */
export function topEarner(items = []) {
  const total = sum(items.map((item) => toNumber(item.revenue)))
  if (total <= 0) return null
  const best = items.reduce((top, item) => (toNumber(item.revenue) > toNumber(top.revenue) ? item : top))
  const revenue = toNumber(best.revenue)
  return { name: best.name || '', revenue, share: Math.round((revenue / total) * 100) }
}

/** @param {Array<{ type?: string }>} items @param {string} type */
export function itemsOfType(items = [], type) {
  return items.filter((item) => item.type === type)
}

/**
 * @param {{ gender_distribution?: Record<string, number> } | null | undefined} snapshot
 * @returns {Array<{ key: string, label: string, value: number }>} non-zero entries, largest first
 */
export function genderBreakdown(snapshot) {
  const data = snapshot?.gender_distribution || {}
  return GENDERS
    .map(({ key, label }) => ({ key, label, value: toNumber(data[key]) }))
    .filter((entry) => entry.value > 0)
    .sort((a, b) => b.value - a.value)
}

/**
 * @param {{ age_distribution?: Record<string, number> } | null | undefined} snapshot
 * @returns {Array<{ label: string, value: number, isPeak: boolean }>} all buckets in order, or [] if no data
 */
export function ageBreakdown(snapshot) {
  const data = snapshot?.age_distribution || {}
  const values = AGE_BUCKETS.map(({ key }) => toNumber(data[key]))
  const peak = Math.max(...values)
  if (peak <= 0) return []
  const peakIndex = values.indexOf(peak)
  return AGE_BUCKETS.map(({ label }, index) => ({ label, value: values[index], isPeak: index === peakIndex }))
}

/**
 * SVG stroke geometry for a progress ring.
 * @param {number} percent 0-100 (clamped) @param {number} radius circle radius
 * @returns {{ circumference: number, offset: number }} use as stroke-dasharray / stroke-dashoffset
 */
export function ringDash(percent, radius) {
  const circumference = 2 * Math.PI * radius
  const clamped = Math.min(100, Math.max(0, toNumber(percent)))
  return { circumference, offset: circumference * (1 - clamped / 100) }
}

/**
 * Value shown by a count-up animation at a given progress (ease-out cubic).
 * @param {number} target final value @param {number} progress 0-1 (clamped)
 * @returns {number} whole number between 0 and target
 */
export function countUpValue(target, progress) {
  const t = Math.min(1, Math.max(0, toNumber(progress)))
  const eased = 1 - (1 - t) ** 3
  return t >= 1 ? toNumber(target) : Math.round(toNumber(target) * eased)
}

/** @param {string | undefined} name @returns {string} up to two initials, or '?' */
export function initialsOf(name) {
  const words = String(name || '').trim().split(/\s+/).filter(Boolean)
  if (!words.length) return '?'
  return words.slice(0, 2).map((word) => word[0].toUpperCase()).join('')
}

/**
 * Position of a value on a light-to-dark colour scale, relative to the largest value.
 * @param {number} value @param {number} max @param {number} steps number of shades
 * @returns {number} 0 (lightest) to steps - 1 (darkest)
 */
export function shadeIndex(value, max, steps) {
  if (toNumber(max) <= 0 || steps <= 1) return 0
  const ratio = Math.min(1, Math.max(0, toNumber(value) / toNumber(max)))
  return Math.round(ratio * (steps - 1))
}

const FILE_NAME_UNSAFE = /[\\/:*?"<>|]/g

/** @param {string | undefined} eventName @returns {string} page title used as the PDF file name */
export function reportFileTitle(eventName) {
  const clean = String(eventName || '').replace(FILE_NAME_UNSAFE, '').replace(/\s+/g, ' ').trim()
  return `${clean || 'Event'} - Sales Report`
}
