<script setup>
    import axios from '@/axios';
    import { onMounted, reactive, ref, watch } from 'vue';
    import { useArtistStore } from '@/stores/artist'

    const props = defineProps({
        value: Object,
        iconSrc: String
    })

    const loadingCard = ref(true)

    const series = ref([])

    // const artistId = ref("1")
    const artistStore = useArtistStore()
    const recent10Series = ref(null)
    const recent30Series = ref(null)
    const allSeries = ref(null)
    const selection = ref('10_hashtags')

    const fetch10Hashtag = async () => {
        
        if (recent10Series.value) {
            series.value = recent10Series.value
            return
        }
        try {
            loadingCard.value = true
            selection.value = '10_hashtags'

            const data = await axios.get(`/${props.value.apiType}/v1/hashtag/most-used-five?artist_id=${artistStore.mid}`)
            const result = data.data.data
            // console.log(result)
    
            const hashtags = result.map((e, i) => {
                return {
                    x: e._id,
                    y: e.count,
                };
            });

          // update the series with axios data
            series.value = [
                {
                    name: 'Counts',
                    data: hashtags,
                }
            ];
            loadingCard.value = false
        } catch (e) {
            console.error(e);
        }
    }
    const fetch30Hashtag = async () => {
        if (recent30Series.value) {
            series.value = recent30Series.value
            return
        }

        try{
            loadingCard.value = true
            selection.value = '30_hashtags'

            const data = await axios.get(`/${props.value.apiType}/v1/hashtag/most-used-eight?artist_id=${artistStore.mid}`)
            const result = data.data.data
    
            const hashtags = result.map((e, i) => {
                return {
                x: e._id,
                y: e.count,
                };
            });
    
          // update the series with axios data
            series.value = recent30Series.value = [
                {
                    name: 'Counts',
                    data: hashtags,
                }
            ];
            loadingCard.value = false
            
        } catch(e) {
            console.error(e);
        }
        }

    const fetchAllHashtag = async () => {
        if (allSeries.value) {
            series.value = allSeries.value
            return
        }
        try{
            loadingCard.value = true
            selection.value = 'all'

            const data = await axios.get(`/${props.value.apiType}/v1/hashtag/most-used-twelve?artist_id=${artistStore.mid}`)
            const result = data.data.data
    
            const hashtags = result.map((e, i) => {
                return {
                x: e._id,
                y: e.count,
                };
            });
    
          // update the series with axios data
            series.value = allSeries.value = [
                {
                    name: 'Counts',
                    data: hashtags,
                }
            ];
            loadingCard.value = false
            
        } catch(e) {
            console.error(e);
        }
    }

    const chartOptions = {
        chart: {
            type: 'bar',
            height: '350px',
        },
        dataLabels: {
            enabled: false
        },
        noData: {
          text: 'No relevant data',
          align: 'center',
          verticalAlign: 'middle',
          offsetX: 0,
          offsetY: 0,
          style: {
            fontSize: '14px',
            fontFamily: 'Cairo, sans-serif',
            fontWeight: 600,
          }
        },
        plotOptions: {
            bar: {
                borderRadius: 4,
                borderRadiusApplication: 'around',
                horizontal: true,
                columnWidth: '50%',
            }
        },
        fill: {
                type: 'gradient',
                gradient: {
                // shade: 'dark',
                type: "horizontal",
                shadeIntensity: 0.5,
                gradientToColors: ['#ffcf92'], // optional, if not defined - uses the shades of same color in series
                inverseColors: true,
                opacityFrom: 1,
                opacityTo: 1,
                stops: [0, 50, 100],
                colorStops: []
            }
        },
        colors: ['#dd4ee5'],
        xaxis: {
          labels: {
            show: true,
            // formatter: (value) => {
            //   return Number(value).toLocaleString()
            // }
          },
          title: {
            text: 'Occurrence',
            offsetX: 0,
            offsetY: 0,
            style: {
                color: undefined,
                fontSize: '12px',
                fontFamily: 'Cairo, sans-serif',
                fontWeight: 600,
              // cssClass: 'apexcharts-xaxis-title',
            },
          },
        },
        yaxis: {
          type: 'category',
          labels: {
            show: true,
            trim: true,
            style: {
              colors: [],
              fontSize: '12px',
              fontFamily: 'Cairo, sans-serif',
              fontWeight: 400,
              // cssClass: 'apexcharts-xaxis-label',
            },
          }
        },
    }

    onMounted(() => {
        fetch10Hashtag()
    })

    watch(
        () => artistStore.mid,
        (newMid) => {
          if (newMid) {
            // console.log("🎯 hashtag mid changed:", newMid)
            fetch10Hashtag()
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
                    {{ $t(`Top 10 Most-used Hashtags`) }}
                </span>
                <v-tooltip
                location="bottom"
                :text="props.value.usedCol.tooltipText">
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
            <div :width="100" :class="['d-flex', 'justify-start']">
                <div>
                    <v-btn
                        :class="['mx-1']"
                        size='x-small'
                        variant='outlined'
                        color="blue-grey-darken-2"
                        dark
                        rounded
                        :active="selection === '10_hashtags'"
                        @click="fetch10Hashtag()"
                    >
                    Latest 10 Posts
                    </v-btn>
                    <v-btn
                        :class="['mx-1']"
                        size='x-small'
                        variant='outlined'
                        color="blue-grey-darken-2"
                        dark
                        rounded
                        :active="selection === '30_hashtags'"
                        @click="fetch30Hashtag()"
                    >
                    Latest 30 Posts
                    </v-btn>
                    <v-btn
                        :class="['mx-1']"
                        size='x-small'
                        variant='outlined'
                        color="blue-grey-darken-2"
                        dark
                        rounded
                        :active="selection === 'all'"
                        @click="fetchAllHashtag()"
                    >
                    All Posts
                    </v-btn>
                </div>
            </div>
            <apexchart
                width="100%"
                height="180%"
                :options="chartOptions" 
                :series="series">
            </apexchart>
        </template>
    </v-card>
</template>
