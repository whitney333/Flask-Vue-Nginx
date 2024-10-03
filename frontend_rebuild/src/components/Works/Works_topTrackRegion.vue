<script setup>
import axios from '@/axios';
import { ref, watch } from 'vue';

    const props = defineProps({
        iconSrc: String
    })
    const tracks = ref({})
    const selected = ref('')
    const trackList = ref([])
    const country = ref('KR')
    const end_date = ref('')
    const drange = ref('')
    const chartOptions = ref({})
    const series = ref({})
    const loadingCard = ref(true)
    const upperCaseFirstLetter = (word) => {
        return word.charAt(0).toUpperCase() + word.slice(1)
    }

    chartOptions.value = {
            chart: {
                height: 350,
                type: 'radar',
            },
            title: {
                text: ''
            },
            yaxis: {
                stepSize: 20
            },
            xaxis: {
                categories: [
                    "North America",
                    "Asia",
                    "Oceania",
                    "Europe",
                    "South America"
                ]
            },
            colors: ['#1db954']
        }

    const getTopTrackRegion = async () => {
        try {
            loadingCard.value = true
            const res = await axios.get(`/api/spotify/top-track/region?track=${selected.value}`, {setTimeout: 10000})
            tracks.value = res.data['result'][0]["track_info"]
            trackList.value = res.data["track_select_list"][0]["track"]
            console.log(tracks.value);
            console.log(trackList.value);
            const formattedData = tracks.value.map((e, i) => {
                return {
                    x: e.region,
                    y: e.agg_popularity
                }
            })
            // update the series with axios data
            series.value = [
                {
                    name: 'Popularity',
                    data: formattedData,
                }
            ]
            
            loadingCard.value = false
        } catch (e) {
            console.error(e);
        }
    }

    const getTopSong = async () => {
        try {
            loadingCard.value = true
            const date = new Date()
            end_date.value = date.toISOString().split('T')[0]
    
            const res = await axios.get(`/api/spotify/top-track?end=${end_date.value}&country=${country.value}&drange=${drange.value}`, {setTimeout: 5000})
            selected.value = res.data["posts"][0]["top_track"][0]["track"]
            loadingCard.value = false

        } catch (e) {
            console.error(e);
        }
    }

    const created = async () => {
        loadingCard.value = true
        await getTopSong()
        await getTopTrackRegion()
        loadingCard.value = false
    }

    await created()
    watch(selected, getTopTrackRegion)

</script>

<template>
    <v-card :loading="loadingCard" class="pa-2 ma-2">
        <template v-slot:title>
            <div :class="['d-flex', 'align-center']">
                <v-img
                :src="props.iconSrc"
                max-height="30px"
                max-width="30px"
                :class="['mr-3']"
                ></v-img>
                <span>
                    {{ $t('By Region') }}
                </span>
                <v-tooltip
                location="bottom">
                    <span>
                        {{ $t('Popularity of top tracks by different region') }}
                    </span>

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
            <div :class="['d-flex', 'justify-space-between', '']">
                <span :class="['text-h6', 'font-weight-bold']"> {{ `${upperCaseFirstLetter(selected)}` }}</span>
                <v-select
                :items="trackList"
                variant="outlined"
                rounded
                density="compact"
                v-model="selected"
                :maxWidth="150"
                >
                <template v-slot:label>{{ $t('Track') }}</template>
                    
                </v-select>
            </div>
            <apexchart type="radar" height="320" :options="chartOptions" :series="series"></apexchart>

        </template>
    </v-card>
</template>
