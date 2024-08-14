<script setup>
    import axios from '@/axios';
    import { reactive, ref } from 'vue';

    const props = defineProps({
        value: Object
    })

    const loadingCard = ref(true)
    const series = ref([])
    const chartOptions = ref({})
    const recent10Series = ref(null)
    const recent30Series = ref(null)
    const allSeries = ref(null)

    const fetch10Hashtag = async () => {
        if (recent10Series.value) {
            series.value = recent10Series.value
            return
        }
        try {
            loadingCard.value = true
            const data = await axios.get(`/api/${props.value.apiType}/hashtags/most-engaged/recent-ten-posts`)
            const result = data.data.result
            
    
            const hashtags = result.map((e, i) => {
                return {
                    x: e._id,
                    y: e.eng_rate_per_hashtag,
                };
            });
    
          // update the series with axios data
            series.value = recent10Series.value = [
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
        try{
            
            loadingCard.value = true
            const data = await axios.get(`/api/${props.value.apiType}/hashtags/most-engaged/recent-thirty-posts`)
            const result =  data.data.result
    
            const hashtags = result.map((e, i) => {
                return {
                x: e._id,
                y: e.eng_rate_per_hashtag,
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
        try{
            loadingCard.value = true
            const data = await axios.get(`/api/${props.value.apiType}/hashtags/most-engaged/overall-posts`)
            const result =  data.data.result
    
            const hashtags = result.map((e, i) => {
                return {
                x: e._id,
                y: e.eng_rate_per_hashtag,
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
        } catch (e) {
            console.error(e);
        }
    }

    chartOptions.value = {
        chart: {
            type: 'bar',
            height: '356px',
        },
        plotOptions: {
            bar: {
                borderRadius: 7,
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
                gradientToColors: ['#ab93ff'], // optional, if not defined - uses the shades of same color in series
                inverseColors: true,
                opacityFrom: 1,
                opacityTo: 1,
                stops: [0, 50, 100],
                colorStops: []
            }
        },
        colors: ['#10a3ff'],
        // legend: {
        //   show: false
        // },
        // yaxis: {
        //   type: 'category',
        //   labels: {
        //     show: true,
        //     trim: true,
        //     style: {
        //       colors: [],
        //       fontSize: '14px',
        //       fontFamily: 'Cairo, sans-serif',
        //       fontWeight: 400,
        //       // cssClass: 'apexcharts-xaxis-label',
        //     },
        //   }
        // },
        xaxis: {
          labels: {
            show: true,
            formatter: (value) => {
              return Number(value).toLocaleString()
            }
          },
          title: {
            text: 'Occurrence',
            offsetX: 0,
            offsetY: 0,
            style: {
                color: undefined,
                fontSize: '14px',
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
              fontSize: '14px',
              fontFamily: 'Cairo, sans-serif',
              fontWeight: 400,
              // cssClass: 'apexcharts-xaxis-label',
            },
          }
        },
    }
    fetch10Hashtag()



</script>

<template>
    <v-card :loading="loadingCard" class="pa-2 ma-2">
        <template v-slot:title>
            <div :class="['d-flex', 'align-center']">
                <v-img
                :src="props.value.iconSrc"
                max-height="30px"
                max-width="30px"
                :class="['mr-3']"
                ></v-img>
                <span>
                    {{ $t('Top 10 Most-engaged Hashtags') }}
                </span>
                <v-tooltip
                location="bottom"
                :text="props.value.engagedCol.tooltipText">
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
