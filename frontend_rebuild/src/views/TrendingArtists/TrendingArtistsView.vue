<script setup>
import { computed, onMounted, ref, watch, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router'
import axios from '@/axios'

const { t, locale } = useI18n()
const route = useRoute()
const router = useRouter()

// Filters live in the URL (?country=kr&year=2026&week=34&type=Actor) so a
// filtered view is shareable and browser back/forward works.
const queryString = (key) => {
  const value = route.query[key]
  return Array.isArray(value) ? value[0] : value
}
const queryInt = (key) => {
  const number = Number.parseInt(queryString(key) ?? '', 10)
  return Number.isFinite(number) ? number : null
}
import TACard from '@/views/TrendingArtists/components/TA_card.vue'
import TAPodium from '@/views/TrendingArtists/components/TA_podium.vue'

// top 3 get the podium treatment; the table starts at #4
const PODIUM_SIZE = 3

const loading = ref(false)

const GLOBAL_COUNTRY = { title: 'Global', value: 'global', type: 'icon', icon: 'mdi-earth' }
const selectCountry = ref(GLOBAL_COUNTRY)

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

const types = ref(['All', 'Actor', 'Musician'])
const selectType = ref(types.value.includes(queryString('type')) ? queryString('type') : 'All')
const artistList = ref([])

// footer info from the API: rows available beyond the returned page, last update
const listMeta = ref({ totalAvailable: null, updatedAt: null })

// rank_change only exists from 2026 W32 onwards; older weeks return null for
// every row (and change_type defaults to "new"), so key off the number, not the type.
const hasRankChange = computed(() =>
  artistList.value.some((artist) => Number.isFinite(artist.rank_change))
)

// Podium (desktop only) shows the top 3 when there are enough rows for it to make sense.
// The table always renders every artist; the first 3 rows are hidden at md+ via CSS.
const showPodium = computed(() => artistList.value.length > PODIUM_SIZE)
const podiumArtists = computed(() => (showPodium.value ? artistList.value.slice(0, PODIUM_SIZE) : []))

// this week's leader, used to scale every row's popularity bar
const maxPopularity = computed(() =>
  artistList.value.reduce((max, artist) => Math.max(max, Number(artist.popularity) || 0), 0)
)

const headerSubtitle = computed(() => {
  const countryKey = selectCountry.value.title.toLowerCase().replace(/\s+/g, '_')
  return [
    t(`country.${countryKey}`),
    `${currentYear.value} W${currentWeek.value}`,
    t('trending_artist.artist_count', { n: artistList.value.length }),
  ].join(' · ')
})

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

// initial filters: URL query first, then defaults
const initialYear = queryInt('year')
const initialWeek = queryInt('week')
const currentYear = ref(initialYear && initialYear >= 2020 && initialYear <= thisYear ? initialYear : thisYear)
const currentWeek = ref(initialWeek && initialWeek >= 1 && initialWeek <= 53 ? initialWeek : thisWeek)
selectCountry.value = countries.value.find((c) => c.value === queryString('country')) ?? GLOBAL_COUNTRY

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

  // The API returns each artist's stored rank across all types. When a type
  // filter is active, renumber the visible list (1, 2, 3...) while keeping the
  // original rank on the item for the artist detail page.
  const isTypeFiltered = selectType.value !== 'All'

  return artists.map((artist, index) => ({
    ...artist,
    artistId: artist.artistId ?? artist.artist_id,
    artistName: artist.artistName ?? artist.english_name ?? '',
    artistKoreanName: artist.artistKoreanName ?? artist.korean_name ?? '',
    artistImg: artist.image ?? artist.image_url ?? '',
    popularity: artist.popularity ?? artist.popularity_score ?? 0,
    displayRank: isTypeFiltered ? index + 1 : artist.rank,
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
    listMeta.value = {
      totalAvailable: Number.isFinite(response.data?.total_available) ? response.data.total_available : null,
      updatedAt: response.data?.updated_at ?? null,
    }
    // the calibration path above bypasses the filter watcher, so re-sync the URL here
    syncQuery()

    // fetch the max available week for this year
    if (currentYear.value === thisYear && !hasCalibrated.value) {
      maxAvailableWeekForThisYear.value = currentWeek.value
      hasCalibrated.value = true
    }

  } catch (e) {
    console.error(e)
    artistList.value = []
    listMeta.value = { totalAvailable: null, updatedAt: null }
  } finally {
    loading.value = false
  }
}

// clear filters
const resetFilters = () => {
  selectCountry.value = GLOBAL_COUNTRY
  selectType.value = 'All'
  currentYear.value = thisYear
  currentWeek.value = maxAvailableWeekForThisYear.value
}

// --- week stepper (prev / next, crossing year boundaries) ---
const MIN_YEAR = 2020
const LAST_WEEK_OF_YEAR = 53

const lastSelectableWeek = (year) =>
  year === thisYear ? maxAvailableWeekForThisYear.value : LAST_WEEK_OF_YEAR

const canStepPrev = computed(() => currentWeek.value > 1 || currentYear.value > MIN_YEAR)
const canStepNext = computed(() =>
  currentWeek.value < lastSelectableWeek(currentYear.value) || currentYear.value < thisYear
)

const stepWeek = (delta) => {
  const target = currentWeek.value + delta

  if (target < 1) {
    if (currentYear.value <= MIN_YEAR) return
    currentYear.value -= 1
    currentWeek.value = LAST_WEEK_OF_YEAR
    return
  }

  if (target > lastSelectableWeek(currentYear.value)) {
    if (currentYear.value >= thisYear) return
    currentYear.value += 1
    currentWeek.value = 1
    return
  }

  currentWeek.value = target
}

// keep the URL in sync with the filters (replace, so stepping weeks doesn't spam history)
const syncQuery = () => {
  const query = {
    ...route.query,
    country: selectCountry.value.value,
    year: String(currentYear.value),
    week: String(currentWeek.value),
    type: selectType.value,
  }
  const changed = Object.keys(query).some((key) => query[key] !== queryString(key))
  if (changed) {
    router.replace({ query })
  }
}

// --- footer ---
const footerText = computed(() => {
  const parts = []
  if (artistList.value.length && Number.isFinite(listMeta.value.totalAvailable)) {
    parts.push(t('trending_artist.showing_of', { shown: artistList.value.length, total: listMeta.value.totalAvailable }))
  }
  if (listMeta.value.updatedAt) {
    const date = new Date(listMeta.value.updatedAt)
    if (!Number.isNaN(date.getTime())) {
      parts.push(t('trending_artist.updated', {
        date: date.toLocaleDateString(locale.value, { year: 'numeric', month: 'short', day: 'numeric' }),
      }))
    }
  }
  return parts.join(' · ')
})

watch([selectCountry, currentYear, currentWeek, selectType], () => {
  if (!isCalibrating) {
    if (currentYear.value !== thisYear) {
      hasCalibrated.value = false
    }
    syncQuery()
    fetchArtistList()
  }
})

onMounted(() => {
  syncQuery()
  fetchArtistList()
})
</script>

<template>
  <div class="min-h-screen bg-gray-100 w-full">
    <div class="max-w-7xl mx-auto px-4 py-6">
      <!--  PAGE HEADER  -->
      <header class="mb-4 md:mb-6">
        <h1 class="text-2xl md:text-3xl font-black tracking-tight text-gray-900">
          {{ $t('trending_artist.title') }}
        </h1>
        <p class="mt-1 text-sm text-gray-500 tabular-nums">
          {{ headerSubtitle }}
        </p>
      </header>

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

          <!-- mobile: stepper + clear on one line, segmented control wraps to a full-width line below -->
          <div class="flex items-center gap-2 flex-wrap md:flex-nowrap w-full md:w-auto md:ml-auto">

            <!-- week stepper: [<] [year ▾][W## ▾] [>] -->
            <div class="flex items-center h-9 md:h-10 rounded-lg bg-gray-50 border border-transparent overflow-hidden flex-shrink-0">
              <button
                  type="button"
                  @click="stepWeek(-1)"
                  :disabled="!canStepPrev"
                  :aria-label="$t('trending_artist.prev_week')"
                  :title="$t('trending_artist.prev_week')"
                  class="grid place-items-center h-full w-8 md:w-9 text-gray-500 hover:bg-gray-100 hover:text-gray-800 disabled:opacity-30 disabled:hover:bg-transparent transition"
              >
                <v-icon icon="mdi-chevron-left" size="18" />
              </button>

              <select
                  v-model="currentYear"
                  :aria-label="$t('trending_artist.year')"
                  class="h-full pl-2 pr-1 bg-transparent text-xs md:text-sm font-medium text-gray-700 tabular-nums cursor-pointer focus:outline-none"
              >
                <option v-for="y in yearOptions" :key="y" :value="y">{{ y }}</option>
              </select>

              <select
                  v-model="currentWeek"
                  :aria-label="$t('trending_artist.week')"
                  class="h-full pl-1 pr-2 bg-transparent text-xs md:text-sm font-semibold text-gray-800 tabular-nums cursor-pointer focus:outline-none"
              >
                <option v-for="w in weekOptions" :key="w" :value="w">W{{ w }}</option>
              </select>

              <button
                  type="button"
                  @click="stepWeek(1)"
                  :disabled="!canStepNext"
                  :aria-label="$t('trending_artist.next_week')"
                  :title="$t('trending_artist.next_week')"
                  class="grid place-items-center h-full w-8 md:w-9 text-gray-500 hover:bg-gray-100 hover:text-gray-800 disabled:opacity-30 disabled:hover:bg-transparent transition"
              >
                <v-icon icon="mdi-chevron-right" size="18" />
              </button>
            </div>

            <!-- artist type: segmented control -->
            <div
                role="radiogroup"
                :aria-label="$t('trending_artist.type')"
                class="flex items-center h-9 md:h-10 p-1 rounded-lg bg-gray-50 border border-transparent flex-shrink-0 w-full md:w-auto max-md:order-last"
            >
              <button
                  v-for="option in types"
                  :key="option"
                  type="button"
                  role="radio"
                  :aria-checked="selectType === option"
                  @click="selectType = option"
                  class="h-full px-3 rounded-md text-xs md:text-sm font-medium transition whitespace-nowrap flex-1 md:flex-none"
                  :class="selectType === option
                    ? 'bg-white text-gray-900 shadow-sm'
                    : 'text-gray-500 hover:text-gray-800'"
              >
                {{ $t(`trending_artist.type_${option.toLowerCase()}`) }}
              </button>
            </div>

            <button
                @click="resetFilters"
                class="grid place-items-center h-9 w-9 md:h-10 md:w-10 rounded-lg bg-gray-50 hover:bg-gray-100 border border-transparent text-gray-400 hover:text-gray-600 transition flex-shrink-0 select-none ml-auto md:ml-0"
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
      <!--  PODIUM (top 3)  -->
      <section
        v-if="loading || showPodium"
        :aria-label="$t('trending_artist.top_three')"
        class="hidden md:grid md:grid-cols-3 gap-4 mb-6"
      >
        <template v-if="loading">
          <div
            v-for="i in PODIUM_SIZE"
            :key="`podium-skeleton-${i}`"
            class="flex items-center gap-4 rounded-3xl border border-gray-200 bg-white px-5 py-4 skeleton-shimmer"
          >
            <div class="w-[72px] h-[72px] rounded-2xl skeleton-box shrink-0"></div>
            <div class="flex-1 space-y-2">
              <div class="h-4 w-32 skeleton-box"></div>
              <div class="h-3 w-20 skeleton-box opacity-60"></div>
              <div class="h-6 w-16 skeleton-box mt-3"></div>
            </div>
          </div>
        </template>
        <template v-else>
          <TAPodium
            v-for="(artist, i) in podiumArtists"
            :key="artist.artistId ?? i"
            :value="artist"
            :place="i + 1"
            :year="currentYear"
            :week="currentWeek"
            :show-rank-change="hasRankChange"
          />
        </template>
      </section>

      <!-- TABLE  -->
      <!-- overflow-clip (not hidden): hidden would make this card the scroll container
           for the sticky column header below and stop it from sticking to the viewport -->
      <div class="bg-white rounded-3xl shadow-sm border overflow-clip"> <!-- Header -->
        <!-- sticky so column labels survive a 100-row scroll; offset = app bar height -->
        <div class="hidden md:grid grid-cols-12 px-6 py-4 bg-gray-50 text-sm font-semibold sticky top-[64px] z-10 border-b border-gray-100">
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
          <!-- one label per score column, matching the 3-col grid in TA_card -->
          <div class="col-span-3 grid grid-cols-3 gap-2">
            <div>{{ $t('trending_artist.music') }}</div>
            <div>{{ $t('trending_artist.sns') }}</div>
            <div>{{ $t('trending_artist.drama') }}</div>
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
            <!-- every artist is a row; on md+ the first three are hidden here and shown on the podium -->
            <TACard v-for="(artist, i) in artistList"
                    :key="artist.artistId ?? i"
                    :value="artist"
                    :year="currentYear"
                    :week="currentWeek"
                    :show-rank-change="hasRankChange"
                    :max-popularity="maxPopularity"
                    :index="i"
                    :class="showPodium && i < PODIUM_SIZE ? 'md:hidden' : ''"/>

            <!-- empty state -->
            <div
              v-if="!artistList.length"
              class="px-6 py-16 text-center text-sm text-gray-400"
            >
              {{ $t('trending_artist.empty') }}
            </div>
          </div>
        </transition>

        <!-- footer: "Showing 100 of 551 · Updated 1 Sep 2026" -->
        <div
          v-if="!loading && footerText"
          class="px-6 py-3 bg-gray-50 border-t border-gray-100 text-xs text-gray-500 tabular-nums text-center md:text-left"
        >
          {{ footerText }}
        </div>
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
