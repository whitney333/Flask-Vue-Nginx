<script setup>
import { computed } from 'vue';
import VueApexCharts from 'vue3-apexcharts';

const props = defineProps({
  ticketItems: {
    type: Array,
    default: () => []
  },
  title: {
    type: String,
    default: 'Ticket Zone Performance'
  }
});

// formatting function
const formatNum = (val) => Number(val || 0).toLocaleString('en-US');

const chartOptions = computed(() => ({
  chart: {
    type: 'bar',
    height: '100%',
    stacked: true,
    toolbar: { show: false }
  },
  plotOptions: {
    bar: {
      horizontal: true,
      borderRadius: 6,
      barHeight: '55%'
    }
  },
  dataLabels: {
    enabled: false
  },
  stroke: {
    show: true,
    width: 1,
    colors: ['#fff']
  },
  xaxis: {
    categories: props.ticketItems.map(item => item.name || 'Zone'),
    labels: {
      style: {
        fontSize: '12px',
        fontWeight: 'bold',
        fontFamily: 'Cairo, sans-serif'
      }
    }
  },
  yaxis: {
    labels: {
      style: {
        fontSize: '12px',
        fontWeight: 'bold',
        fontFamily: 'Cairo, sans-serif'
      }
    }
  },
  tooltip: {
    shared: true,
    intersect: false,
    y: {
      formatter: (val) => `${formatNum(val)} tickets`
    }
  },
  legend: {
    position: 'bottom',
    horizontalAlign: 'center',
    fontSize: '12px',
    fontFamily: 'Cairo, sans-serif'
  },
  colors: ['#4F46E5', '#E5E7EB'] // Net Sold (Indigo), Remaining (Light Gray)
}));

const series = computed(() => {
  if (!props.ticketItems || props.ticketItems.length === 0) {
    return [];
  }

  const netSoldData = props.ticketItems.map(item => Number(item.net_sold) || 0);
  const remainingData = props.ticketItems.map(item => {
    const total = Number(item.total_quantity) || 0;
    const netSold = Number(item.net_sold) || 0;
    return Math.max(0, total - netSold);
  });

  return [
    { name: 'Net Sold', data: netSoldData },
    { name: 'Remaining Inventory', data: remainingData }
  ];
});
</script>

<template>
  <div class="bg-white rounded-xl shadow p-6 border border-gray-200 w-full h-full flex flex-col justify-between">
    <!-- Header -->
    <div class="flex items-center justify-between pb-3 border-b border-gray-100 mb-4">
      <div class="flex items-center gap-3 min-w-0">
        <div class="p-2 bg-indigo-50 text-indigo-600 rounded-lg">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        </div>
        <div>
          <h3 class="text-lg font-semibold text-gray-800">{{ props.title }}</h3>
          <p class="text-xs text-gray-400">Comparing net sold vs remaining inventory per zone</p>
        </div>
      </div>
    </div>

    <div class="w-full h-72 sm:h-80">
      <VueApexCharts
        width="100%"
        height="100%"
        type="bar"
        :options="chartOptions"
        :series="series">
      </VueApexCharts>
    </div>
  </div>
</template>
