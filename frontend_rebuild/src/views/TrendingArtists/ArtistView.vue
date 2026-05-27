<script setup>
import { computed, onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from '@/axios';
import AVCard from '@/views/TrendingArtists/components/AV_card.vue';

const route = useRoute();
const router = useRouter();

const artistId = route.params.artistId;
const artistName = route.params.artistName;
const artistInfo = ref({});
const artistRanks = ref({});
const rankMeta = ref({
  artist_id: artistId,
  year: Number(route.query.year) || null,
  week: Number(route.query.week) || null,
});

const countries = [
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
];

const fallbackImage = 'https://cdn.revmishkan.com/dist/mishkan-logo.svg';

const getWeekNumber = (date = new Date()) => {
  const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
  const dayNum = d.getUTCDay() || 7;
  d.setUTCDate(d.getUTCDate() + 4 - dayNum);
  const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
  return Math.ceil(((d - yearStart) / 86400000 + 1) / 7);
};

const getLastISOWeek = () => {
  const d = new Date();
  d.setDate(d.getDate() - 7);

  return {
    year: d.getFullYear(),
    week: getWeekNumber(d),
  };
};

const fallbackWeek = getLastISOWeek();
const currentYear = ref(Number(route.query.year) || fallbackWeek.year);
const currentWeek = ref(Number(route.query.week) || fallbackWeek.week);

const toNumber = (value) => {
  const number = Number(value ?? 0);
  return Number.isFinite(number) ? number : 0;
};

const formatScore = (value) => {
  const number = toNumber(value);

  if (number === 0) {
    return '-';
  }

  return number.toLocaleString('en-US', {
    maximumFractionDigits: 2,
  });
};

const artistDetails = computed(() => ({
  artistId,
  artistName: artistInfo.value.artist || artistName,
  koreanName: artistInfo.value.korean_name || route.query.koreanName || '',
  image: artistInfo.value.image || route.query.image || fallbackImage,
  type: artistInfo.value.type || route.query.type || '-',
  popularity: toNumber(route.query.popularityScore),
  sns: toNumber(route.query.snsScore),
  music: toNumber(route.query.musicScore),
  drama: toNumber(route.query.dramaScore),
}));

const artistDisplayName = computed(() => {
  if (!artistDetails.value.koreanName || artistDetails.value.koreanName === artistDetails.value.artistName) {
    return artistDetails.value.artistName;
  }

  return `${artistDetails.value.artistName} (${artistDetails.value.koreanName})`;
});

const artistTypeColor = computed(() => {
  const colors = {
    Actor: 'blue',
    Musician: 'deep-purple',
  };

  return colors[artistDetails.value.type] || 'grey';
});

const socialLinks = computed(() => [
  {
    key: 'instagram',
    href: artistInfo.value.instagram_user ? `https://instagram.com/${artistInfo.value.instagram_user}` : '',
    icon: 'https://cdn.revmishkan.com/dist/instagram-logo.svg',
  },
  {
    key: 'spotify',
    href: artistInfo.value.spotify_id ? `https://open.spotify.com/artist/${artistInfo.value.spotify_id}` : '',
    icon: 'https://cdn.revmishkan.com/dist/spotify-logo.svg',
  },
  {
    key: 'tiktok',
    href: artistInfo.value.tiktok_id ? `https://www.tiktok.com/@${artistInfo.value.tiktok_id}` : '',
    icon: 'https://cdn.revmishkan.com/dist/tiktok-logo.svg',
  },
  {
    key: 'youtube',
    href: artistInfo.value.youtube_id ? `https://youtube.com/channel/${artistInfo.value.youtube_id}` : '',
    icon: 'https://cdn.revmishkan.com/dist/youtube-logo.svg',
  },
  {
    key: 'weibo',
    href: artistInfo.value.weibo_id ? `https://weibo.com/u/${artistInfo.value.weibo_id}` : '',
    icon: 'https://cdn.revmishkan.com/dist/weibo-logo.svg',
  },
  {
    key: 'bilibili',
    href: artistInfo.value.bilibili_id ? `https://space.bilibili.com/${artistInfo.value.bilibili_id}` : '',
    icon: 'https://cdn.revmishkan.com/dist/bilibili-logo.svg',
  },
].filter((link) => link.href));

const countryRankItems = computed(() => {
  return countries.map((country) => {
    const rank = artistRanks.value?.[country.value];

    return {
      ...country,
      rank,
      hasRank: rank !== undefined && rank !== null,
    };
  });
});

const rankedCountryCount = computed(() => {
  return countryRankItems.value.filter((country) => country.hasRank).length;
});

const scoreCards = computed(() => [
  {
    mode: 'metric',
    title: 'Popularity',
    type: 'Popularity',
    icon: 'mdi-fire',
    color: 'orange',
    value: artistDetails.value.popularity,
    tooltipText: 'Trending artist overall popularity score',
  },
  {
    mode: 'metric',
    title: 'SNS',
    type: 'SNS',
    icon: 'mdi-account-group-outline',
    color: 'teal',
    value: artistDetails.value.sns,
    tooltipText: 'Trending artist SNS score',
  },
  {
    mode: 'metric',
    title: 'Music',
    type: 'Music',
    icon: 'mdi-music-note',
    color: 'deep-purple',
    value: artistDetails.value.music,
    tooltipText: 'Trending artist music score',
  },
  {
    mode: 'metric',
    title: 'Drama',
    type: 'Drama',
    icon: 'mdi-television',
    color: 'blue',
    value: artistDetails.value.drama,
    tooltipText: 'Trending artist drama score',
  },
]);

const handleBackBtn = () => {
  router.go(-1);
};

const fetchArtistInfo = async () => {
  try {
    const response = await axios.get('/artist/info', {
      params: {
        artist_id: artistId,
      },
    });

    artistInfo.value = response.data?.data?.[0] || {};
  } catch (error) {
    console.error('Fetch artist info failed:', error);
    artistInfo.value = {};
  }
};

const fetchArtistRankMeta = async () => {
  try {
    const res = await axios.get('/trending-artist/v2/ranks', {
      params: {
        artist_id: artistId,
        year: currentYear.value,
        week: currentWeek.value,
      },
    });

    const data = res.data?.data || {};

    artistRanks.value = data.rank || {};
    rankMeta.value = {
      artist_id: data.artist_id || artistId,
      year: Number(data.year) || currentYear.value,
      week: Number(data.week) || currentWeek.value,
    };
  } catch (err) {
    console.error('Fetch ranks failed:', err);
    artistRanks.value = {};
  }
};

onMounted(() => {
  fetchArtistInfo();
  fetchArtistRankMeta();
});
</script>

<template>
  <div class="min-h-screen bg-gray-100">
    <div class="max-w-7xl mx-auto px-4 py-6">
      <v-btn
        icon="mdi-arrow-left"
        @click="handleBackBtn"
        variant="text"
        class="mb-4"
      />

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <section class="lg:col-span-5 bg-white rounded-3xl border border-gray-200 shadow-sm p-6">
          <div class="flex flex-col sm:flex-row gap-5">
            <div class="w-32 h-32 rounded-2xl overflow-hidden bg-gray-100 shrink-0">
              <img
                :src="artistDetails.image"
                :alt="artistDisplayName"
                class="w-full h-full object-cover"
              />
            </div>

            <div class="min-w-0 flex-1">
              <div class="flex flex-wrap items-center gap-2 mb-3">
                <v-chip
                  :color="artistTypeColor"
                  size="small"
                  variant="tonal"
                  rounded="lg"
                >
                  {{ artistDetails.type }}
                </v-chip>
                <v-chip
                  size="small"
                  variant="tonal"
                  rounded="lg"
                >
                  Week {{ rankMeta.week || currentWeek }}
                </v-chip>
              </div>

              <h1 class="text-2xl font-bold text-gray-900 leading-tight">
                {{ artistDisplayName }}
              </h1>

              <div
                v-if="socialLinks.length"
                class="flex flex-wrap gap-3 mt-5"
              >
                <a
                  v-for="link in socialLinks"
                  :key="link.key"
                  :href="link.href"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="w-9 h-9 rounded-lg border border-gray-200 flex items-center justify-center hover:bg-gray-50 transition"
                >
                  <img
                    :src="link.icon"
                    :alt="link.key"
                    class="max-w-5 max-h-5"
                  />
                </a>
              </div>
            </div>
          </div>
        </section>

        <section class="lg:col-span-7 bg-white rounded-3xl border border-gray-200 shadow-sm p-6">
          <div class="flex items-start justify-between gap-4 mb-5">
            <div>
              <div class="flex items-center gap-2 text-gray-900 font-semibold">
                <v-icon icon="mdi-trophy" color="amber" size="20" />
                Country Ranking
              </div>
              <div class="text-sm text-gray-500 mt-1">
                {{ rankMeta.year || currentYear }} Week {{ rankMeta.week || currentWeek }} · {{ rankedCountryCount }} ranked markets
              </div>
            </div>
          </div>

          <div class="flex flex-wrap gap-3">
            <v-tooltip
              v-for="country in countryRankItems"
              :key="country.value"
              location="top"
            >
              <template #activator="{ props }">
                <div
                  v-bind="props"
                  class="w-10 h-10 rounded-xl border border-gray-200 bg-white flex items-center justify-center cursor-default"
                  :class="{ 'ranked-country': country.hasRank, 'unranked-country': !country.hasRank }"
                >
                  <v-icon
                    v-if="country.type === 'icon'"
                    :icon="country.icon"
                    size="24"
                    :color="country.hasRank ? 'primary' : 'grey'"
                  />
                  <span
                    v-else
                    :class="['fi', `fi-${country.flag}`, { 'flag-muted': !country.hasRank }]"
                  />
                </div>
              </template>
              <span v-if="country.hasRank">
                {{ country.title }} #{{ country.rank }}
              </span>
              <span v-else>
                {{ country.title }} no ranking
              </span>
            </v-tooltip>
          </div>
        </section>
      </div>

      <v-row class="mt-6">
        <v-col
          v-for="card in scoreCards"
          :key="card.type"
          cols="12"
          md="6"
          lg="3"
        >
          <AVCard :value="card" />
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<style scoped>
.ranked-country {
  box-shadow: 0 1px 2px rgba(15, 23, 42, 0.08);
}

.unranked-country {
  opacity: 0.55;
}

.flag-muted {
  filter: grayscale(1);
}
</style>
