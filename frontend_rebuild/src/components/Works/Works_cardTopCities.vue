<script setup>
    import axios from '@/axios';
    import { ref } from 'vue';

    const props = defineProps({
        iconSrc: String,
        colors: Object,
        value: Object
    })

    const citiesData = ref([])
    const cities = ref([])
    const lastUpdate = ref("")
    const series = ref([])
    const loadingCard = ref(true)
    const chartOptions = ref({})
    const monthlyListeners = ref(0)

    const getData = async () => {
        try{
            loadingCard.value = true
            const res = await axios.get('/api/spotify/top-city', {setTimeout: 10000})
            
            citiesData.value = res.data.result
            lastUpdate.value = res.data.result[0].date
            monthlyListeners.value = res.data.result[0].monthly_listeners
            // console.log(res.data.result[0]);
            
            
            const formattedData = citiesData.value.map((e, i) => {
                return {
                    x: e.city,
                    y: e.city_listener
                }
            })
            cities.value = citiesData.value.map((val) => val.city)
            series.value = [
                {
                    name: "Popularity",
                    data: formattedData,
                }
            ]
            loadingCard.value = false
        }catch(e) {
            console.error(e);
        }
    }
        
        chartOptions.value = {
            chart: {
                type: 'bar',
                height: 350
            },
            plotOptions: {
                bar: {
                    borderRadius: 4,
                    borderRadiusApplication: 'around',
                    horizontal: true,
                }
            },
            // dataLabels: {
            //     enabled: true,
            //     offsetX: -6,
            //     style: {
            //         fontSize: '12px',
            //         colors: ['#fff']
            //     }
            // },
            dataLabels: {
                enabled: false
            },

            colors: [
                function ({ value, seriesIndex, dataPointIndex, w }) {
                    
                    if (dataPointIndex % 2) {
                        return '#191414';
                    } else {
                        return '#1db954';
                    }
                }
            ],
            xaxis: {
                categories: cities.value
            }
        }

    getData()
</script>

<template>
    <v-card :loading="loadingCard" width="400" height="500">
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
            <div :class="['d-flex', 'justify-space-between', 'align-center']">
                <div>
                    <span :class="['text-h5', 'font-weight-bold']"> {{ monthlyListeners }}</span>
                    <span style="font-size: 12px;">{{ ` ${$t('Monthly Listeners')}` }} </span>
                </div>

                <span style="color: #757575;" :class="['text-caption']"> {{ `${$t('Last updated')}: ${lastUpdate}` }}</span>
            </div>
            <apexchart type="bar" height="385" :options="chartOptions" :series="series"></apexchart>

        </template>
    </v-card>
</template>
