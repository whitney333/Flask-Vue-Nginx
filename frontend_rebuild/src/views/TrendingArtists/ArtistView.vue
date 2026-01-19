<script setup>
    import axios from '@/axios';
    import { onMounted, ref, computed } from 'vue';
    import { useRoute, useRouter } from 'vue-router';
    import getUnicodeFlagIcon from 'country-flag-icons/unicode'
    import AVCard from '@/views/TrendingArtists/components/AV_card.vue'

    const route = useRoute()
    const router = useRouter()
    const artistName = route.params.artistName
    const artistId = route.params.artistId

    // Helper function to get ISO week number
    const getISOWeek = (date) => {
        const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
        const dayNum = d.getUTCDay() || 7;
        d.setUTCDate(d.getUTCDate() + 4 - dayNum);
        const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
        return Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
    }

    // Year and week for API calls
    const currentYear = ref(new Date().getFullYear())
    const currentWeek = ref(getISOWeek(new Date()))

    // Loading and error states
    const loading = ref(true)
    const error = ref(null)

    // Artist data - reactive, populated from API
    const artist = ref({
        artistId: null,
        artistName: '',
        icon: 'https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/twitter-logo.svg',
        type: '',
        country: '',
        popularity: 0,
        sns: 0,
        music: 0,
        drama: 0,
        // TODO: rank by country not implemented - showing empty for now
        rank: {},
        globalRank: null,
        spotifyLink: '',
        instaLink: '',
        youtubeLink: '',
        tiktokLink: '',
    })

    // Nation to country name mapping
    const nationToCountry = {
        'TW': 'Taiwan',
        'HK': 'Hong Kong',
        'JP': 'Japan',
        'KR': 'South Korea',
        'TH': 'Thailand',
        'VN': 'Vietnam',
        'PH': 'Philippines',
        'ID': 'Indonesia',
        'US': 'United States',
        'CA': 'Canada',
        'BR': 'Brazil',
        'MX': 'Mexico',
        'GB': 'United Kingdom',
        'DE': 'Germany',
        'FR': 'France',
        'ES': 'Spain',
        'IT': 'Italy',
        'AU': 'Australia'
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

    const handleBackBtn = () => {
        router.go(-1)
    }

    const formatNumber = (number) => {
        if (!number) return '-'
        return number.toLocaleString('en-US')
    }

    // Fetch artist details from API
    const fetchArtistDetails = async () => {
        if (!artistId) {
            error.value = 'No artist ID provided'
            loading.value = false
            return
        }

        loading.value = true
        error.value = null

        try {
            const response = await axios.get(
                `/trending-artist/v1/artist/${artistId}`,
                {
                    params: {
                        year: currentYear.value,
                        week: currentWeek.value
                    }
                }
            )

            if (response.data && response.data.data) {
                const data = response.data.data

                // Get country name from nation code
                const countryName = nationToCountry[data.nation] || data.nation || 'Unknown'

                // Construct social media links from platform IDs
                const instaLink = data.instagram_user
                    ? `https://instagram.com/${data.instagram_user}`
                    : ''
                const spotifyLink = data.spotify_id
                    ? `https://open.spotify.com/artist/${data.spotify_id}`
                    : ''
                const youtubeLink = data.youtube_id
                    ? `https://youtube.com/channel/${data.youtube_id}`
                    : ''
                const tiktokLink = data.tiktok_id
                    ? `https://tiktok.com/@${data.tiktok_id}`
                    : ''

                artist.value = {
                    artistId: data.artist_id,
                    artistName: data.english_name || data.korean_name || artistName,
                    icon: data.image_url || 'https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/twitter-logo.svg',
                    type: Array.isArray(data.type) ? data.type[0] : (data.type || ''),
                    country: countryName,
                    popularity: data.popularity || 0,
                    sns: data.total_sns_score || 0,
                    music: data.total_music_score || 0,
                    drama: data.total_drama_score || 0,
                    // TODO: rank by country not implemented
                    rank: data.rank_by_country || {},
                    globalRank: data.global_rank,
                    spotifyLink,
                    instaLink,
                    youtubeLink,
                    tiktokLink,
                    // Store IDs for chart components
                    instagramId: data.instagram_id,
                    youtubeId: data.youtube_id,
                    spotifyId: data.spotify_id,
                }
            }
        } catch (err) {
            console.error('Error fetching artist details:', err)
            error.value = 'Failed to load artist details. Please try again.'
        } finally {
            loading.value = false
        }
    }

    // Chart configurations - these will be passed to AVCard components
    // Note: The fetchURL paths need to match existing backend endpoints
    const popularityDetails = computed(() => ({
        chart: "popularityDetails",
        title: "Popularity",
        type: 'Popularity',
        tooltipText: "Number of followers on Instagram",
        fetchURL: `/instagram/v1/follower?artist_id=${artist.value.instagramId}`,
        fetchFollowerType: 'result',
        followerDataType: 'follower_count',
        fetchDateType: 'datetime',
    }))

    const snsDetails = computed(() => ({
        title: 'SNS',
        chart: "snsDetails",
        type: 'SNS',
        tooltipText: "Threads followers count",
        fetchURL: `/instagram/v1/threads-follower?artist_id=${artist.value.instagramId}`,
        fetchFollowerType: 'result',
        followerDataType: 'threads_followers',
        fetchDateType: 'datetime',
    }))

    const musicDetails = computed(() => ({
        title: 'Music',
        chart: "musicDetails",
        type: 'Music',
        tooltipText: "Music streaming performance",
        fetchURL: `/instagram/v1/comment?artist_id=${artist.value.instagramId}`,
        fetchFollowerType: 'result',
        followerDataType: 'total_comment',
        fetchDateType: 'datetime',
    }))

    // Fetch data on mount
    onMounted(() => {
        fetchArtistDetails()
    })
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

        <!-- Loading State -->
        <v-container v-if="loading" class="d-flex justify-center align-center" style="min-height: 400px;">
            <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
        </v-container>

        <!-- Error State -->
        <v-container v-else-if="error">
            <v-alert type="error" class="my-3">
                {{ error }}
            </v-alert>
        </v-container>

        <!-- Main Content -->
        <v-container v-else>
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
                                    :src="artist.icon">
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
                                        {{ artist.artistName || artistName }}
                                    </span>
                                    <span v-if="artist.globalRank" :class="['text-body-1', 'ml-2']">
                                        (Global #{{ artist.globalRank }})
                                    </span>
                                </template>
                                <template v-slot:text>
                                    <!-- TODO: Rank by country not implemented yet -->
                                    <!-- Will show country flags with ranks when implemented -->
                                    <template
                                    v-for="(rank, country) in artist.rank"
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
                                    </template>
                                    <br />
                                    <div :class="['my-2']" v-if="artist.country && countriesFlag[artist.country]">
                                        <span
                                        :class="['text-h5']"
                                        >
                                        {{ `${getUnicodeFlagIcon(countriesFlag[artist.country])} ` }}
                                        </span>
                                        <span
                                        :class="['text-h6', 'font-weight-800']">
                                        {{ `${artist.country}` }}
                                        </span>
                                    </div>
                                    <v-row>
                                        <v-col
                                        md="3"
                                        v-if="artist.instaLink">
                                            <a
                                            style="max-height: 35px; max-width: 35px;"
                                            :href="artist.instaLink"
                                            target="_blank">
                                            <v-img
                                            max-height="35"
                                            max-width="35"
                                            src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/instagram-logo.svg" />
                                            </a>
                                        </v-col>
                                        <v-col
                                        md="3"
                                        v-if="artist.spotifyLink">
                                            <a
                                            style="max-height: 35px; max-width: 35px;"
                                            :href="artist.spotifyLink"
                                            target="_blank">
                                                <v-img
                                                max-height="35"
                                                max-width="35"
                                                src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/spotify-logo.svg" />
                                            </a>
                                        </v-col>
                                        <v-col
                                        md="3"
                                        v-if="artist.tiktokLink">
                                            <a
                                            style="max-height: 35px; max-width: 35px;"
                                            :href="artist.tiktokLink"
                                            target="_blank">
                                                <v-img
                                                max-height="35"
                                                max-width="35"
                                                src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/tiktok-logo.svg" />
                                            </a>
                                        </v-col>
                                        <v-col
                                        md="3"
                                        v-if="artist.youtubeLink">
                                            <a
                                            style="max-height: 35px; max-width: 35px;"
                                            :href="artist.youtubeLink"
                                            target="_blank">
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
                                    <div v-if="artist.popularity != 0" :class="['text-h5', 'font-weight-bold']">
                                        {{ formatNumber(artist.popularity) }}
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
                                    <div v-if="artist.sns != 0" :class="['text-h5', 'font-weight-bold']">
                                        {{ formatNumber(artist.sns) }}
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
                                    <div v-if="artist.music != 0" :class="['text-h5', 'font-weight-bold']">
                                        {{ formatNumber(artist.music) }}
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
                                    <div v-if="artist.drama != 0" :class="['text-h5', 'font-weight-bold']">
                                        {{ formatNumber(artist.drama) }}
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
            <!-- Only show charts if we have the required IDs -->
            <AVCard v-if="artist.instagramId" :value="popularityDetails" />
            <AVCard v-if="artist.instagramId" :value="snsDetails" />
            <AVCard v-if="artist.instagramId" :value="musicDetails" />
        </v-container>
    </v-container>
</template>