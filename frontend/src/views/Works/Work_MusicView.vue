<script setup>
    import WorksFanEngagementContainer from '@/views/Works/components/Works_fanEngagementContainer.vue';
    import { ref } from 'vue';
    import WorksWeeklyMusicChartsContainer from '@/views/Works/components/Works_weeklyMusicChartsContainer.vue';
    import WorkstopTrackContainer from '@/views/Works/components/Works_topTrackContainer.vue';


    const iconSrc = "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/spotify-logo.svg"
</script>

<template>
    <WorkstopTrackContainer :iconSrc="iconSrc"></WorksTopTrackContainer>
    <v-divider></v-divider>
    <WorksFanEngagementContainer :iconSrc="iconSrc"></WorksFanEngagementContainer>
    <v-divider></v-divider>
    <WorksWeeklyMusicChartsContainer></WorksWeeklyMusicChartsContainer>
</template>

