<script setup>
import { computed, onMounted, ref, watch, nextTick } from 'vue'
import axios from '@/axios'
import TACard from '@/views/TrendingArtists/components/TA_card.vue'

const loading = ref(false)

const selectCountry = ref({ title: 'Global', value: 'global', type: 'icon', icon: 'mdi-earth' })

const countries = ref([
  { title: 'Global', value: 'global', type: 'icon', icon: 'mdi-earth' },
  { title: 'Australia', value: 'au', flag: 'au' },
  { title: 'Brazil', value: 'br', flag: 'br' },
  { title: 'Canada', value: 'ca', flag: 'ca' },
  { title: 'France', value: 'fr', flag: 'fr' },
  { title: 'Germany', value: 'de', flag: 'de' },
  { title: 'Hong Kong', value: 'hk', flag: 'hk' },
  { title: 'India', value: 'in', flag: 'in' },
  { title: 'Indonesia', value: 'id', flag: 'id' },
  { title: 'Italy', value: 'it', flag: 'it' },
  { title: 'Japan', value: 'jp', flag: 'jp' },
  { title: 'Malaysia', value: 'my', flag: 'my' },
  { title: 'Mexico', value: 'mx', flag: 'mx' },
  { title: 'Philippines', value: 'ph', flag: 'ph' },
  { title: 'Singapore', value: 'sg', flag: 'sg' },
  { title: 'South Korea', value: 'kr', flag: 'kr' },
  { title: 'Spain', value: 'es', flag: 'es' },
  { title: 'Taiwan', value: 'tw', flag: 'tw' },
  { title: 'Thailand', value: 'th', flag: 'th' },
  { title: 'United Kingdom', value: 'gb', flag: 'gb' },
  { title: 'United States', value: 'us', flag: 'us' },
  { title: 'Vietnam', value: 'vn', flag: 'vn' },
])

const selectType = ref('All')
const types = ref(['All', 'Actor', 'Musician'])
const artistList = ref([])

const thisYear = new Date().getFullYear()

const getWeekNumber = () => {
  const date = new Date()
  const target = new Date(date.valueOf())
  const dayNr = (date.getDay() + 6) % 7
  target.setDate(target.getDate() - dayNr + 3)
  const firstThursday = target.valueOf()
  target.setMonth(0, 1)
  if (target.getDay() !== 4) {
    target.setMonth(0, 1 + ((4 - target.getDay()) + 7) % 7)
  }
  return Math.ceil((firstThursday - target) / 604800000)
}

const thisWeek = getWeekNumber()

const currentYear = ref(thisYear)
const currentWeek = ref(thisWeek)

// max week for this year
const maxAvailableWeekForThisYear = ref(thisWeek)

// check if this week has been calibrated
const hasCalibrated = ref(false)

const yearOptions = computed(() =>
  Array.from({ length: thisYear - 2020 + 1 }, (_, i) => thisYear - i)
)

// selectable week options
const weekOptions = computed(() => {
  const maxWeek = currentYear.value === thisYear ? maxAvailableWeekForThisYear.value : 53
  return Array.from({ length: maxWeek }, (_, i) => i + 1)
})

const normalizeArtists = (payload) => {
  const artists = payload?.artists || payload?.data || payload || []
  if (!Array.isArray(artists)) return []

  return artists.map((artist) => ({
    ...artist,
    artistId: artist.artistId ?? artist.artist_id,
    artistName: artist.artistName ?? artist.english_name ?? '',
    artistKoreanName: artist.artistKoreanName ?? artist.korean_name ?? '',
    artistImg: artist.image ?? artist.image_url ?? '',
    popularity: artist.popularity ?? artist.popularity_score ?? 0,
  }))
}

let isCalibrating = false

const fetchArtistList = async () => {
  loading.value = true
  try {
    const response = await axios.get('/trending-artist/v2/popularity', {
      params: {
        year: currentYear.value,
        week: currentWeek.value,
        country: selectCountry.value.value,
        artist_type: selectType.value
      },
    })

    const normalizedData = normalizeArtists(response.data)

    // if the specific year, week has no data, try to fetch the previous week
    if (normalizedData.length === 0 && currentYear.value === thisYear && !hasCalibrated.value && currentWeek.value > 1) {
      // console.warn(`Week ${currentWeek.value} data not available...`)

      isCalibrating = true
      currentWeek.value -= 1
      await nextTick()
      isCalibrating = false

      await fetchArtistList()
      return
    }

    artistList.value = normalizedData

    // fetch the max available week for this year
    if (currentYear.value === thisYear && !hasCalibrated.value) {
      maxAvailableWeekForThisYear.value = currentWeek.value
      hasCalibrated.value = true
    }

  } catch (e) {
    console.error(e)
    artistList.value = []
  } finally {
    loading.value = false
  }
}

// clear filters
const resetFilters = () => {
  selectCountry.value = { title: 'Global', value: 'global', type: 'icon', icon: 'mdi-earth' }
  selectType.value = 'All'
  currentYear.value = thisYear
  currentWeek.value = maxAvailableWeekForThisYear.value
}

watch([selectCountry, currentYear, currentWeek, selectType], () => {
  if (!isCalibrating) {
    if (currentYear.value !== thisYear) {
      hasCalibrated.value = false
    }
    fetchArtistList()
  }
})

onMounted(fetchArtistList)
</script>

<template>
  <div class="min-h-screen bg-gray-100 w-full">
    <div class="max-w-7xl mx-auto px-4 py-6">
      <!--  FILTER BAR  -->
      <div class="relative mb-4 md:mb-6">
        <div class="flex flex-col md:flex-row md:items-center gap-2 rounded-xl bg-white/80 backdrop-blur-md shadow-sm p-2 md:p-2.5 border border-gray-100">
          <div class="flex items-center justify-between gap-2 w-full md:w-auto">

            <v-select
                v-model="selectCountry"
                :items="countries"
                item-title="title"
                item-value="value"
                return-object
                placeholder="Country"
                variant="solo-filled"
                density="compact"
                hide-details
                flat
                class="flex-1 md:flex-none md:w-[160px] custom-v-select"
                hide-selected
            >
              <template #selection="{ item }">
                <div class="flex items-center gap-2 py-0.5">
                  <img
                      v-if="item.raw?.flag"
                      :src="`https://flagcdn.com/16x12/${item.raw.flag}.png`"
                      class="w-4 h-3 rounded-sm object-cover flex-shrink-0"
                  />
                  <v-icon v-else size="16" class="text-gray-500">
                    {{ item.raw?.icon }}
                  </v-icon>
                  <span class="text-sm font-medium text-gray-800 truncate">
              {{ item.raw.title }}
            </span>
                </div>
              </template>

              <template #item="{ props, item }">
                <v-list-item v-bind="props" class="text-sm">
                  <template #prepend>
                    <img
                        v-if="item.raw?.flag"
                        :src="`https://flagcdn.com/16x12/${item.raw.flag}.png`"
                        class="w-4 h-3 rounded-sm mr-2 object-cover"
                    />
                    <v-icon v-else size="16" class="mr-2 text-gray-400">
                      {{ item.raw?.icon }}
                    </v-icon>
                  </template>
                </v-list-item>
              </template>
            </v-select>

          </div>

          <div class="flex items-center gap-2 overflow-x-auto w-full md:w-auto md:ml-auto no-scrollbar">

            <select
                v-model="currentYear"
                class="h-9 md:h-10 px-2.5 md:px-3 rounded-lg bg-gray-50 hover:bg-gray-100 border border-transparent transition text-xs md:text-sm font-medium text-gray-700 cursor-pointer flex-1 md:flex-none min-w-[75px] md:min-w-[100px] focus:outline-none"
            >
              <option v-for="y in yearOptions" :key="y" :value="y">{{ y }}</option>
            </select>

            <select
                v-model="currentWeek"
                class="h-9 md:h-10 px-2.5 md:px-3 rounded-lg bg-gray-50 hover:bg-gray-100 border border-transparent transition text-xs md:text-sm font-medium text-gray-700 cursor-pointer flex-1 md:flex-none min-w-[85px] md:min-w-[100px] focus:outline-none"
            >
              <option v-for="w in weekOptions" :key="w" :value="w">Week {{ w }}</option>
            </select>

            <select
                v-model="selectType"
                class="h-9 md:h-10 px-2.5 md:px-3 rounded-lg bg-gray-50 hover:bg-gray-100 border border-transparent transition text-xs md:text-sm font-medium text-gray-700 cursor-pointer flex-1 md:flex-none min-w-[95px] md:min-w-[120px] focus:outline-none"
            >
              <option v-for="t in types" :key="t" :value="t">{{ t }}</option>
            </select>

            <button
                @click="resetFilters"
                class="grid place-items-center h-9 w-9 md:h-10 md:w-10 rounded-lg bg-gray-50 hover:bg-gray-100 border border-transparent text-gray-400 hover:text-gray-600 transition flex-shrink-0 select-none order-1 md:order-last md:ml-auto"
                title="Clear Filters"
            >
              <svg class="w-4 h-4 md:w-4.5 md:h-4.5 flex-shrink-0" fill="none" stroke="currentColor"
                   viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
      <!-- TABLE  -->
      <div class="bg-white rounded-3xl shadow-sm border overflow-hidden"> <!-- Header -->
        <div class="hidden md:grid grid-cols-12 px-6 py-4 bg-gray-50 text-sm font-semibold">
          <div class="col-span-1 text-center">
            {{ $t('trending_artist.rank')}}
          </div>
          <div class="col-span-4">
            {{ $t('trending_artist.artist')}}
          </div>
          <div class="col-span-2">
            {{ $t('trending_artist.type')}}
          </div>
          <div class="col-span-2">
            {{ $t('trending_artist.popularity')}}
          </div>
          <div class="col-span-3">
            {{ $t('trending_artist.scores')}}
          </div>
        </div>
        <transition name="fade" mode="out-in">
          <!--  SKELETON  -->
          <div v-if="loading" key="loading">
            <div v-for="i in 10" :key="i"
                 class="flex flex-col md:grid md:grid-cols-12 gap-4 px-4 md:px-6 py-4 skeleton-shimmer border-b border-gray-100">
              <!-- MOBILE -->
              <div class="flex items-center gap-3 md:hidden">
                <!-- rank -->
                <div class="h-5 w-6 skeleton-box shrink-0"></div>
                <!-- avatar -->
                <div class="h-12 w-12 rounded-full skeleton-box shrink-0"></div>
                <!-- content -->
                <div class="flex-1 space-y-2">
                  <div class="h-3 w-32 skeleton-box"></div>
                  <div class="h-2 w-20 skeleton-box opacity-60"></div>
                  <div class="flex gap-2 pt-1">
                    <div class="h-2 w-12 skeleton-box"></div>
                    <div class="h-2 w-16 skeleton-box"></div>
                  </div>
                </div>
              </div>
              <!-- DESKTOP -->
              <!-- Rank -->
              <div class="hidden md:flex col-span-1 justify-center">
                <div class="h-4 w-6 skeleton-box"></div>
              </div>
              <!-- Artist -->
              <div class="hidden md:flex col-span-4 items-center gap-3">
                <div class="h-10 w-10 rounded-full skeleton-box"></div>
                <div class="space-y-2 flex-1">
                  <div class="h-3 w-32 skeleton-box"></div>
                  <div class="h-2 w-20 skeleton-box opacity-60"></div>
                </div>
              </div>
              <!-- Type -->
              <div class="hidden md:block col-span-2">
                <div class="h-3 w-16 skeleton-box"></div>
              </div>
              <!-- Popularity -->
              <div class="hidden md:block col-span-2">
                <div class="h-3 w-20 skeleton-box"></div>
              </div>
              <!-- Scores -->
              <div class="hidden md:block col-span-3">
                <div class="h-3 w-28 skeleton-box"></div>
              </div>
            </div>
          </div>
          <!--  DATA -->
          <div v-else key="data">
            <TACard v-for="(artist, i) in artistList"
                    :key="i"
                    :value="artist"
                    :year="currentYear"
                    :week="currentWeek"/>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* SKELETON BASE */
.skeleton-box {
  position: relative;
  overflow: hidden;
  border-radius: 8px;
  background: #e5e7eb;
}

/*  SHIMMER */
.skeleton-shimmer {
  position: relative;
  overflow: hidden;
}

.skeleton-shimmer::after {
  content: "";
  position: absolute;
  top: 0;
  left: -150%;
  width: 150%;
  height: 100%;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0) 0%, rgba(255, 255, 255, 0.6) 50%, rgba(255, 255, 255, 0) 100%);
  animation: shimmer 1.2s infinite;
}

@keyframes shimmer {
  0% {
    transform: translateX(0%);
  }
  100% {
    transform: translateX(200%);
  }
}

/* FADE TRANSITION */
.fade-enter-active, .fade-leave-active {
  transition: opacity .2s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}


/* hide scrollbar */
::-webkit-scrollbar {
  display: none;
}


</style>
