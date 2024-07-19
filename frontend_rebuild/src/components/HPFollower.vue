<script setup>
import axios from '@/axios';
import { computed, ref } from 'vue';
import AreaCharts from './AreaCharts.vue';

const props = defineProps({
    type: String,
    fetchURL: String,
    iconHref: String,
    iconSrc: String,
    fetchFollowerType: String,
    followerDataType: String,
    fetchDateType: String,
    colors: Object,
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
          width: 3,
          dashArray: [0, 2]
        },
        xaxis: {
          // categories: [],
          type: 'datetime',
          labels: {
            format: 'MM/dd',
            rotate: -45,
            trim: true,
            style: {
              fontSize: '12px',
              fontWeight: '500',
              fontFamily: 'Cairo, sans-serif',
            }
          },
          tickAmount: 4,
          tooltip: {
            enabled: false
          }
        },
        tooltip: {
          theme: 'light',
          custom: function ({series, seriesIndex, dataPointIndex, w}) {
            var data = w.globals.initialSeries[seriesIndex].data[dataPointIndex];
            return (
                '<div class="arrow_box">' +
                new Date(data.x).toDateString() +
                "<ul>" +
                "<span>" +
                "<li>" +
                // w.globals.labels[dataPointIndex] +
                `${props.type}: ` +
                (series[0][dataPointIndex]).toLocaleString() +
                "</li>" +
                "</span>" +
                "</ul>" +
                "</div>"
            );
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
              formatter: function (value) {
                if (String(value).length < 4) {
                  return Number(value).toLocaleString();
                } else if (String(value).length < 7) {
                  return Number(value / 1000).toLocaleString() + 'K';
                } else if (String(value).length < 10) {
                  return Number(value / 1000000).toLocaleString() + 'M';
                } else {
                  return Number(value / 1000000000).toLocaleString() + 'B';
                }
              },
            }
          },
        ],
        colors: props.colors,
        grid: {
          show: false
        }
    }

const getData = async () => {
    loadingBar.value = true
    const data = await axios.get(props.fetchURL, {setTimeout: 10000})
    follower.value = data.data[props.fetchFollowerType]
    index_number.value = follower.value[follower.value.length - 1][props.followerDataType]

    let formattedData = follower.value.map((e, i) => {
        return {
            x: e[props.fetchDateType],
            y: e[props.followerDataType],
        };
    });
    // update the series with axios data
    series.value = [
        {
            name: props.type,
            data: formattedData,
        }
    ]
    loadingBar.value = false
}

const fetchAll = async () => {
    await getData()
    console.log("series", series);
    console.log("chartOptions", chartOptions);
}
fetchAll()

</script>

<template>
    <v-card :loading="loadingBar" hover :width="300" :height="250" rounded="20" >
        <template v-slot:title >
            <v-row>
                <v-col class="flex-grow-1">
                    <a :href="props.iconHref">
                        <v-img
                        :src="props.iconSrc"
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
                        {{ $t(props.type) }}
                    </span>
                </v-col>
            </v-row>
        </template>
        <v-card-text :class="['pa-0']">
            <AreaCharts :series="series" :chartOptions="chartOptions" ></AreaCharts>
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