<script setup>
import { computed, onMounted, ref, watch } from 'vue';
import getUnicodeFlagIcon from 'country-flag-icons/unicode'
import axios from '@/axios';
import TACard from '@/views/TrendingArtists/components/TA_card.vue';

// Helper function to get ISO week number
const getISOWeek = (date) => {
    const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
    const dayNum = d.getUTCDay() || 7;
    d.setUTCDate(d.getUTCDate() + 4 - dayNum);
    const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
    return Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
}

// Country code mapping for API calls
const countryCodeMap = {
    'Global': 'global',
    'Taiwan': 'taiwan',
    'Hong Kong': 'hong-kong',
    'Japan': 'japan',
    'South Korea': 'south-korea',
    'Thailand': 'thailand',
    'Vietnam': 'vietnam',
    'Philippines': 'philippines',
    'Indonesia': 'indonesia',
    'United States': 'united-states',
    'Canada': 'canada',
    'Brazil': 'brazil',
    'Mexico': 'mexico',
    'United Kingdom': 'united-kingdom',
    'Germany': 'germany',
    'France': 'france',
    'Spain': 'spain',
    'Italy': 'italy',
    'Australia': 'australia'
}

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
        value: 'Global',
    })
const countries = ref([
    {
        title: `${getUnicodeFlagIcon(countriesFlag['Global'])} ${'Global'}`,
        value: 'Global',
    },
    {
        title: `${getUnicodeFlagIcon(countriesFlag['Taiwan'])} ${'Taiwan'}`,
        value: 'Taiwan',
    },
    {
        title: `${getUnicodeFlagIcon(countriesFlag['Hong Kong'])} ${'Hong Kong'}`,
        value: 'Hong Kong',
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
])
const selectType = ref('All')
const types = ref(['All', 'Actor', 'Musician'])

// Loading and error states
const loading = ref(false)
const error = ref(null)

// Year and week for API calls (defaults to current)
const currentYear = ref(new Date().getFullYear())
const currentWeek = ref(getISOWeek(new Date()))

// Artist list - starts empty, populated from API
const artistList = ref([])

const artistPresentList = computed(() => {
    if (selectType.value == 'Actor') {
        return artistList.value.filter((x) => x.type == 'Actor')
    } else if (selectType.value == 'Musician') {
        return artistList.value.filter((x) => x.type == 'Musician')
    } else {
        return artistList.value
    }
})

// Fetch Artist List from API
const fetchArtistList = async () => {
    loading.value = true
    error.value = null

    try {
        const countryCode = countryCodeMap[selectCountry.value.value] || 'global'
        const response = await axios.get(
            `/trending-artist/v1/rank/${countryCode}`,
            {
                params: {
                    year: currentYear.value,
                    week: currentWeek.value
                }
            }
        )

        // Map API response to component's expected format
        if (response.data && response.data.data) {
            artistList.value = response.data.data.map((artist) => ({
                artistId: artist.artist_id,
                artistName: artist.english_name || artist.korean_name || 'Unknown',
                rank: artist.rank,
                icon: artist.image_url || 'https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/twitter-logo.svg',
                type: Array.isArray(artist.type) ? artist.type[0] : (artist.type || 'Unknown'),
                popularity: artist.popularity || 0,
                nation: artist.nation,
                // Additional data for potential use
                musicScore: artist.total_music_score || 0,
                snsScore: artist.total_sns_score || 0,
                dramaScore: artist.total_drama_score || 0,
            }))
        }
    } catch (err) {
        console.error('Error fetching artist list:', err)
        error.value = 'Failed to load artist rankings. Please try again.'
        // Keep existing data if fetch fails
    } finally {
        loading.value = false
    }
}

// Watch for country changes and refetch
watch(selectCountry, () => {
    fetchArtistList()
})

// Fetch on component mount
onMounted(() => {
    fetchArtistList()
})
</script>

<template>
    <v-container
    fluid
    :class="['bg-grey-lighten-4', 'fill-height', 'align-start']"
    >
    <v-container
    >
        <div :class="['d-flex', 'justify-end', 'align-center', 'ga-5']">
            <!-- Region Selection -->
                <v-select
                    bg-color="#FFFFFF"
                    :minWidth="100"
                    :maxWidth="200"
                    label="Standard"
                    :items="countries"
                    variant="outlined"
                    single-line
                    density="compact"
                    return-object
                    v-model="selectCountry"
                    item-title="title"
                    rounded
                >
                </v-select>
                <v-select
                    bg-color="#FFFFFF"

                    :minWidth="100"
                    :maxWidth="200"
                    rounded
                    label="Type"
                    :items="types"
                    variant="outlined"
                    density="compact"
                    single-line
                    return-object
                    v-model="selectType"
                    item-title="region"
                >
                    <template v-if="selectType == 'All'" v-slot:prepend-inner>
                        <v-icon :icon="'mdi-view-dashboard'" />
                    </template>
                </v-select>
        </div>
        <v-row
        :class="['px-3']">
            <v-col
            cols="1">
            <span :class="['font-weight-medium', 'text-body-1']">{{ $t('Rank') }}</span>
            </v-col>
            <v-col
            cols="6">
            <span :class="['font-weight-medium', 'text-body-1']">{{ $t('Artist') }}</span>
            </v-col>
            <v-col
            cols="2">
            <span :class="['font-weight-medium', 'text-body-1']">{{ $t('Popularity') }}</span>
            </v-col>
            <v-col
            cols="3">
            <span :class="['font-weight-medium', 'text-body-1']">{{ $t('7-day Change') }}</span>
            </v-col>
        </v-row>
        <!-- Loading State -->
        <v-row v-if="loading" justify="center" class="my-5">
            <v-progress-circular indeterminate color="primary"></v-progress-circular>
        </v-row>

        <!-- Error State -->
        <v-alert v-else-if="error" type="error" class="my-3">
            {{ error }}
        </v-alert>

        <!-- Empty State -->
        <v-alert v-else-if="artistPresentList.length === 0" type="info" class="my-3">
            No artists found for the selected criteria.
        </v-alert>

        <!-- Artist Cards -->
        <TACard v-else v-for="(artist, i) in artistPresentList" :value="artist" :key="i">
        </TACard>
    </v-container>

    </v-container>
</template>
<style scoped>
    .selection-appearence {
        border-radius: 20% !important;
    }

</style>