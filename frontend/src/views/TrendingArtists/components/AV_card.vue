
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

    watch(selectDate, updateData(selectDate.value.title))
</script>

<template>
    <v-card
    :loading="loadingBar"
    flat>
        <template v-slot:title>
            <div :class="['d-flex', 'align-center', 'justify-space-between']">
                <div>
                    <span :class="['text-h4']">
                        {{ props.value.title }}
                        <v-tooltip
                        :text="props.value.tooltipText">
                            <template v-slot:activator="{ props }">
                                <v-icon
                                size="25"
                                v-bind="props"
                                icon="mdi-information-outline"
                                ></v-icon>
                            </template>
                        </v-tooltip>
                    </span>
                </div>
                <v-select
                    :maxWidth="150"
                    label="Standard"
                    :items="selectDates"
                    background-color="amber-lighten-1"
                    variant="outlined"
                    single-line
                    density="compact"
                    return-object
                    v-model="selectDate"
                    @update:modelValue="updateData(selectDate.value)"
                    item-title="title"
                >
                </v-select>

            </div>
        </template>
        <template v-slot:text>
            <apexchart
                :id="props.value.chart"
                ref="chart"
                width="100%"
                height="200%"
                type="line"
                :options="chartOptions" 
                :series="series">
            </apexchart>
        </template>
    </v-card>
</template>