<script setup>
    import axios from '@/axios';
    import { computed, onMounted, reactive, ref, watch } from 'vue';
    import { useArtistStore } from '@/stores/artist'
    import { useUserStore } from '@/stores/user'
    import { useDisplay } from 'vuetify';

    const props = defineProps({
        value: Object,
        iconSrc: String
    })
    const { mobile } = useDisplay();
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

    // 使用 computed 確保在桌機/手機切換時，圖表會重新渲染配置
    const chartOptions = computed(() => ({
      chart: {
        type: 'bar',
        toolbar: {show: false},
        redrawOnParentResize: true, // 重要：隨容器大小自動重繪
        fontFamily: 'Cairo, sans-serif',
      },
      noData: {
        text: 'No relevant data',
        style: {fontSize: '14px', fontWeight: 600}
      },
      plotOptions: {
        bar: {
          borderRadius: 4,
          // 桌機 (非 mobile) 設為橫向 (true)，手機設為直向 (false)
          horizontal: !mobile.value,
          columnWidth: '50%',
          barHeight: '70%'
        }
      },
      dataLabels: {enabled: false},
      fill: {
        type: 'gradient',
        gradient: {
          type: mobile.value ? "vertical" : "horizontal",
          shadeIntensity: 0.5,
          gradientToColors: ['#ffcf92'],
          inverseColors: true,
          opacityFrom: 1,
          opacityTo: 1,
          stops: [0, 100]
        }
      },
      colors: ['#dd4ee5'],
      xaxis: {
        type: 'category',
        labels: {
          show: true,
          rotate: mobile.value ? -45 : 0, // 手機版標籤傾斜避免重疊
        },
        title: {
          text: mobile.value ? '' : 'Occurrence', // 手機版隱藏標題節省空間
        }
      },
      yaxis: {
        labels: {
          show: true,
          maxWidth: mobile.value ? 100 : 150, // 防止長 Hashtag 撐破畫面
        }
      }
    }))

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
  <v-card :loading="loadingCard" class="pa-3 ma-2 overflow-hidden">
    <template v-slot:title>
      <div class="flex items-center w-full min-w-0">
        <v-img :src="props.iconSrc" width="20" height="20" class="mr-2 flex-none"/>

        <span
            class="font-bold truncate text-sm md:text-lg lg:text-xl text-gray-800 flex-shrink min-w-0 max-w-[180px] sm:max-w-[300px] md:max-w-none">
          {{ $t(`Most-used #`) }}
        </span>

        <v-tooltip location="bottom">
          <template v-slot:activator="{ props: tooltipProps }">
            <v-icon size="14" class="ml-1 flex-none opacity-70" v-bind="tooltipProps" icon="mdi-information-outline"/>
          </template>
          <span>{{ props.value.usedCol.tooltipText }}</span>
        </v-tooltip>

        <v-spacer/>
      </div>
    </template>

    <v-card-text class="pa-0">
      <v-divider class="mb-3 mx-4"></v-divider>

      <div class="flex flex-nowrap overflow-x-auto no-scrollbar gap-1 mb-2 px-4">
        <v-btn
          v-for="v in [5, 8, 12]"
          :key="v"
          size="x-small"
          variant="tonal"
          :color="range === v ? 'primary' : 'blue-grey-darken-2'"
          rounded
          :disabled="!userStore.isPremium && v !== 5"
          @click="fetchHashtag(v)"
          class="flex-none"
        >
          Latest {{ v }}
        </v-btn>
      </div>

      <div class="w-full px-2 overflow-hidden">
        <apexchart
          width="100%"
          :height="mobile ? 280 : 320"
          :options="chartOptions"
          :series="series"
        />
      </div>
    </v-card-text>
  </v-card>
</template>

<style scoped>
/* 隱藏按鈕橫向捲軸的 CSS (Tailwind 預設通常不含 hide-scrollbar) */
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
  /* 確保手機滑動順暢 */
  -webkit-overflow-scrolling: touch;
}
</style>
