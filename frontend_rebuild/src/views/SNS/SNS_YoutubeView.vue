<script setup>
    import PageHolder from '@/components/PageHolder.vue'
    import SNSCard from '@/views/SNS/components/SNS_card.vue'
    import SNSCardHolder from '@/views/SNS/components/SNS_card_holder.vue'
    import SNSHashtagAnalytics from '@/views/SNS/components/SNS_HashtagAnalytics.vue';
    import SNSTopicAnalytics from '@/views/SNS/components/SNS_TopicAnalytics.vue';
    import SNSAllPosts from '@/views/SNS/components/SNS_AllPosts.vue'
    import youtubeJSON from './json/youtubeViewDetails.json'
    import { ref } from 'vue';
    import axios from '@/axios';
    
    const iconSrc = "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/youtube-logo.svg"
    const colors = ["#D62828", "#FCBF49"]
    const posts = ref([])
    const platform = "youtube"

    const cardValueLists = [
        youtubeJSON.youtubeSubscribersValue,
        youtubeJSON.youtubeTotalChannelVideosValue,
        youtubeJSON.youtubeTotalChannelViewsValue,
        youtubeJSON.youtubeTotalVideoViewsValue,
        youtubeJSON.youtubeTotalVideoLikesValue,
        youtubeJSON.youtubeTotalVideoCommentsValue,
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
                    <SNSCard :iconSrc="iconSrc" :colors="colors" :value="card" ></SNSCard>
                </div>
            </div>
        </div>
        <v-divider></v-divider>
        <SNSHashtagAnalytics :iconSrc="iconSrc" :colors="colors" :value="youtubeJSON.hashtagAnalyticsValue"></SNSHashtagAnalytics>
        <v-divider></v-divider>
        <SNSAllPosts :platform="platform"></SNSAllPosts>
    </v-container>
</template>