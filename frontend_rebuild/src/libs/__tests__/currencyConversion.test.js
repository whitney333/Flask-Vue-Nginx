import { test } from 'node:test'
import assert from 'node:assert/strict'
import {
  canConvertToUsd,
  convertSnapshotToUsd,
  fetchUsdRates,
  parseUsdRates,
  rateLabel,
  toUsd,
} from '../currencyConversion.js'

const PAYLOAD = Object.freeze({
  result: 'success',
  base_code: 'USD',
  time_last_update_utc: 'Fri, 13 Nov 2026 00:02:31 +0000',
  rates: { USD: 1, HKD: 7.8, TWD: 32.5, BAD: -1, NAN: 'x' },
})
const RATES = Object.freeze({ USD: 1, HKD: 7.8, TWD: 32.5 })

const SNAPSHOT = Object.freeze({
  id: 's1',
  ticket_items: Object.freeze([
    Object.freeze({ name: 'VIP', type: 'ticket', currency: 'HKD', price: 1560, net_sold: 10, revenue: 15600 }),
  ]),
})

test('parseUsdRates keeps only valid positive rates and the update time', () => {
  assert.deepEqual(parseUsdRates(PAYLOAD), {
    rates: { USD: 1, HKD: 7.8, TWD: 32.5 },
    updatedAt: '2026-11-13T00:02:31.000Z',
  })
})

test('parseUsdRates rejects failed or non-USD responses', () => {
  assert.equal(parseUsdRates({ ...PAYLOAD, result: 'error' }), null)
  assert.equal(parseUsdRates({ ...PAYLOAD, base_code: 'EUR' }), null)
  assert.equal(parseUsdRates({ ...PAYLOAD, rates: null }), null)
  assert.equal(parseUsdRates(null), null)
})

test('toUsd divides by the rate and passes USD through', () => {
  assert.equal(toUsd(780, 'HKD', RATES), 100)
  assert.equal(toUsd(50, 'USD', RATES), 50)
})

test('toUsd returns null when the currency has no rate', () => {
  assert.equal(toUsd(100, 'XYZ', RATES), null)
  assert.equal(toUsd(100, '', RATES), null)
})

test('canConvertToUsd needs a rate for every item currency', () => {
  assert.equal(canConvertToUsd([SNAPSHOT], RATES), true)
  const odd = { ticket_items: [{ currency: 'XYZ' }] }
  assert.equal(canConvertToUsd([SNAPSHOT, odd], RATES), false)
  assert.equal(canConvertToUsd([SNAPSHOT], null), false)
})

test('convertSnapshotToUsd converts prices and revenue without mutating the input', () => {
  const converted = convertSnapshotToUsd(SNAPSHOT, RATES)

  assert.deepEqual(converted.ticket_items[0], {
    name: 'VIP', type: 'ticket', currency: 'USD', price: 200, net_sold: 10, revenue: 2000,
  })
  assert.equal(SNAPSHOT.ticket_items[0].currency, 'HKD')
  assert.equal(converted.id, 's1')
})

test('rateLabel describes the rate used for a currency', () => {
  assert.equal(rateLabel('HKD', RATES), '1 USD = 7.80 HKD')
  assert.equal(rateLabel('XYZ', RATES), '')
})

test('fetchUsdRates returns parsed rates from the API', async () => {
  const fakeFetch = async (url) => {
    assert.match(url, /^https:\/\/open\.er-api\.com\/v6\/latest\/USD$/)
    return { ok: true, json: async () => PAYLOAD }
  }
  const result = await fetchUsdRates(fakeFetch)
  assert.equal(result.rates.HKD, 7.8)
})

test('fetchUsdRates throws a friendly error on HTTP or payload failure', async () => {
  await assert.rejects(fetchUsdRates(async () => ({ ok: false, status: 503 })), /exchange rate/i)
  await assert.rejects(
    fetchUsdRates(async () => ({ ok: true, json: async () => ({ result: 'error' }) })),
    /exchange rate/i
  )
})
