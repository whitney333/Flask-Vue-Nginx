<script setup>
    import axios from '@/axios';
    import { onMounted, ref, watch } from 'vue';
    import { useArtistStore } from "@/stores/artist.js";

    const props = defineProps({
        iconSrc: String
    })
    const tracks = ref({})
    const selected = ref('')
    const trackList = ref([])
    const country = ref('KR')
    const end_date = ref('')

    // const artistId = ref('1')
    const artistStore = useArtistStore()

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

            const res = await axios.get(`/spotify/v1/region/top-tracks?artist_id=${artistStore.mid}&country=KR`, {setTimeout: 10000})
            tracks.value = res.data.data[0]["track_info"]
            // console.log(tracks)
            trackList.value = res.data["track_list_result"][0]["tracks"]

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

            const res = await axios.get(`/spotify/v1/country/top-tracks?artist_id=${artistStore.mid}&country=${country.value}`, {setTimeout: 5000})
            selected.value = res.data.data[0]["top_track"][0]["track"]

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

    onMounted(() => {
        created()
    }) 

    watch(selected, getTopTrackRegion)

    watch(
        () => artistStore.mid,
        async (newMid) => {
          if (newMid) {
            console.log("🎯 mid changed:", newMid)
            await getTopSong()
            await getTopTrackRegion()
          }
        },
        {immediate: true}
    )

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
