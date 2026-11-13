import { test } from 'node:test'
import assert from 'node:assert/strict'
import {
  ageBreakdown,
  countUpValue,
  genderBreakdown,
  initialsOf,
  itemsOfType,
  overallSold,
  reportFileTitle,
  revenueSplit,
  ringDash,
  shadeIndex,
  topEarner,
} from '../shareReport.js'

const ITEMS = Object.freeze([
  { name: 'VIP區', type: 'ticket', total_quantity: 200, net_sold: 180, revenue: 270000 },
  { name: 'A區', type: 'ticket', total_quantity: 50, net_sold: 40, revenue: 40000 },
  { name: '小卡', type: 'benefit', total_quantity: 100, net_sold: 100, revenue: 30000 },
  { name: '擊掌', type: 'benefit', total_quantity: 20, net_sold: 20, revenue: 8000 },
  { name: '貼紙', type: 'benefit', total_quantity: 50, net_sold: 50, revenue: 10000 },
])

test('revenueSplit returns rounded shares that add up to 100', () => {
  assert.deepEqual(revenueSplit(310000, 48000), { ticketPct: 87, benefitPct: 13 })
})

test('revenueSplit returns zeros when there is no revenue', () => {
  assert.deepEqual(revenueSplit(0, 0), { ticketPct: 0, benefitPct: 0 })
})

test('overallSold sums net sold over capacity across all items', () => {
  assert.deepEqual(overallSold(ITEMS), { sold: 390, total: 420, percent: 92.9 })
})

test('overallSold handles empty input', () => {
  assert.deepEqual(overallSold([]), { sold: 0, total: 0, percent: 0 })
})

test('topEarner picks the highest revenue item and its share of the total', () => {
  assert.deepEqual(topEarner(ITEMS), { name: 'VIP區', revenue: 270000, share: 75 })
})

test('topEarner returns null when nothing earned', () => {
  assert.equal(topEarner([]), null)
  assert.equal(topEarner([{ name: 'x', revenue: 0 }]), null)
})

test('itemsOfType filters without mutating the input', () => {
  const tickets = itemsOfType(ITEMS, 'ticket')
  assert.deepEqual(tickets.map((i) => i.name), ['VIP區', 'A區'])
  assert.equal(ITEMS.length, 5)
})

test('genderBreakdown lists non-zero genders, largest first', () => {
  const snapshot = { gender_distribution: { male: 35, female: 65, other: 0, unknown: 0 } }
  assert.deepEqual(genderBreakdown(snapshot), [
    { key: 'female', label: 'Female', value: 65 },
    { key: 'male', label: 'Male', value: 35 },
  ])
})

test('genderBreakdown returns an empty list when no data', () => {
  assert.deepEqual(genderBreakdown({}), [])
  assert.deepEqual(genderBreakdown(null), [])
  assert.deepEqual(genderBreakdown({ gender_distribution: { male: 0, female: 0 } }), [])
})

test('ageBreakdown keeps bucket order and flags the peak bucket', () => {
  const snapshot = {
    age_distribution: { age_10s: 5, age_20s: 70, age_30s: 20, age_40s: 5, age_50_plus: 0 },
  }
  assert.deepEqual(ageBreakdown(snapshot), [
    { label: '10s', value: 5, isPeak: false },
    { label: '20s', value: 70, isPeak: true },
    { label: '30s', value: 20, isPeak: false },
    { label: '40s', value: 5, isPeak: false },
    { label: '50+', value: 0, isPeak: false },
  ])
})

test('ageBreakdown returns an empty list when all buckets are zero', () => {
  assert.deepEqual(ageBreakdown({ age_distribution: { age_20s: 0 } }), [])
  assert.deepEqual(ageBreakdown(undefined), [])
})

test('ringDash returns the circumference and the unfilled offset', () => {
  const { circumference, offset } = ringDash(50, 40)
  assert.equal(Math.round(circumference * 100) / 100, 251.33)
  assert.equal(Math.round(offset * 100) / 100, 125.66)
})

test('ringDash clamps the percent between 0 and 100', () => {
  assert.equal(ringDash(150, 40).offset, 0)
  assert.equal(ringDash(-5, 40).offset, ringDash(0, 40).circumference)
})

test('countUpValue eases from 0 to the target and never overshoots', () => {
  assert.equal(countUpValue(358000, 0), 0)
  assert.equal(countUpValue(358000, 1), 358000)
  assert.equal(countUpValue(358000, 2), 358000)
  const half = countUpValue(358000, 0.5)
  assert.ok(half > 179000 && half < 358000, 'ease-out is past halfway at half time')
  assert.equal(Number.isInteger(half), true)
})

test('initialsOf returns up to two uppercase initials', () => {
  assert.equal(initialsOf('NOVA'), 'N')
  assert.equal(initialsOf('Kim Ye rin'), 'KY')
  assert.equal(initialsOf(''), '?')
  assert.equal(initialsOf(undefined), '?')
})

test('shadeIndex maps a value onto a light-to-dark scale relative to the max', () => {
  assert.equal(shadeIndex(70, 70, 5), 4)
  assert.equal(shadeIndex(20, 70, 5), 1)
  assert.equal(shadeIndex(5, 70, 5), 0)
  assert.equal(shadeIndex(0, 70, 5), 0)
})

test('shadeIndex is safe with a zero max or a single step', () => {
  assert.equal(shadeIndex(10, 0, 5), 0)
  assert.equal(shadeIndex(10, 10, 1), 0)
})

test('reportFileTitle builds a clean PDF file name from the event name', () => {
  assert.equal(reportFileTitle('NOVA Fan Meeting Tour'), 'NOVA Fan Meeting Tour - Sales Report')
})

test('reportFileTitle strips characters that are not allowed in file names', () => {
  assert.equal(reportFileTitle('A/B: "Live" <HK>?*|'), 'AB Live HK - Sales Report')
})

test('reportFileTitle falls back when there is no event name', () => {
  assert.equal(reportFileTitle(''), 'Event - Sales Report')
  assert.equal(reportFileTitle(undefined), 'Event - Sales Report')
})
