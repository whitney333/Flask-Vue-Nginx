<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import publicApi from '@/libs/publicApi.js'
import {
  computeEventSummaryMetrics,
  currencySymbol,
  formatMoney,
  snapshotCurrency,
} from '@/libs/eventMetrics.js'
import {
  ageBreakdown,
  genderBreakdown,
  initialsOf,
  itemsOfType,
  overallSold,
  reportFileTitle,
  revenueSplit,
  shadeIndex,
  topEarner,
} from '@/libs/shareReport.js'
import ShareItemLines from './components/ShareItemLines.vue'
import ShareSkeleton from './components/ShareSkeleton.vue'
import ShareCurrencyToggle from './components/ShareCurrencyToggle.vue'
import ShareSoldRing from './components/ShareSoldRing.vue'
import { useCountUp } from './useCountUp.js'
import { useUsdRates } from './useUsdRates.js'
import {
  RATES_ATTRIBUTION_URL,
  canConvertToUsd,
  convertSnapshotToUsd,
  rateLabel,
} from '@/libs/currencyConversion.js'
import { AGE_SHADES, CARD, EYEBROW, GENDER_FILLS, SERIES } from './shareTheme.js'
import SalesTrendLineChart from '@/views/Campaign/components/OfflineEvent_SalesTrendLineChart.vue'

// Keep this private page out of search engines and stop the URL leaking via Referer.
const PRIVATE_META = [
  { name: 'robots', content: 'noindex, nofollow' },
  { name: 'referrer', content: 'no-referrer' },
]

const route = useRoute()

const status = ref('loading') // 'loading' | 'ready' | 'invalid' | 'error'
const report = ref(null)
const activeSnapshotId = ref(null)
const imageFailed = ref(false)

const event = computed(() => report.value?.event || {})
const artist = computed(() => report.value?.artists?.[0] || null)
const rawSnapshots = computed(() => report.value?.snapshots || [])

// Currency display: original (as entered by the admin) or USD at today's live rate
const displayCurrency = ref('original') // 'original' | 'usd'
const { rates, updatedAt: ratesUpdatedAt, status: ratesStatus, load: loadRates } = useUsdRates()
const canConvert = computed(() => canConvertToUsd(rawSnapshots.value, rates.value))
const isUsd = computed(() => displayCurrency.value === 'usd' && canConvert.value)
const snapshots = computed(() =>
  isUsd.value ? rawSnapshots.value.map((s) => convertSnapshotToUsd(s, rates.value)) : rawSnapshots.value
)
// The event's own currency (from the first snapshot); '' when items mix currencies
const originalCode = computed(() => {
  const codes = new Set((rawSnapshots.value[0]?.ticket_items || []).map((i) => i.currency).filter(Boolean))
  return codes.size === 1 ? [...codes][0] : ''
})
const showCurrencyToggle = computed(() => originalCode.value !== 'USD' && rawSnapshots.value.length > 0)
const usdRateNote = computed(() => (originalCode.value ? rateLabel(originalCode.value, rates.value) : ''))
// set when a retry also fails, so the viewer sees why USD did not switch on
const usdUnavailable = ref(false)
const retryUsd = async () => {
  const loaded = await loadRates()
  usdUnavailable.value = !loaded
  if (loaded) displayCurrency.value = 'usd'
}
const activeSnapshot = computed(
  () => snapshots.value.find((s) => s.id === activeSnapshotId.value) || null
)
const items = computed(() => activeSnapshot.value?.ticket_items || [])
const tickets = computed(() => itemsOfType(items.value, 'ticket'))
const benefits = computed(() => itemsOfType(items.value, 'benefit'))
const currency = computed(() => snapshotCurrency(activeSnapshot.value))
// Totals are plain sums, so they are only meaningful when every item shares one currency.
const hasMixedCurrencies = computed(
  () => new Set(items.value.map((item) => item.currency).filter(Boolean)).size > 1
)
const totalCurrency = computed(() => (hasMixedCurrencies.value ? '' : currency.value))
const money = (value) => formatMoney(value, totalCurrency.value)

const metrics = computed(() => computeEventSummaryMetrics(activeSnapshot.value, snapshots.value))
const split = computed(() => revenueSplit(metrics.value.ticketRevenue, metrics.value.benefitRevenue))
const sold = computed(() => overallSold(items.value))
const top = computed(() => topEarner(items.value))
const genders = computed(() => genderBreakdown(activeSnapshot.value))
const ages = computed(() => ageBreakdown(activeSnapshot.value))
const displayedTotal = useCountUp(computed(() => metrics.value.totalRevenue))

const maxAge = computed(() => Math.max(0, ...ages.value.map((a) => a.value)))
const ageShade = (value) => AGE_SHADES[shadeIndex(value, maxAge.value, AGE_SHADES.length)]
const genderFill = (index) => GENDER_FILLS[Math.min(index, GENDER_FILLS.length - 1)]
// Staggered entrance: each card starts slightly after the previous one
const RISE_STEP_MS = 60
const rise = (index) => ({ animationDelay: `${index * RISE_STEP_MS}ms` })

const artistName = computed(() =>
  (report.value?.artists || []).map((a) => a.artist_en_name || a.artist_kr_name).filter(Boolean).join(' · ')
)
const artistInitials = computed(() => initialsOf(artist.value?.artist_en_name || artist.value?.artist_kr_name))
const location = computed(() =>
  [event.value.venue, event.value.held_city, event.value.held_country].filter(Boolean).join(', ')
)
const formatDate = (value, withTime = false) => {
  if (!value) return ''
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return ''
  return date.toLocaleDateString('en-US', {
    year: 'numeric', month: 'long', day: 'numeric',
    ...(withTime ? { hour: '2-digit', minute: '2-digit' } : {}),
  })
}
const headerMeta = computed(() =>
  [formatDate(event.value.event_date), event.value.session, location.value].filter(Boolean).join(' · ')
)
const oneDecimal = (value) => Math.round((Number(value) || 0) * 10) / 10

const addedHeadTags = []
const previousTitle = document.title
let isUnmounted = false
let requestId = 0

const addHeadTag = (tag, attrs) => {
  const el = document.createElement(tag)
  Object.entries(attrs).forEach(([key, value]) => el.setAttribute(key, value))
  document.head.appendChild(el)
  addedHeadTags.push(el)
}

// Browsers save the PDF under the page title, so give it a clean file name while printing.
const downloadPdf = () => {
  const titleBefore = document.title
  document.title = reportFileTitle(event.value.event_name)
  window.addEventListener('afterprint', () => { document.title = titleBefore }, { once: true })
  window.print()
}

const loadReport = async () => {
  // ignore responses that arrive after unmount or after a newer request started
  const thisRequest = ++requestId
  const isStale = () => isUnmounted || thisRequest !== requestId
  status.value = 'loading'
  try {
    const res = await publicApi.get(`/share/v1/events/${encodeURIComponent(route.params.token)}`)
    if (isStale()) return
    report.value = res.data?.data || null
    activeSnapshotId.value = report.value?.snapshots?.[0]?.id || null
    imageFailed.value = false
    document.title = `${report.value?.event?.event_name || 'Event report'} | Mishkan`
    status.value = 'ready'
  } catch (err) {
    if (isStale()) return
    status.value = err?.response?.status === 404 ? 'invalid' : 'error'
  }
}

onMounted(() => {
  PRIVATE_META.forEach((attrs) => addHeadTag('meta', attrs))
  loadReport()
  loadRates()
})

// same component instance is reused when navigating between two share links
watch(() => route.params.token, (next, prev) => {
  if (next && next !== prev) loadReport()
})

onBeforeUnmount(() => {
  isUnmounted = true
  addedHeadTags.forEach((el) => el.remove())
  document.title = previousTitle
})
</script>

<template>
  <main class="relative isolate min-h-screen overflow-x-clip bg-stone-50 text-slate-900 print:!min-h-0">
    <!-- Soft indigo/violet wash at the top of the page -->
    <div
        class="pointer-events-none absolute inset-x-0 top-0 -z-10 h-[36rem] bg-[radial-gradient(56rem_28rem_at_12%_-8%,rgba(99,102,241,0.20),transparent_62%),radial-gradient(40rem_24rem_at_92%_-4%,rgba(168,85,247,0.16),transparent_62%)]"
        aria-hidden="true"
    ></div>
    <!-- Loading -->
    <ShareSkeleton v-if="status === 'loading'" />

    <!-- Invalid / error -->
    <div
        v-else-if="status !== 'ready'"
        class="mx-auto flex min-h-screen max-w-md flex-col items-center justify-center px-6 text-center"
    >
      <p class="text-5xl" aria-hidden="true">🔒</p>
      <h1 class="mt-4 text-xl font-bold">
        {{ status === 'invalid' ? 'This link is not available' : 'Something went wrong' }}
      </h1>
      <p class="mt-2 text-sm text-slate-500">
        {{ status === 'invalid'
          ? 'The link may have been replaced or turned off. Please ask your contact for a new one.'
          : 'We could not load the report. Please check your connection and try again.' }}
      </p>
      <button
          v-if="status === 'error'"
          type="button"
          class="mt-6 rounded-full bg-gradient-to-r from-indigo-600 to-violet-600 px-5 py-2 text-sm font-semibold text-white shadow-lg shadow-indigo-500/25 transition hover:brightness-110"
          @click="loadReport"
      >Try again</button>
    </div>

    <!-- Report -->
    <div v-else class="mx-auto max-w-5xl px-4 pb-16 pt-6 sm:px-6 sm:pt-10 print:!px-0 print:!pb-0 print:!pt-0">
      <header class="flex flex-wrap items-center gap-4">
        <img
            v-if="artist?.image_url && !imageFailed"
            :src="artist.image_url"
            :alt="artistName"
            width="56" height="56"
            class="h-12 w-12 shrink-0 rounded-2xl object-cover shadow-lg ring-2 ring-white sm:h-14 sm:w-14"
            referrerpolicy="no-referrer"
            @error="imageFailed = true"
        />
        <div
            v-else
            class="grid h-12 w-12 shrink-0 place-items-center rounded-2xl bg-gradient-to-br from-indigo-500 via-violet-500 to-fuchsia-500 text-lg font-bold text-white shadow-lg shadow-violet-500/30 sm:h-14 sm:w-14"
            aria-hidden="true"
        >{{ artistInitials }}</div>
        <div class="min-w-0">
          <p class="bg-gradient-to-r from-indigo-600 to-violet-600 bg-clip-text text-xs font-semibold uppercase tracking-[0.2em] text-transparent">{{ artistName || 'Artist' }}</p>
          <h1 class="mt-1 text-2xl font-extrabold leading-tight tracking-tight sm:text-3xl">{{ event.event_name || 'Event report' }}</h1>
          <p v-if="headerMeta" class="mt-1 text-sm text-slate-500">{{ headerMeta }}</p>
        </div>
        <div class="flex w-full flex-wrap items-center gap-2 sm:ml-auto sm:w-auto print:hidden">
          <ShareCurrencyToggle
              v-if="showCurrencyToggle"
              v-model="displayCurrency"
              :original-code="originalCode"
              :rates-status="ratesStatus"
              :can-convert="canConvert"
              @retry="retryUsd"
          />
          <button
              type="button"
              class="inline-flex items-center gap-2 rounded-full bg-slate-900 px-4 py-2 text-sm font-semibold text-white shadow-lg shadow-slate-900/15 transition hover:bg-slate-800 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 active:scale-[0.98]"
              @click="downloadPdf"
          >
            <svg class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path d="M10.75 2.75a.75.75 0 0 0-1.5 0v8.614L6.295 8.235a.75.75 0 1 0-1.09 1.03l4.25 4.5a.75.75 0 0 0 1.09 0l4.25-4.5a.75.75 0 0 0-1.09-1.03l-2.955 3.129V2.75Z" />
              <path d="M3.5 12.75a.75.75 0 0 0-1.5 0v2.5A2.75 2.75 0 0 0 4.75 18h10.5A2.75 2.75 0 0 0 18 15.25v-2.5a.75.75 0 0 0-1.5 0v2.5c0 .69-.56 1.25-1.25 1.25H4.75c-.69 0-1.25-.56-1.25-1.25v-2.5Z" />
            </svg>
            Download PDF
          </button>
        </div>
      </header>

      <p v-if="isUsd" class="mt-4 text-xs text-slate-500" role="note">
        Shown in US dollars at today's exchange rate<template v-if="usdRateNote"> ({{ usdRateNote }})</template><template v-if="ratesUpdatedAt">, updated {{ formatDate(ratesUpdatedAt) }}</template>.
        <a :href="RATES_ATTRIBUTION_URL" target="_blank" rel="noopener noreferrer" class="underline decoration-slate-300 underline-offset-2 hover:text-slate-700">Rates by Exchange Rate API</a>
      </p>
      <p v-else-if="usdUnavailable" class="mt-4 text-xs text-amber-700 print:hidden" role="alert">
        Today's exchange rate could not be loaded, so amounts are shown in the original currency. Tap USD to try again.
      </p>

      <nav v-if="snapshots.length > 1" class="mt-6 -mx-4 overflow-x-auto px-4 print:hidden" aria-label="Report snapshots">
        <div class="flex w-max gap-1 rounded-full bg-white/60 p-1 ring-1 ring-indigo-950/5 backdrop-blur-xl">
          <button
              v-for="snapshot in snapshots"
              :key="snapshot.id"
              type="button"
              class="rounded-full px-4 py-1.5 text-sm font-medium transition focus-visible:outline focus-visible:outline-2 focus-visible:outline-indigo-600"
              :class="snapshot.id === activeSnapshotId
                ? 'bg-slate-900 text-white shadow-sm'
                : 'text-slate-600 hover:bg-white hover:text-slate-900'"
              :aria-pressed="snapshot.id === activeSnapshotId"
              @click="activeSnapshotId = snapshot.id"
          >{{ snapshot.snapshot_name }}</button>
        </div>
      </nav>

      <p
          v-if="hasMixedCurrencies"
          class="mt-4 rounded-2xl bg-amber-50/80 px-4 py-3 text-sm text-amber-900 ring-1 ring-amber-600/20 backdrop-blur"
          role="note"
      >
        This report includes items priced in different currencies. Totals are added up without
        currency conversion; see each item for its own currency.
      </p>

      <section v-if="!activeSnapshot" class="mt-8 rounded-3xl border border-dashed border-indigo-200 bg-white/60 p-10 text-center text-sm text-slate-500 backdrop-blur">
        Sales figures have not been published for this event yet.
      </section>

      <div v-else class="mt-6 grid grid-cols-1 gap-3 sm:gap-4 lg:grid-cols-6 print:grid-cols-6 print:gap-3">
        <!-- Revenue -->
        <section class="share-rise relative overflow-hidden rounded-3xl bg-gradient-to-br from-indigo-950 via-slate-950 to-slate-900 p-6 text-white shadow-2xl shadow-indigo-950/30 ring-1 ring-white/10 sm:p-8 print:break-inside-avoid print:shadow-none lg:col-span-4 print:col-span-4" :style="rise(0)" aria-label="Total revenue">
          <div class="pointer-events-none absolute -right-16 -top-24 h-72 w-72 rounded-full bg-violet-500/35 blur-3xl" aria-hidden="true"></div>
          <div class="pointer-events-none absolute -top-10 right-1/3 h-40 w-40 rounded-full bg-fuchsia-500/20 blur-3xl" aria-hidden="true"></div>
          <div class="pointer-events-none absolute -bottom-24 left-10 h-56 w-56 rounded-full bg-amber-400/15 blur-3xl" aria-hidden="true"></div>
          <div class="relative">
            <p class="text-[11px] font-semibold uppercase tracking-[0.14em] text-indigo-200/70">
              Total revenue<template v-if="totalCurrency"> · {{ totalCurrency }}</template>
            </p>
            <p class="mt-1 break-words bg-gradient-to-br from-white via-white to-indigo-200 bg-clip-text pb-1 text-4xl font-black tabular-nums tracking-tight text-transparent sm:text-6xl">{{ money(displayedTotal) }}</p>
            <div class="mt-6 flex h-3 overflow-hidden rounded-full bg-white/10" aria-hidden="true">
              <div class="share-grow h-full" :class="SERIES.ticket.fill" :style="{ width: `${split.ticketPct}%` }"></div>
              <div class="share-grow h-full" :class="SERIES.benefit.fill" :style="{ width: `${split.benefitPct}%` }"></div>
            </div>
            <div class="mt-2 flex flex-wrap justify-between gap-2 text-xs text-indigo-100/80 tabular-nums">
              <span><span class="mr-1.5 inline-block h-2 w-2 rounded-full bg-indigo-400"></span>Tickets {{ money(metrics.ticketRevenue) }} · {{ split.ticketPct }}%</span>
              <span><span class="mr-1.5 inline-block h-2 w-2 rounded-full bg-orange-400"></span>Benefits {{ money(metrics.benefitRevenue) }} · {{ split.benefitPct }}%</span>
            </div>
            <p class="mt-4 text-xs text-indigo-200/60">Figures as of {{ formatDate(activeSnapshot.observed_at, true) }}</p>
          </div>
        </section>

        <!-- Overall sold -->
        <section :class="[CARD, 'flex flex-col items-center justify-center lg:col-span-2 print:col-span-2']" :style="rise(1)" aria-label="Overall sold">
          <p class="self-start" :class="EYEBROW">Overall sold</p>
          <ShareSoldRing class="my-3" :percent="sold.percent" />
          <p class="text-xs text-slate-500 tabular-nums">{{ sold.sold.toLocaleString('en-US') }} of {{ sold.total.toLocaleString('en-US') }} sold</p>
        </section>

        <!-- Tickets / benefits -->
        <section v-if="tickets.length" :class="[CARD, 'lg:col-span-3 print:col-span-3']" :style="rise(2)" aria-label="Tickets">
          <div class="flex items-center justify-between gap-2">
            <h2 :class="EYEBROW"><span class="mr-1.5 inline-block h-2 w-2 rounded-full" :class="SERIES.ticket.dot"></span>Tickets</h2>
            <span class="rounded-full px-2.5 py-0.5 text-xs font-semibold" :class="SERIES.ticket.badge">{{ oneDecimal(metrics.ticketSellThrough) }}% sold</span>
          </div>
          <ShareItemLines :items="tickets" tone="ticket" />
        </section>
        <section v-if="benefits.length" :class="[CARD, 'lg:col-span-3 print:col-span-3']" :style="rise(3)" aria-label="Benefits">
          <div class="flex items-center justify-between gap-2">
            <h2 :class="EYEBROW"><span class="mr-1.5 inline-block h-2 w-2 rounded-full" :class="SERIES.benefit.dot"></span>Benefits</h2>
            <span class="rounded-full px-2.5 py-0.5 text-xs font-semibold" :class="SERIES.benefit.badge">{{ oneDecimal(metrics.benefitSellThrough) }}% sold</span>
          </div>
          <ShareItemLines :items="benefits" tone="benefit" />
        </section>

        <!-- Highlights + audience -->
        <section :class="[CARD, 'lg:col-span-2 print:col-span-2']" :style="rise(4)" aria-label="Top earner">
          <p :class="EYEBROW">Top earner</p>
          <template v-if="top">
            <p class="mt-3 break-words text-2xl font-bold tracking-tight">{{ top.name }}</p>
            <p class="mt-1 text-xs text-slate-500 tabular-nums">{{ money(top.revenue) }} · <span class="font-semibold text-violet-600">{{ top.share }}%</span> of all revenue</p>
          </template>
          <p v-else class="mt-2 text-sm text-slate-400">No sales yet.</p>
        </section>
        <section :class="[CARD, 'lg:col-span-2 print:col-span-2']" :style="rise(5)" aria-label="Audience gender">
          <p :class="EYEBROW">Gender</p>
          <template v-if="genders.length">
            <div class="mt-4 flex h-3 gap-0.5 overflow-hidden rounded-full bg-slate-100" aria-hidden="true">
              <div v-for="(g, i) in genders" :key="g.key" class="share-grow h-full" :class="genderFill(i)" :style="{ width: `${g.value}%` }"></div>
            </div>
            <div class="mt-2 flex flex-wrap justify-between gap-2 text-xs text-slate-600 tabular-nums">
              <span v-for="(g, i) in genders" :key="g.key">
                <span class="mr-1.5 inline-block h-2 w-2 rounded-full" :class="genderFill(i)"></span>{{ g.label }} {{ g.value }}%
              </span>
            </div>
          </template>
          <p v-else class="mt-2 text-sm text-slate-400">Shared after the event closes.</p>
        </section>
        <section :class="[CARD, 'lg:col-span-2 print:col-span-2']" :style="rise(6)" aria-label="Audience age">
          <p :class="EYEBROW">Age</p>
          <div v-if="ages.length" class="mt-3 space-y-2">
            <div v-for="a in ages" :key="a.label" class="grid grid-cols-[2.25rem_1fr_2.5rem] items-center gap-2 text-xs tabular-nums">
              <span class="text-slate-500">{{ a.label }}</span>
              <div class="h-2 overflow-hidden rounded-full bg-indigo-100/60">
                <div class="share-grow h-full rounded-full" :class="ageShade(a.value)" :style="{ width: `${a.value}%` }"></div>
              </div>
              <span :class="a.isPeak ? 'text-indigo-700' : 'text-slate-700'" class="text-right font-semibold">{{ a.value }}%</span>
            </div>
          </div>
          <p v-else class="mt-2 text-sm text-slate-400">Shared after the event closes.</p>
        </section>

        <!-- Trend, only when there is more than one snapshot to compare -->
        <div v-if="snapshots.length > 1" class="share-rise lg:col-span-6 print:col-span-6" :style="rise(7)">
          <SalesTrendLineChart
              :snapshots="snapshots"
              :currency-symbol="currencySymbol(totalCurrency)"
              title="Revenue over time"
          />
        </div>
      </div>

      <footer class="mt-12 flex justify-center print:!mt-4 print:break-inside-avoid">
        <p class="inline-flex items-center gap-2 rounded-full bg-white/60 px-4 py-2 text-xs text-slate-500 ring-1 ring-indigo-950/5 backdrop-blur">
          <svg class="h-3.5 w-3.5 text-indigo-500" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
            <path fill-rule="evenodd" d="M10 1a4.5 4.5 0 0 0-4.5 4.5V9H5a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-6a2 2 0 0 0-2-2h-.5V5.5A4.5 4.5 0 0 0 10 1Zm3 8V5.5a3 3 0 1 0-6 0V9h6Z" clip-rule="evenodd" />
          </svg>
          Private report prepared by Mishkan · Please do not forward this link
        </p>
      </footer>
    </div>
  </main>
</template>

<style scoped>
/* Entrance motion: compositor-only (opacity/transform), disabled for reduced motion */
.share-rise {
  animation: share-rise 600ms cubic-bezier(0.16, 1, 0.3, 1) both;
}
.share-grow,
:deep(.share-grow) {
  transform-origin: left center;
  animation: share-grow 900ms cubic-bezier(0.16, 1, 0.3, 1) 200ms both;
}
@keyframes share-rise {
  from { opacity: 0; transform: translateY(12px); }
}
@keyframes share-grow {
  from { transform: scaleX(0); }
}
@media (prefers-reduced-motion: reduce) {
  .share-rise,
  .share-grow,
  :deep(.share-grow) { animation: none; }
}

/* Download PDF (browser print): A4, true colours, no motion */
@media print {
  @page { size: A4; margin: 10mm; }
  main {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  .share-rise,
  .share-grow,
  :deep(.share-grow) { animation: none; }
}
</style>
