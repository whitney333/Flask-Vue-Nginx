
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
    default: 'Age Distribution'
  }
});

const series = ref([]);

const ageLabels = ['10s', '20s', '30s', '40s', '50+'];

const ageColors = [
  '#E0E7FF', // 10s - Indigo 100
  '#C7D2FE', // 20s - Indigo 200
  '#818CF8', // 30s - Indigo 400
  '#6366F1', // 40s - Indigo 500
  '#4F46E5'  // 50+ - Indigo 600
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

// Process snapshot data
const processSnapshotData = () => {
  if (!isClosedSnapshot()) {
    series.value = [];
    return;
  }

  const data = props.snapshot?.age_distribution || {};

  series.value = [
    Number(data.age_10s) || 0,
    Number(data.age_20s) || 0,
    Number(data.age_30s) || 0,
    Number(data.age_40s) || 0,
    Number(data.age_50_plus) || 0
  ];
};

// ApexCharts options
const chartOptions = ref({
  chart: {
    id: 'age-distribution-chart',
    type: 'bar',
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

  colors: ageColors,

  plotOptions: {
    bar: {
      horizontal: true,
      distributed: true,
      borderRadius: 6,
      borderRadiusApplication: 'end',
      barHeight: '42%',
      dataLabels: {
        position: 'top'
      }
    }
  },

  dataLabels: {
    enabled: true,
    textAnchor: 'start',
    formatter: (value) => formatPercentage(value),
    offsetX: 8,
    style: {
      fontSize: '12px',
      fontWeight: 600,
      colors: ['#4F46E5']
    },
    background: {
      enabled: false
    }
  },

  xaxis: {
    categories: ageLabels,
    min: 0,
    max: 100,
    tickAmount: 5,
    labels: {
      formatter: (value) => `${value}%`,
      style: {
        colors: '#9CA3AF',
        fontSize: '11px'
      }
    },
    axisBorder: {
      show: false
    },
    axisTicks: {
      show: false
    }
  },

  yaxis: {
    labels: {
      style: {
        colors: '#4B5563',
        fontSize: '13px',
        fontWeight: 500
      }
    }
  },

  grid: {
    borderColor: '#E5E7EB',
    strokeDashArray: 4,
    xaxis: {
      lines: {
        show: true
      }
    },
    yaxis: {
      lines: {
        show: false
      }
    },
    padding: {
      left: 8,
      right: 30
    }
  },

  fill: {
    opacity: 1
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
          bar: {
            barHeight: '50%'
          }
        },
        dataLabels: {
          style: {
            fontSize: '10px'
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
              d="M3 3v18h18M7 14l4-4 4 4 6-7"
            />
          </svg>
        </div>

        <div class="min-w-0">
          <h3 class="text-base font-semibold text-gray-800 truncate">
            {{ title }}
          </h3>
          <p class="text-xs text-gray-400 mt-1">
            Audience breakdown by age group
          </p>
        </div>
      </div>
    </div>

    <!-- Chart -->
    <div class="flex-1 min-h-[260px]">
      <VueApexCharts
        v-if="series.length && series.some(value => value > 0)"
        width="100%"
        height="280"
        type="bar"
        :options="chartOptions"
        :series="[{ name: 'Percentage', data: series }]"
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
            d="M3 3v18h18M7 14l4-4 4 4 6-7"
          />
        </svg>

        <p class="text-sm">
          No age distribution data available.
        </p>
      </div>
    </div>
  </div>
</template>
