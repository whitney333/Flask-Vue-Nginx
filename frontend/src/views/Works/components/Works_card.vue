<script setup>
    import { computed, onMounted, ref } from 'vue';
    import axios from '@/axios';
    const props = defineProps({
        value: Object,
        colors: Object,
        iconSrc: String,
        end: String
    })
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
            const res = await axios.get(`${props.value.fetchURL}?end=${props.end}&range=${props.value.range}`, {setTimeout: 10000})
            
            data.value = res.data[props.value.fetchFollowerType]
            latest_date.value = data.value[data.value.length - 1][props.value.fetchDateType]
            first_day.value = data.value[0][props.value.fetchDateType]
            if (data.value.length > 30) {
                one_month.value = data.value[data.value.length - 30][props.value.fetchDateType]
            } else {
                one_month.value = data.value[0][props.value.fetchDateType]
            }
            if (data.value.length > 90) {
                three_months.value = data.value[data.value.length - 90][props.value.fetchDateType]
            } else {
                three_months.value = data.value[0][props.value.fetchDateType]
            }
            if (data.value.length > 180) {
                six_months.value = data.value[data.value.length - 180][props.value.fetchDateType]
            } else {
                six_months.value = data.value[0][props.value.fetchDateType]
            }
            
            index_number.value = data.value[data.value.length - 1][props.value.followerDataType]
            last_month_data.value = data.value[data.value.length - 30][props.value.followerDataType]

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
            // update the series with axios data
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

    const indexDifference = () => {
        return ((index_number.value - last_month_data.value) / last_month_data.value) * 100
    }

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
                        @click="updateData('all')" 
                        :active="selection === 'all'"
                        :class="['mx-1']"
                    >
                    ALL
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
