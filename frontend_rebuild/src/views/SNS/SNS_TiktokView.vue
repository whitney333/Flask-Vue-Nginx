<script setup>
    import PageHolder from '@/components/PageHolder.vue'
    import SNSCard from '@/components/SNS/SNS_card.vue'
    import SNSCardHolder from '@/components/SNS/SNS_card_holder.vue'
    import SNSHashtagAnalytics from '@/components/SNS/SNS_HashtagAnalytics.vue';
    import SNSTopicAnalytics from '@/components/SNS/SNS_TopicAnalytics.vue';
    import tiktokJSON from './json/tiktokViewDetails.json'
    const iconSrc = "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/tiktok-logo.svg"
    const colors = ["#000000", "#000000"]

    const cardValueLists = [
        tiktokJSON.tiktokFollowerValue,
        tiktokJSON.tiktokTotalLikesValue,
        tiktokJSON.tiktokTotalViewsValue,
        tiktokJSON.tiktokTotalCommentsValue,
        tiktokJSON.tiktokTotalSharesValue,
        tiktokJSON.tiktokTotalSavesValue,
        tiktokJSON.tiktokEngagementRateValue,
    ]
    
    const allPostsValue = {
        
    }


</script>

<template>
    <v-container
    fluid
    :class="['bg-grey-lighten-4']">
        <div
        :class="['justify-center', 'd-flex', 'align-center']">
            <div
            :class="['justify-center','ga-4', 'd-flex', 'flex-wrap', 'align-center']">
                <div v-for="(card, index) in cardValueLists" :key="index">
                    <SNSCard :iconSrc="iconSrc" :colors="colors" :value="card" ></SNSCard>
                </div>
            </div>
        </div>
    </v-container>
    <v-divider></v-divider>
        <SNSHashtagAnalytics :iconSrc="iconSrc" :value="tiktokJSON.hashtagAnalyticsValue"></SNSHashtagAnalytics>
    <v-divider></v-divider>
        <SNSAllPosts :value="allPostsValue"></SNSAllPosts>
</template>