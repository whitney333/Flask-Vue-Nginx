<script setup>
import { computed } from 'vue';
import { RouterLink } from 'vue-router';
import RankChange from '@/views/TrendingArtists/components/RankChange.vue';

    // rows above this index load their avatar eagerly (visible on first paint);
    // the rest lazy-load as the user scrolls
    const EAGER_ROWS = 5

    const props = defineProps({
        value: Object,
        year: Number,
        week: Number,
        // parent decides per week whether rank-change data exists; hidden otherwise
        showRankChange: { type: Boolean, default: false },
        // position in the list, used for eager vs lazy avatar loading
        index: { type: Number, default: 0 },
    })

    const artistId = computed(() => props.value?.artistId ?? props.value?.artist_id ?? '')
    const artistName = computed(() => {
        return props.value?.artistName
            ?? props.value?.english_name
            ?? props.value?.korean_name
            ?? '-'
    })
    const artistKoreanName = computed(() => props.value?.artistKoreanName ?? props.value?.korean_name ?? '')

    const artistImage = computed(() => props.value?.artistImg ?? props.value?.image ?? '')
    const artistType = computed(() => props.value?.type || '-')
    const popularityScore = computed(() => {
        return props.value?.popularity
            ?? props.value?.popularity_score
            ?? 0
    })
    const scoreItems = computed(() => [
        {
            label: 'Music',
            value: props.value?.music_score,
            icon: 'mdi-music-note',
        },
        {
            label: 'SNS',
            value: props.value?.sns_score,
            icon: 'mdi-account-group-outline',
        },
        {
            label: 'Drama',
            value: props.value?.drama_score,
            icon: 'mdi-television',
        },
    ])

    const formatScore = (value) => {
        const number = Number(value ?? 0)

        if (!Number.isFinite(number) || number === 0) {
            return '-'
        }

        return number.toLocaleString('en-US', {
            maximumFractionDigits: 2,
        })
    }

    // Route for the artist detail page. Rendered as a real <a> via RouterLink so the
    // row is keyboard-focusable, middle/cmd-clickable and has a copyable href.
    const artistRoute = computed(() => {
        if (!artistId.value) {
            return null
        }

        return {
            name: 'Artist',
            params: {
                artistId: artistId.value,
                artistName: artistName.value,
            },
            query: {
                rank: props.value?.rank,
                image: artistImage.value,
                koreanName: artistKoreanName.value,
                type: artistType.value,
                popularityScore: popularityScore.value,
                musicScore: props.value?.music_score ?? 0,
                snsScore: props.value?.sns_score ?? 0,
                dramaScore: props.value?.drama_score ?? 0,
                year: props.year,
                week: props.week,
            },
        }
    })

    // Falls back to a plain div for the rare row with no artist id.
    const rowTag = computed(() => (artistRoute.value ? RouterLink : 'div'))
    const rowAttrs = computed(() => (artistRoute.value ? { to: artistRoute.value } : {}))

    const avatarLoading = computed(() => (props.index < EAGER_ROWS ? 'eager' : 'lazy'))

    const displayRank = computed(() => props.value?.displayRank ?? props.value?.rank)

    // Screen-reader summary of the row, including the rank change when shown.
    const rowAriaLabel = computed(() => {
        const parts = [`Rank ${displayRank.value}`, artistName.value]

        if (props.showRankChange) {
            const change = props.value?.rank_change
            if (props.value?.change_type === 'new' || !Number.isFinite(change)) {
                parts.push('new this week')
            } else if (change > 0) {
                parts.push(`up ${change}`)
            } else if (change < 0) {
                parts.push(`down ${Math.abs(change)}`)
            } else {
                parts.push('no change')
            }
        }

        return parts.join(', ')
    })
    const artistTypes = computed(() => {
      if (Array.isArray(artistType.value)) {
        return artistType.value
      }

      if (artistType.value) {
        return [artistType.value]
      }

      return []
    })

    const getArtistTypeColor = (type) => {
      const colors = {
        Musician: 'deep-purple',
        Actor: 'blue',
      }

      return colors[type] || 'grey'
    }

</script>

<template>
    <component
        :is="rowTag"
        v-bind="rowAttrs"
        :aria-label="rowAriaLabel"
        class="
            relative
            bg-white
            p-4 md:px-6 md:py-4

            flex flex-col gap-3
            md:grid md:grid-cols-12 md:items-center

            text-gray-900 no-underline
            hover:bg-gray-50
            focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-indigo-400
            transition cursor-pointer group
        "
    >
        <!-- TOP ROW (Mobile optimized) -->
        <div class="flex items-center justify-between md:contents">

            <!-- Rank (+ change vs last week, stacked underneath) -->
            <div class="md:col-span-1 flex flex-col items-center justify-center gap-0.5">
                <div class="text-md font-bold text-gray-700">
                    {{ props.value.displayRank ?? props.value.rank }}
                </div>
                <RankChange
                    v-if="props.showRankChange"
                    :rank-change="props.value.rank_change"
                    :change-type="props.value.change_type"
                    :previous-rank="props.value.previous_rank"
                    icon-size="14"
                />
            </div>

            <!-- Arrow (mobile show right side) -->
            <div class="md:hidden">
                <v-icon icon="mdi-chevron-right" class="text-gray-400" />
            </div>
        </div>

        <!-- Artist -->
        <div class="md:col-span-4 flex items-center gap-3">
            <div
                class="
                    w-10 h-10 md:w-12 md:h-12
                    rounded-xl overflow-hidden
                    bg-gray-100
                    shrink-0
                "
            >
                <img
                    v-if="artistImage"
                    :src="artistImage"
                    :alt="artistName"
                    :loading="avatarLoading"
                    decoding="async"
                    width="48"
                    height="48"
                    class="w-full h-full object-cover"
                />
                <v-icon
                    v-else
                    icon="mdi-account-circle"
                    size="32"
                    class="text-gray-400"
                />
            </div>

            <div class="leading-tight">
                <div class="font-semibold text-gray-900">
                    {{ artistName }}
                </div>

                <div
                    v-if="artistKoreanName && artistKoreanName !== artistName"
                    class="text-sm text-gray-400"
                >
                    {{ artistKoreanName }}
                </div>
            </div>
        </div>

        <!-- Type -->
        <div class="md:col-span-2 flex flex-wrap gap-2">
            <v-chip
                v-for="type in artistTypes"
                :key="type"
                :color="getArtistTypeColor(type)"
                size="small"
                variant="tonal"
                rounded="lg"
            >
                {{ type }}
            </v-chip>
        </div>

        <!-- Popularity -->
        <div class="md:col-span-2 flex items-center gap-2">
          <div class="text-xs text-gray-400 md:hidden inline-flex items-center gap-1">
            <v-icon size="16" class="text-orange-500">mdi-fire</v-icon>
            <span>Popularity</span>
          </div>
          <div class="text-md font-medium text-gray-700">
            {{ formatScore(popularityScore) }}
          </div>
        </div>

        <!-- Scores -->
        <div class="md:col-span-3 flex flex-wrap gap-1">
            <v-chip
                v-for="item in scoreItems"
                :key="item.label"
                size="small"
                variant="tonal"
                rounded="lg"
            >
                <v-icon :icon="item.icon" size="14" start />
                {{ formatScore(item.value) }}
            </v-chip>
        </div>

        <!-- Desktop arrow -->
      <div
          class="
            hidden md:flex
            absolute right-6
            top-1/2 -translate-y-1/2
          "
      >
        <v-icon
            icon="mdi-chevron-right"
            class="text-gray-400 group-hover:translate-x-1 transition"
        />
      </div>
    </component>
</template>
