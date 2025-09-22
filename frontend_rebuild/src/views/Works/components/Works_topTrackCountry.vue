<script setup>
  import axios from '@/axios';
  import { onMounted, ref, watch } from 'vue';
  import getUnicodeFlagIcon from 'country-flag-icons/unicode'
  import { useArtistStore } from "@/stores/artist.js";

  const props = defineProps({
        iconSrc: String
    })
    const tracks = ref({})
    // const artistId = ref('1')
    const artistStore = useArtistStore()

    const selected = ref('South Korea')
    const trackList = ref([])
    const country = ref('KR')
    const lastUpdate = ref('')

    // const end_date = ref(new Date().toISOString().split('T')[0])
    // const drange = ref('')

    const chartOptions = ref({})
    const series = ref({})
    const loadingCard = ref(true)
    const upperCaseFirstLetter = (word) => {
        return word.charAt(0).toUpperCase() + word.slice(1)
    }

    const countriesFlag = {
        'Australia': 'AU',
        'Brazil': 'BR',
        'Canada': 'CA',
        'France': 'FR',
        'Germany': 'DE',
        'Hong Kong': 'HK',
        "India": "IN",
        'Indonesia': 'ID',
        'Italy': 'IT',
        'Japan': 'JP',
        "Macao": "MO",
        "Malaysia": "MY",
        'Mexico': 'MX',
        'Philippines': 'PH',
        'South Korea': 'KR',
        'Spain': 'ES',
        'Taiwan': 'TW',
        'Thailand': 'TH',
        'United Kingdom': 'GB',
        'United States': 'US',
        'Vietnam': 'VN'
    }

    const countries = [
    {
        title: `${getUnicodeFlagIcon(countriesFlag['Taiwan'])} ${'Taiwan'}`,
        value: 'Taiwan',
    },
    {
        title: `${getUnicodeFlagIcon(countriesFlag['Hong Kong'])} ${'Hong Kong'}`,
        value: 'Hong Kong',
    },
    {
        title: `${getUnicodeFlagIcon(countriesFlag['Macao'])} ${'Macao'}`,
        value: 'Macao',
    },
    {
        title: `${getUnicodeFlagIcon(countriesFlag['Japan'])} ${'Japan'}`,
        value: 'Japan',
    },
    {
        title: `${getUnicodeFlagIcon(countriesFlag['South Korea'])} ${'South Korea'}`,
        value: 'South Korea',
    },
    {
        title: `${getUnicodeFlagIcon(countriesFlag['Thailand'])} ${'Thailand'}`,
        value: 'Thailand',
        
    },
    {
        title: `${getUnicodeFlagIcon(countriesFlag['Malaysia'])} ${'Malaysia'}`,
        value: 'Malaysia',
    },
    {
        title: `${getUnicodeFlagIcon(countriesFlag['India'])} ${'India'}`,
        value: 'India',
    },
    {
        title: `${getUnicodeFlagIcon(countriesFlag['Vietnam'])} ${'Vietnam'}`,
        value: 'Vietnam',
        
    },
    {
        title: `${getUnicodeFlagIcon(countriesFlag['Philippines'])} ${'Philippines'}`,
        value: 'Philippines',
    },
    {
        title: `${getUnicodeFlagIcon(countriesFlag['Indonesia'])} ${'Indonesia'}`,
        value: 'Indonesia',
    },
    {
        title: `${getUnicodeFlagIcon(countriesFlag['United States'])} ${'United States'}`,
        value: 'United States',
        
    },
    {
        title: `${getUnicodeFlagIcon(countriesFlag['Canada'])} ${'Canada'}`,
        value: 'Canada',
    },
    {
        title: `${getUnicodeFlagIcon(countriesFlag['Brazil'])} ${'Brazil'}`,
        value: 'Brazil',
    },
    {
        title: `${getUnicodeFlagIcon(countriesFlag['Mexico'])} ${'Mexico'}`,
        value: 'Mexico',
    },
    {
        title: `${getUnicodeFlagIcon(countriesFlag['United Kingdom'])} ${'United Kingdom'}`,
        value: 'United Kingdom',
    },
    {
        title: `${getUnicodeFlagIcon(countriesFlag['Germany'])} ${'Germany'}`,
        value: 'Germany',
    },
    {
        title: `${getUnicodeFlagIcon(countriesFlag['France'])} ${'France'}`,
        value: 'France',
        
    },
    {
        title: `${getUnicodeFlagIcon(countriesFlag['Spain'])} ${'Spain'}`,
        value: 'Spain',
        
    },
    {
        title: `${getUnicodeFlagIcon(countriesFlag['Italy'])} ${'Italy'}`,
        value: 'Italy',
        
    },
    {
        title: `${getUnicodeFlagIcon(countriesFlag['Australia'])} ${'Australia'}`,
        value: 'Australia',
    }
]

    chartOptions.value = {
            chart: {
                height: 350,
                type: 'bar',
            },
            plotOptions: {
                bar: {
                    borderRadius: 4,
                    borderRadiusApplication: 'around',
                    horizontal: true,
                }
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
            dataLabels: {
                enabled: false
            },
            xaxis: {
                categories: trackList.value
            }
        }

    const getTopTrackRegion = async () => {
        try {
            loadingCard.value = true

            const res = await axios.get(`/spotify/v1/country/top-tracks?artist_id=${artistStore.mid}&country=${countriesFlag[selected.value]}`, {setTimeout: 10000})
            const data = res.data.data[0]

            lastUpdate.value = data.datetime
            trackList.value = data.top_track.map((val) => val.track)
            

            const formattedData = data.top_track.map((e, i) => {
                return {
                    x: e.track,
                    y: e.popularity,
                }
            })
            // // update the series with axios data
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

            const res = await axios.get(`/spotify/v1/country/top-tracks?artist_id=${artistStore.mid}&country=${selected.value}`, {setTimeout: 5000})
            selected.value = res.data.data["top_track"]

            loadingCard.value = false

        } catch (e) {
            console.error(e);
        }
    }

    const created = async () => {
        loadingCard.value = true
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
                    {{ $t('By Country') }}
                </span>
                <v-tooltip
                location="bottom">
                    <span>
                        {{ $t('Popularity of top tracks by different country') }}
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
            <div :class="['d-flex', 'justify-space-between', 'align-center']">
                <span style="color: #757575;" :class="['text-caption']"> {{ `${$t('Last updated')}: ${lastUpdate}` }}</span>
                <v-select
                    :items="countries"
                    variant="outlined"
                    item-title="title"
                    rounded
                    density="compact"
                    v-model="selected"
                    :minWidth="100"
                    :maxWidth="200"
                >
                    <template v-slot:label>{{ $t('Country') }}</template>
                </v-select>
            </div>
            <apexchart type="bar" height="320" :options="chartOptions" :series="series"></apexchart>

        </template>
    </v-card>
</template>
