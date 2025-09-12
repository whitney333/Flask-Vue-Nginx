<script setup>
    import PageHolder from '@/components/PageHolder.vue'
    import SNSCard from '@/views/SNS/components/SNS_card.vue'
    import SNSCardHolder from '@/views/SNS/components/SNS_card_holder.vue'
    import SNSHashtagAnalytics from '@/views/SNS/components/SNS_HashtagAnalytics.vue';
    import SNSTopicAnalytics from '@/views/SNS/components/SNS_TopicAnalytics.vue';
    import SNSAllPosts from '@/views/SNS/components/SNS_AllPosts.vue'
    import instaJSON from './json/instagramViewDetails.json'
    import axios from '@/axios';
    import {computed, ref, watch} from 'vue';
    import { useArtistStore } from "@/stores/artist.js";

    const iconSrc = "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/instagram-logo.svg"
    const colors = ["#405DE6", "#FCAF45"]
    const posts = ref([])
    const platform = "instagram"
    const { profile } = defineProps({
        profile: Object
    })
    const artistStore = useArtistStore()
     // date value
    const today = new Date().toISOString().slice(0, 10)
    const cardValueLists = computed(() => {
      // if mid not exists, do not render the chart
      if (!artistStore.mid) return []
      const keys = [
        instaJSON.instagramFollowerValue,
        instaJSON.instagramThreadsFollowerValue,
        instaJSON.instagramPostsValue,
        instaJSON.instagramLikesValue,
        instaJSON.instagramCommentsValue,
        // instaJSON.instagramEngagementRateValue,
      ]

      return keys.map((base) => ({
          ...base,
          fetchURL: `${base.fetchURL}?date_end=${today}&filter=365d&artist_id=${artistStore.mid}`,
      }))
    })

    watch(
        () => artistStore.mid,
        (newMid) => {
          if (newMid) {
            console.log("🎯 mid changed:", newMid)
            console.log("cardValueLists updated:", cardValueLists.value)
          }
        },
        {immediate: true}
    )

    // const cardValueLists = [
    //     instaJSON.instagramFollowerValue,
    //     instaJSON.instagramThreadsFollowerValue,
    //     instaJSON.instagramPostsValue,
    //     instaJSON.instagramLikesValue,
    //     instaJSON.instagramCommentsValue,
    //     instaJSON.instagramEngagementRateValue,
    // ]

</script>

<template>
    <v-container
    fluid
    class="bg-[#F5F5F5]">
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
        <SNSHashtagAnalytics :iconSrc="iconSrc" :colors="colors" :value="instaJSON.hashtagAnalyticsValue"></SNSHashtagAnalytics>
        <v-divider></v-divider>
<!--        <SNSTopicAnalytics :iconSrc="iconSrc" :colors="colors" :value="instaJSON.topAnalyticsValue"></SNSTopicAnalytics>-->
        <v-divider></v-divider>
        <SNSAllPosts :platform="platform"></SNSAllPosts>
    </v-container>
</template>