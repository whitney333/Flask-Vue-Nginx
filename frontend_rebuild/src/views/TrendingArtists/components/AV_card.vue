<!-- Artist View Chart card -->

<script setup>
import axios from '@/axios';
import { computed, onMounted, ref, watch } from 'vue';
    const props = defineProps({
        value: Object
    })

    const loadingBar = ref(false)
    const index_number =  ref("")
    const selection = ref('one_month')
    const series = ref([])
    const data = ref("")
    const latest_date = ref("")
    const first_day = ref("")
    const chart = ref(null)
    const one_month = ref("")
    const three_months = ref("")
    const six_months = ref("")
    const one_year = ref("")
    const last_month_data = ref("")
    const chartOptions = ref({})
    const follower = ref({})
    const isMetricCard = computed(() => props.value?.mode === 'metric' || !props.value?.fetchURL)
    const formatNumber = computed(() =>
        {
            return formatNumFunc(index_number.value)
        }
    )
    
    const selectDates = [
        {
            title: "All",
            value: 'all'
        },
        {
            title: "1 Month",
            value: 'one_month'
        },
        {
            title: "3 Months",
            value: 'three_months'
        },
        {
            title: "6 Months",
            value: 'six_months'
        },
        {
            title: "1 Year",
            value: 'one_year'
        },
    ]

    const selectDate = ref({
        title: "All",
        value: "all"
    })
    const formatNumFunc = (value) => {
        const number = Number(value ?? 0)

        if (!Number.isFinite(number) || number === 0) {
            return '-'
        }

        if (String(Math.round(number)).length < 4) {
            const res = number.toLocaleString('en-US', { maximumFractionDigits: 2 });
            return props.value.percentageData ? res + "%" : res
        } else if (String(Math.round(number)).length < 7) {
            const res = Number(number / 1000).toLocaleString('en-US', { maximumFractionDigits: 2 }) + 'K';
            return props.value.percentageData ? res + "%" : res
        } else if (String(Math.round(number)).length < 10) {
            const res = Number(number / 1000000).toLocaleString('en-US', { maximumFractionDigits: 2 }) + 'M';
            return props.value.percentageData ? res + "%" : res
        } else {
            const res = Number(number / 1000000000).toLocaleString('en-US', { maximumFractionDigits: 2 }) + 'B';
            return props.value.percentageData ? res + "%" : res
        }
    }


    chartOptions.value = {
            chart: {
            height: '100%',
            width: '100%',
            type: 'markers',
            group: 'homepage',
            toolbar: {
                tools: {
                download: true,
                selection: false,
                zoom: true,
                zoomin: false,
                zoomout: false,
                pan: false,
                reset: true
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
            markers: {
                size: 0,
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
                fontFamily: 'Cairo',
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
              row: {
                colors: ['#FFFFFF', 'transparent'], // takes an array which will be repeated on columns
                opacity: 0.5
              },
            }
        }
    const fetchData = async () => {
        if (isMetricCard.value) {
            return
        }

        try {
            loadingBar.value = true
            const res = await axios.get(props.value.fetchURL, {setTimeout: 10000})
            data.value = res.data[props.value.fetchFollowerType]
            latest_date.value = data.value[data.value.length - 1][props.value.fetchDateType]
            first_day.value = data.value[0][props.value.fetchDateType]
            one_month.value = data.value[data.value.length - 30 > 0 ? data.value.length - 30 : 0][props.value.fetchDateType]
            three_months.value = data.value[data.value.length - 90 > 0 ? data.value.length - 90 : 0][props.value.fetchDateType]
            six_months.value = data.value[data.value.length - 180 > 0 ? data.value.length - 180 : 0][props.value.fetchDateType]
            one_year.value = data.value[data.value.length - 365 > 0 ? data.value.length - 365 : 0][props.value.fetchDateType]

            index_number.value = data.value[data.value.length - 1][props.value.followerDataType]
            last_month_data.value = data.value[data.value.length - 30 > 0 ? data.value.length - 30 : 0][props.value.followerDataType]

            const formattedData = data.value.map((e, i) => {
                return {
                    x: e[props.value.fetchDateType],
                    y: e[props.value.followerDataType],
                };
            });
            series.value = [
                    {
                        name: props.value.type,
                        data: formattedData,
                    }
                ]
            loadingBar.value = false
        } catch (e) {
            console.error(e);
        }
    }

    const updateData = (timeline) => {
        if (isMetricCard.value || !chart.value) {
            return
        }

        selection.value = timeline

        switch (timeline) {
        case 'one_month':
            chart.value.zoomX(
                new Date(one_month.value).getTime(),
                new Date(latest_date.value).getTime()
            )
            break
        case 'three_months':
            chart.value.zoomX(
                new Date(three_months.value).getTime(),
                new Date(latest_date.value).getTime()
            )
            break
        case 'six_months':
            chart.value.zoomX(
                new Date(six_months.value).getTime(),
                new Date(latest_date.value).getTime()
            )
            break
        case 'one_year':
            chart.value.zoomX(
                new Date(one_year.value).getTime(),
                new Date(latest_date.value).getTime()
            )
            break
        case 'all':
            chart.value.zoomX(
                new Date(first_day.value).getTime(),
                new Date(latest_date.value).getTime()
            )
        }
    }  
    onMounted(() => {
        fetchData()
    })

    watch(selectDate, (newValue) => {
        updateData(newValue.value)
    })
</script>

<template>
  <v-card flat :loading="loadingBar" class="pa-4">

    <!-- HEADER -->
    <div class="flex items-center justify-between mb-4">

      <div class="flex items-center gap-3">

        <v-avatar
          v-if="value.icon"
          :color="value.color || 'grey'"
          size="40"
          variant="tonal"
        >
          <v-icon :icon="value.icon" />
        </v-avatar>

        <div class="text-lg font-semibold">
          {{ value.title }}
        </div>

      </div>

      <!-- SELECT -->
      <v-select
        v-if="isChartCard"
        v-model="selectDate"
        :items="selectDates"
        item-title="title"
        return-object
        density="compact"
        variant="outlined"
        hide-details
        style="max-width: 150px"
        @update:modelValue="updateData(selectDate.value)"
      />

    </div>

    <!-- METRIC BLOCK -->
    <div v-if="isMetricCard" class="text-4xl font-black">
      {{ formatNumFunc(value.value) }}
    </div>

    <!-- CHART BLOCK -->
    <div v-if="isChartCard" class="mt-2">
      <apexchart
        ref="chart"
        width="100%"
        height="260"
        type="line"
        :options="chartOptions"
        :series="series"
      />
    </div>

  </v-card>
</template>