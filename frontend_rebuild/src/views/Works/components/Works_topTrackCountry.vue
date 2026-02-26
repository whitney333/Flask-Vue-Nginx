<script setup>
import axios from '@/axios';
import {onMounted, ref, watch, computed} from 'vue';
import getUnicodeFlagIcon from 'country-flag-icons/unicode'
import {useArtistStore} from "@/stores/artist.js";
import {useAuthStore} from "@/stores/auth.js";

const props = defineProps({
  iconSrc: String
})

const artistStore = useArtistStore()
const authStore = useAuthStore()
const selected = ref('South Korea')
const trackList = ref([])
const lastUpdate = ref('')
const loadingCard = ref(true)

const countriesFlag = {
  'Australia': 'AU',
  'Brazil': 'BR',
  'Canada': 'CA',
  'France': 'FR',
  'Germany': 'DE',
  'Hong Kong': 'HK',
  'India': 'IN',
  'Indonesia': 'ID',
  'Italy': 'IT',
  'Japan': 'JP',
  'Macao': 'MO',
  'Malaysia': 'MY',
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

const countries = Object.keys(countriesFlag).map(name => ({
  title: `${getUnicodeFlagIcon(countriesFlag[name])} ${name}`,
  value: name
}))

// overlay 判斷
const noSpotifyId = computed(() => !artistStore.artist?.spotify_id)
const overlayText = computed(() => noSpotifyId.value ? 'Spotify data not available' : '')

const series = ref([])
const chartOptions = ref({
  chart: {height: 350, type: 'bar'},
  plotOptions: {bar: {borderRadius: 4, borderRadiusApplication: 'around', horizontal: true}},
  colors: [{}, function ({dataPointIndex}) {
    return dataPointIndex % 2 ? '#191414' : '#1db954'
  }],
  dataLabels: {enabled: false},
  xaxis: {categories: trackList.value}
})

const upperCaseFirstLetter = (word) => word.charAt(0).toUpperCase() + word.slice(1)

// ===== API Calls =====
const getTopTrackRegion = async () => {
  if (!artistStore.artist?.spotify_id) {
    series.value = []
    loadingCard.value = false
    return
  }
  if (!artistStore.artistId) return

  try {
    loadingCard.value = true
    const res = await axios.get(
        `/spotify/v1/country/top-tracks`,
        {params: {artist_id: artistStore.artistId, country: 'KR'}, timeout: 10000}
    )
    const data = res.data?.data?.[0]
    if (!data) {
      series.value = []
      return
    }

    lastUpdate.value = data.datetime || ""
    trackList.value = data.top_track?.map(val => val.track) || []

    const formattedData = data.top_track?.map(e => ({x: e.track, y: e.popularity ?? 0})) || []

    series.value = [{name: "Popularity", data: formattedData}]
  } catch (e) {
    console.error(e)
    series.value = []
  } finally {
    loadingCard.value = false
  }
}

const getTopSong = async () => {
  if (!artistStore.artist?.spotify_id || !artistStore.artistId) {
    series.value = []
    loadingCard.value = false
    return
  }

  try {
    loadingCard.value = true
    const res = await axios.get(
        `/spotify/v1/country/top-tracks`,
        {params: {artist_id: artistStore.artistId, country: countriesFlag[selected.value]}, timeout: 5000}
    )
    const firstData = res.data?.data?.[0]
    if (firstData) selected.value = firstData.country || selected.value
  } catch (e) {
    console.error(e)
  } finally {
    loadingCard.value = false
  }
}

// ===== Lifecycle =====
const created = async () => {
  if (!artistStore.artist?.spotify_id) {
    loadingCard.value = false
    return
  }
  loadingCard.value = true
  await getTopSong()
  await getTopTrackRegion()
  loadingCard.value = false
}

onMounted(() => created())

watch(selected, (newVal) => {
  if (newVal) getTopTrackRegion()
})
watch(() => artistStore.artistId, async (newId) => {
  if (newId) {
    await getTopSong();
    await getTopTrackRegion()
  }
}, {immediate: true})

</script>


<template>
  <v-card class="pa-2 ma-2 relative" :loading="loadingCard">
    <!-- Overlay if no Spotify ID -->
    <div v-if="noSpotifyId" class="absolute inset-0 z-10 flex items-center justify-center bg-white/70">
      <span class="text-caption text-grey">{{ overlayText }}</span>
    </div>

    <!-- Title -->
    <template v-slot:title>
      <div class="d-flex align-center">
        <v-img :src="props.iconSrc" max-height="30px" max-width="30px" class="mr-3"></v-img>
        <span>{{ $t('By Country') }}</span>
        <v-tooltip location="bottom">
          <span>{{ $t('Popularity of top tracks by different country') }}</span>
          <template v-slot:activator="{ props }">
            <v-icon size="20" class="mx-1" v-bind="props" icon="mdi-information-outline"></v-icon>
          </template>
        </v-tooltip>
      </div>
    </template>

    <!-- Content -->
    <template v-slot:text>
      <v-divider></v-divider>
      <br/>
      <div class="d-flex justify-space-between align-center">
        <span class="text-caption" style="color:#757575;">{{ `${$t('Last updated')}: ${lastUpdate}` }}</span>
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
