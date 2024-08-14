<script setup>
    import axios from '@/axios';
    import { reactive, ref } from 'vue';
    import SNSHashtagMostUsedCard from './SNS_Hashtag_MostUsedCard.vue';
    import SNSHashtagMostEngagedCard from './SNS_Hashtag_MostEngagedCard.vue';
    const props = defineProps({
        value: Object
    })

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
                {{ $t('Hashtags Analytics') }}
                </span>
            </template >
            <template v-slot:text>
                <v-row>
                    <v-col
                    cols="12"
                    lg="6">
                        <SNSHashtagMostUsedCard :value="props.value"></SNSHashtagMostUsedCard>
                    </v-col>
                    <v-col
                    cols="12"
                    lg="6">
                        <SNSHashtagMostEngagedCard :value="props.value"></SNSHashtagMostEngagedCard>
                    </v-col>
                </v-row>

            </template>
        </v-card>

    </v-container>

</template>