<script setup>
import { computed, onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from '@/axios';
import AVCard from '@/views/TrendingArtists/components/AV_card.vue';
import { useI18n } from 'vue-i18n'

const i18n = useI18n()
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

  return colors[artistDetails.value.type] || 'green';
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

const scoreCardKeys = [
  {
    key: 'popularity',
    icon: 'mdi-fire',
    color: 'orange',
    valueKey: 'popularity'
  },
  { key: 'sns',
    icon: 'mdi-account-group-outline',
    color: 'teal',
    valueKey: 'sns'
  },
  {
    key: 'music',
    icon: 'mdi-music-note',
    color: 'deep-purple',
    valueKey: 'music'
  },
  {
    key: 'drama',
    icon: 'mdi-television',
    color: 'blue',
    valueKey: 'drama'
  }
]

const scoreCards = computed(() =>
  scoreCardKeys.map(c => ({
    ...c,
    title: i18n.t(`trending_artist.${c.key}`),
    value: artistDetails.value[c.valueKey],
  }))
)

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
    <div class="max-w-7xl mx-auto px-4 py-6 space-y-6">

      <!-- back button -->
      <v-btn
        icon="mdi-arrow-left"
        @click="handleBackBtn"
        variant="text"
        class="transition hover:scale-105 active:scale-95"
      />

      <!-- ROW 1 -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">

        <!-- ARTIST -->
        <section
          class="lg:col-span-5
                 bg-transparent lg:bg-white
                 lg:border lg:border-gray-200
                 lg:rounded-3xl lg:shadow-sm
                 lg:p-6"
        >
          <div class="flex flex-col sm:flex-row gap-5 items-center sm:items-start text-center sm:text-left">

            <div class="w-28 h-28 sm:w-32 sm:h-32 rounded-2xl overflow-hidden bg-gray-100 shrink-0
                        transition duration-300 hover:scale-105">
              <img
                :src="artistDetails.image"
                :alt="artistDisplayName"
                class="w-full h-full object-cover"
              />
            </div>

            <div class="flex-1 min-w-0">

              <v-chip :color="artistTypeColor"
                      size="small"
                      variant="tonal"
                      v-for="type in artistDetails.type"
                      :key="type"
              >
                {{ type }}
              </v-chip>

              <h1 class="text-xl sm:text-2xl font-bold text-gray-900 mt-2">
                {{ artistDisplayName }}
              </h1>

              <div
                v-if="socialLinks.length"
                class="flex gap-3 mt-4 justify-center sm:justify-start flex-wrap"
              >
                <a
                  v-for="link in socialLinks"
                  :key="link.key"
                  :href="link.href"
                  target="_blank"
                  class="w-9 h-9 flex items-center justify-center rounded-lg border
                         border-gray-200 hover:bg-gray-50 transition
                         hover:scale-105 active:scale-95"
                >
                  <img :src="link.icon" class="w-5 h-5" />
                </a>
              </div>

            </div>
          </div>
        </section>

        <!-- COUNTRY RANKING -->
        <section
          class="lg:col-span-7
                 bg-transparent lg:bg-white
                 lg:border lg:border-gray-200
                 lg:rounded-3xl lg:shadow-sm
                 lg:p-6
                 p-4"
        >

          <!-- header -->
          <div class="flex items-start justify-between mb-4">
            <div>
              <div class="flex items-center gap-2 font-semibold text-gray-900">
                <v-icon icon="mdi-trophy" color="amber" size="20"/>
                {{ $t('trending_artist.country_ranking') }}
              </div>

              <div class="text-xs sm:text-sm text-gray-500 mt-1">
                {{ rankMeta.year || currentYear }} W{{ rankMeta.week || currentWeek }}
                · {{ rankedCountryCount }} markets
              </div>
            </div>
          </div>

          <!-- flags (FIXED SCOPE) -->
          <div
            class="
              flex gap-3 pb-2 scrollbar-hide
              flex-nowrap overflow-x-auto
              lg:flex-wrap lg:overflow-visible
            "
          >
            <v-tooltip
              v-for="country in countryRankItems"
              :key="country.value"
              location="top"
            >
              <template #activator="{ props }">
                <div
                  v-bind="props"
                  class="
                    w-10 h-10 flex-shrink-0
                    rounded-xl border
                    flex items-center justify-center
                    transition duration-200 hover:scale-110
                  "
                  :class="country.hasRank
                    ? 'bg-white border-gray-200'
                    : 'bg-gray-50 border-gray-200 opacity-40'"
                >

                  <v-icon
                    v-if="country.type === 'icon'"
                    :icon="country.icon"
                    size="22"
                    :color="country.hasRank ? 'primary' : 'grey'"
                  />

                  <span v-else :class="['fi', `fi-${country.flag}`]" />
                </div>
              </template>

              <span v-if="country.hasRank">
                {{ $t(`country.${country.title}`) }} #{{ country.rank }}
              </span>

              <span v-else>
                {{ $t(`country.${country.title}`) }} no ranking
              </span>
            </v-tooltip>
          </div>

        </section>

      </div>

      <!-- SCORE ROW -->
      <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <AVCard
          v-for="card in scoreCards"
          :key="card.type"
          :value="card"
        />
      </section>

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
