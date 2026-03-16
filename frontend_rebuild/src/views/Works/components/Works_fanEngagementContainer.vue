<script setup>
    import {computed, ref, watch, onMounted} from 'vue';
    import WorksCard from './Works_card.vue';
    import musicJSON from '@/views/Works/json/MusicViewDetails.json'
    import WorksCardTopCities from './Works_cardTopCities.vue';
    import axios from '@/axios';
    import { useArtistStore } from "@/stores/artist";
    import { useUserStore } from "@/stores/user.js";

    const artistStore = useArtistStore()
    const userStore = useUserStore()
    // const artistId = ref('1')
    const end = new Date().toISOString().slice(0, 10)
    const hasSpotifyId = computed(() => {
      const id = artistStore.artist?.spotify_id
      return typeof id === 'string' && id.trim().length > 0
    })

    const hasMelonId = computed(() => {
      const id = artistStore.artist?.melon_id
      return typeof id === 'string' && id.trim().length > 0
    })


    const props = defineProps({
        iconSrc: String
    })

    // console.log("music mid: ", artistStore.mid.value)
    const spotifyHexCode = ['#1db954', '#191414', '#1db954', '#191414', '#1db954']
    const melonHexCode = ['#00cf35']
    const melonIconSrc = "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/melon.svg"

    const spotifyFollowersValue = computed(() => {
      if (!hasSpotifyId.value) {
        return {
          ...musicJSON.spotifyFollowersValue,
          disabled: true,
          disabledReason: 'NO_SPOTIFY_ID'
        }
      }

      return {
        ...musicJSON.spotifyFollowersValue,
        fetchURL: `/spotify/v1/follower`,
        range: userStore.hasActivePremium ? "365d" : "28d"
      }
    })

    const spotifyMonthlyListenersValue = computed(() => {
      if (!hasSpotifyId.value) {
        return {
          ...musicJSON.spotifyMonthlyListenersValue,
          disabled: true,
          disabledReason: 'NO_SPOTIFY_ID'
        }
      }

      return {
        ...musicJSON.spotifyMonthlyListenersValue,
        fetchURL: `/spotify/v1/monthly-listener`,
        range: userStore.hasActivePremium ? "365d" : "28d"
      }
    })

    const spotifyFanConversionRateValue = computed(() => {
      if (!hasSpotifyId.value) {
        return {
          ...musicJSON.spotifyFanConversionRateValue,
          disabled: true,
          disabledReason: 'NO_SPOTIFY_ID'
        }
      }

      return {
        ...musicJSON.spotifyFanConversionRateValue,
        fetchURL: `/spotify/v1/conversion-rate`,
        range: userStore.hasActivePremium ? "365d" : "28d"
      }
    })

    const spotifyTopCitiesValue = computed(() => {
      if (!hasSpotifyId.value) {
        return {
          ...musicJSON.spotifyTopCitiesValue,
          disabled: true,
          disabledReason: 'NO_SPOTIFY_ID'
        }
      }

      return {
        ...musicJSON.spotifyTopCitiesValue
      }
    })

    const spotifyPopularityIndexValue = computed(() => {
      if (!hasSpotifyId.value) {
        return {
          ...musicJSON.spotifyPopularityIndexValue,
          disabled: true,
          disabledReason: 'NO_SPOTIFY_ID'
        }
      }

      return {
        ...musicJSON.spotifyPopularityIndexValue,
        fetchURL: `/spotify/v1/popularity`,
        range: userStore.hasActivePremium ? "365d" : "28d"
      }
    })

    const melonFollowerValue = computed(() => {
      if (!hasMelonId.value) {
        return {
          ...musicJSON.melonFollowerValue,
          disabled: true,
          disabledReason: 'NO_MELON_ID'
        }
      }

      return {
        ...musicJSON.melonFollowerValue,
        fetchURL: `/melon/v1/follower`,
        range: userStore.hasActivePremium ? "365d" : "28d"
      }
    })

    watch(
        () => artistStore.artistId,
        (newMid) => {
          if (newMid) {
            // console.log("Music component 拿到 artistId:", newMid)
          }
        },
        {immediate: true} // run at the first time
    )

</script>

<template>
    <v-container
    fluid
    style="background-color: #f8f7f2;">
        <v-card 
            style="background-color: #f8f7f2;"
            flat
            >
            <template v-slot:title>
                <span :class="['text-h4']">
                    {{ $t('Fan Engagement') }}
                </span>
            </template >
            <template v-slot:text>
                <div
                :class="['justify-center', 'd-flex', 'align-center']">
                    <div
                    :class="['justify-center','ga-4', 'd-flex', 'flex-wrap', 'align-center']">
                        <WorksCard
                            :iconSrc="props.iconSrc"
                            :colors="spotifyHexCode"
                            :value="spotifyFollowersValue"
                            :end="end"></WorksCard>
                        <WorksCard
                            :iconSrc="props.iconSrc"
                            :colors="spotifyHexCode"
                            :value="spotifyMonthlyListenersValue"
                            :end="end" ></WorksCard>
                        <WorksCard
                            :iconSrc="props.iconSrc"
                            :colors="spotifyHexCode"
                            :value="spotifyFanConversionRateValue"
                            :end="end" ></WorksCard>
                        <WorksCardTopCities
                            :iconSrc="props.iconSrc"
                            :colors="spotifyHexCode"
                            :value="spotifyTopCitiesValue"></WorksCardTopCities>
                        <WorksCard
                            :iconSrc="props.iconSrc"
                            :colors="spotifyHexCode"
                            :value="spotifyPopularityIndexValue"
                            :end="end" ></WorksCard>
                        <WorksCard
                            :iconSrc="melonIconSrc"
                            :colors="melonHexCode"
                            :value="melonFollowerValue"
                            :end="end" ></WorksCard>
                    </div>
                </div>
            </template>
        </v-card>
    </v-container>
</template>
