<script setup>
import { computed, ref } from 'vue';
import axios from '@/axios';
import AreaCharts from '@/components/AreaCharts.vue'
import { useRoute, useRouter } from 'vue-router';

    const props = defineProps({
        value: Object,
    })
    const router = useRouter()
    const loadingBar = ref(false)
    const index_number =  ref("")
    const selection = ref('one_month')
    const series = ref([])
    const chartOptions = ref({})
    const follower = ref({})
    const formatNumber = computed(() => formatNumFunc(index_number.value))

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
            width: 1.5,
            dashArray: [0, 2]
            },
            xaxis: {
            // categories: [],
                type: 'datetime',
                show: false,
                labels: {
                    show: false,
                    datetimeFormatter: {
                        year: 'yyyy',
                        month: 'MMM \'yy',
                        day: 'dd MMM',
                        hour: 'HH:mm'
                    }
                },
                axisBorder: {
                    show: false
                },
                axisTicks: {
                    show: false
                },
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
                show: false,
                labels: {
                    show: false,
                    formatter: formatNumFunc,
                },
                axisBorder: {
                    show: false
                },
                axisTicks: {
                    show: false
                }
            }
            ],
            colors: props.value.colors,
            grid: {
            show: false
            }
        }

    const fetchChart = async () => {
        loadingBar.value = true
        const data = await axios.get(`/api/instagram/chart/follower`, {setTimeout: 10000})
        follower.value = data.data['result']
        index_number.value = follower.value[follower.value.length - 1]['follower_count']

        let formattedData = follower.value.map((e, i) => {
            return {
                x: e['datetime'],
                y: e['follower_count'],
            };
        });
        // update the series with axios data
        series.value = [
            {
                name: 'Popularity',
                data: formattedData,
            }
        ]
        loadingBar.value = false
    }
    const handleToArtist = () => {
        console.log(props.value.artistId);
        router.push(`/artist/${props.value.artistId}/${props.value.artistName}`)

    }
    fetchChart()

</script>

<template>
    <v-card
    :loading="loadingBar"
    hover
    @click="handleToArtist"
    :class="['px-3', 'py-1', 'my-3']">
        <v-row
        align="center"
        justify="center">
            <v-col
            cols="1">
            <span>{{ `#${props.value.rank}` }}</span>
            </v-col>
            <v-col
            cols="1">
            <v-avatar color="info">
                <v-icon icon="mdi-account-circle"></v-icon>
            </v-avatar>

            </v-col>
            <v-col
            cols="2">
                <span>{{ props.value.artistName}}</span>
            </v-col>
            <v-col
            cols="3">
                <v-chip :color="props.value.type == 'Actor' ? 'blue' : 'purple'">{{ props.value.type}}</v-chip>
            </v-col>
            <v-col
            cols="1">
            <span>{{ props.value.popularity.toLocaleString('en-US') }}</span>
            </v-col>
            <v-col
            cols="3">
            <AreaCharts width="90%" height="60%" :series="series" :chartOptions="chartOptions" ></AreaCharts>
            </v-col>
            <v-col
            cols="1">
            <v-btn variant="plain" icon="mdi-chevron-right"></v-btn>
            </v-col>

        </v-row>
    </v-card>

</template>