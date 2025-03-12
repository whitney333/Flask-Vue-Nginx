<script setup>
    import axios from '@/axios';
    import { computed, ref, watch } from 'vue';
    const platforms = [
        {
            value: 'spotify',
            title: 'Spotify',
            iconSrc: "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/spotify-logo.svg"
        },
        {
            value: 'youtube',
            title: 'Youtube',
            iconSrc: "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/youtube-logo.svg"
        },
        {
            value: 'billboard',
            title: 'Billboard',
            iconSrc: "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/billboard-logo.svg"
        },
        {
            value: 'melon',
            title: 'Melon',
            iconSrc: "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/melon.svg"
        },
        {
            value: 'Genie_music',
            title: 'Genie music',
            iconSrc: "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/Genie_music_logo.svg"
        },
        {
            value: 'QQ_music',
            title: 'QQ music',
            iconSrc: "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/QQ_music_logo.svg"
        }
    ]

    const songs = ref([])
    const selectedPlatform = ref(platforms[0])
    const loadingCard = ref(true)
    const selectedValue = ref('')
    const selectedDate = ref(new Date().toISOString().slice(0, 10))
    const selectedYear = computed(() => {
        return new Date(selectedDate.value).getFullYear()
    })
    const selectedWeek = computed(() => {
        return getWeekNumber(new Date(selectedDate.value))
    })
    const subtractOneWeek = () => {
        const d = new Date(selectedDate.value)
        d.setDate(d.getDate() - 7)
        selectedDate.value = d.toISOString().slice(0, 10)
    }
    const addOneWeek = () => {
        const d = new Date(selectedDate.value)
        d.setDate(d.getDate() + 7)
        selectedDate.value = d.toISOString().slice(0, 10)
    }
    const displaySongs = computed(() => {
        return songs.value.filter((s) => (s.title.toLowerCase()).includes(selectedValue.value.toLowerCase(), 0) || (s.artist.toLowerCase()).includes(selectedValue.value.toLowerCase(), 0))
    })

    const getWeekNumber = (d) => {
        // Copy date so don't modify original
        d = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
        // Set to nearest Thursday: current date + 4 - current day number
        // Make Sunday's day number 7
        d.setUTCDate(d.getUTCDate() + 4 - (d.getUTCDay()||7));
        // Get first day of year
        var yearStart = new Date(Date.UTC(d.getUTCFullYear(),0,1));
        // Calculate full weeks to nearest Thursday
        var weekNo = Math.ceil(( ( (d - yearStart) / 86400000) + 1)/7);
        // Return array of year and week number
        return weekNo
    }


    const headers = [
        { title: 'Rank', key: 'rank' },
        { title: 'Rank Change', key: 'rank_change' },
        { title: 'Artist', key: 'artist'},
        { title: 'Song', key: 'title'},
        { title: 'Peak', key: 'peak'},
        { title: 'Streams', key: 'streams'},
        { title: 'Streak', key: 'streak'},

    ]
    const getData = async () => {
        loadingCard.value = true
        const {data} = await axios.get(`/weekly/music-charts?year=${selectedYear.value}&week=${selectedWeek.value}&pl=${selectedPlatform.value.value}`, {setTimeout: 10000})
        songs.value = data.posts
        console.log(data);
        loadingCard.value = false
        
    }

    const getColor = (value) => {
        if (value == '–') {
            return 'grey'
        } else if (value == '+New') {
            return 'blue'
        } else if (value[0] == '-') {
            return 'red'
        } else {
            return 'green'
        }
    }
    getData()
    watch([selectedDate, selectedPlatform], getData)
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
                    {{ $t('Weekly Music Charts Overview') }}
                </span>
            </template >
            <template v-slot:text>
                <v-card :loading="loadingCard">
                    <template v-slot:title>
                            <div :class="['d-flex', 'align-center', 'ma-5']">
                                <v-img
                                :src="selectedPlatform.iconSrc"
                                max-height="30px"
                                max-width="30px"
                                :class="['mr-3']"
                                ></v-img>
                                <span :class="['text-h5']">
                                    {{ $t(selectedPlatform.title) }}
                                </span>
                            </div>
                    </template>
                    <template v-slot:text>
                        <v-divider></v-divider>
                        <br />
                        <div :class="['d-md-flex', 'justify-space-between', 'ga-10', 'f']">
                            <v-select
                            variant="outlined"
                            :maxWidth="300"
                            label="Platform"
                            item-title="title"
                            return-object
                            v-model="selectedPlatform"
                            :items="platforms"
                            rounded="lg"
                            >
                            <v-icon v-slot:prepand-inner-icon icon="mdi-fire">

                            </v-icon>

                            </v-select>
                            <div :class="['d-sm-flex', 'justify-space-between', 'ga-5']">

                            <v-text-field
                            label="Search for..."
                            v-model="selectedValue"
                            clearable
                            @click:clear="() => {selectedValue = ''}"
                            single-line
                            variant="underlined"
                            prepend-inner-icon="mdi-magnify"
                            :minWidth="200"

                            ></v-text-field>

                            <div :class="['d-flex', 'justify-space-between', 'ga-2']">
                                <v-btn
                                icon="mdi-chevron-left"
                                :class="'mt-1'"
                                @click="subtractOneWeek"
                                variant="text">
                                </v-btn>
                                <v-text-field 
                                :minWidth="160"
                                :maxWidth="160"
                                v-model="selectedDate"
                                type='date'
                                variant="outlined"
                                rounded="lg"
                                >
                                </v-text-field>
                                <v-btn
                                icon="mdi-chevron-right"
                                :class="'mt-1'"
                                :disabled="isThisWeek"
                                @click="addOneWeek"
                                variant="text">
                                </v-btn>
                                
                            </div>
                            </div>
                            

                        </div>
                        <v-data-table
                        :height="580"
                        :items="displaySongs"
                        :headers="headers"
                        items-per-page="10"
                        >
                        <template v-slot:item.rank_change="{ value }">
                            <v-chip :color="getColor(value)" :minWidth="20" variant="elevated">
                                {{ value }}
                            </v-chip>
                        </template>
                        </v-data-table>

                    </template>
                </v-card>
            </template>
        </v-card>
    </v-container>
</template>