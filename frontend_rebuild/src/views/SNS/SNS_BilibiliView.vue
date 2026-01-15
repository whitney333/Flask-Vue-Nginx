<script setup>
    import PageHolder from '@/components/PageHolder.vue'
    import SNSCard from '@/views/SNS/components/SNS_card.vue'
    import SNSAllPosts from '@/views/SNS/components/SNS_AllPosts.vue'
    import SNSCardHolder from '@/views/SNS/components/SNS_card_holder.vue'
    import SNSHashtagAnalytics from '@/views/SNS/components/SNS_HashtagAnalytics.vue';
    import SNSTopicAnalytics from '@/views/SNS/components/SNS_TopicAnalytics.vue';
    import bilibiliJSON from './json/bilibiliViewDetails.json'
    import { useArtistStore } from "@/stores/artist.js";
    import {computed, watch} from "vue";
     import { useUserStore } from "@/stores/user.js";

    const iconSrc = "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/bilibili-logo.svg"
    const platform ="bilibili"
    const colors = ["#286ed6", "#49e1fc"]
    const artistStore = useArtistStore()
    const userStore = useUserStore()

     // date value
    const today = new Date().toISOString().slice(0, 10)
    const cardValueLists = computed(() => {
      // if mid not exists, do not render the chart
      if (!artistStore.artistId) return []
      if (userStore.isPremium === undefined) return []

      const range = userStore.isPremium ? "365d" : "28d"

      const keys = [
        bilibiliJSON.bilibiliTotalFollowersValue,
        bilibiliJSON.bilibiliTotalViewsValue,
        bilibiliJSON.bilibiliTotalLikesValue,
        bilibiliJSON.bilibiliTotalCommentsValue,
        bilibiliJSON.bilibiliTotalSharesValue,
        bilibiliJSON.bilibiliTotalBulletChatsValue,
        bilibiliJSON.bilibiliTotalCoinsValue,
        bilibiliJSON.bilibiliTotalCollectsValue,
        bilibiliJSON.bilibiliEngagementRateValue,
      ]

      return keys.map((base) => ({
          ...base,
          fetchURL: `${base.fetchURL}?date_end=${today}&range=${range}&artist_id=${artistStore.artistId}`,
      }))
    })

    watch(
        () => artistStore.artistId,
        (newMid) => {
          if (newMid) {
            // console.log("🎯 mid changed:", newMid)
            // console.log("cardValueLists updated:", cardValueLists.value)
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