<script setup>
    import PageHolder from '@/components/PageHolder.vue'
    import SNSCard from '@/views/SNS/components/SNS_card.vue'
    import SNSAllPosts from '@/views/SNS/components/SNS_AllPosts.vue'
    import SNSCardHolder from '@/views/SNS/components/SNS_card_holder.vue'
    import SNSHashtagAnalytics from '@/views/SNS/components/SNS_HashtagAnalytics.vue';
    import SNSTopicAnalytics from '@/views/SNS/components/SNS_TopicAnalytics.vue';
    import bilibiliJSON from './json/bilibiliViewDetails.json'
    import { useArtistStore } from "@/stores/artist.js";
    import {computed, watch, ref} from "vue";
    import { useUserStore } from "@/stores/user.js";

    const iconSrc = "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/bilibili-logo.svg"
    const platform ="bilibili"
    const colors = ["#286ed6", "#49e1fc"]
    const hasBilibili = computed(() => {
      return !!artistStore.artist?.bilibili_id
    })
    const artistStore = useArtistStore()
    const userStore = useUserStore()

     // date value
    const today = new Date().toISOString().slice(0, 10)
    const cardValueLists = computed(() => {
      // if platform id not exists, do not render the chart
      if (!artistStore.artist?.bilibili_id) return []
      if (userStore.isPremium === undefined) return []

      const range = userStore.hasActivePremium ? "365d" : "28d"

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
  <!-- ===== Full width background ===== -->
  <div class="w-full min-h-screen bg-white">

    <!-- ===== Content wrapper ===== -->
    <div class="mx-auto w-full max-w-7xl px-6 py-10">

      <!-- ===== NO BILIBILI ACCOUNT ===== -->
      <div
        v-if="!hasBilibili"
        class="flex justify-center"
      >
        <div class="flex items-center bg-red-50 text-red-500 px-4 py-2 rounded-md">
          <svg class="w-5 h-5 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11H9v4h2V7zm0 6H9v2h2v-2z"
                  clip-rule="evenodd"/>
          </svg>
          <span class="text-sm font-medium">
            {{ $t('This artist does not have a Bilibili account.') }}
          </span>
        </div>
      </div>

      <!-- ===== HAS BILIBILI ===== -->
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

        <!-- full-bleed background (content stays centered) -->
        <div class="section-bleed section-bleed--hashtags">
          <SNSHashtagAnalytics
            :iconSrc="iconSrc"
            :colors="colors"
            :value="bilibiliJSON.hashtagAnalyticsValue"
          />
        </div>

        <!-- posts -->
        <div class="section-bleed section-bleed--posts">
          <SNSAllPosts :platform="platform" />
        </div>

      </template>

    </div>
  </div>
</template>

<style scoped>
.section-bleed {
  position: relative;
  z-index: 0;
}

.section-bleed::before {
  content: "";
  position: absolute;
  top: 0;
  bottom: 0;
  left: 50%;
  width: 100vw;
  transform: translateX(-50%);
  z-index: -1;
}

.section-bleed--hashtags::before {
  background-color: #f8f7f2; /* matches SNS_HashtagAnalytics inline background */
}

.section-bleed--posts::before {
  background-color: #f3f4f6; /* tailwind bg-gray-100 */
}
</style>
