<script setup>
import axios from '@/axios';
import { watch, computed, onMounted, ref } from 'vue';
import { useUserStore } from "@/stores/user.js";

const props = defineProps({
  value: {
    type: Object,
    required: true
  },
  campaignId: {
    type: String,
    required: true
  },
  campaignData: {
    type: Array,
    required: true,
    default: () => []
  }
})

const userStore = useUserStore()
const loadingBar = ref(true)
const series = ref([])
const labels = ref([])
const hasFetched = ref(false)
const chartOptions = ref({})

//fetch data
const fetchData = async () => {
  if (!Array.isArray(props.campaignData) || props.campaignData.length === 0) {
    series.value = []
    labels.value = []
    loadingBar.value = false
    return
  }

  try {
    loadingBar.value = true
    // convert API data to series/labels
    series.value = props.campaignData.map(item => item.count)
    labels.value = props.campaignData.map(item => item.name)

    // console.log("series:", series.value)
    // console.log("labels:", labels.value)

    chartOptions.value = {
      chart: {
        type: 'pie',
        toolbar: {show: false},
        animations: { enabled: true }
      },
      labels: labels.value || [],
      dataLabels: {
        enabled: true,
        style: {
          fontSize: '14px',
          fontWeight: 'bold',
          fontFamily: 'Cairo, sans-serif',
        },
        dropShadow: {enabled: false},
      },
      responsive: [{
        breakpoint: 600,
        options: {
          chart: {
            height: 'auto'
          },
          legend: {
            position: 'bottom',
            fontSize: '11px',
            itemMargin: { vertical: 2 },
          }
        }
      }],
      legend: {
        show: true,
        fontSize: '14px',
        fontWeight: '500',
        fontFamily: 'Cairo, sans-serif',
        position: 'bottom',
        horizontalAlign: 'left',
        markers: { width: 10, height: 10 },
        itemMargin: { horizontal: 5, vertical: 2 },
        labels: { colors: '#555' },
      },
      colors: props.value.colors || [],
      plotOptions: {
        pie: {
          donut: {size: '70%'},
          dataLabels: {offset: -10}
        }
      }
    }
    loadingBar.value = false
  } catch (err) {
    console.error(err);
    loadingBar.value = false
  }
}

// fetch data on mounted
watch(() => props.campaignData, fetchData, { deep: true })
onMounted(fetchData)

</script>

<template>
    <v-card :loading="loadingBar"
            class="flex flex-col items-center justify-center p-4"
            style="width: 100%;">
      <template v-slot:title>
        <div class="text-left mb-2 font-semibold text-base text-gray-800">
          <span>
            {{ $t(props.value.title) }}
          </span>
          <v-tooltip
              location="bottom"
              :text="props.value.tooltipText">
            <template v-slot:activator="{ props }">
              <v-icon
                  size="20"
                  :class="['mx-1']"
                  v-bind="props"
                  icon="mdi-information-outline"
              ></v-icon>
            </template>
          </v-tooltip>
        </div>
      </template>
      <v-card-text
          class="flex items-center justify-center w-full p-0"
          style="padding: 0;"
      >
        <apexchart
            :id="campaign_percent_chart"
            width="100%"
            height="auto"
            type="pie"
            :series="series"
            :options="chartOptions"
            style="max-width: 100%; width: 100%;">
        </apexchart>
      </v-card-text>
    </v-card>
</template>

<style scoped>
.v-card {
  transition: transform 0.2s ease;
}
.v-card:hover {
  transform: translateY(-2px);
}
</style>
