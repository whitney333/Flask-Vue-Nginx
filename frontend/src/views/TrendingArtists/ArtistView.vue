<script setup>
    import axios from '@/axios';
    import { useRoute, useRouter } from 'vue-router';
    import getUnicodeFlagIcon from 'country-flag-icons/unicode'
    import AVCard from '@/views/TrendingArtists/components/AV_card.vue'

    const route = useRoute()
    const router = useRouter()
    const artistName = route.params.artistName
    const artistId = route.params.artistId
    const handleBackBtn = () => {
        router.go(-1)
    }
    const artistExample = {
        artistId: 15,
        artistName: 'Byeon WooSeok',
        rank: 1,
        icon: 'https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/twitter-logo.svg',
        type: 'Actor',
        country: 'South Korea',
        popularity: 78426,
        sns: 35421,
        music: 52123,
        drama: 0,
        rank: {
            'Taiwan': 12,
            'Hong Kong': 12,
            'Japan': 12,
            'South Korea': 120,
            'Thailand': 120,
            'Vietnam': 12,
            'Philippines': 120,
            'Indonesia': 12,
            'United States': 12,
            'Canada': 12,
            'Brazil': 120,
            'Mexico': 12,
            'United Kingdom': 12,
            'Germany': 12,
            'France': 120,
            'Spain': 12,
            'Italy': 120,
            'Australia': 120
        },
        spotifyLink: '',
        instaLink: '',
        youtubeLink: '',
        tiktokLink: '',
    }
    const countriesFlag = {
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
    const formatNumber = (number) => {

    }



    const fetchArtistDetails = () => {
        const data = axios.get(``)
    }

    const popularityDetails = {
        chart: "popularityDetails",
        title: "Popularity",
        type: 'Popularity',
        tooltipText: "Number of followers on Instagram",
        fetchURL: "/instagram/chart/follower",
        fetchFollowerType: 'result',
        followerDataType: 'follower_count',
        fetchDateType: 'datetime',
    }

    const snsDetails = {
        title: 'SNS',
        chart: "snsDetails",
        type: 'SNS',
        tooltipText: "Todo",
        fetchURL: "/instagram/threads/follower",
        fetchFollowerType: 'result',
        followerDataType: 'threads_followers',
        fetchDateType: 'datetime',
    }

    const musicDetails = {
        title: 'Music',
        tooltipText: 'To do',
        chart: "musicDetails",
        type: 'Music',
        tooltipText: "todo",
        fetchURL: "/instagram/chart",
        fetchFollowerType: 'result',
        followerDataType: 'total_comment',
        fetchDateType: 'datetime',
    }

</script>

<template>
    <v-container
    fluid
    :class="['fill-height', 'align-start']"
    >
        <v-btn
        icon="mdi-arrow-left"
        @click="handleBackBtn"
        position="fixed"
        variant="text"
        style="z-index: 1;"
        >

        </v-btn>
        <v-container>
            <v-row
            align="center">
                <v-col cols="12" lg="6">
                    <v-row
                    align="center"
                    justify="center">
                        <v-col cols="12" md="6" >
                            <v-avatar 
                                color="info" 
                                size="200">
                                    <v-img
                                    :src="artistExample.icon">
                                    </v-img>
                                </v-avatar>
                        </v-col>
                        <v-col cols="12" md="6">
                            <v-card
                            flat
                            :class="['py-10']">
                                <template 
                                v-slot:title>
                                    <span
                                    :class="['text-h5', 'font-weight-bold']">
                                        {{ artistName }}
                                    </span>
                                </template>
                                <template v-slot:text>
                                    <template
                                    v-for="(rank, country) in artistExample.rank"
                                    :key="country"
                                    >
                                    <span 
                                    v-if="rank <= 100"
                                    :class="['text-h6']">
                                        {{  getUnicodeFlagIcon(countriesFlag[country]) }}
                                        <v-tooltip
                                            activator="parent"
                                            location="right"
                                            >
                                        {{`${country} #${rank}`}}
                                        </v-tooltip>
                                    </span>
                                    <span 
                                    v-else
                                    :class="['text-h6']"
                                    style="filter: grayscale(100%);">
                                        {{  getUnicodeFlagIcon(countriesFlag[country]) }}
                                    <v-tooltip
                                        activator="parent"
                                        location="right"
                                        >
                                    {{`${country} # -`}}
                                    </v-tooltip>
                                    </span>
                                    <!-- {{ country }} -->
                                    </template>
                                    <br />
                                    <div :class="['my-2']">
                                        <span
                                        :class="['text-h5']"
                                        >
                                        {{ `${getUnicodeFlagIcon(countriesFlag[artistExample.country])} ` }}
                                        </span>
                                        <span
                                        :class="['text-h6', 'font-weight-800']">
                                        {{ `${artistExample.country}` }}
                                        </span>
                                    </div>
                                    <v-row>
                                        <v-col
                                        md="3">
                                            <a 
                                            style="max-height: 35px; max-width: 35px;"
                                            :href="artistExample.instaLink">
                                            <v-img
                                            max-height="35"
                                            max-width="35"
                                            src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/instagram-logo.svg" />
                                            </a>
                                        </v-col>
                                        <v-col
                                        md="3">
                                            <a
                                            style="max-height: 35px; max-width: 35px;"
                                            :href="artistExample.spotifyLink">
                                                <v-img
                                                max-height="35"
                                                max-width="35"
                                                src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/spotify-logo.svg" />
                                            </a>
                                        </v-col>
                                        <v-col
                                        md="3">
                                            <a
                                            style="max-height: 35px; max-width: 35px;"
                                            :href="artistExample.tiktokLink">
                                                <v-img
                                                max-height="35"
                                                max-width="35"
                                                src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/tiktok-logo.svg" />
                                            </a>
                                        </v-col>
                                        <v-col
                                        md="3">
                                            <a
                                            style="max-height: 35px; max-width: 35px;"
                                            :href="artistExample.youtubeLink">
                                                <v-img
                                                max-height="35"
                                                max-width="35"
                                                src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/youtube-logo.svg" />
                                            </a>
                                        </v-col>
                                    </v-row>

                                
                                </template>
                            </v-card>
                        </v-col>
                    </v-row>
                </v-col>
                <v-col cols="12" lg="6" :class="['align-self']" >
                    <v-card rounded="xl" :class="['bg-grey-lighten-4', 'pa-3']">
                        <template v-slot:text>
                            <v-row
                            align="center"
                            justify="center">
                                <v-col
                                cols="6"
                                md="3"
                                :class="['text-center']">
                                    <v-icon 
                                    :class="['mb-1']" 
                                    icon="mdi-fire"></v-icon>
                                    <span>
                                        Popularity
                                    </span>
                                    <div v-if="artistExample.popularity != 0" :class="['text-h5', 'font-weight-bold']">
                                        {{ artistExample.popularity.toLocaleString('en-US') }}
                                    </div>
                                    <div v-else :class="['text-h5', 'font-weight-bold']">
                                        -
                                    </div>

                                    
                                </v-col>
                                <v-divider vertical></v-divider>
                                <v-col
                                cols="6"
                                md="3"
                                :class="['text-center']">
                                    <v-icon 
                                    :class="['mb-1']" 
                                    icon="mdi-account-group-outline"></v-icon>
                                    <span>
                                        SNS
                                    </span>
                                    <div v-if="artistExample.sns != 0" :class="['text-h5', 'font-weight-bold']">
                                        {{ artistExample.sns.toLocaleString('en-US') }}
                                    </div>
                                    <div v-else :class="['text-h5', 'font-weight-bold']">
                                        -
                                    </div>
                                </v-col>
                                <v-divider vertical :class="['d-none', 'd-md-block']"></v-divider>
                                <v-col
                                cols="6"
                                md="3"
                                :class="['text-center']">
                                    <v-icon 
                                    :class="['mb-1']" 
                                    icon="mdi-music-note"></v-icon>
                                    <span>
                                        Music
                                    </span>
                                    <div v-if="artistExample.music != 0" :class="['text-h5', 'font-weight-bold']">
                                        {{ artistExample.music.toLocaleString('en-US') }}
                                    </div>
                                    <div v-else :class="['text-h5', 'font-weight-bold']">
                                        -
                                    </div>

                                    
                                </v-col>
                                <v-divider vertical></v-divider>
                                <v-col
                                cols="6"
                                md="3"
                                :class="['text-center']">
                                    <v-icon 
                                    :class="['mb-1']" 
                                    icon="mdi-television"></v-icon>
                                    <span>
                                        Drama
                                    </span>
                                    <div v-if="artistExample.drama != 0" :class="['text-h5', 'font-weight-bold']">
                                        {{ artistExample.drama.toLocaleString('en-US') }}
                                    </div>
                                    <div v-else :class="['text-h5', 'font-weight-bold']">
                                        -
                                    </div>

                                </v-col>
                            </v-row>
                        </template>
                    </v-card>

                </v-col>
            </v-row>
            <br />
            <br />
            <AVCard :value="popularityDetails" />
            <AVCard :value="snsDetails" />
            <AVCard :value="musicDetails" />

        </v-container>
    </v-container>

</template>