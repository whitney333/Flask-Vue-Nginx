<script setup>
    import PageHolder from '@/components/PageHolder.vue'
    import SNSCard from '@/views/SNS/components/SNS_card.vue'
    import SNSCardHolder from '@/views/SNS/components/SNS_card_holder.vue'
    import SNSHashtagAnalytics from '@/views/SNS/components/SNS_HashtagAnalytics.vue';
    import SNSTopicAnalytics from '@/views/SNS/components/SNS_TopicAnalytics.vue';
    import SNSAllPosts from '@/views/SNS/components/SNS_AllPosts.vue'
    import instaJSON from './json/instagramViewDetails.json'
    import axios from '@/axios';
    import { ref } from 'vue';
    
    const iconSrc = "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/instagram-logo.svg"
    const colors = ["#405DE6", "#FCAF45"]
    const posts = ref([])
    const platform = "instagram"
    const { profile } = defineProps({
        profile: Object
    })

    const cardValueLists = [
        instaJSON.instagramFollowerValue,
        instaJSON.instagramThreadsFollowerValue,
        instaJSON.instagramPostsValue,
        instaJSON.instagramLikesValue,
        instaJSON.instagramCommentsValue,
        instaJSON.instagramEngagementRateValue,
    ]

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
        <SNSHashtagAnalytics :iconSrc="iconSrc" :colors="colors" :value="instaJSON.hashtagAnalyticsValue"></SNSHashtagAnalytics>
    <v-divider></v-divider>
        <SNSTopicAnalytics :iconSrc="iconSrc" :colors="colors" :value="instaJSON.topAnalyticsValue"></SNSTopicAnalytics>
    <v-divider></v-divider>
        <SNSAllPosts :platform="platform"></SNSAllPosts>
</template>