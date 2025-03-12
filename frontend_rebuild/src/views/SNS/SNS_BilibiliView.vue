<script setup>
    import PageHolder from '@/components/PageHolder.vue'
    import SNSCard from '@/views/SNS/components/SNS_card.vue'
    import SNSCardHolder from '@/views/SNS/components/SNS_card_holder.vue'
    import SNSHashtagAnalytics from '@/views/SNS/components/SNS_HashtagAnalytics.vue';
    import SNSTopicAnalytics from '@/views/SNS/components/SNS_TopicAnalytics.vue';
    import bilibiliJSON from './json/bilibiliViewDetails.json'


    const iconSrc = "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/bilibili-logo.svg"
    const platform ="bilibili"
    const cardValueLists = [
        bilibiliJSON.bilibiliTotalVideosValue,
        bilibiliJSON.bilibiliTotalViewsValue,
        bilibiliJSON.bilibiliTotalLikesValue,
        bilibiliJSON.bilibiliTotalCommentsValue,
        bilibiliJSON.bilibiliTotalSharesValue,
        bilibiliJSON.bilibiliTotalBulletChatsValue,
        bilibiliJSON.bilibiliTotalCoinsValue,
        bilibiliJSON.bilibiliTotalCollectsValue,
        bilibiliJSON.bilibiliEngagementRateValue,
    ]
    
</script>

<template>
    <v-container
    fluid
    :class="['bg-grey-lighten-4']">
        <div
        class="flex w-full justify-center my-10">
            <div
            class="ga-4 justify-center flex flex-wrap ">
                <div v-for="(card, index) in cardValueLists" :key="index">
                    <SNSCard :iconSrc="iconSrc" :colors="colors" :value="card"></SNSCard>
                </div>
            </div>
        </div>
        <v-divider></v-divider>
        <!-- <SNSHashtagAnalytics :iconSrc="iconSrc" :value="tiktokJSON.hashtagAnalyticsValue"></SNSHashtagAnalytics> -->
        <v-divider></v-divider>
        <SNSAllPosts :platform="platform"></SNSAllPosts>
    </v-container>
</template>