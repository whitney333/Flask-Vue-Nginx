/**
 * Offline event sales metrics, shared by the admin event page and the public share page.
 * Pure functions: no Vue, no I/O, inputs are never mutated.
 */

const MS_PER_HOUR = 1000 * 60 * 60

/**
 * @typedef {{ type?: string, price?: number, total_quantity?: number, sold?: number, refund?: number, currency?: string }} TicketItem
 * @typedef {{ id?: string, observed_at?: string, ticket_items?: TicketItem[] }} Snapshot
 */

const EMPTY_METRICS = Object.freeze({
  ticketRevenue: 0,
  benefitRevenue: 0,
  totalRevenue: 0,
  ticketSellThrough: 0,
  benefitSellThrough: 0,
  salesVelocity: '0.0 / hr',
  ticketRemaining: 0,
  benefitRemaining: 0,
  ticketRefundRate: 0,
  benefitRefundRate: 0,
})

const EMPTY_TOTALS = Object.freeze({ revenue: 0, totalQty: 0, netSold: 0, sold: 0, refund: 0 })

const toNumber = (value) => Number(value) || 0

const percent = (part, whole) => (whole > 0 ? Number(((part / whole) * 100).toFixed(2)) : 0)

/** @param {TicketItem} item */
const netSoldOf = (item) => Math.max(0, toNumber(item.sold) - toNumber(item.refund))

/** @param {TicketItem[]} items @param {string} type */
const totalsFor = (items, type) =>
  items
    .filter((item) => item.type === type)
    .reduce((acc, item) => {
      const netSold = netSoldOf(item)
      return {
        revenue: acc.revenue + netSold * toNumber(item.price),
        totalQty: acc.totalQty + toNumber(item.total_quantity),
        netSold: acc.netSold + netSold,
        sold: acc.sold + toNumber(item.sold),
        refund: acc.refund + toNumber(item.refund),
      }
    }, EMPTY_TOTALS)

/** @param {Snapshot} snapshot @param {Snapshot[]} snapshots @param {number} currentNetSold */
const salesVelocity = (snapshot, snapshots, currentNetSold) => {
  const sorted = [...snapshots].sort((a, b) => new Date(a.observed_at) - new Date(b.observed_at))
  const index = sorted.findIndex((s) => s.id === snapshot.id)
  if (index <= 0) return EMPTY_METRICS.salesVelocity

  const previous = sorted[index - 1]
  const elapsedMs = new Date(snapshot.observed_at) - new Date(previous.observed_at)
  const hours = elapsedMs > 0 ? elapsedMs / MS_PER_HOUR : 1
  const previousNetSold = (previous.ticket_items || []).reduce((sum, item) => sum + netSoldOf(item), 0)
  const perHour = (currentNetSold - previousNetSold) / hours

  return `${perHour >= 0 ? '+' : ''}${perHour.toFixed(1)} / hr`
}

/**
 * @param {Snapshot | null} snapshot  the snapshot being viewed
 * @param {Snapshot[]} snapshots      all snapshots of the event (for sales velocity)
 */
export function computeEventSummaryMetrics(snapshot, snapshots = []) {
  if (!snapshot || !Array.isArray(snapshot.ticket_items)) return { ...EMPTY_METRICS }

  const ticket = totalsFor(snapshot.ticket_items, 'ticket')
  const benefit = totalsFor(snapshot.ticket_items, 'benefit')

  return {
    ticketRevenue: ticket.revenue,
    benefitRevenue: benefit.revenue,
    totalRevenue: ticket.revenue + benefit.revenue,
    ticketSellThrough: percent(ticket.netSold, ticket.totalQty),
    benefitSellThrough: percent(benefit.netSold, benefit.totalQty),
    salesVelocity: salesVelocity(snapshot, snapshots || [], ticket.netSold + benefit.netSold),
    ticketRemaining: Math.max(0, ticket.totalQty - ticket.netSold),
    benefitRemaining: Math.max(0, benefit.totalQty - benefit.netSold),
    ticketRefundRate: percent(ticket.refund, ticket.sold),
    benefitRefundRate: percent(benefit.refund, benefit.sold),
  }
}

/**
 * 'symbol' (not 'narrowSymbol') keeps dollar currencies apart: HKD -> HK$, TWD -> NT$, USD -> $.
 * @param {string | undefined} code ISO 4217 code
 * @param {number} [fractionDigits] fixed decimals; omit for the currency default
 * @returns {Intl.NumberFormat | null}
 */
const currencyFormatter = (code, fractionDigits) => {
  if (!code) return null
  try {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: code,
      currencyDisplay: 'symbol',
      ...(fractionDigits === undefined
        ? {}
        : { minimumFractionDigits: fractionDigits, maximumFractionDigits: fractionDigits }),
    })
  } catch {
    return null
  }
}

/** @param {string | undefined} code @returns {string} e.g. 'JPY' -> '¥', 'HKD' -> 'HK$', unknown -> '' */
export function currencySymbol(code) {
  const formatter = currencyFormatter(code)
  if (!formatter) return ''
  return formatter.formatToParts(0).find((part) => part.type === 'currency')?.value || ''
}

/**
 * Whole amounts drop the decimals ('HK$358,000'); amounts with cents keep them ('$45,893.22').
 * @param {number} value @param {string | undefined} code
 * @returns {string}
 */
export function formatMoney(value, code) {
  const amount = toNumber(value)
  const formatter = currencyFormatter(code, Number.isInteger(amount) ? 0 : undefined)
  return formatter ? formatter.format(amount) : amount.toLocaleString('en-US')
}

/** @param {Snapshot | null} snapshot @returns {string} the snapshot's currency code, or '' */
export function snapshotCurrency(snapshot) {
  return snapshot?.ticket_items?.find((item) => item.currency)?.currency || ''
}
