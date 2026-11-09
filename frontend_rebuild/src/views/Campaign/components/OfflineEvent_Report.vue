<script setup>
import { ref, computed, watch } from 'vue'
import logoImg from '@/assets/mishkan-logo.svg'

const mishkanLogo = ref(logoImg)

const props = defineProps({
  event: {
    type: Object,
    default: () => ({})
  },
  selectedSnapshot: {
    type: Object,
    default: null
  },
  snapshots: {
    type: Array,
    default: () => []
  },
  artists: {
    type: Array,
    default: () => [],
  },
  summaryMetrics: {
    type: Object,
    default: () => ({})
  }
})

const reportElement = ref(null)
const artistThumbnailLoadFailed = ref(false)

const primaryArtist = computed(() => props.artists?.[0] || null)

const artistName = computed(() => {
  const artist = primaryArtist.value

  if (!artist) return 'Unknown Artist'

  return (
    artist.artist_en_name ||
    artist.english_name ||
    artist.artist_kr_name ||
    artist.korean_name ||
    'Unknown Artist'
  )
})

const artistThumbnail = computed(() => {
  const artist = primaryArtist.value
  if (!artist) return null

  return (
    artist.image ||
    artist.image_url ||
    artist.avatar ||
    artist.profile_image ||
    artist.thumbnail ||
    artist.img ||
    null
  )
})

watch(
  artistThumbnail,
  () => {
    artistThumbnailLoadFailed.value = false
  }
)

const formattedSession = computed(() => {
  return String(props.event?.session || 'Unknown')
})

const formattedEventDate = computed(() => {
  const value = props.event?.event_date
  if (!value) return '-'

  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return String(value)

  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')

  return `${year}-${month}-${day}`
})

const formatDateTime = value => {
  if (!value) return '-'

  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return String(value)

  return date.toLocaleString()
}

defineExpose({
  getElement: () => reportElement.value
})

const number = value => Number(value) || 0

const getNetSold = item => {
  if (item.net_sold != null) {
    return number(item.net_sold)
  }

  return Math.max(0, number(item.sold) - number(item.refund))
}

const getRevenue = item => {
  if (item.revenue != null) {
    return number(item.revenue)
  }

  return getNetSold(item) * number(item.price)
}

const formatNumber = value =>
  number(value).toLocaleString('en-US', {
    maximumFractionDigits: 2
  })

const formatDate = value => {
  if (!value) return '-'

  const date = new Date(value)

  if (Number.isNaN(date.getTime())) return String(value)

  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const allSnapshots = computed(() =>
  [...props.snapshots].sort(
    (a, b) =>
      new Date(a.observed_at || 0) -
      new Date(b.observed_at || 0)
  )
)

const closedSnapshot = computed(() =>
  allSnapshots.value.find(
    snapshot =>
      snapshot.snapshot_name === 'Closed' ||
      snapshot.snapshot_type === 'closed'
  )
)

const selectedItems = computed(
  () => props.selectedSnapshot?.ticket_items || []
)

const ticketItems = computed(() =>
  selectedItems.value.filter(item => item.type === 'ticket')
)

const benefitItems = computed(() =>
  selectedItems.value.filter(item => item.type === 'benefit')
)

const revenueByCurrency = computed(() => {
  const result = {}

  selectedItems.value.forEach(item => {
    const currency = item.currency || 'Unknown'

    if (!result[currency]) {
      result[currency] = {
        ticket: 0,
        benefit: 0
      }
    }

    if (item.type === 'ticket') {
      result[currency].ticket += getRevenue(item)
    } else if (item.type === 'benefit') {
      result[currency].benefit += getRevenue(item)
    }
  })

  return Object.entries(result).map(([currency, values]) => ({
    currency,
    ticket: values.ticket,
    benefit: values.benefit,
    total: values.ticket + values.benefit
  }))
})

const trendData = computed(() =>
  allSnapshots.value.map(snapshot => {
    const totals = {};

    (snapshot.ticket_items || []).forEach(item => {
      const currency = item.currency || 'Unknown'

      if (!totals[currency]) {
        totals[currency] = {
          ticket: 0,
          benefit: 0
        }
      }

      if (item.type === 'ticket') {
        totals[currency].ticket += getRevenue(item)
      } else if (item.type === 'benefit') {
        totals[currency].benefit += getRevenue(item)
      }
    })

    return {
      name: snapshot.snapshot_name || 'Snapshot',
      observedAt: snapshot.observed_at,
      currencies: Object.entries(totals).map(([currency, values]) => ({
        currency,
        ticket: values.ticket,
        benefit: values.benefit,
        total: values.ticket + values.benefit
      }))
    }
  })
)

// Line chart configuration
const trendChartWidth = 760
const trendChartHeight = 440

const trendChartPadding = {
  top: 25,
  right: 30,
  bottom: 100,
  left: 90
}

// Format Y-axis values
const formatChartAxisValue = value =>
  Number(value).toLocaleString('en-US', {
    notation: 'compact',
    maximumFractionDigits: 1
  })

// Generate line chart data for each currency
const trendCharts = computed(() => {
  const currencies = [
    ...new Set(
      trendData.value.flatMap(snapshot =>
        snapshot.currencies.map(item => item.currency)
      )
    )
  ]

  const plotWidth =
    trendChartWidth -
    trendChartPadding.left -
    trendChartPadding.right

  const plotHeight =
    trendChartHeight -
    trendChartPadding.top -
    trendChartPadding.bottom

  return currencies.map(currency => {
    const rows = trendData.value.map(snapshot => {
      const currencyData = snapshot.currencies.find(
        item => item.currency === currency
      )

      return {
        label: snapshot.name,
        ticket: number(currencyData?.ticket),
        benefit: number(currencyData?.benefit)
      }
    })

    const maxValue = Math.max(
      1,
      ...rows.flatMap(row => [row.ticket, row.benefit])
    )

    // Calculate X position
    const getX = index => {
      const step = plotWidth / Math.max(rows.length, 1)

      return trendChartPadding.left + (index + 0.5) * step
    }

    // Calculate Y position
    const getY = value =>
      trendChartPadding.top +
      plotHeight -
      (value / maxValue) * plotHeight

    // Y-axis grid lines
    const yTicks = Array.from({ length: 5 }, (_, index) => {
      const value = (maxValue * (4 - index)) / 4

      return {
        value,
        y: getY(value),
        label: formatChartAxisValue(value)
      }
    })

    // X-axis snapshot labels
    // Wrap long snapshot labels
    const wrapAxisLabel = (value, maxChars = 14) => {
      const words = String(value || '').trim().split(/\s+/)
      const lines = []
      let currentLine = ''

      words.forEach(word => {
        if (word.length > maxChars) {
          if (currentLine) {
            lines.push(currentLine)
            currentLine = ''
          }

          for (let i = 0; i < word.length; i += maxChars) {
            lines.push(word.slice(i, i + maxChars))
          }

          return
        }

        const candidate = currentLine
            ? `${currentLine} ${word}`
            : word

        if (candidate.length > maxChars && currentLine) {
          lines.push(currentLine)
          currentLine = word
        } else {
          currentLine = candidate
        }
      })

      if (currentLine) {
        lines.push(currentLine)
      }

      return lines.length ? lines : ['']
    }

    const labelStep = plotWidth / Math.max(rows.length, 1)

    const labelMaxChars = Math.max(
        7,
        Math.min(18, Math.floor(labelStep / 6.5))
    )

    const xLabels = rows.map((row, index) => ({
      label: row.label,
      lines: wrapAxisLabel(row.label, labelMaxChars),
      x: getX(index)
    }))

    // Ticket and Benefit lines
    const seriesConfig = [
      {
        key: 'ticket',
        label: 'Ticket Revenue',
        color: '#2563EB'
      },
      {
        key: 'benefit',
        label: 'Benefit Revenue',
        color: '#F97316'
      }
    ]

    const series = seriesConfig.map(config => {
      const points = rows.map((row, index) => ({
        x: getX(index),
        y: getY(row[config.key]),
        value: row[config.key],
        label: row.label
      }))

      const path = points
        .map((point, index) =>
          `${index === 0 ? 'M' : 'L'} ${point.x} ${point.y}`
        )
        .join(' ')

      return {
        ...config,
        points,
        path
      }
    })

    return {
      currency,
      width: trendChartWidth,
      height: trendChartHeight,
      padding: trendChartPadding,
      yTicks,
      xLabels,
      series
    }
  })
})

const zoneData = computed(() => {
  return [...ticketItems.value, ...benefitItems.value].map(item => {
    const quantity = Math.max(0, number(item.total_quantity))
    const netSold = Math.max(0, getNetSold(item))

    // Remaining inventory after deducting net sold
    const remainingInventory = Math.max(0, quantity - netSold)

    const sellThrough = quantity > 0
      ? (netSold / quantity) * 100
      : 0

    return {
      type: item.type,
      name: item.name || '-',
      currency: item.currency || '',
      quantity,
      netSold,
      remainingInventory,
      sellThrough,

      // Ticket: Blue / Benefit: Orange
      color: item.type === 'ticket'
        ? '#2563EB'
        : '#F97316'
    }
  })
})

const zoneBarChart = computed(() => {
  // Sort by sell-through rate, then net sold
  const items = [...zoneData.value].sort(
    (a, b) =>
      b.sellThrough - a.sellThrough ||
      b.netSold - a.netSold
  )

  const width = 760
  const rowHeight = 36

  const padding = {
    top: 28,
    right: 90,
    bottom: 60,
    left: 195
  }

  const plotHeight = Math.max(
    120,
    items.length * rowHeight
  )

  const height =
    padding.top + plotHeight + padding.bottom

  const plotWidth =
    width - padding.left - padding.right

  const maxQuantity = Math.max(
    1,
    ...items.map(item =>
      item.netSold + item.remainingInventory
    )
  )

  // Generate a readable maximum axis value
  const rawStep = maxQuantity / 4
  const magnitude = Math.pow(
    10,
    Math.floor(Math.log10(rawStep))
  )

  const normalizedStep = rawStep / magnitude

  const niceMultiplier =
    normalizedStep <= 1 ? 1 :
    normalizedStep <= 2 ? 2 :
    normalizedStep <= 5 ? 5 : 10

  const step = niceMultiplier * magnitude
  const maxValue = step * 4

  // X-axis ticks
  const xTicks = Array.from({ length: 5 }, (_, index) => {
    const value = step * index

    return {
      value,
      x: padding.left + (value / maxValue) * plotWidth
    }
  })

  // Calculate chart rows
  const rowSpacing = items.length > 0
    ? plotHeight / items.length
    : rowHeight

  const rows = items.map((item, index) => {
    const totalBarValue =
      item.netSold + item.remainingInventory

    const soldWidth =
      (item.netSold / maxValue) * plotWidth

    const remainingWidth =
      (item.remainingInventory / maxValue) * plotWidth

    return {
      ...item,

      displayName:
        item.name.length > 22
          ? `${item.name.slice(0, 19)}...`
          : item.name,

      y: padding.top + (index + 0.5) * rowSpacing,

      barHeight: Math.min(20, rowSpacing * 0.6),

      soldWidth,
      remainingWidth,

      totalBarWidth:
        (totalBarValue / maxValue) * plotWidth
    }
  })

  return {
    width,
    height,
    padding,
    plotWidth,
    plotHeight,
    maxValue,
    xTicks,
    rows
  }
})

const genderData = computed(() => {
  const gender = closedSnapshot.value?.gender_distribution || {}

  return [
    { label: 'Male', value: number(gender.male), color: '#6B7280' },
    { label: 'Female', value: number(gender.female), color: '#9CA3AF' },
    { label: 'Other', value: number(gender.other), color: '#D1D5DB' }
  ]
})

const ageData = computed(() => {
  const age = closedSnapshot.value?.age_distribution || {}

  return [
    { label: '10s', value: number(age.age_10s), color: '#C7D2FE' },
    { label: '20s', value: number(age.age_20s), color: '#A5B4FC' },
    { label: '30s', value: number(age.age_30s), color: '#818CF8' },
    { label: '40s', value: number(age.age_40s), color: '#6366F1' },
    { label: '50+', value: number(age.age_50_plus), color: '#4338CA' }
  ]
})

const hasDemographics = computed(() => !!closedSnapshot.value)

const summaryCards = computed(() => {
  const metrics = props.summaryMetrics || {}

  return [
    {
      key: 'totalRevenue',
      label: 'Total Revenue',
      value: metrics.totalRevenue,
      format: 'currency',
      iconBg: 'bg-indigo-50',
      iconColor: 'text-indigo-600'
    },
    {
      key: 'ticketRevenue',
      label: 'Ticket Revenue',
      value: metrics.ticketRevenue,
      format: 'currency',
      iconBg: 'bg-blue-50',
      iconColor: 'text-blue-600'
    },
    {
      key: 'benefitRevenue',
      label: 'Benefit Revenue',
      value: metrics.benefitRevenue,
      format: 'currency',
      iconBg: 'bg-purple-50',
      iconColor: 'text-purple-600'
    },
    {
      key: 'ticketSellThrough',
      label: 'Ticket Sell-through',
      value: metrics.ticketSellThrough,
      format: 'percent',
      iconBg: 'bg-emerald-50',
      iconColor: 'text-emerald-600'
    },
    {
      key: 'benefitSellThrough',
      label: 'Benefit Sell-through',
      value: metrics.benefitSellThrough,
      format: 'percent',
      iconBg: 'bg-amber-50',
      iconColor: 'text-amber-600'
    },
    {
      key: 'salesVelocity',
      label: 'Sales Velocity',
      value: metrics.salesVelocity,
      format: 'number',
      iconBg: 'bg-rose-50',
      iconColor: 'text-rose-600'
    }
  ]
})

const formatMetric = card => {
  if (card.value == null) return '-'

  const value = formatNumber(card.value)

  if (card.format === 'percent') return `${value}%`

  if (card.format === 'currency') return value

  return value
}

const hasSalesData = computed(() =>
  selectedItems.value.length > 0
)

const generatedAt = new Date()
</script>

<template>
  <div
      ref="reportElement"
      class="box-border w-[190mm] max-w-full mx-auto bg-white font-[Arial,Helvetica,sans-serif] text-[11px] leading-[1.4] text-gray-800"
  >
    <article class="report-page">
      <div class="report-page-body">
        <!-- Report Header -->
        <header class="mb-5">
          <div class="mb-3 flex items-center justify-between">
            <!-- Logo -->
            <img
                :src="mishkanLogo"
                alt="Mishkan Logo"
                class="h-8 object-contain"
                crossorigin="anonymous"
            />
            <div class="rounded-full bg-indigo-50 px-2.5 py-1 text-[9px] font-bold tracking-wider text-indigo-600">
              OFFLINE EVENT REPORT
            </div>
          </div>

          <div class="mb-3.5 h-0.5 bg-indigo-600"></div>

          <h1 class="m-0 text-[22px] font-extrabold leading-tight text-gray-900">{{
              event.event_name || 'Offline Event'
            }}</h1>

          <p class="my-1 mb-2.5 text-xs text-gray-500">
            Event Performance Report
          </p>

          <div class="flex flex-col gap-1 text-[9px] text-gray-500 border-t border-gray-100 pt-2 mt-2">
            <div class="flex justify-between items-center">
              <span>
                {{ formattedEventDate }}{{ event.session ? `, ${event.session}` : '' }}
              </span>
              <span>
                Generated: {{ formatDate(generatedAt) }}
              </span>
            </div>
            <div>
              {{ event.held_city || '-' }}, {{ event.held_country || '-' }}
            </div>
          </div>
        </header>

        <!-- 01 Event Information -->
        <section class="mb-5">
          <div class="mb-3 flex items-center gap-2 border-b border-gray-200 pb-1.5">
        <span
            class="flex h-[22px] w-[22px] items-center justify-center rounded-[5px] bg-indigo-50 text-[10px] font-extrabold text-indigo-700">01</span>
            <h2 class="m-0 text-sm font-bold text-gray-900">Event Information</h2>
          </div>

          <!-- Artist Thumbnail Row -->
          <div class="flex items-center gap-3 rounded-md bg-gray-50 px-3 py-2 mb-2 break-inside-avoid">
            <img
                v-if="artistThumbnail && !artistThumbnailLoadFailed"
                :src="artistThumbnail"
                :alt="artistName"
                class="w-12 h-12 flex-shrink-0 object-cover rounded-md bg-gray-100"
                crossorigin="anonymous"
                @error="artistThumbnailLoadFailed = true"
            />

            <div v-else
                 class="w-12 h-12 flex-shrink-0 flex items-center justify-center rounded-md bg-indigo-50 text-indigo-600 font-bold text-base">
              {{ artistName.charAt(0) || 'A' }}
            </div>

            <div class="min-w-0">
              <div class="mb-0.5 text-[9px] font-semibold uppercase tracking-wider text-gray-500">Artist</div>
              <div class="break-words text-xs font-semibold text-gray-900">{{ artistName }}</div>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-2 break-inside-avoid">
            <div class="col-span-2 rounded-md bg-gray-50 px-3 py-2">
              <div class="mb-0.5 text-[9px] font-semibold uppercase tracking-wider text-gray-500">Event Type</div>
              <div class="break-words text-xs font-semibold text-gray-900">{{ event?.type || '-' }}</div>
            </div>

            <div class="rounded-md bg-gray-50 px-3 py-2">
              <div class="mb-0.5 text-[9px] font-semibold uppercase tracking-wider text-gray-500">Location</div>
              <div class="break-words text-xs font-semibold text-gray-900">
                {{ event?.held_city || '-' }}, {{ event?.held_country || '-' }}
              </div>
            </div>

            <div class="rounded-md bg-gray-50 px-3 py-2">
              <div class="mb-0.5 text-[9px] font-semibold uppercase tracking-wider text-gray-500">Date</div>
              <div class="break-words text-xs font-semibold text-gray-900">
                {{ formattedEventDate }}{{ event?.session ? `, ${event.session}` : '' }}
              </div>
            </div>

            <div class="rounded-md bg-gray-50 px-3 py-2">
              <div class="mb-0.5 text-[9px] font-semibold uppercase tracking-wider text-gray-500">Venue</div>
              <div class="break-words text-xs font-semibold text-gray-900">{{ event?.venue || '-' }}</div>
            </div>
            <div class="rounded-md bg-gray-50 px-3 py-2">
              <div class="mb-0.5 text-[9px] font-semibold uppercase tracking-wider text-gray-500">Organizer</div>
              <div class="break-words text-xs font-semibold text-gray-900">{{ event?.organizer || '-' }}</div>
            </div>

            <div class="rounded-md bg-gray-50 px-3 py-2">
              <div class="mb-0.5 text-[9px] font-semibold uppercase tracking-wider text-gray-500">Ticket Release</div>
              <div class="break-words text-xs font-semibold text-gray-900">{{
                  formatDateTime(event?.ticket_release)
                }}
              </div>
            </div>
            <div class="rounded-md bg-gray-50 px-3 py-2">
              <div class="mb-0.5 text-[9px] font-semibold uppercase tracking-wider text-gray-500">Ticket Close</div>
              <div class="break-words text-xs font-semibold text-gray-900">{{
                  formatDateTime(event?.ticket_close)
                }}
              </div>
            </div>
          </div>
        </section>

        <!-- 02 Summary -->
        <section class="mb-5 mt-10">
          <div class="mb-3 flex items-center gap-2 border-b border-gray-200 pb-1.5">
            <span
                class="flex h-[22px] w-[22px] items-center justify-center rounded-[5px] bg-indigo-50 text-[10px] font-extrabold text-indigo-700">02</span>
            <h2 class="m-0 text-sm font-bold text-gray-900">Event Summary</h2>
          </div>

          <div class="mb-2.5 flex items-center gap-2 rounded-md bg-violet-50 px-2.5 py-2 text-[10px] text-indigo-600">
            <span>Selected Snapshot</span>
            <strong>{{ selectedSnapshot?.snapshot_name || '-' }}</strong>
            <span class="ml-auto text-[9px] text-gray-500">
          {{ formatDate(selectedSnapshot?.observed_at) }}
        </span>
          </div>

          <div class="grid grid-cols-3 gap-2.5">
            <div
                v-for="card in summaryCards"
                :key="card.label"
                class="relative flex flex-col justify-between rounded-lg border border-gray-100 bg-gradient-to-br from-white to-gray-50/50 p-3 shadow-sm"
            >
              <div class="flex items-start justify-between">
                <span class="text-[9px] font-medium tracking-wide text-gray-500 uppercase">{{ card.label }}</span>
                <div
                    class="flex h-6 w-6 items-center justify-center rounded-md"
                    :class="card.iconBg"
                >
                  <!-- Total Revenue Icon -->
                  <svg v-if="card.key === 'totalRevenue'" class="h-3.5 w-3.5" :class="card.iconColor" fill="none"
                       viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round"
                          d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                  <!-- Ticket Revenue Icon -->
                  <svg v-else-if="card.key === 'ticketRevenue'" class="h-3.5 w-3.5" :class="card.iconColor" fill="none"
                       viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round"
                          d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z"/>
                  </svg>
                  <!-- Benefit Revenue Icon -->
                  <svg v-else-if="card.key === 'benefitRevenue'" class="h-3.5 w-3.5" :class="card.iconColor" fill="none"
                       viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round"
                          d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"/>
                  </svg>
                  <!-- Ticket Sell-through Icon -->
                  <svg v-else-if="card.key === 'ticketSellThrough'" class="h-3.5 w-3.5" :class="card.iconColor"
                       fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round"
                          d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
                  </svg>
                  <!-- Benefit Sell-through Icon -->
                  <svg v-else-if="card.key === 'benefitSellThrough'" class="h-3.5 w-3.5" :class="card.iconColor"
                       fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
                  </svg>
                  <!-- Sales Velocity Icon -->
                  <svg v-else class="h-3.5 w-3.5" :class="card.iconColor" fill="none" viewBox="0 0 24 24"
                       stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                  </svg>
                </div>
              </div>
              <div class="mt-2">
                <strong class="block break-words text-[15px] font-extrabold tracking-tight text-gray-900">{{
                    formatMetric(card)
                  }}</strong>
              </div>
            </div>
          </div>
        </section>
      </div>
      <footer class="report-page-footer">
        <div class="flex items-center justify-between border-t-2 border-indigo-600 pt-3 text-[9px] text-gray-400">
          <img
              :src="mishkanLogo"
              alt="Mishkan Logo"
              class="h-5 w-auto object-contain"
              crossorigin="anonymous"
          />
          <span>Page 1 / 5</span>
        </div>
      </footer>
    </article>

    <!-- 03 Sales Details -->
    <article class="report-page report-page-start">
      <div class="report-page-body">
        <section class="mb-5">
          <div class="mb-3 flex items-center gap-2 border-b border-gray-200 pb-1.5">
            <span
                class="flex h-[22px] w-[22px] items-center justify-center rounded-[5px] bg-indigo-50 text-[10px] font-extrabold text-indigo-700">03</span>
            <h2 class="m-0 text-sm font-bold text-gray-900">Ticket & Benefit Sales</h2>
          </div>

          <div v-if="hasSalesData">
            <table class="w-full table-fixed border-collapse text-[9px]">
              <thead>
              <tr>
                <th class="w-[11%] bg-indigo-50 px-1 py-1.5 text-left font-bold text-indigo-800">Type</th>
                <th class="w-[20%] bg-indigo-50 px-1 py-1.5 text-left font-bold text-indigo-800">Item</th>
                <th class="w-[9%] bg-indigo-50 px-1 py-1.5 text-left font-bold text-indigo-800">Currency</th>
                <th class="w-[10%] bg-indigo-50 px-1 py-1.5 text-right font-bold text-indigo-800">Price</th>
                <th class="w-[10%] bg-indigo-50 px-1 py-1.5 text-right font-bold text-indigo-800">Qty</th>
                <th class="w-[9%] bg-indigo-50 px-1 py-1.5 text-right font-bold text-indigo-800">Refund</th>
                <th class="w-[10%] bg-indigo-50 px-1 py-1.5 text-right font-bold text-indigo-800">Net Sold</th>
                <th class="w-[10%] bg-indigo-50 px-1 py-1.5 text-right font-bold text-indigo-800">Revenue</th>
                <th class="w-[11%] bg-indigo-50 px-1 py-1.5 text-right font-bold text-indigo-800">Sell-Through</th>
              </tr>
              </thead>

              <tbody>
              <tr
                  class="even:bg-gray-50 break-inside-avoid"
                  v-for="(item, index) in selectedItems"
                  :key="index"
              >
                <td class="border-b border-gray-200 px-1 py-1.5 text-gray-700 break-words [overflow-wrap:anywhere]">
            <span
                class="inline-block rounded-[8px] px-1.5 py-0.5 text-[8px] font-bold capitalize"
                :class="item.type === 'ticket' ? 'bg-indigo-50 text-indigo-700' : 'bg-purple-100 text-purple-800'"
            >
              {{ item.type }}
            </span>
                </td>
                <td class="border-b border-gray-200 px-1 py-1.5 text-gray-700 break-words [overflow-wrap:anywhere]">
                  {{ item.name || '-' }}
                </td>
                <td class="border-b border-gray-200 px-1 py-1.5 text-gray-700 break-words [overflow-wrap:anywhere]">
                  {{ item.currency || '-' }}
                </td>
                <td class="border-b border-gray-200 px-1 py-1.5 text-right text-gray-700 break-words [overflow-wrap:anywhere]">
                  {{ formatNumber(item.price) }}
                </td>
                <td class="border-b border-gray-200 px-1 py-1.5 text-right text-gray-700 break-words [overflow-wrap:anywhere]">
                  {{ formatNumber(item.total_quantity) }}
                </td>
                <td class="border-b border-gray-200 px-1 py-1.5 text-right text-gray-700 break-words [overflow-wrap:anywhere]">
                  {{ formatNumber(item.refund) }}
                </td>
                <td class="border-b border-gray-200 px-1 py-1.5 text-right text-gray-700 break-words [overflow-wrap:anywhere]">
                  {{ formatNumber(getNetSold(item)) }}
                </td>
                <td class="border-b border-gray-200 px-1 py-1.5 text-right text-gray-700 break-words [overflow-wrap:anywhere]">
                  {{ formatNumber(getRevenue(item)) }}
                </td>
                <td class="border-b border-gray-200 px-1 py-1.5 text-right text-gray-700 break-words [overflow-wrap:anywhere]">
                  {{
                    item.total_quantity > 0 ? formatNumber((getNetSold(item) / number(item.total_quantity)) * 100) : '0'
                  }}%
                </td>
              </tr>
              </tbody>
            </table>
          </div>

          <p v-else class="rounded-md border border-dashed border-gray-300 p-3 text-center text-[10px] text-gray-400">
            No sales data available for this snapshot.
          </p>
        </section>
      </div>
      <footer class="report-page-footer">
        <div class="flex items-center justify-between border-t-2 border-indigo-600 pt-3 text-[9px] text-gray-400">
          <img
              :src="mishkanLogo"
              alt="Mishkan Logo"
              class="h-5 w-auto object-contain"
              crossorigin="anonymous"
          />
          <span>Page 2 / 5</span>
        </div>
      </footer>
    </article>

    <!-- 04 Sales Revenue Trend -->
    <article class="report-page report-page-start">
      <div class="report-page-body">
        <section class="mb-5">

          <!-- Section Header -->
          <div class="mb-3 flex items-center gap-2 border-b border-gray-200 pb-1.5">
          <span class="flex h-[22px] w-[22px] items-center justify-center rounded-[5px] bg-indigo-50 text-[10px] font-extrabold text-indigo-700">
            04
          </span>

            <h2 class="m-0 text-sm font-bold text-gray-900">
              Sales Revenue Trend
            </h2>
          </div>

          <p class="-mt-1 mb-3 text-[9px] text-gray-500">
            Revenue growth trajectory and progression across event snapshots.
          </p>

          <!-- Line Charts -->
          <div v-if="trendCharts.length" class="space-y-4">

            <div
                v-for="chart in trendCharts"
                :key="chart.currency"
                class="break-inside-avoid rounded-lg border border-gray-200 p-3"
            >

              <!-- Chart Header -->
              <div class="mb-3">
                <h3 class="m-0 text-[11px] font-bold text-gray-900">
                  Revenue Trend
                  <span class="ml-1 text-gray-900">
                ({{ chart.currency }})
              </span>
                </h3>
              </div>

              <!-- SVG Line Chart -->
              <svg
                  :viewBox="`0 0 ${chart.width} ${chart.height}`"
                  class="block w-full h-auto"
                  xmlns="http://www.w3.org/2000/svg"
              >

                <!-- Y-axis grid lines -->
                <g
                    v-for="tick in chart.yTicks"
                    :key="tick.value"
                >
                  <line
                      :x1="chart.padding.left"
                      :x2="chart.width - chart.padding.right"
                      :y1="tick.y"
                      :y2="tick.y"
                      stroke="#E5E7EB"
                      stroke-width="1"
                      stroke-dasharray="4 4"
                  />

                  <text
                      :x="chart.padding.left - 12"
                      :y="tick.y + 3"
                      text-anchor="end"
                      fill="#9CA3AF"
                      font-size="11"
                  >
                    {{ tick.label }}
                  </text>
                </g>

                <!-- X-axis -->
                <line
                    :x1="chart.padding.left"
                    :x2="chart.width - chart.padding.right"
                    :y1="chart.height - chart.padding.bottom"
                    :y2="chart.height - chart.padding.bottom"
                    stroke="#D1D5DB"
                    stroke-width="1"
                />

                <!-- Revenue Lines -->
                <g
                    v-for="series in chart.series"
                    :key="series.key"
                >

                  <!-- Ticket: Solid / Benefit: Dashed -->
                  <path
                      v-if="series.points.length > 0"
                      :d="series.path"
                      fill="none"
                      :stroke="series.color"
                      :stroke-dasharray="
                  series.key === 'benefit' ? '7 5' : 'none'
                "
                      stroke-width="3"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                  />

                  <!-- Data Points -->
                  <g
                      v-for="(point, index) in series.points"
                      :key="`${series.key}-${index}`"
                  >
                    <circle
                        :cx="point.x"
                        :cy="point.y"
                        r="5"
                        fill="#FFFFFF"
                        :stroke="series.color"
                        stroke-width="2.5"
                    />

                    <title>
                      {{ point.label }} -
                      {{ series.label }}:
                      {{ chart.currency }}
                      {{ formatNumber(point.value) }}
                    </title>
                  </g>
                </g>

                <!-- Horizontal X-axis Labels -->
                <g
                    v-for="(item, index) in chart.xLabels"
                    :key="index"
                >
                  <text
                      :x="item.x"
                      :y="chart.height - chart.padding.bottom + 23"
                      text-anchor="middle"
                      fill="#6B7280"
                      font-size="10"
                  >
                    <tspan
                        v-for="(line, lineIndex) in item.lines"
                        :key="lineIndex"
                        :x="item.x"
                        :dy="lineIndex === 0 ? 0 : 12"
                    >
                      {{ line }}
                    </tspan>
                  </text>
                </g>

              </svg>

              <!-- Centered Legend Below X-axis -->
              <div class="mt-3 mb-2 flex items-center justify-center gap-6 text-[10px] text-gray-600">

                <!-- Ticket -->
                <div class="flex items-center gap-2">
                  <span class="block h-[3px] w-6 rounded-full bg-[#2563EB]"></span>
                  <span class="font-medium">Ticket Revenue</span>
                </div>

                <!-- Benefit -->
                <div class="flex items-center gap-2">
                  <span class="block w-6 border-t-2 border-dashed border-[#F97316]"></span>
                  <span class="font-medium">Benefit Revenue</span>
                </div>

              </div>

            </div>
          </div>

          <!-- Empty State -->
          <p
              v-else
              class="rounded-md border border-dashed border-gray-300 p-3 text-center text-[10px] text-gray-400"
          >
            No sales trend data available.
          </p>

        </section>
      </div>

      <!-- Footer -->
      <footer class="report-page-footer">
        <div class="flex items-center justify-between border-t-2 border-indigo-600 pt-3 text-[9px] text-gray-400">
          <img
              :src="mishkanLogo"
              alt="Mishkan Logo"
              class="h-5 w-auto object-contain"
              crossorigin="anonymous"
          />
          <span>Page 3 / 5</span>
        </div>
      </footer>
    </article>

    <!-- 05 Ticket Zone Performance -->
    <article class="report-page report-page-start">
      <div class="report-page-body">
        <section class="mb-5">
          <div class="mb-3 flex items-center gap-2 border-b border-gray-200 pb-1.5">
            <span class="flex h-[22px] w-[22px] items-center justify-center rounded-[5px] bg-indigo-50 text-[10px] font-extrabold text-indigo-700">
              05
            </span>

            <h2 class="m-0 text-sm font-bold text-gray-900">
              Ticket Zone Performance
            </h2>
          </div>

          <!-- Horizontal Bar Chart -->
          <div
              v-if="zoneBarChart.rows.length"
              class="report-chart-frame report-zone-chart-frame"
          >

            <p class="mb-3 text-[9px] text-gray-500">
              Comparison of net sold and remaining inventory across ticket zones and benefits.
              Sorted by sell-through rate from highest to lowest.
            </p>

            <!-- SVG Chart -->
            <svg
                :viewBox="`0 0 ${zoneBarChart.width} ${zoneBarChart.height}`"
                class="block w-full h-auto"
                xmlns="http://www.w3.org/2000/svg"
            >

              <!-- Sell-through Header -->
              <text
                  :x="zoneBarChart.width - zoneBarChart.padding.right + 10"
                  :y="zoneBarChart.padding.top - 10"
                  fill="#64748B"
                  font-size="10"
                  font-weight="bold"
              >
                Sell-through
              </text>

              <!-- X-axis Grid Lines -->
              <g
                  v-for="tick in zoneBarChart.xTicks"
                  :key="tick.value"
              >
                <line
                    :x1="tick.x"
                    :x2="tick.x"
                    :y1="zoneBarChart.padding.top - 5"
                    :y2="zoneBarChart.padding.top + zoneBarChart.plotHeight"
                    stroke="#E5E7EB"
                    stroke-width="1"
                    stroke-dasharray="4 4"
                />

                <text
                    :x="tick.x"
                    :y="zoneBarChart.height - 32"
                    text-anchor="middle"
                    fill="#9CA3AF"
                    font-size="11"
                >
                  {{ formatNumber(tick.value) }}
                </text>
              </g>

              <!-- Chart Rows -->
              <g
                  v-for="(item, index) in zoneBarChart.rows"
                  :key="`${item.type}-${item.name}-${index}`"
              >

                <!-- Item Label -->
                <text
                    :x="zoneBarChart.padding.left - 12"
                    :y="item.y + 4"
                    text-anchor="end"
                    font-size="11"
                >
                  <tspan
                      :fill="item.color"
                      font-weight="bold"
                  >
                    {{ item.type === 'ticket' ? 'Ticket' : 'Benefit' }} ·
                  </tspan>

                  <tspan fill="#374151">
                    {{ item.displayName }}
                  </tspan>

                  <title>{{ item.name }}</title>
                </text>

                <!-- Remaining Inventory -->
                <rect
                    :x="zoneBarChart.padding.left + item.soldWidth"
                    :y="item.y - item.barHeight / 2"
                    :width="item.remainingWidth"
                    :height="item.barHeight"
                    rx="3"
                    fill="#E2E8F0"
                />

                <!-- Net Sold -->
                <rect
                    :x="zoneBarChart.padding.left"
                    :y="item.y - item.barHeight / 2"
                    :width="item.soldWidth"
                    :height="item.barHeight"
                    rx="3"
                    :fill="item.color"
                />

                <!-- Net Sold Value -->
                <text
                    v-if="item.soldWidth >= 38"
                    :x="zoneBarChart.padding.left + item.soldWidth / 2"
                    :y="item.y + 3.5"
                    text-anchor="middle"
                    fill="#FFFFFF"
                    font-size="9"
                    font-weight="bold"
                >
                  {{ formatNumber(item.netSold) }}
                </text>

                <!-- Remaining Inventory Value -->
                <text
                    v-if="item.remainingWidth >= 38"
                    :x="zoneBarChart.padding.left + item.soldWidth + item.remainingWidth / 2"
                    :y="item.y + 3.5"
                    text-anchor="middle"
                    fill="#475569"
                    font-size="9"
                    font-weight="bold"
                >
                  {{ formatNumber(item.remainingInventory) }}
                </text>

                <!-- Sell-through Percentage -->
                <text
                    :x="zoneBarChart.width - zoneBarChart.padding.right + 10"
                    :y="item.y + 4"
                    fill="#374151"
                    font-size="11"
                    font-weight="bold"
                >
                  {{ formatNumber(item.sellThrough) }}%
                </text>

                <!-- Tooltip -->
                <title>
                  {{ item.name }}
                  | Type: {{ item.type }}
                  | Net Sold: {{ formatNumber(item.netSold) }}
                  | Remaining Inventory: {{ formatNumber(item.remainingInventory) }}
                  | Total Quantity: {{ formatNumber(item.quantity) }}
                  | Sell-through: {{ formatNumber(item.sellThrough) }}%
                </title>

              </g>

              <!-- X-axis Title -->
              <text
                  :x="zoneBarChart.padding.left + zoneBarChart.plotWidth / 2"
                  :y="zoneBarChart.height - 8"
                  text-anchor="middle"
                  fill="#6B7280"
                  font-size="10"
              >
                Quantity
              </text>

            </svg>

            <!-- Centered Legend -->
            <div class="mt-4 mb-3 flex flex-wrap items-center justify-center gap-x-6 gap-y-2 text-[10px] text-gray-600">

              <div class="flex items-center gap-2">
                <span class="h-2.5 w-2.5 rounded-sm bg-[#2563EB]"></span>
                <span class="font-medium">Ticket Net Sold</span>
              </div>

              <div class="flex items-center gap-2">
                <span class="h-2.5 w-2.5 rounded-sm bg-[#F97316]"></span>
                <span class="font-medium">Benefit Net Sold</span>
              </div>

              <div class="flex items-center gap-2">
                <span class="h-2.5 w-2.5 rounded-sm bg-[#E2E8F0] border border-gray-300"></span>
                <span class="font-medium">Remaining Inventory</span>
              </div>

            </div>

            <!-- Calculation Note -->
            <div class="report-zone-chart-note">
          <span class="font-semibold text-gray-600">
            Sell-through Rate
          </span>

              <span>
            Net Sold ÷ Total Quantity × 100%
          </span>
            </div>

          </div>

          <!-- Empty State -->
          <p
              v-else
              class="rounded-md border border-dashed border-gray-300 p-3 text-center text-[10px] text-gray-400"
          >
            No ticket or benefit sales data available.
          </p>

        </section>
      </div>

      <!-- Footer -->
      <footer class="report-page-footer">
        <div class="flex items-center justify-between border-t-2 border-indigo-600 pt-3 text-[9px] text-gray-400">
          <img
              :src="mishkanLogo"
              alt="Mishkan Logo"
              class="h-5 w-auto object-contain"
              crossorigin="anonymous"
          />

          <span>Page 4 / 5</span>
        </div>
      </footer>
    </article>

    <!-- 06 Audience Demographics -->
    <article class="report-page report-page-start">
      <div class="report-page-body">
        <section class="mb-5">
          <div class="mb-3 flex items-center gap-2 border-b border-gray-200 pb-1.5">
            <span
                class="flex h-[22px] w-[22px] items-center justify-center rounded-[5px] bg-indigo-50 text-[10px] font-extrabold text-indigo-700">06</span>
            <h2 class="m-0 text-sm font-bold text-gray-900">Audience Demographics</h2>
          </div>

          <div v-if="hasDemographics">
            <p class="-mt-1 mb-2.5 text-[9px] text-gray-500">
              Audience distribution based on the Closed snapshot.
            </p>

            <div class="grid grid-cols-1 gap-3">
              <!-- Gender -->
              <div class="break-inside-avoid rounded-md border border-gray-200 p-2.5">
                <h3 class="mb-2.5 mt-0 text-[11px] font-bold text-gray-900">Gender Distribution</h3>

                <div
                    v-for="item in genderData"
                    :key="item.label"
                    class="mb-2"
                >
                  <div class="mb-1 flex justify-between text-[9px] text-gray-600">
                    <span>{{ item.label }}</span>
                    <strong class="font-bold text-gray-900">{{ formatNumber(item.value) }}%</strong>
                  </div>

                  <div class="h-[7px] w-full overflow-hidden rounded-full bg-gray-100">
                    <div
                        class="h-full rounded-full"
                        :style="{
                    width: `${Math.min(100, Math.max(0, item.value))}%`,
                    backgroundColor: item.color
                  }"
                    ></div>
                  </div>
                </div>
              </div>

              <!-- Age -->
              <div class="break-inside-avoid rounded-md border border-gray-200 p-2.5">
                <h3 class="mb-2.5 mt-0 text-[11px] font-bold text-gray-900">Age Distribution</h3>

                <div
                    v-for="item in ageData"
                    :key="item.label"
                    class="mb-2"
                >
                  <div class="mb-1 flex justify-between text-[9px] text-gray-600">
                    <span>{{ item.label }}</span>
                    <strong class="font-bold text-gray-900">{{ formatNumber(item.value) }}%</strong>
                  </div>

                  <div class="h-[7px] w-full overflow-hidden rounded-full bg-gray-100">
                    <div
                        class="h-full rounded-full"
                        :style="{
                    width: `${Math.min(100, Math.max(0, item.value))}%`,
                    backgroundColor: item.color
                  }"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <p v-else class="rounded-md border border-dashed border-gray-300 p-3 text-center text-[10px] text-gray-400">
            Audience demographics are available after the Closed snapshot is recorded.
          </p>
        </section>

      </div>
      <footer class="report-page-footer">
        <div class="flex justify-between items-center border-t-2 border-indigo-600 pt-3 text-[9px] text-gray-400">
          <img
              :src="mishkanLogo"
              alt="Mishkan Logo"
              class="h-5 w-auto object-contain"
              crossorigin="anonymous"
          />
          <span>Page 5 / 5</span>
        </div>
      </footer>
    </article>
  </div>
</template>

<style>
.report-page {
  box-sizing: border-box;
  width: 190mm;

  /* Leave a small buffer for PDF page rounding */
  min-height: 266mm;

  display: flex;
  flex-direction: column;
  padding: 10mm;
  background: #ffffff;
}

.report-page-body {
  flex: 1 1 auto;
  min-height: 0;
}

.report-page-footer {
  flex: 0 0 auto;
  margin-top: auto;
  padding-top: 6mm;
}

.report-chart-frame {
  width: 100%;
  min-height: 0;
  overflow: hidden;
}

.report-zone-chart-frame {
  overflow: visible;
  padding-bottom: 4mm;
}

.report-zone-chart-frame svg {
  display: block;
  overflow: visible;
}

.report-zone-chart-note {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 6px;
  width: 100%;
  box-sizing: border-box;
  margin-top: 12px;
  margin-bottom: 8px;
  padding: 9px 12px;
  border-radius: 6px;
  background: #F8FAFC;
  color: #64748B;
  font-size: 9px;
  line-height: 1.6;
  text-align: center;
  overflow: visible;
  break-inside: avoid;
}
</style>
