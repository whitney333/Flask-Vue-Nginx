<script setup>
import { computed, onMounted, ref } from 'vue';
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

    // ==========================================================================
    // TODO: Mini chart currently shows Instagram followers as a proxy for popularity.
    // FUTURE: Fetch from artist_score_history collection once implemented.
    // ==========================================================================
    const fetchChart = async () => {
        // Skip if no instagramId available
        if (!props.value.instagramId) {
            loadingBar.value = false
            series.value = []
            return
        }

        loadingBar.value = true
        try {
            const today = new Date().toISOString().slice(0, 10)
            const response = await axios.get('/instagram/v1/follower', {
                params: {
                    artist_id: props.value.instagramId,
                    date_end: today,
                    filter: '28d'  // 30 days for mini chart
                },
                timeout: 10000
            })

            const result = response.data?.data || []
            if (result.length === 0) {
                series.value = []
                loadingBar.value = false
                return
            }

            follower.value = result
            index_number.value = result[result.length - 1]?.follower || 0

            const formattedData = result.map(e => ({
                x: e.datetime,
                y: e.follower,
            }))

            series.value = [{
                name: 'Popularity',
                data: formattedData,
            }]
        } catch (err) {
            series.value = []
        } finally {
            loadingBar.value = false
        }
    }
    const handleToArtist = () => {
        router.push(`/artist/${props.value.artistId}/${props.value.artistName}`)

    }
    onMounted(() => {
        fetchChart()
    })

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
                <v-img
                    :src="props.value.icon"
                    :alt="props.value.artistName"
                >
                    <template v-slot:placeholder>
                        <v-icon icon="mdi-account-circle"></v-icon>
                    </template>
                </v-img>
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
            <span>{{ props.value.popularity ? props.value.popularity.toLocaleString('en-US') : '-' }}</span>
            </v-col>
            <v-col
            cols="3">
            <template v-if="series.length > 0 && series[0].data?.length > 0">
                <AreaCharts width="90%" height="60%" :series="series" :chartOptions="chartOptions" />
            </template>
            <template v-else-if="!loadingBar">
                <span class="text-grey text-caption">No trend data</span>
            </template>
            </v-col>
            <v-col
            cols="1">
            <v-btn variant="plain" icon="mdi-chevron-right"></v-btn>
            </v-col>

        </v-row>
    </v-card>

</template>