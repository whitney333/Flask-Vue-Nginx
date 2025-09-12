<script setup>
    import {computed, ref, watch} from 'vue';
    import WorksCard from './Works_card.vue';
    import musicJSON from '@/views/Works/json/MusicViewDetails.json'
    import WorksCardTopCities from './Works_cardTopCities.vue';
    import axios from '@/axios';
    import { useArtistStore } from "@/stores/artist";

    const artistStore = useArtistStore()
    const artistId = ref('1')
    const end = new Date().toISOString().slice(0, 10)
    const filter = ref('365d')
    const spotifyUrl = `/spotify/v1`
    console.log("artistId: ", artistId.value)
    console.log("artistStore: ", artistStore.mid)

    const props = defineProps({
        iconSrc: String
    })
    // console.log("music mid: ", artistStore.mid.value)
    const spotifyHexCode = ['#1db954', '#191414', '#1db954', '#191414', '#1db954']
    const melonHexCode = ['#00cf35']
    const melonIconSrc = "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/melon.svg"

    const spotifyFollowersValue = computed(() => {
      return {
        ...musicJSON.spotifyFollowersValue,
        fetchURL: `/spotify/v1/follower?artist_id=${artistStore.mid}`
      }
    })

    const spotifyMonthlyListenersValue = computed(() => {
      return {
        ...musicJSON.spotifyMonthlyListenersValue,
        fetchURL: `/spotify/v1/monthly-listener?artist_id=${artistStore.mid}`
      }
    })

    const spotifyFanConversionRateValue = computed(() => {
      return {
        ...musicJSON.spotifyFanConversionRateValue,
        fetchURL: `/spotify/v1/conversion-rate?artist_id=${artistStore.mid}`
      }
    })

    const spotifyTopCitiesValue = computed(() => {
      return {
        ...musicJSON.spotifyTopCitiesValue,
        fetchURL: ``
      }
    })

    const spotifyPopularityIndexValue = computed(() => {
      return {
        ...musicJSON.spotifyPopularityIndexValue,
        fetchURL: `/spotify/v1/popularity?artist_id=${artistStore.mid}`
      }
    })

    const melonFollowerValue = computed(() => {
      return {
        ...musicJSON.melonFollowerValue,
        fetchURL: `/melon/v1/follower?artist_id=${artistStore.mid}`
      }
    })

    watch(
        () => artistStore.mid,
        (newMid) => {
          if (newMid) {
            console.log("Music component 拿到 mid:", newMid)
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
                        <WorksCard :iconSrc="props.iconSrc" :colors="spotifyHexCode" :value="spotifyFollowersValue" :end="end"></WorksCard>
                        <WorksCard :iconSrc="props.iconSrc" :colors="spotifyHexCode" :value="spotifyMonthlyListenersValue" :end="end" ></WorksCard>
                        <WorksCard :iconSrc="props.iconSrc" :colors="spotifyHexCode" :value="spotifyFanConversionRateValue" :end="end" ></WorksCard>
                        <WorksCardTopCities :iconSrc="props.iconSrc" :colors="spotifyHexCode" :value="spotifyTopCitiesValue"></WorksCardTopCities>
                        <!-- <WorksCard :iconSrc="props.iconSrc" :colors="spotifyHexCode" :value="spotifyTopCitiesValue" :end="end" ></WorksCard> -->
                        <WorksCard :iconSrc="props.iconSrc" :colors="spotifyHexCode" :value="spotifyPopularityIndexValue" :end="end" ></WorksCard>
                        <WorksCard :iconSrc="melonIconSrc" :colors="melonHexCode" :value="melonFollowerValue" :end="end" ></WorksCard>
                    </div>
                </div>

            </template>
        </v-card>
    </v-container>
</template>