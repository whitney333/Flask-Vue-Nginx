<!-- Dashboard Top Statics Card -->
<script setup>
import axios from '@/axios';
import { watch, computed, onMounted, ref } from 'vue';
import AreaCharts from '@/components/AreaCharts.vue';

const props = defineProps({
  value: {type: Object, required: true}

})

const latest_date = ref("")
const latest_follower_count =  ref("")
const past_month_follower_count =  ref("")
const index_number =  ref("")
const selection = ref('one_month')
const loadingBar = ref(true)
const series = ref([])
const chartOptions = ref({})
const follower = ref({})

const formatNumber = computed(() =>
    {
      if (String(index_number.value).length < 4) {
        return Number(index_number.value).toLocaleString();
      } else if (String(index_number.value).length < 7) {
        return Number(index_number.value / 1000).toLocaleString() + 'K';
      } else if (String(index_number.value).length < 10) {
        return Number(index_number.value / 1000000).toLocaleString() + 'M';
      } else {
        return Number(index_number.value / 1000000000).toLocaleString() + 'B';
      }
    }
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
    loadingBar.value = true

    // clean old data
    series.value = []
    index_number.value = 0

    try {
      const data = await axios.get(props.value.fetchURL, {setTimeout: 10000})
      follower.value = data.data[props.value.fetchFollowerType]
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

    // follower.value = data.data[props.value.fetchFollowerType]
    // index_number.value = follower.value[follower.value.length - 1][props.value.followerDataType]

    // let formattedData = follower.value.map((e, i) => {
    //     return {
    //         x: e[props.value.fetchDateType],
    //         y: e[props.value.followerDataType],
    //     };
    // });

    // update the series with axios data
    // series.value = [
    //     {
    //         name: props.value.type,
    //         data: formattedData,
    //     }
    // ]
}


  onMounted(() => {
    getData(props.value.fetchURL)
  })

  watch(
    () => props.value.fetchURL,
    async (newUrl, oldUrl) => {
      if (newUrl && newUrl !== oldUrl) {
        // console.log("🔄 fetchURL changed:", newUrl)
        series.value = []
        index_number.value = 0
        try {
          await getData(newUrl)
        } catch (err) {
          console.log("Error in watcher callback: ", err)
        }

      }
    },
    {immediate: true} // execute when first enter
  )
</script>

<template>
    <v-card :loading="loadingBar" hover :width="300" :height="250">
        <template v-slot:title >
            <v-row>
                <v-col class="flex-grow-1">
                    <a :href="props.value.iconHref">
                        <v-img
                        :src="props.value.iconSrc"
                        max-height="30px"
                        max-width="30px"
                        class="mr-3"
                        ></v-img>
                    </a>
                </v-col>
                <v-col class="flex-grow-10">
                    <span class="px-1" style="font-size: 24px; font-weight: bold; font-family: 'Cairo', sans-serif;">
                        {{ formatNumber }}
                    </span>
                    <span style="font-size: 12px;">
                        {{ $t(props.value.type) }}
                    </span>
                </v-col>
            </v-row>
        </template>
        <v-card-text :class="['pa-0']">
            <AreaCharts width="100%" height="100%" :series="series" :chartOptions="chartOptions" ></AreaCharts>
        </v-card-text>
    </v-card>
    
</template>

<style scoped>
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