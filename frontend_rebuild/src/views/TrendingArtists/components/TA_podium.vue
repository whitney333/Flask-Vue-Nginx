<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import RankChange from '@/views/TrendingArtists/components/RankChange.vue'
import { buildArtistRoute } from '@/views/TrendingArtists/components/artistRoute.js'
import { MEDALS } from '@/views/TrendingArtists/components/medals.js'

// Podium card for the top 3 of the trending list. Same data shape as TA_card.
const props = defineProps({
    value: { type: Object, required: true },
    // 1, 2 or 3: drives the medal accent
    place: { type: Number, required: true },
    year: Number,
    week: Number,
    showRankChange: { type: Boolean, default: false },
})

const medal = computed(() => MEDALS[props.place] ?? MEDALS[3])

const artistName = computed(() =>
    props.value?.artistName ?? props.value?.english_name ?? props.value?.korean_name ?? '-'
)
const artistKoreanName = computed(() => props.value?.artistKoreanName ?? props.value?.korean_name ?? '')
const artistImage = computed(() => props.value?.artistImg ?? props.value?.image ?? '')
const displayRank = computed(() => props.value?.displayRank ?? props.value?.rank ?? props.place)

const popularity = computed(() => {
    const number = Number(props.value?.popularity ?? props.value?.popularity_score ?? 0)
    return Number.isFinite(number) && number !== 0
        ? number.toLocaleString('en-US', { maximumFractionDigits: 2 })
        : '-'
})

const route = computed(() => buildArtistRoute(props.value, props.year, props.week))
const rootTag = computed(() => (route.value ? RouterLink : 'div'))
const rootAttrs = computed(() => (route.value ? { to: route.value } : {}))
</script>

<template>
    <component
        :is="rootTag"
        v-bind="rootAttrs"
        :aria-label="`Rank ${displayRank}, ${artistName}`"
        class="
            relative overflow-hidden
            flex items-center gap-4
            rounded-3xl border border-gray-200 bg-white
            px-5 py-4
            text-gray-900 no-underline
            transition hover:-translate-y-0.5 hover:shadow-md
            focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-400
            group
        "
    >
        <!-- soft medal-tinted wash, top-left only -->
        <div
            class="pointer-events-none absolute inset-0 bg-gradient-to-br to-transparent opacity-70"
            :class="medal.glow"
        />

        <!-- avatar with medal ring + rank badge -->
        <div class="relative shrink-0">
            <div
                class="w-[72px] h-[72px] rounded-2xl overflow-hidden bg-gray-100 ring-2 ring-offset-2 ring-offset-white"
                :class="medal.ring"
            >
                <img
                    v-if="artistImage"
                    :src="artistImage"
                    :alt="artistName"
                    loading="eager"
                    decoding="async"
                    width="72"
                    height="72"
                    class="w-full h-full object-cover"
                />
                <v-icon v-else icon="mdi-account-circle" size="48" class="text-gray-400" aria-hidden="true" />
            </div>
            <div
                class="absolute -top-2 -left-2 w-7 h-7 rounded-full grid place-items-center text-sm font-black shadow-sm"
                :class="medal.badge"
            >
                {{ displayRank }}
            </div>
        </div>

        <!-- name + popularity -->
        <div class="relative min-w-0 flex-1 leading-tight">
            <div class="text-lg font-bold text-gray-900 truncate">
                {{ artistName }}
            </div>
            <div
                v-if="artistKoreanName && artistKoreanName !== artistName"
                class="text-sm text-gray-400 truncate"
            >
                {{ artistKoreanName }}
            </div>

            <div class="mt-2 flex items-baseline gap-2">
                <span class="text-2xl font-black tabular-nums text-gray-900">{{ popularity }}</span>
                <span class="text-xs text-gray-400">{{ $t('trending_artist.popularity') }}</span>
                <RankChange
                    v-if="showRankChange"
                    :rank-change="value.rank_change"
                    :change-type="value.change_type"
                    :previous-rank="value.previous_rank"
                    icon-size="16"
                    class="ml-auto"
                />
            </div>
        </div>
    </component>
</template>
