<script setup>
import { computed } from 'vue';
import { RouterLink } from 'vue-router';
import { useI18n } from 'vue-i18n';
import RankChange from '@/views/TrendingArtists/components/RankChange.vue';
import { buildArtistRoute } from '@/views/TrendingArtists/components/artistRoute.js';
import { medalForRank } from '@/views/TrendingArtists/components/medals.js';

    // rows above this index load their avatar eagerly (visible on first paint);
    // the rest lazy-load as the user scrolls
    const EAGER_ROWS = 5

    const { t } = useI18n()

    const props = defineProps({
        value: Object,
        year: Number,
        week: Number,
        // parent decides per week whether rank-change data exists; hidden otherwise
        showRankChange: { type: Boolean, default: false },
        // position in the list, used for eager vs lazy avatar loading
        index: { type: Number, default: 0 },
        // highest popularity score in the current list; scales the popularity bar
        maxPopularity: { type: Number, default: 0 },
    })

    // 0-100 width of the popularity bar relative to this week's leader
    const popularityPercent = computed(() => {
        const score = Number(props.value?.popularity ?? props.value?.popularity_score ?? 0)
        if (!props.maxPopularity || !Number.isFinite(score) || score <= 0) {
            return 0
        }
        return Math.max(4, Math.min(100, (score / props.maxPopularity) * 100))
    })

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
            label: t('trending_artist.music'),
            value: props.value?.music_score,
            icon: 'mdi-music-note',
        },
        {
            label: t('trending_artist.sns'),
            value: props.value?.sns_score,
            icon: 'mdi-account-group-outline',
        },
        {
            label: t('trending_artist.drama'),
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
    const artistRoute = computed(() => buildArtistRoute(props.value, props.year, props.week))

    // Falls back to a plain div for the rare row with no artist id.
    const rowTag = computed(() => (artistRoute.value ? RouterLink : 'div'))
    const rowAttrs = computed(() => (artistRoute.value ? { to: artistRoute.value } : {}))

    const avatarLoading = computed(() => (props.index < EAGER_ROWS ? 'eager' : 'lazy'))

    const displayRank = computed(() => props.value?.displayRank ?? props.value?.rank)

    // Top 3 get the podium's medal ring + badge on the avatar. On desktop these
    // rows are hidden behind the podium, so this is effectively the mobile treatment.
    const medal = computed(() => medalForRank(displayRank.value))

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
            relative isolate
            bg-white
            p-4 md:px-6 md:py-4

            flex flex-col gap-3
            md:grid md:grid-cols-12 md:items-center

            text-gray-900 no-underline
            max-md:border-b max-md:border-gray-100 max-md:last:border-b-0
            hover:bg-gray-50
            focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-indigo-400
            transition cursor-pointer group
        "
    >
        <!-- medal-tinted wash for the top 3 (same as the podium); -z-10 inside the
             isolated root paints it above the white background, below the content -->
        <div
            v-if="medal"
            class="pointer-events-none absolute inset-0 -z-10 bg-gradient-to-br to-transparent opacity-70"
            :class="medal.glow"
            aria-hidden="true"
        />

        <!-- TOP ROW (Mobile optimized) -->
        <div class="flex items-center justify-between md:contents">

            <!-- Rank + change vs last week: side by side on mobile, stacked in the desktop column -->
            <div class="md:col-span-1 flex items-center gap-2 md:flex-col md:justify-center md:gap-0.5">
                <!-- top 10 get a heavier numeral so the head of the chart scans while scrolling -->
                <div
                    class="font-bold tabular-nums"
                    :class="displayRank <= 10 ? 'text-lg text-gray-900' : 'text-md text-gray-700'"
                >
                    {{ displayRank }}
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
            <div class="relative shrink-0">
            <div
                class="
                    w-10 h-10 md:w-12 md:h-12
                    rounded-xl overflow-hidden
                    bg-gray-100
                "
                :class="medal ? ['ring-2 ring-offset-2 ring-offset-white', medal.ring] : ''"
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
            <!-- medal badge on the avatar corner (top 3 only) -->
            <div
                v-if="medal"
                class="absolute -top-1.5 -left-1.5 w-5 h-5 rounded-full grid place-items-center text-[11px] font-black shadow-sm"
                :class="medal.badge"
                aria-hidden="true"
            >
                {{ displayRank }}
            </div>
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

        <!-- Popularity: number with a bar scaled to this week's leader -->
        <div class="md:col-span-2 flex flex-col gap-1 md:pr-6">
          <div class="flex items-center justify-between gap-2">
            <div class="text-xs text-gray-400 md:hidden inline-flex items-center gap-1">
              <v-icon size="16" class="text-orange-500" aria-hidden="true">mdi-fire</v-icon>
              <span>{{ $t('trending_artist.popularity') }}</span>
            </div>
            <div class="text-md font-semibold tabular-nums text-gray-800">
              {{ formatScore(popularityScore) }}
            </div>
          </div>
          <div class="h-1.5 w-full rounded-full bg-gray-100 overflow-hidden" aria-hidden="true">
            <div
              class="h-full rounded-full bg-orange-400 transition-[width] duration-500"
              :style="{ width: `${popularityPercent}%` }"
            />
          </div>
        </div>

        <!-- Scores: three labelled columns (labels hidden on desktop, shown in the table header) -->
        <div class="md:col-span-3 grid grid-cols-3 gap-2">
            <div
                v-for="item in scoreItems"
                :key="item.label"
                class="min-w-0 leading-tight"
            >
                <div class="text-[11px] text-gray-400 md:hidden inline-flex items-center gap-1">
                    <v-icon :icon="item.icon" size="12" aria-hidden="true" />
                    <span>{{ item.label }}</span>
                </div>
                <div
                    class="text-sm tabular-nums"
                    :class="formatScore(item.value) === '-' ? 'text-gray-300' : 'font-medium text-gray-700'"
                >
                    {{ formatScore(item.value) === '-' ? '–' : formatScore(item.value) }}
                </div>
            </div>
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
