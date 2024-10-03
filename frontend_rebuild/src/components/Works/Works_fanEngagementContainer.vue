<script setup>
    import WorksCard from './Works_card.vue';
    import musicJSON from '@/views/Works/json/MusicViewDetails.json'
    import WorksCardTopCities from './Works_cardTopCities.vue';
    const spotifyUrl = `/api/spotify/index`
    const melonUrl = `/api/melon/follower`

    const props = defineProps({
        iconSrc: String
    })

    const spotifyHexCode = ['#1db954', '#191414', '#1db954', '#191414', '#1db954']
    const melonHexCode = ['#00cf35']
    const melonIconSrc = "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/melon.svg"

    const end = new Date().toISOString().slice(0, 10)


    const spotifyFollowersValue = {
        ...musicJSON.spotifyFollowersValue,
        fetchURL: spotifyUrl,
    }
    const spotifyMonthlyListenersValue = {
        ...musicJSON.spotifyMonthlyListenersValue,
        fetchURL: spotifyUrl
    }
    const spotifyFanConversionRateValue = {
        ...musicJSON.spotifyFanConversionRateValue,
        fetchURL: spotifyUrl
    }
    const spotifyTopCitiesValue = {
        ...musicJSON.spotifyTopCitiesValue,
        fetchURL: spotifyUrl
    }
    const spotifyPopularityIndexValue = {
        ...musicJSON.spotifyPopularityIndexValue,
        fetchURL: spotifyUrl
    }
    const melonFollowerValue = {
        ...musicJSON.melonFollowerValue,
        fetchURL: melonUrl
    }
    

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