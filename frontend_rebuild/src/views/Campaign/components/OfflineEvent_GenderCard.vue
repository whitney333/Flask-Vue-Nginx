<script setup>
import { ref, watch } from 'vue';
import VueApexCharts from 'vue3-apexcharts';

const props = defineProps({
  snapshot: {
    type: Object,
    default: null
  },
  title: {
    type: String,
    default: 'Gender Distribution'
  }
});

const series = ref([]);

const genderLabels = ['Male', 'Female', 'Other', 'Unknown'];

const genderColors = [
  '#4B5563', // Male
  '#9CA3AF', // Female
  '#D1D5DB'  // Other
];

const genderLegend = [
   { label: 'Male', key: 'male', color: '#4B5563' },
   { label: 'Female', key: 'female', color: '#9CA3AF' },
   { label: 'Other', key: 'other', color: '#D1D5DB' }
];

// Check whether the selected snapshot is Closed
const isClosedSnapshot = () => {
  return (
    props.snapshot?.snapshot_type === 'closed' ||
    props.snapshot?.snapshot_name === 'Closed'
  );
};

// Format percentage
const formatPercentage = (value) => {
  return `${Number(value || 0).toFixed(1)}%`;
};

// Get gender percentage
const getGenderValue = (index) => {
  return Number(series.value[index] || 0);
};

// Process snapshot data
const processSnapshotData = () => {
  if (!isClosedSnapshot()) {
    series.value = [];
    return;
  }

  const data = props.snapshot?.gender_distribution || {};

  series.value = [
    Number(data.male) || 0,
    Number(data.female) || 0,
    Number(data.other) || 0
  ];
};

// ApexCharts options
const chartOptions = ref({
  chart: {
    id: 'gender-distribution-chart',
    type: 'donut',
    height: 280,
    toolbar: {
      show: false
    },
    fontFamily: 'inherit',
    animations: {
      enabled: true,
      easing: 'easeinout',
      speed: 500
    }
  },

  labels: genderLabels,
  colors: genderColors,

  stroke: {
    show: true,
    width: 4,
    colors: ['#FFFFFF']
  },

  plotOptions: {
    pie: {
      expandOnClick: false,
      donut: {
        size: '72%',
        background: 'transparent',
        labels: {
          show: true,

          name: {
            show: true,
            fontSize: '12px',
            fontWeight: 500,
            color: '#9CA3AF',
            offsetY: -8
          },

          value: {
            show: true,
            fontSize: '24px',
            fontWeight: 700,
            color: '#4F46E5',
            offsetY: 4,
            formatter: (value) => formatPercentage(value)
          },

          total: {
            show: true,
            showAlways: true,
            label: 'Total',
            fontSize: '12px',
            fontWeight: 500,
            color: '#9CA3AF',
            formatter: () => '100%'
          }
        }
      }
    }
  },

  dataLabels: {
    enabled: false
  },

  legend: {
    show: false
  },

  tooltip: {
    enabled: true,
    theme: 'light',
    y: {
      formatter: (value) => formatPercentage(value)
    }
  },

  states: {
    hover: {
      filter: {
        type: 'darken',
        value: 0.08
      }
    },
    active: {
      filter: {
        type: 'none'
      }
    }
  },

  responsive: [
    {
      breakpoint: 768,
      options: {
        chart: {
          height: 260
        },
        plotOptions: {
          pie: {
            donut: {
              size: '68%'
            }
          }
        }
      }
    }
  ]
});

// Watch snapshot changes
watch(
  () => props.snapshot,
  () => {
    processSnapshotData();
  },
  {
    deep: true,
    immediate: true
  }
);
</script>

<template>
  <div
    v-if="isClosedSnapshot()"
    class="bg-white rounded-2xl shadow-sm p-6 border border-gray-200 w-full h-full flex flex-col"
  >
    <!-- Header -->
    <div
      class="flex items-center justify-between pb-4 border-b border-gray-100 mb-4"
    >
      <div class="flex items-center gap-3 min-w-0">
        <div
          class="p-2.5 bg-indigo-50 text-indigo-600 rounded-xl flex-shrink-0"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="1.8"
              d="M16 21v-2a4 4 0 00-4-4H6a4 4 0 00-4 4v2m6-10a4 4 0 100-8 4 4 0 000 8zm14 10v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"
            />
          </svg>
        </div>

        <div class="min-w-0">
          <h3 class="text-base font-semibold text-gray-800 truncate">
            {{ title }}
          </h3>
          <p class="text-xs text-gray-400 mt-1">
            Audience breakdown by gender
          </p>
        </div>
      </div>
    </div>

    <!-- Chart and Legend -->
    <div
      class="flex flex-col sm:flex-row items-center justify-center gap-5 flex-1 min-h-[260px]"
    >
      <!-- Donut Chart -->
      <div class="w-full sm:w-1/2 max-w-[280px]">
        <VueApexCharts
          v-if="series.length && series.some(value => value > 0)"
          width="100%"
          height="280"
          type="donut"
          :options="chartOptions"
          :series="series"
        />

        <div
          v-else
          class="h-[260px] flex flex-col items-center justify-center gap-2 text-gray-400"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="w-8 h-8 text-gray-300"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="1.5"
              d="M12 3v9l7.5 4.5M12 3a9 9 0 100 18 9 9 0 000-18z"
            />
          </svg>

          <p class="text-sm">
            No gender distribution data available.
          </p>
        </div>
      </div>

      <!-- Legend -->
      <div class="w-full sm:w-1/2 flex flex-col gap-4">
        <div
          v-for="(item, index) in genderLegend"
          :key="item.key"
          class="flex items-center justify-between gap-3"
        >
          <div class="flex items-center gap-2.5 min-w-0">
            <span
              class="w-3 h-3 rounded-full flex-shrink-0"
              :style="{ backgroundColor: item.color }"
            ></span>

            <span class="text-sm text-gray-600 font-medium truncate">
              {{ item.label }}
            </span>
          </div>

          <span class="text-sm font-semibold text-gray-800 tabular-nums">
            {{ formatPercentage(getGenderValue(index)) }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>
