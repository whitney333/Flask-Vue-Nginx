<script setup>
import { computed, onMounted, ref, watch } from 'vue';
import getUnicodeFlagIcon from 'country-flag-icons/unicode'
import axios from '@/axios';
import TACard from '@/views/TrendingArtists/components/TA_card.vue';

  const countriesFlag = {
      'Global': 'UN',
      'Taiwan': 'TW',
      'Hong Kong': 'HK',
      'Japan': 'JP',
      'South Korea': 'KR',
      'Thailand': 'TH',
      'Vietnam': 'VN',
      'Philippines': 'PH',
      'Indonesia': 'ID',
      'United States': 'US',
      'Canada': 'CA',
      'Brazil': 'BR',
      'Mexico': 'MX',
      'United Kingdom': 'GB',
      'Germany': 'DE',
      'France': 'FR',
      'Spain': 'ES',
      'Italy': 'IT',
      'Australia': 'AU'
  }

  const selectCountry = ref({
          title: `${getUnicodeFlagIcon(countriesFlag['Global'])} ${'Global'}`,
          value: 'global',
      })
  const countries = ref([
      {
          title: `${getUnicodeFlagIcon(countriesFlag['Global'])} ${'Global'}`,
          value: 'global',
      },
      {
          title: `${getUnicodeFlagIcon(countriesFlag['Taiwan'])} ${'Taiwan'}`,
          value: 'tw',
      },
      {
          title: `${getUnicodeFlagIcon(countriesFlag['Hong Kong'])} ${'Hong Kong'}`,
          value: 'hk',
      },
      {
          title: `${getUnicodeFlagIcon(countriesFlag['Japan'])} ${'Japan'}`,
          value: 'jp',
      },
      {
          title: `${getUnicodeFlagIcon(countriesFlag['South Korea'])} ${'South Korea'}`,
          value: 'kr',
      },
      {
          title: `${getUnicodeFlagIcon(countriesFlag['Thailand'])} ${'Thailand'}`,
          value: 'th',

      },
      {
          title: `${getUnicodeFlagIcon(countriesFlag['Vietnam'])} ${'Vietnam'}`,
          value: 'vn',

      },
      {
          title: `${getUnicodeFlagIcon(countriesFlag['Philippines'])} ${'Philippines'}`,
          value: 'ph',
      },
      {
          title: `${getUnicodeFlagIcon(countriesFlag['Indonesia'])} ${'Indonesia'}`,
          value: 'id',
      },
      {
          title: `${getUnicodeFlagIcon(countriesFlag['United States'])} ${'United States'}`,
          value: 'us',

      },
      {
          title: `${getUnicodeFlagIcon(countriesFlag['Canada'])} ${'Canada'}`,
          value: 'ca',
      },
      {
          title: `${getUnicodeFlagIcon(countriesFlag['Brazil'])} ${'Brazil'}`,
          value: 'br',
      },
      {
          title: `${getUnicodeFlagIcon(countriesFlag['Mexico'])} ${'Mexico'}`,
          value: 'mx',
      },
      {
          title: `${getUnicodeFlagIcon(countriesFlag['United Kingdom'])} ${'United Kingdom'}`,
          value: 'gb',
      },
      {
          title: `${getUnicodeFlagIcon(countriesFlag['Germany'])} ${'Germany'}`,
          value: 'de',
      },
      {
          title: `${getUnicodeFlagIcon(countriesFlag['France'])} ${'France'}`,
          value: 'fr',

      },
      {
          title: `${getUnicodeFlagIcon(countriesFlag['Spain'])} ${'Spain'}`,
          value: 'es',

      },
      {
          title: `${getUnicodeFlagIcon(countriesFlag['Italy'])} ${'Italy'}`,
          value: 'it',

      },
      {
          title: `${getUnicodeFlagIcon(countriesFlag['Australia'])} ${'Australia'}`,
          value: 'au',
      }
  ])
  const selectType = ref('All')
  const types = ref(['All', 'Actor', 'Musician'])
  const artistList = ref([])
  const thisYear = new Date().getFullYear()
  const currentYear = ref(thisYear)

  // ISO week
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
  const currentWeek = ref(thisWeek)
  const yearOptions = computed(() => {
      return Array.from({ length: thisYear - 2020 + 1 }, (_, i) => thisYear - i)
  })
  const weekOptions = computed(() => {
      const maxWeek = currentYear.value === thisYear ? thisWeek : 53
      return Array.from({ length: maxWeek }, (_, i) => i + 1)
  })

  const artistPresentList = computed(() => {
    if (selectType.value == 'Actor') {
      return artistList.value.filter((x) => x.type == 'Actor')
    } else if (selectType.value == 'Musician') {
      return artistList.value.filter((x) => x.type == 'Musician')
    } else {
      return artistList.value
    }
    // todo Region
  })

    const normalizeArtists = (payload) => {
      const artists = payload?.artists || payload?.data || payload || []

      if (!Array.isArray(artists)) {
        return []
      }

      return artists.map((artist) => ({
        ...artist,
        artistId: artist.artistId ?? artist.artist_id,
        artistName: artist.artistName ?? artist.english_name ?? '',
        artistKoreanName: artist.artistKoreanName ?? artist.korean_name ?? '',
        artistImg: artist.image ?? artist.image_url ?? '',
        popularity: artist.popularity ?? artist.popularity_score ?? 0,
      }))
    }

    // fetch Artist List everytime the country changed
    const fetchArtistList = async () => {
      try {
        const response = await axios.get('/trending-artist/v2/popularity', {
          params: {
            year: currentYear.value,
            week: currentWeek.value,
            country: selectCountry.value.value
          }
        })

        artistList.value = normalizeArtists(response.data)

      } catch (error) {
        console.error('Fetch trending artist failed:', error)
        artistList.value = []
      }
    }

    watch(currentYear, () => {
      const maxWeek = currentYear.value === thisYear ? thisWeek : 53

      if (currentWeek.value > maxWeek) {
        currentWeek.value = maxWeek
      }
    })

    watch([selectCountry, currentYear, currentWeek], fetchArtistList)

    onMounted(() => {
      fetchArtistList()
    })
</script>

<template>
    <div class="min-h-screen bg-gray-100 w-full">
        <div class="max-w-7xl mx-auto px-4 py-6">

            <!-- Top Filter Bar -->
            <div
                class="bg-white rounded-2xl shadow-sm border border-gray-200 p-4 mb-6"
            >
                <div class="flex flex-wrap justify-end gap-4">

                    <div class="w-full sm:w-[180px]">
                        <v-select
                            bg-color="#FFFFFF"
                            label="Standard"
                            :items="countries"
                            variant="outlined"
                            density="compact"
                            single-line
                            rounded
                            return-object
                            v-model="selectCountry"
                            item-title="title"
                            hide-details
                        />
                    </div>

                    <div class="w-full sm:w-[140px]">
                        <v-select
                            bg-color="#FFFFFF"
                            label="Year"
                            :items="yearOptions"
                            variant="outlined"
                            density="compact"
                            single-line
                            rounded
                            hide-details
                            v-model="currentYear"
                        />
                    </div>

                    <div class="w-full sm:w-[140px]">
                        <v-select
                            bg-color="#FFFFFF"
                            label="Week"
                            :items="weekOptions"
                            variant="outlined"
                            density="compact"
                            single-line
                            rounded
                            hide-details
                            v-model="currentWeek"
                        />
                    </div>

                    <div class="w-full sm:w-[180px]">
                        <v-select
                            bg-color="#FFFFFF"
                            label="Type"
                            :items="types"
                            variant="outlined"
                            density="compact"
                            single-line
                            rounded
                            hide-details
                            return-object
                            v-model="selectType"
                            item-title="region"
                        >
                            <template
                                v-if="selectType == 'All'"
                                v-slot:prepend-inner
                            >
                                <v-icon icon="mdi-view-dashboard" />
                            </template>
                        </v-select>
                    </div>
                </div>
            </div>

            <!-- Table -->
            <div
                class="bg-white rounded-3xl shadow-sm border border-gray-200 overflow-hidden"
            >

              <!-- Header -->
              <div
                  class="
                  hidden md:grid
                  grid-cols-12 items-center
                  px-6 py-4
                  bg-gray-50 border-b border-gray-200
                  text-sm font-semibold text-gray-600
                  uppercase tracking-wide
                  "
              >
                <div class="col-span-1 text-center">
                  {{ $t('Rank') }}
                </div>

                <div class="col-span-4">
                  {{ $t('Artist') }}
                </div>

                <div class="col-span-2">
                  {{ $t('Type') }}
                </div>

                <div class="col-span-2">
                  {{ $t('Popularity') }}
                </div>

                <div class="col-span-3">
                  {{ $t('Scores') }}
                </div>

                <div class="col-span-1"></div>
              </div>

                <!-- Rows -->
                <div class="divide-y divide-gray-100">
                    <TACard
                        v-for="(artist, i) in artistPresentList"
                        :key="i"
                        :value="artist"
                    />
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
    .selection-appearence {
        border-radius: 20% !important;
    }

</style>
