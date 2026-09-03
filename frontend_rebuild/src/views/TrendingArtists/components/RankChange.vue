<script setup>
import { computed } from 'vue'

// rank_change is positive when the artist climbed, negative when it fell.
// change_type: 'up' | 'down' | 'same' | 'new'
const props = defineProps({
    rankChange: { type: Number, default: null },
    changeType: { type: String, default: '' },
    previousRank: { type: Number, default: null },
    iconSize: { type: [Number, String], default: 16 },
})

// moves of this many places or more get a tinted pill so breakout artists pop
const BIG_MOVE = 10

const indicator = computed(() => {
    const change = props.rankChange
    const hasChange = Number.isFinite(change)

    if (props.changeType === 'new' || !hasChange) {
        return { kind: 'new', icon: null, label: '', class: 'text-blue-600 bg-blue-50 rounded-full px-1.5 py-0.5' }
    }

    const isBigMove = Math.abs(change) >= BIG_MOVE
    const pill = isBigMove ? ' rounded-full px-1.5 py-0.5' : ''

    if (change > 0) {
        return { kind: 'up', icon: 'mdi-menu-up', label: String(change), class: 'text-green-600' + (isBigMove ? ' bg-green-50' : '') + pill }
    }
    if (change < 0) {
        return { kind: 'down', icon: 'mdi-menu-down', label: String(Math.abs(change)), class: 'text-red-500' + (isBigMove ? ' bg-red-50' : '') + pill }
    }
    return { kind: 'same', icon: 'mdi-minus', label: '', class: 'text-gray-400' }
})

const title = computed(() => (props.previousRank ? `Last week #${props.previousRank}` : ''))
</script>

<template>
    <div
        class="inline-flex items-center text-xs font-semibold leading-none"
        :class="indicator.class"
        :title="title"
    >
        <v-icon v-if="indicator.icon" :icon="indicator.icon" :size="iconSize" />
        <span v-if="indicator.kind === 'new'">{{ $t('trending_artist.new') }}</span>
        <span v-else-if="indicator.label">{{ indicator.label }}</span>
    </div>
</template>
