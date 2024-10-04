<script setup>
    import WorksTopTrackContainer from '@/components/Works/Works_topTrackContainer.vue';
    import WorksFanEngagementContainer from '@/components/Works/Works_fanEngagementContainer.vue';
    import { ref } from 'vue';
    import WorksWeeklyMusicChartsContainer from '@/components/Works/Works_weeklyMusicChartsContainer.vue';


    const iconSrc = "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/spotify-logo.svg"
</script>

<template>
    <WorksTopTrackContainer :iconSrc="iconSrc"></WorksTopTrackContainer>
    <v-divider></v-divider>
    <WorksFanEngagementContainer :iconSrc="iconSrc"></WorksFanEngagementContainer>
    <v-divider></v-divider>
    <WorksWeeklyMusicChartsContainer></WorksWeeklyMusicChartsContainer>
</template>

