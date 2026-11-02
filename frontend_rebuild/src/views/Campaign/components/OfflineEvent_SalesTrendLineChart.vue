<script setup>
import { ref, watch, nextTick, onMounted } from 'vue';
import VueApexCharts from 'vue3-apexcharts';

const props = defineProps({
  snapshots: {
    type: Array,
    default: () => []
  },
  title: {
    type: String,
    default: 'Sales Revenue Trend'
  },
  iconSrc: {
    type: String,
    default: ''
  },
  colors: {
    type: Array,
    default: () => ['#4F46E5', '#9333EA'] // Ticket: Indigo, Benefit: Purple
  }
});

const chart = ref(null);
const series = ref([]);
const loadingBar = ref(false);

const latest_date = ref('');
const currentTotalRevenue = ref(0);
const revenueDifference = ref(0);

// 金額縮寫與千分位格式化
const formatNumFunc = (value) => {
  const num = Number(value || 0);
  const units = [
    { value: 1e9, suffix: 'B' },
    { value: 1e6, suffix: 'M' },
    { value: 1e3, suffix: 'K' },
  ];

  const unit = units.find(u => Math.abs(num) >= u.value);

  if (unit) {
    const formatted = (num / unit.value).toFixed(1).replace(/\.0$/, '');
    return `$${formatted}${unit.suffix}`;
  }

  return `$${num.toLocaleString('en-US')}`;
};

const chartOptions = ref({
  chart: {
    id: 'sales-trend-line-chart',
    height: 320,
    width: '100%',
    type: 'line',
    zoom: {
      autoScaleYaxis: true
    },
    toolbar: {
      tools: {
        download: true,
        selection: true,
        zoom: true,
        zoomin: false,
        zoomout: false,
        pan: true,
        reset: true
      }
    }
  },
  grid: {
    row: {
      colors: ['#FFFFFF', 'transparent'],
      opacity: 0.5
    },
    padding: {
      bottom: 20
    }
  },
  dataLabels: {
    enabled: false,
  },
  stroke: {
    curve: 'smooth',
    width: 3
  },
  xaxis: {
    type: 'datetime',
    labels: {
      rotate: -45,
      trim: true,
      style: {
        fontSize: '12px',
        fontWeight: 'bold',
        fontFamily: 'Cairo, sans-serif'
      },
      datetimeFormatter: {
        year: 'yyyy',
        month: "MMM 'yy",
        day: 'dd MMM',
        hour: 'HH:mm'
      }
    },
    tickAmount: 4,
    tooltip: {
      enabled: false
    }
  },
  legend: {
    fontSize: '12px',
    fontWeight: '500',
    fontFamily: 'Cairo, sans-serif',
    position: 'bottom',
    horizontalAlign: 'center'
  },
  yaxis: [
    {
      labels: {
        style: {
          fontSize: '12px',
          fontWeight: 'bold',
          fontFamily: 'Cairo, sans-serif'
        },
        formatter: (val) => formatNumFunc(val)
      }
    }
  ],
  colors: props.colors,
  responsive: [
    {
      breakpoint: 768,
      options: {
        chart: { height: 280 },
        xaxis: {
          tickAmount: 3,
          labels: { rotate: 0, style: { fontSize: '10px' } }
        }
      }
    }
  ]
});

// 解析 snapshots 轉換為 Chart 數據與計算指標
const processSnapshotData = () => {
  loadingBar.value = true;

  if (!props.snapshots || props.snapshots.length === 0) {
    series.value = [];
    currentTotalRevenue.value = 0;
    revenueDifference.value = 0;
    loadingBar.value = false;
    return;
  }

  // 依觀察時間排序
  const sortedSnapshots = [...props.snapshots].sort(
    (a, b) => new Date(a.observed_at) - new Date(b.observed_at)
  );

  const ticketSeriesData = [];
  const benefitSeriesData = [];

  sortedSnapshots.forEach(snapshot => {
    const timestamp = new Date(snapshot.observed_at).getTime();
    let ticketRev = 0;
    let benefitRev = 0;

    if (snapshot.ticket_items && Array.isArray(snapshot.ticket_items)) {
      snapshot.ticket_items.forEach(item => {
        const price = Number(item.price) || 0;
        const sold = Number(item.sold) || 0;
        const refund = Number(item.refund) || 0;
        const netSold = Math.max(0, sold - refund);
        const revenue = netSold * price;

        if (item.type === 'ticket') {
          ticketRev += revenue;
        } else if (item.type === 'benefit') {
          benefitRev += revenue;
        }
      });
    }

    ticketSeriesData.push({ x: timestamp, y: ticketRev });
    benefitSeriesData.push({ x: timestamp, y: benefitRev });
  });

  series.value = [
    { name: 'Ticket Revenue', data: ticketSeriesData },
    { name: 'Benefit Revenue', data: benefitSeriesData }
  ];

  const lastIndex = sortedSnapshots.length - 1;
  const latestSnapshot = sortedSnapshots[lastIndex];
  latest_date.value = latestSnapshot ? latestSnapshot.observed_at : '';

  const latestTotal = (ticketSeriesData[lastIndex]?.y || 0) + (benefitSeriesData[lastIndex]?.y || 0);
  const prevTotal = lastIndex > 0 ? (ticketSeriesData[lastIndex - 1]?.y || 0) + (benefitSeriesData[lastIndex - 1]?.y || 0) : latestTotal;

  currentTotalRevenue.value = latestTotal;
  revenueDifference.value = prevTotal > 0 ? ((latestTotal - prevTotal) / prevTotal) * 100 : 0;

  loadingBar.value = false;
};

watch(
  () => props.snapshots,
  () => {
    processSnapshotData();
  },
  { deep: true, immediate: true }
);

onMounted(async () => {
  await nextTick();
  processSnapshotData();
});
</script>

<template>
<div class="bg-white rounded-xl shadow p-6 border border-gray-200 w-full h-full flex flex-col justify-between">
    <div>
      <!-- Header -->
      <div class="flex items-center justify-between pb-3 border-b border-gray-100 mb-4">
        <div class="flex items-center gap-3 min-w-0">
          <div class="p-2 bg-indigo-50 text-indigo-600 rounded-lg flex-shrink-0">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
          </div>
          <div class="min-w-0">
            <h3 class="text-lg font-semibold text-gray-800 truncate">{{ props.title }}</h3>
            <p class="text-xs text-gray-400">Revenue growth trajectory across snapshot history</p>
          </div>
        </div>
      </div>
      <!--  index -->
      <div class="flex items-center justify-between gap-3 mb-2">
        <div>
          <span class="text-2xl font-bold text-gray-900">
            {{ formatNumFunc(currentTotalRevenue) }}
          </span>
          <span
            class="ml-2 px-2 py-0.5 text-xs font-semibold rounded-full inline-flex items-center"
            :class="revenueDifference >= 0 ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'">
            {{ revenueDifference >= 0 ? '+' : '' }}{{ revenueDifference.toFixed(2) }}%
          </span>
        </div>
        <div v-if="latest_date" class="text-right">
          <span class="text-[11px] text-gray-400">
            Last updated: {{ latest_date }}
          </span>
        </div>
      </div>
    </div>

    <div class="w-full h-72 sm:h-80">
      <VueApexCharts
        ref="chart"
        width="100%"
        height="100%"
        type="line"
        :options="chartOptions"
        :series="series">
      </VueApexCharts>
    </div>
  </div>
</template>
