<script setup>
    import axios from '@/axios';
    import { reactive, ref } from 'vue';
    import SNSHashtagMostUsedCard from './SNS_Hashtag_MostUsedCard.vue';
    import SNSHashtagMostEngagedCard from './SNS_Hashtag_MostEngagedCard.vue';
    const props = defineProps({
        value: Object,
        iconSrc: String,
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
          <!-- Title -->
          <div class="px-4 pt-4 min-w-0">
            <h2 class="text-lg sm:text-xl md:text-2xl font-semibold text-gray-800">
              {{ $t('Hashtags Analytics') }}
            </h2>
          </div>
          <!-- Content -->
          <v-card-text>
            <v-row>
              <v-col cols="12" lg="6">
                <SNSHashtagMostUsedCard :iconSrc="iconSrc" :value="props.value"/>
              </v-col>

              <v-col cols="12" lg="6">
                <SNSHashtagMostEngagedCard :iconSrc="iconSrc" :value="props.value"/>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
    </v-container>
</template>
