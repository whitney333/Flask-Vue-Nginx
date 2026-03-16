<!-- Dashboard Top Statics Card -->
<script setup>
import axios from '@/axios';
import { watch, computed, ref } from 'vue';
import AreaCharts from '@/components/AreaCharts.vue';
import { useArtistStore } from '@/stores/artist';

const props = defineProps({
  value: {type: Object, required: true}

})

const artistStore = useArtistStore()
const latest_date = ref("")
const latest_follower_count =  ref("")
const past_month_follower_count =  ref("")
const index_number =  ref("")
const selection = ref('one_month')
const loadingBar = ref(true)
const series = ref([])
const chartOptions = ref({})
const follower = ref({})

const platformId = computed(() => {
  return artistStore.artist?.[props.value.platformKey]
})

const hasPlatform = computed(() =>
    !!platformId.value
)

const formatNumFunc = (value) => {
  if (String(Math.round(value)).length < 4) {
    const res = Number(value).toLocaleString();
    return props.value.percentageData ? res + "%" : res
  } else if (String(Math.round(value)).length < 7) {
    const res = Number(value / 1000).toLocaleString() + 'K';
    return props.value.percentageData ? res + "%" : res
  } else if (String(Math.round(value)).length < 10) {
    const res = Number(value / 1000000).toLocaleString() + 'M';
    return props.value.percentageData ? res + "%" : res
  } else {
    const res = Number(value / 1000000000).toLocaleString() + 'B';
    return props.value.percentageData ? res + "%" : res
  }
}

const formattedIndexNumber = computed(() => formatNumFunc(index_number.value || 0))


chartOptions.value = {
  chart: {
    height: '100%',
    width: '100%',
    type: 'area',
    group: 'homepage',
    toolbar: {
      tools: {
        download: false,
        selection: false,
        zoom: false,
        zoomin: false,
        zoomout: false,
        pan: false,
        reset: false
      }
    }
  },
  dataLabels: {
    enabled: false,
  },
  stroke: {
    curve: 'smooth',
    width: 2,
    dashArray: [0, 2]
  },
  xaxis: {
    // categories: [],
    type: 'datetime',
    labels: {
      // format: 'MM/dd',
      rotate: -45,
      trim: true,
      style: {
        fontSize: '12px',
        fontWeight: 'bold',
        fontFamily: 'Cairo, sans-serif',
      },
      datetimeFormatter: {
        year: 'yyyy',
        month: 'MMM \'yy',
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
    fontSize: '14px',
    fontWeight: '500',
    fontFamily: 'Cairo, sans-serif',
    position: 'top',
    horizontalAlign: 'left'
  },
  yaxis: [
    {
      tickAmount: 4,
      labels: {
        style: {
          fontSize: '12px',
          fontWeight: '500',
          fontFamily: 'Cairo, sans-serif',
        },
        formatter: formatNumFunc,
      }
    },
  ],
  colors: props.value.colors,
  grid: {
    show: false
  }
}

const getData = async () => {
  if (!hasPlatform.value) {
    series.value = [{
      name: props.value.type,
      data: []
    }]
    index_number.value = 0
    loadingBar.value = false
    return
  }

    loadingBar.value = true
    // clean old data
    series.value = []
    index_number.value = 0

    try {
      const data = await axios.get(props.value.fetchURL, { timeout: 10000 })
      follower.value = data.data[props.value.fetchFollowerType] || []

      if (!follower.value.length) {
        series.value = [{name: props.value.type, data: []}]
        return
      }

      index_number.value = follower.value[follower.value.length - 1][props.value.followerDataType]

      let formattedData = follower.value.map((e, i) => {
        return {
          x: e[props.value.fetchDateType],
          y: e[props.value.followerDataType],
        };
      });

      //update the series with axios data
      series.value = [
        {
          name: props.value.type,
          data: formattedData,
        }
      ]

    } catch (err) {
      console.error("Error fetching data:", err)
    } finally {
      loadingBar.value = false
    }
}

watch(
  [platformId, () => props.value.fetchURL, () => artistStore.artistId],
  () => {
    getData()
  },
  { immediate: true }
)
</script>

<template>
  <v-card
    :loading="loadingBar"
    width="300"
    height="250"
    class="db-ts-card relative rounded-2xl"
  >
    <template #title>
      <div class="flex items-center gap-3">
        <v-img
          :src="props.value.iconSrc"
          max-height="28"
          max-width="28"
          :class="{ 'opacity-40': !hasPlatform }"
        />

        <div>
          <div class="text-xl font-bold">
            {{ formattedIndexNumber }}
          </div>
          <div class="text-xs text-gray-500">
            {{ props.value.type }}
          </div>
        </div>
      </div>
    </template>

    <v-card-text class="pa-0 relative h-[160px]">
      <AreaCharts
        width="100%"
        height="100%"
        :series="series"
        :chartOptions="chartOptions"
      />

      <!-- overlay -->
      <div
        v-if="!hasPlatform"
        class="absolute inset-0 flex flex-col items-center justify-center
               bg-white/80 backdrop-blur-sm text-center px-4"
      >
        <v-icon icon="mdi-link-off" size="28" />
        <span class="text-xs text-gray-500">
          This artist doesn't have a {{ props.value.platform }} account
        </span>
      </div>
    </v-card-text>
  </v-card>
</template>

<style scoped>
.db-ts-card {
  transition: transform 220ms cubic-bezier(0.22, 1, 0.36, 1), box-shadow 220ms ease;
  box-shadow: 0 3px 10px rgba(15, 23, 42, 0.06);
  will-change: transform;
}

.db-ts-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 28px rgba(15, 23, 42, 0.14);
}

.toolbar .index_number {
        padding-left: 20px;
        padding-right: 10px;
        color: #000000;
        display: inline-flex;
        font-size: 24px;
        font-weight: bold;
        font-family: 'Cairo', sans-serif;
    }
</style>
