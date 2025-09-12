<script setup>
    import PageHolder from '@/components/PageHolder.vue'
    import SNSCard from '@/views/SNS/components/SNS_card.vue'
    import SNSCardHolder from '@/views/SNS/components/SNS_card_holder.vue'
    import SNSHashtagAnalytics from '@/views/SNS/components/SNS_HashtagAnalytics.vue';
    import SNSTopicAnalytics from '@/views/SNS/components/SNS_TopicAnalytics.vue';
    import tiktokJSON from './json/tiktokViewDetails.json'
    import {computed, ref, watch} from 'vue';
    import SNSAllPosts from '@/views/SNS/components/SNS_AllPosts.vue';
    import axios from '@/axios';
    import { useArtistStore } from "@/stores/artist.js";

    const artistStore = useArtistStore()
    const iconSrc = "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/tiktok-logo.svg"
    const colors = ["#000000", "#000000"]
    const posts = ref([])
    const platform = "tiktok"

    // date value
    const today = new Date().toISOString().slice(0, 10)
    const cardValueLists = computed(() => {
      // if mid not exists, do not render the chart
      if (!artistStore.mid) return []
      const keys = [
        tiktokJSON.tiktokFollowerValue,
        tiktokJSON.tiktokHashtagValue,
        tiktokJSON.tiktokTotalLikesValue,
        // tiktokJSON.tiktokTotalViewsValue,
        // tiktokJSON.tiktokTotalCommentsValue,
        // tiktokJSON.tiktokTotalSharesValue,
        // tiktokJSON.tiktokTotalSavesValue,
        // tiktokJSON.tiktokEngagementRateValue,
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
<!--        <SNSHashtagAnalytics :iconSrc="iconSrc" :value="tiktokJSON.hashtagAnalyticsValue"></SNSHashtagAnalytics>-->
        <v-divider></v-divider>
<!--        <SNSAllPosts :platform="platform"></SNSAllPosts>-->
    </v-container>
</template>