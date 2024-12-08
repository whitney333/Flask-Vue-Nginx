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
const artistList = ref([
    {
        artistId: 15,
        artistName: 'Byeon WooSeok',
        rank: 1,
        icon: 'https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/twitter-logo.svg',
        type: 'Actor',
        popularity: 78426,

    },
    {
        artistId: 2,
        artistName: 'Kim SooHyun',
        rank: 2,
        icon: 'https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/twitter-logo.svg',
        type: 'Actor',
        popularity: 72391
    },
    {
        artistId: 44,
        artistName: 'Kim JiWon',
        rank: 3,
        icon: 'https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/twitter-logo.svg',
        type: 'Actor',
        popularity: 70514
    },
    {
        artistId: 10,
        artistName: 'Kim HyeYoon',
        rank: 4,
        icon: 'https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/twitter-logo.svg',
        type: 'Actor',
        popularity: 69685
    },
    {
        artistId: 55,
        artistName: 'NewJeans',
        rank: 5,
        icon: 'https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/twitter-logo.svg',
        type: 'Musician',
        popularity: 68125
    }

])
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

    // fetch Artist List everytime the country changed
    const fetchArtistList = async () => {
        const data = await axios.get(`trendingartist/rank/${selectCountry.value.split(" ").join('').toLowerCase()}`)
        artistList.value = data
    }
    
    // watch(selectCountry, fetchArtistList)
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
        <TACard v-for="(artist, i) in artistPresentList" :value="artist" :key="i">

        </TACard>
    </v-container>

    </v-container>
</template>
<style scoped>
    .selection-appearence {
        border-radius: 20% !important;
    }

</style>