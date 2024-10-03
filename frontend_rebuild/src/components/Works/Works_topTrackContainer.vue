<script setup>
    import WorksTopTrackCountry from './Works_topTrackCountry.vue';
    import WorksTopTrackRegion from './Works_topTrackRegion.vue';

    const props = defineProps({
        iconSrc: String
    })
</script>

<template>
    <v-container
    fluid
    :class="['bg-grey-lighten-4']">
        <v-card 
        :class="['bg-grey-lighten-4']"
        flat
        >
            <template v-slot:title>
                <span :class="['text-h4']">
                    {{ $t('Popularity of Spotify Top Tracks') }}
                </span>
            </template >
            <template v-slot:text>
                <v-row>
                    <v-col
                    cols="12"
                    lg="6">
                        <WorksTopTrackRegion :iconSrc="props.iconSrc"></WorksTopTrackRegion>
                    </v-col>
                    <v-col
                    cols="12"
                    lg="6">
                        <WorksTopTrackCountry :iconSrc="props.iconSrc"></WorksTopTrackCountry>
                    </v-col>
                </v-row>

            </template>
        </v-card>
    </v-container>
</template>