// Run with: npm run test:unit   (Node's built-in test runner, no extra deps)
import { test, describe } from 'node:test'
import assert from 'node:assert/strict'
import {
  computeEventSummaryMetrics,
  currencySymbol,
  formatMoney,
  snapshotCurrency,
} from '../eventMetrics.js'

const item = (overrides) => ({
  name: 'VIP', type: 'ticket', currency: 'JPY',
  price: 1500, total_quantity: 200, sold: 180, refund: 0,
  ...overrides,
})

const closed = {
  id: 'closed',
  observed_at: '2026-10-03T00:00:00',
  ticket_items: [
    item({}),
    item({ name: 'Zone A', price: 1000, total_quantity: 50, sold: 40 }),
    item({ name: 'Photo Card', type: 'benefit', price: 300, total_quantity: 100, sold: 100 }),
    item({ name: 'Hi-Touch', type: 'benefit', price: 400, total_quantity: 20, sold: 20 }),
    item({ name: 'Sticker', type: 'benefit', price: 200, total_quantity: 50, sold: 50 }),
  ],
}

describe('computeEventSummaryMetrics', () => {
  test('returns zeroed metrics when there is no snapshot', () => {
    const metrics = computeEventSummaryMetrics(null, [])

    assert.equal(metrics.totalRevenue, 0)
    assert.equal(metrics.salesVelocity, '0.0 / hr')
  })

  test('totals revenue, sell-through and remaining stock per type', () => {
    const metrics = computeEventSummaryMetrics(closed, [closed])

    assert.equal(metrics.ticketRevenue, 310000)
    assert.equal(metrics.benefitRevenue, 48000)
    assert.equal(metrics.totalRevenue, 358000)
    // (180 + 40) / (200 + 50) = 220 / 250
    assert.equal(metrics.ticketSellThrough, 88)
    assert.equal(metrics.benefitSellThrough, 100)
    assert.equal(metrics.ticketRemaining, 30)
    assert.equal(metrics.benefitRemaining, 0)
  })

  test('subtracts refunds from revenue and reports refund rate', () => {
    const snapshot = { id: 's', observed_at: '2026-10-03', ticket_items: [item({ sold: 100, refund: 10, total_quantity: 200 })] }

    const metrics = computeEventSummaryMetrics(snapshot, [snapshot])

    assert.equal(metrics.ticketRevenue, 90 * 1500)
    assert.equal(metrics.ticketRefundRate, 10)
  })

  test('computes sales velocity against the previous snapshot', () => {
    const earlier = { id: 'e', observed_at: '2026-10-01T00:00:00', ticket_items: [item({ sold: 100 })] }
    const later = { id: 'l', observed_at: '2026-10-01T10:00:00', ticket_items: [item({ sold: 150 })] }

    const metrics = computeEventSummaryMetrics(later, [later, earlier])

    assert.equal(metrics.salesVelocity, '+5.0 / hr')
  })

  test('does not mutate the snapshots it is given', () => {
    const snapshots = [closed, { id: 'x', observed_at: '2026-09-01', ticket_items: [] }]
    const before = JSON.stringify(snapshots)

    computeEventSummaryMetrics(closed, snapshots)

    assert.equal(JSON.stringify(snapshots), before)
  })
})

describe('currency helpers', () => {
  test('currencySymbol maps ISO codes to symbols', () => {
    assert.equal(currencySymbol('JPY'), '¥')
    assert.equal(currencySymbol('USD'), '$')
  })

  test('currencySymbol falls back to empty string for missing or invalid codes', () => {
    assert.equal(currencySymbol(undefined), '')
    assert.equal(currencySymbol('not-a-currency'), '')
  })

  test('formatMoney formats yen without decimals', () => {
    assert.equal(formatMoney(358000, 'JPY'), '¥358,000')
  })

  test('currencySymbol keeps dollar currencies distinguishable from USD', () => {
    assert.equal(currencySymbol('HKD'), 'HK$')
    assert.equal(currencySymbol('TWD'), 'NT$')
  })

  test('formatMoney labels HKD as HK$ and drops decimals for whole amounts', () => {
    assert.equal(formatMoney(358000, 'HKD'), 'HK$358,000')
  })

  test('formatMoney keeps cents when the amount has them', () => {
    assert.equal(formatMoney(45893.217, 'USD'), '$45,893.22')
    assert.equal(formatMoney(1234.5, 'USD'), '$1,234.50')
  })

  test('formatMoney falls back to a plain number without a valid currency', () => {
    assert.equal(formatMoney(1234.5, ''), '1,234.5')
  })

  test('snapshotCurrency reads the first item currency', () => {
    assert.equal(snapshotCurrency(closed), 'JPY')
    assert.equal(snapshotCurrency(null), '')
    assert.equal(snapshotCurrency({ ticket_items: [] }), '')
  })
})
