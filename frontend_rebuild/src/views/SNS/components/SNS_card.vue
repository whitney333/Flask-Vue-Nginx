<script setup>
    import { computed, onMounted, ref, watch } from 'vue';
    import axios from '@/axios';
    import { useUserStore } from "@/stores/user.js";
    import { useArtistStore } from "@/stores/artist.js";
    import { nextTick } from 'vue'

    const userStore = useUserStore()
    const artistStore = useArtistStore()
    const props = defineProps({
        value: Object,
        colors: Object,
        iconSrc: String,
    })
    const series = ref([])

    const date_end = new Date().toISOString().slice(0, 10);
    const allowedRanges = ref([])
    const maxRange = ref("28d")
    const RANGE_MAP = {
      one_month: "28d",
      three_months: "90d",
      six_months: "180d",
      one_year: "365d"
    }
    const latest_date = ref("")
    const index_number = ref("")
    const last_month_data = ref("")
    const loadingBar = ref(true)
    const data = ref({})
    const first_day = ref('')
    const one_month = ref('')
    const three_months = ref('')
    const six_months = ref('')
    const one_year = ref('')
    const chart = ref(null)
    const selection = ref("all")
    const chartOptions = ref({})
    const formatNumber = computed(() =>
        {
            return formatNumFunc(index_number.value)
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
            id: props.value.chart,
            height: '100%',
            width: '100%',
            type: 'line',
            group: props.value.chart,
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
            colors: ['#FFFFFF', 'transparent'], // takes an array which will be repeated on columns
            opacity: 0.5
            },
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
            fontSize: '12px',
            fontWeight: '400',
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
                        fontFamily: 'Cairo, sans-serif',
                    },
                    formatter: formatNumFunc,
                }
            },
        ],
        colors: props.colors,
    }

    if (props.value.secondChat) {
        const temp = chartOptions.value;
        temp.yaxis = [
            {
                labels: {
                    style: {
                        fontSize: '12px',
                        fontWeight: 'bold',
                        fontFamily: 'Cairo, sans-serif',
                    },
                    formatter: formatNumFunc
                }
            },
            {
                opposite: true,
                labels: {
                    style: {
                        fontSize: '12px',
                        fontWeight: 'bold',
                        fontFamily: 'Cairo, sans-serif',
                    },
                    formatter: formatNumFunc
                }
            }
        ]
        chartOptions.value = temp
    }
    // helper function: calculate data length
    const getStartByLength = (len) => {
      if (!data.value.length) return null
      const idx = Math.max(data.value.length - len, 0)
      return data.value[idx][props.value.fetchDateType]
    }

    const fetchData = async () => {
      try {
        loadingBar.value = true
        const res = await axios.get(props.value.fetchURL,
            {headers: {
              Authorization: `Bearer ${userStore.firebaseToken}`
              }})
        // console.log("fetchURL", props.value.fetchURL)
        if (!res || !res.data) {
          console.warn("Response is empty or invalid");
          data.value = []
          latest_date.value = null
          first_day.value = null
          one_month.value = null
          three_months.value = null
          six_months.value = null
          one_year.value = null
          index_number.value = null
          last_month_data.value = null
          series.value = []
          loadingBar.value = false
          return
        }

        data.value = res.data.data || []
        if (!data.value.length) return

        if (data.value.length === 0) {
          console.warn("No data found for the given type")
          latest_date.value = null
          first_day.value = null
          one_month.value = null
          three_months.value = null
          six_months.value = null
          one_year.value = null
          index_number.value = null
          last_month_data.value = null
          series.value = []
          loadingBar.value = false
          return
        }

        latest_date.value = data.value[data.value.length - 1][props.value.fetchDateType]
        first_day.value = data.value[0][props.value.fetchDateType]

        one_month.value = getStartByLength(28)
        three_months.value = getStartByLength(90)
        six_months.value = getStartByLength(180)
        one_year.value = getStartByLength(365)
        index_number.value = data.value[data.value.length - 1][props.value.followerDataType]
        last_month_data.value = data.value.length > 7 ? data.value[data.value.length - 7][props.value.followerDataType] : index_number.value

        const formattedData = data.value.map((e, i) => {
          return {
            x: e[props.value.fetchDateType],
            y: e[props.value.followerDataType],
          };
        });


        if (props.value.secondChat) {
          const formattedData2 = data.value.map((e, i) => {
            return {
              x: e[props.value.secondChat.fetchDateType],
              y: e[props.value.secondChat.followerDataType],
            };
          })

          series.value = [
            {
              name: props.value.type,
              data: formattedData,
            },
            {
              name: props.value.secondChat.type,
              data: formattedData2
            }
          ]
        } else {
          series.value = [
            {
              name: props.value.type,
              data: formattedData,
            }
          ]
        }

        // set up allowed ranges（UI button enable/disable）
        allowedRanges.value = res.data?.meta?.allowed_ranges || ["28d"]
        const isPremium = res.data?.meta?.is_premium
        // console.log("allowedRanges:", allowedRanges.value, "isPremium:", isPremium)

        // set up zoom
        await nextTick()
        if (allowedRanges.value.includes("365d")) {
          selection.value = "one_year"
          safeZoom(one_year.value)
        } else if (allowedRanges.value.includes("180d")) {
          selection.value = "six_months"
          safeZoom(six_months.value)
        } else {
          selection.value = "one_month"
          safeZoom(one_month.value)
        }

        // update the series with axios data
        loadingBar.value = false
      } catch (e) {
        console.error(e);
      }
    }

    const safeZoom = (start) => {
      if (!start || !latest_date.value) return
      chart.value?.zoomX(
          new Date(start).getTime(),
          new Date(latest_date.value).getTime()
      )
    }

    const updateData = async (timeline) => {
      selection.value = timeline
      if (!chart.value) return

      switch (timeline) {
        case "one_month":
          chart.value.zoomX(
              new Date(one_month.value).getTime(),
              new Date(latest_date.value).getTime()
          )
          break

        case "three_months":
          chart.value.zoomX(
              new Date(three_months.value).getTime(),
              new Date(latest_date.value).getTime()
          )
          break

        case "six_months":
          chart.value.zoomX(
              new Date(six_months.value).getTime(),
              new Date(latest_date.value).getTime()
          )
          break

        case "one_year":
          chart.value.zoomX(
              new Date(one_year.value).getTime(),
              new Date(latest_date.value).getTime()
          )
          break

      }
    }

    onMounted( () => {
        fetchData()
    })

    const indexDifference = () => {
        return ((index_number.value - last_month_data.value) / last_month_data.value) * 100
    }

    // check and disable range button
    const isRangeDisabled = (timeline) => {
      const range = RANGE_MAP[timeline]
      if (!range) return true
      return !allowedRanges.value.includes(range)
    }

    watch(
        () => props.value.fetchURL,
        (newURL) => {
          // clean old data
          series.value = []
          if (newURL) {
            fetchData(newURL);
          }
        }
    );
</script>

<template>
    <v-card :loading="loadingBar" width="400" height="500">
        <template v-slot:title>
            <div :class="['d-flex', 'align-center']">
                <v-img
                :src="props.iconSrc"
                max-height="30px"
                max-width="30px"
                :class="['mr-3']"
                ></v-img>
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
        <template v-slot:text>
            <v-divider></v-divider>
            <br />
            <div :class="['d-flex', 'align-center', 'justify-space-between']">
                <span :class="['text-h5', 'font-weight-bold']"> {{ props.value.percentageData ?  `${Number(index_number).toLocaleString()}%` : formatNumber }}</span>
                <div>
                    <v-btn
                        size='x-small'
                        variant='outlined'
                        color="blue-grey-darken-2"
                        dark
                        rounded
                        @click="updateData('one_month')" 
                        :active="selection === 'one_month'"
                        :disabled="isRangeDisabled('one_month')"
                        :class="['mx-1']"
                    >
                    1M
                    </v-btn>
                    <v-btn
                        size='x-small'
                        variant='outlined'
                        color="blue-grey-darken-2"
                        dark
                        rounded
                        @click="updateData('three_months')" 
                        :active="selection === 'three_months'"
                        :disabled="isRangeDisabled('three_months')"
                        :class="['mx-1']"
                    >
                    3M
                    </v-btn>
                    <v-btn
                        size='x-small'
                        variant='outlined'
                        color="blue-grey-darken-2"
                        dark
                        rounded
                        @click="updateData('six_months')" 
                        :active="selection === 'six_months'"
                        :disabled="isRangeDisabled('six_months')"
                        :class="['mx-1']"
                    >
                    6M
                    </v-btn>
                    <v-btn
                        size='x-small'
                        variant='outlined'
                        color="blue-grey-darken-2"
                        dark
                        rounded
                        @click="updateData('one_year')"
                        :active="selection === 'one_year'"
                        :disabled="isRangeDisabled('one_year')"
                        :class="['mx-1']"
                    >
                    1Y
                    </v-btn>
                </div>
            </div>
            <div :class="['mt-1','d-flex', 'align-center', 'justify-space-between']">
                <div >
                    <v-btn
                    readonly
                    slim
                    density="compact"
                    variant="outlined"
                    :color="indexDifference() > 0 ? 'success' : indexDifference() < 0 ? 'error' : '' "
                    >
                    <span :class="['font-weight-bold']">
                        {{ ` ${indexDifference() > 0 ? "+" : ""}${(indexDifference()).toFixed(2).toLocaleString()}%` }}
                    </span>
                    </v-btn>
                    <span :class="['text-caption', 'mx-1']"> {{ ` ${$t('Past Month')}` }}</span>
                </div>
                <div>
                    <span style="color: #757575;" :class="['text-caption']"> {{ `${$t('Last updated')}: ${latest_date}` }}</span>
                </div>
            </div>
            <!-- <v-btn variant="outlined" rounded="pill" id="one_year" 
                @click="updateData('one_year')" :class="{active: selection==='one_year'}"
                >
            1Y
            </v-btn> -->
            <!-- <br /> -->
    
            <apexchart
                :id="props.value.chart"
                :class="['mt-2']"
                ref="chart"
                width="100%"
                height="142%"
                type="line" 
                :options="chartOptions" 
                :series="series">
            </apexchart>
        </template>

    </v-card>


</template>
