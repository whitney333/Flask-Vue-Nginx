<script setup>
    import axios from '@/axios';
    import {computed, onMounted, ref, watch} from 'vue';
    import { useArtistStore } from '@/stores/artist'
    import { useUserStore } from "@/stores/user.js";
    import {useAuthStore} from "@/stores/auth.js";


    const props = defineProps({
        iconSrc: String,
        colors: Object,
        value: Object
    })

    const artistStore = useArtistStore()
    const userStore = useUserStore()
    const authStore = useAuthStore()
    const citiesData = ref([])
    const cities = ref([])
    const lastUpdate = ref("")
    const series = ref([])
    const loadingCard = ref(true)
    const chartOptions = ref({})
    const monthlyListeners = ref(0)

    const formatNumber = computed(() => {
          return formatNumFunc(index_number.value)
        }
    )
    const formatNumFunc = (value) => {
      const absValue = Math.abs(Number(value)) // 確保是數字
      if (absValue < 1000) {
        return props.value.percentageData ? absValue.toLocaleString() + "%" : absValue.toLocaleString();
      } else if (absValue < 1_000_000) {
        const res = (absValue / 1000).toFixed(1).replace(/\.0$/, '') + 'K';
        return props.value.percentageData ? res + "%" : res;
      } else if (absValue < 1_000_000_000) {
        const res = (absValue / 1_000_000).toFixed(1).replace(/\.0$/, '') + 'M';
        return props.value.percentageData ? res + "%" : res;
      } else {
        const res = (absValue / 1_000_000_000).toFixed(1).replace(/\.0$/, '') + 'B';
        return props.value.percentageData ? res + "%" : res;
      }
    }

    const getData = async () => {
        try{
            loadingCard.value = true

            const res = await axios.get(`/spotify/v1/top-city`,
                {headers: {
                  Authorization: `Bearer ${authStore.idToken}`
                },
                params: {
                  artist_id: artistStore.artistId
                }}
            )
            
            citiesData.value = res.data.data[0].top_city
            // console.log("city: ", citiesData.value)
            lastUpdate.value = res.data.data[0].datetime
            monthlyListeners.value = res.data.data[0].listener

            // console.log(res.data.result[0]);
            
            
            const formattedData = citiesData.value.map((e, i) => {
                return {
                    x: e.city,
                    y: e.listener
                }
            })
            cities.value = citiesData.value.map((val) => val.city)
            series.value = [
                {
                    name: "listeners",
                    data: formattedData,
                }
            ]

        }catch(e) {
            console.error(e);
        } finally {
          loadingCard.value = false
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
            categories: cities.value,
            labels: {
              formatter: formatNumFunc
            }
          }
        }
    
    onMounted(() => {
        getData()
    })

    watch(
        () => artistStore.artistId,
        async (newMid, oldMid) => {
          if (!newMid) return
          // console.log("artist changed:", newMid)
          await getData()
        },
        {immediate: true}
    )

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
