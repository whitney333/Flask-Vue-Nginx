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
     import { useUserStore } from "@/stores/user.js";

    const artistStore = useArtistStore()
    const userStore = useUserStore()

    const iconSrc = "https://cdn.revmishkan.com/dist/tiktok-logo.svg"
    const colors = ["#000000", "#000000"]
    const posts = ref([])
    const platform = "tiktok"
    const hasTiktok = computed(() => {
      return !!artistStore.artist?.tiktok_id
    })

    // date value
    const today = new Date().toISOString().slice(0, 10)
    const cardValueLists = computed(() => {
      // if mid not exists, do not render the chart
      if (!artistStore.artist?.tiktok_id) return []
      if (userStore.isPremium === undefined) return []

      const range = userStore.hasActivePremium ? "365d" : "28d"

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
      console.log("artist id: ", artistStore.artistId)
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

      <!-- ===== NO TIKTOK ACCOUNT ===== -->
      <div
        v-if="!hasTiktok"
        class="flex justify-center"
      >
        <div class="flex items-center bg-red-50 text-red-500 px-4 py-2 rounded-md">
          <svg class="w-5 h-5 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11H9v4h2V7zm0 6H9v2h2v-2z"
                  clip-rule="evenodd"/>
          </svg>
          <span class="text-sm font-medium">
            {{ $t('This artist does not have a Tiktok account.') }}
          </span>
        </div>
      </div>

      <!-- ===== HAS TIKTOK ===== -->
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

        <!-- divider -->
<!--        <div class="my-6 h-px w-full bg-gray-200"></div>-->

        <!-- posts -->
<!--        <SNSAllPosts :platform="platform" />-->

      </template>

    </div>
  </div>
</template>
