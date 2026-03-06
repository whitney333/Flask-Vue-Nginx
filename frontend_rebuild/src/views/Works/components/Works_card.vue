<script setup>
    import {computed, nextTick, onMounted, ref, watch} from 'vue';
    import axios from '@/axios';
    import { useArtistStore } from "@/stores/artist.js";
    import { useUserStore} from "@/stores/user.js";
    import { useAuthStore } from "@/stores/auth.js";

    const props = defineProps({
        value: Object,
        colors: Object,
        iconSrc: String,
        end: String
    })
    const canFetch = computed(() => {
      return (
          props.value &&
          !props.value.disabled &&
          typeof props.value.fetchURL === 'string' &&
          props.value.fetchURL.length > 0
      )
    })
    const userStore = useUserStore()
    const artistStore = useArtistStore()
    const authStore = useAuthStore()
    const allowedRanges = ref([])
    const maxRange = ref("28d")
    const RANGE_MAP = {
      one_month: "28d",
      three_months: "90d",
      six_months: "180d",
      one_year: "365d"
    }
    const ranges = [
      { key: "one_month", label: "1M" },
      { key: "three_months", label: "3M" },
      { key: "six_months", label: "6M" },
      { key: "one_year", label: "1Y" },
    ]
    const series = ref([])
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

    const fetchData = async () => {
        try {
            loadingBar.value = true

            const res = await axios.get(props.value.fetchURL,
            {headers: {
              Authorization: `Bearer ${authStore.idToken}`
              },
              params: {
                date_end: props.end,
                range: props.value.range,
                artist_id: artistStore.artistId
              }})

          // return data
          data.value = res.data[props.value.fetchFollowerType] || []

          // if no data
          if (!Array.isArray(data.value) || data.value.length === 0) {
            series.value = []
            allowedRanges.value = res.data?.meta?.allowed_ranges || ["28d"]
            return
          }
          // calculation
          const lastIndex = data.value.length - 1
          const monthIndex = data.value.length > 30 ? data.value.length - 30 : 0
          const threeMonthIndex = data.value.length > 90 ? data.value.length - 90 : 0
          const sixMonthIndex = data.value.length > 180 ? data.value.length - 180 : 0
          const oneYearIndex = data.value.length > 365 ? data.value.length - 365 : 0


          index_number.value =
              data.value[lastIndex]?.[props.value.followerDataType] ?? 0
          last_month_data.value =
              data.value[monthIndex]?.[props.value.followerDataType] ?? 0
          three_months.value =
              data.value[threeMonthIndex]?.[props.value.fetchDateType] ??
              data.value[0][props.value.fetchDateType]
          six_months.value =
              data.value[sixMonthIndex]?.[props.value.fetchDateType] ??
              data.value[0][props.value.fetchDateType]
          one_year.value =
              data.value[oneYearIndex]?.[props.value.fetchDateType] ??
              data.value[0][props.value.fetchDateType]

          first_day.value = data.value[0][props.value.fetchDateType]
          latest_date.value = data.value[lastIndex][props.value.fetchDateType]
          one_month.value = data.value[monthIndex][props.value.fetchDateType]

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
          } else if (allowedRanges.value.includes("90d")) {
            selection.value = "one_year"
            safeZoom(one_year.value)
          } else {
            selection.value = "one_month"
            safeZoom(one_month.value)
          }

            // update the series with axios data

        } catch (e) {
            console.error(e);
        } finally {
           loadingBar.value = false
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

    onMounted(() => {
      if (!canFetch.value) {
        loadingBar.value = false
        return
      }
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

    const disabledText = computed(() => {
      switch (props.value?.disabledReason) {
        case 'NO_SPOTIFY_ID':
          return 'Spotify data not available'
        case 'NO_MELON_ID':
          return 'Melon data not available'
        default:
          return 'Data not available'
      }
    })

    watch(
        () => [canFetch.value, artistStore.artistId, props.end],
        ([canFetchNow]) => {
          if (!canFetchNow) {
            loadingBar.value = false
            return
          }
          fetchData()
        },
        {immediate: true}
    )

</script>

<template>
  <v-card
    :loading="loadingBar"
    width="400"
    height="500"
    class="relative"
  >
    <!-- ===== Disabled Overlay ===== -->
    <div
      v-if="props.value?.disabled"
      class="absolute inset-0 z-10 flex items-center justify-center bg-white/70"
    >
      <span class="text-caption text-grey">
        {{ disabledText }}
      </span>
    </div>

    <!-- ===== Title ===== -->
    <template #title>
      <div class="d-flex align-center">
        <v-img
          :src="props.iconSrc"
          max-height="30"
          max-width="30"
          class="mr-3"
        />
        <span>{{ $t(props.value.title) }}</span>

        <v-tooltip
          v-if="props.value.tooltipText"
          location="bottom"
          :text="props.value.tooltipText"
        >
          <template #activator="{ props: tooltipProps }">
            <v-icon
              v-bind="tooltipProps"
              size="20"
              class="mx-1"
              icon="mdi-information-outline"
            />
          </template>
        </v-tooltip>
      </div>
    </template>

    <!-- ===== Content ===== -->
    <template #text>
      <v-divider class="mb-3" />

      <!-- ===== Header numbers ===== -->
      <div class="d-flex align-center justify-space-between">
        <span class="text-h5 font-weight-bold">
          {{
            props.value.percentageData
              ? `${Number(index_number).toLocaleString()}%`
              : formatNumber
          }}
        </span>

        <!-- ===== Range buttons ===== -->
        <div>
          <v-btn
            v-for="range in ranges"
            :key="range.key"
            size="x-small"
            variant="outlined"
            color="blue-grey-darken-2"
            rounded
            class="mx-1"
            :active="selection === range.key"
            :disabled="isRangeDisabled(range.key)"
            @click="updateData(range.key)"
          >
            {{ range.label }}
          </v-btn>
        </div>
      </div>

      <!-- ===== Delta + last updated ===== -->
      <div class="mt-1 d-flex align-center justify-space-between">
        <div>
          <v-btn
            readonly
            slim
            density="compact"
            variant="outlined"
            :color="
              indexDifference() > 0
                ? 'success'
                : indexDifference() < 0
                ? 'error'
                : undefined
            "
          >
            <span class="font-weight-bold">
              {{
                `${indexDifference() > 0 ? '+' : ''}${indexDifference()
                  .toFixed(2)
                  .toLocaleString()}%`
              }}
            </span>
          </v-btn>

          <span class="text-caption mx-1">
            {{ $t('Past Month') }}
          </span>
        </div>

        <span class="text-caption text-grey">
          {{ `${$t('Last updated')}: ${latest_date}` }}
        </span>
      </div>

      <!-- ===== Chart ===== -->
      <apexchart
        :id="props.value.chart"
        ref="chart"
        class="mt-2"
        width="100%"
        height="142%"
        type="line"
        :options="chartOptions"
        :series="series"
      />
    </template>
  </v-card>
</template>
