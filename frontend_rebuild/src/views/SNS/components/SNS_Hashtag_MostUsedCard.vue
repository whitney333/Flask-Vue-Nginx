<script setup>
    import axios from '@/axios';
    import { onMounted, reactive, ref, watch } from 'vue';
    import { useArtistStore } from '@/stores/artist'
    import { useUserStore } from '@/stores/user'

    const props = defineProps({
        value: Object,
        iconSrc: String
    })

    const loadingCard = ref(true)

    const series = ref([])

    const userStore = useUserStore()
    const artistStore = useArtistStore()
    const range = ref(5)

    const fetchHashtag = async (limit) => {
      // free user limits to 5
      if (!userStore.isPremium && limit !== 5) {
        return
      }

      range.value = limit
      loadingCard.value = true

      try {
        const {data} = await axios.get(
            `/${props.value.apiType}/v1/hashtag/most-used`,
            {
              headers: {
                Authorization: `Bearer ${userStore.firebaseToken}`
              },
              params: {
                artist_id: artistStore.artistId,
                range: range.value
              }
            }
        )

        const result = data.data || []

        series.value = [
          {
            name: 'Counts',
            data: result.map(e => ({
              x: e._id,
              y: e.count
            }))
          }
        ]
      } catch (e) {
        console.error(e)
      } finally {
        loadingCard.value = false
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
        fetchHashtag(5)
    })

    watch(
        () => artistStore.artistId,
        (newMid) => {
          if (newMid) {
            // console.log("🎯 hashtag mid changed:", newMid)
            fetchHashtag(5)
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
                        :active="range === 5"
                        @click="fetchHashtag(5)"
                    >
                    Latest 5 Posts
                    </v-btn>
                    <v-btn
                        :class="['mx-1']"
                        size='x-small'
                        variant='outlined'
                        color="blue-grey-darken-2"
                        dark
                        rounded
                        :active="range === 8"
                        @click="fetchHashtag(8)"
                    >
                    Latest 8 Posts
                    </v-btn>
                    <v-btn
                        :class="['mx-1']"
                        size='x-small'
                        variant='outlined'
                        color="blue-grey-darken-2"
                        dark
                        rounded
                        :active="range === 12"
                        @click="fetchHashtag(12)"
                    >
                    Latest 12 Posts
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

<style scoped>

</style>
