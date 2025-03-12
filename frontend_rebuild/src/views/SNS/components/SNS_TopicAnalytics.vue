<script setup>
    import axios from '@/axios';
    import { onMounted, reactive, ref } from 'vue';
    import SNSHashtagMostUsedCard from './SNS_Hashtag_MostUsedCard.vue';
    import SNSHashtagMostEngagedCard from './SNS_Hashtag_MostEngagedCard.vue';
    const props = defineProps({
        value: Object,
        iconSrc: String
    })

    const series = ref([])
    const chartOptions = ref({})
    const loadingCard = ref(true)
    const selection = ref('10_posts')
    chartOptions.value = {
        chart: {
            type: 'bar',
            height: '350px',
        },
        dataLabels: {
                enabled: false
        },
        plotOptions: {
            bar: {
                borderRadius: 4,
                borderRadiusApplication: 'around',
                horizontal: true,
                columnWidth: '50%',
                distributed: true
            }
        },
        colors: ['#5BBCFF', '#FFFAB7', '#FFD1E3', '#7EA1FF', '#0C356A',
          '#80BCBD', '#AAD9BB', '#D5F0C1', '#0174BE', '#FFC436'],
        xaxis: {
          labels: {
            show: true,
            formatter: (value) => {
              return Number(value).toLocaleString()
            }
          },
          title: {
            text: 'Engage Percentage',
            offsetX: 0,
            offsetY: 0,
            style: {
              color: undefined,
              fontSize: '14px',
              fontFamily: 'Cairo, sans-serif',
              fontWeight: 600,
              // cssClass: 'apexcharts-xaxis-title',
            },
          },
        },
        yaxis: {
          type: 'category',
          labels: {
            show: true,
            trim: true,
            style: {
              colors: [],
              fontSize: '14px',
              fontFamily: 'Cairo, sans-serif',
              fontWeight: 400,
              // cssClass: 'apexcharts-xaxis-label',
            },
          }
        },
    }

    const fetchData = async (posts_amount) => {
        try {
            loadingCard.value = true
            selection.value = posts_amount
            let post_limit = 0
            switch (posts_amount) {
                case '10_posts': 
                    post_limit = 10
                    break
                case '30_posts':
                    post_limit = 30 // To do
                    break
                case 'all_posts':
                    post_limit = 0
                    break
            }

            const data = await axios.get(`/${props.value.apiType}/post/cat?cat=${post_limit}`, { setTimeout: 10000})
            
            const result = data.data.result.cat

            let _eng_rate_by_cat = result.map((e, i) => {
                return {
                    x: e._id,
                    y: e.eng_rate_by_cat,
                };
              });

              // update the series with axios data
            series.value = [
                {
                    name: 'Engagement Rate',
                    data: _eng_rate_by_cat,
                }
            ];
        loadingCard.value = false
        } catch (e) {
            console.error(e);
        }
    }

    onMounted(() => {
        fetchData('10_posts')
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
                {{ $t('Topic Analytics') }}
                </span>
            </template >
            <template v-slot:text>
                <v-card
                :loading="loadingCard">
                    <template v-slot:title>
                        <div :class="['d-flex', 'align-center']">
                            <v-img
                            :src="props.iconSrc"
                            max-height="30px"
                            max-width="30px"
                            :class="['mr-3']"
                            ></v-img>
                            <span>
                                {{ $t('Engagement Rate by Categories') }}
                            </span>
                            <v-tooltip
                            location="bottom"
                            :text="props.value.tooltipText">
                                <template v-slot:activator="{ props }">
                                    <v-icon
                                    size="20"
                                    :class="['mx-1']"
                                    v-bind="props"
                                    icon="mdi-information-outline"
                                    ></v-icon>
                                </template>
                            </v-tooltip>
                        </div>
                    </template>
                    <template v-slot:text>
                        <v-divider></v-divider>
                        <br />
                        <div :width="100" :class="['d-flex', 'justify-start']">
                            <div>
                                <v-btn
                                    :class="['mx-1']"
                                    size='small'
                                    variant='outlined'
                                    color="blue-grey-darken-2"
                                    dark
                                    rounded
                                    :active="selection === '10_posts'"
                                    @click="fetchData('10_posts')"
                                >
                                Latest 10 Posts
                                </v-btn>
                                <v-btn
                                    :class="['mx-1']"
                                    size='small'
                                    variant='outlined'
                                    color="blue-grey-darken-2"
                                    dark
                                    rounded
                                    :active="selection === '30_posts'"
                                    @click="fetchData('30_posts')"
                                >
                                Latest 30 Posts
                                </v-btn>
                                <v-btn
                                    :class="['mx-1']"
                                    size='small'
                                    variant='outlined'
                                    color="blue-grey-darken-2"
                                    dark
                                    rounded
                                    :active="selection === 'all_posts'"
                                    @click="fetchData('all_posts')"
                                >
                                All Posts
                                </v-btn>
                            </div>
                        </div>
                        <apexchart
                            width="100%"
                            height="180%"
                            :options="chartOptions" 
                            :series="series">
                        </apexchart>

                    </template>
                </v-card>
            </template>
        </v-card>

    </v-container>

</template>