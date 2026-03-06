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
    import { useUserStore } from "@/stores/user.js";

    const iconSrc = "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/instagram-logo.svg"
    const colors = ["#405DE6", "#FCAF45"]
    const posts = ref([])
    const platform = "instagram"
    const { profile } = defineProps({
        profile: Object
    })

    const artistStore = useArtistStore()
    const userStore = useUserStore()
    const hasInstagram = computed(() => {
      return !!artistStore.artist?.instagram_id
    })
     // date value
    const today = new Date().toISOString().slice(0, 10)
    const cardValueLists = computed(() => {
      // if mid not exists, do not render the chart
      if (!artistStore.artist?.instagram_id) return []
      if (userStore.isPremium === undefined) return []

      const range = userStore.hasActivePremium ? "365d" : "28d"

      const keys = [
        instaJSON.instagramFollowerValue,
        instaJSON.instagramThreadsFollowerValue,
        instaJSON.instagramPostsValue,
        // instaJSON.instagramLikesValue,
        // instaJSON.instagramCommentsValue,
        // instaJSON.instagramEngagementRateValue,
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
<!-- ===== Full width background ===== -->
  <div class="w-full min-h-screen bg-white">

    <!-- ===== Content wrapper ===== -->
    <div class="mx-auto w-full max-w-7xl px-6 py-10">

      <!-- ===== NO INSTAGRAM ACCOUNT ===== -->
      <div
        v-if="!hasInstagram"
        class="flex justify-center"
      >
        <div class="flex items-center bg-red-50 text-red-500 px-4 py-2 rounded-md">
          <svg class="w-5 h-5 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11H9v4h2V7zm0 6H9v2h2v-2z"
                  clip-rule="evenodd"/>
          </svg>
          <span class="text-sm font-medium">
            {{ $t('This artist does not have a Instagram account.') }}
          </span>
        </div>
      </div>

      <!-- ===== HAS INSTAGRAM ===== -->
      <template v-else>

        <!-- cards -->
        <div class="mb-10">
          <div class="flex flex-wrap justify-center gap-4">
            <SNSCard
              v-for="(card, index) in cardValueLists"
              :key="index"
              :iconSrc="iconSrc"
              :colors="colors"
              :value="card"
            />
          </div>
        </div>

        <SNSHashtagAnalytics
            :iconSrc="iconSrc"
            :colors="colors"
            :value="instaJSON.hashtagAnalyticsValue">
        </SNSHashtagAnalytics>

        <!-- posts -->
        <SNSAllPosts :platform="platform" />

      </template>

    </div>
  </div>
</template>
