<script setup>
  import axios from '@/axios';
  import { useCounterStore } from '@/stores/counter';
  import { onMounted, reactive, ref } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  import DB_TS_card from '@/views/Dashboard/components/DB_TS_card.vue';
  import { currentProfile } from '@/libs/current-profile';
import { getAuth } from 'firebase/auth';
  const artistInfo = ref({})
  const memberInfo = ref("")
  const hotData = ref([])
  const router = useRouter()
  const counterStore = useCounterStore()
  const mid = ref('1297') // to do
  const page = ref(1)
  const q = ref("t024")
  const limit = ref(10)
  const end = new Date().toISOString().slice(0, 10);

  const graphItems = [
    {
      name: 'Instagram Followers',
      type: 'Followers',
      fetchURL: "/instagram/v1/follower",
      iconHref: "https://www.instagram.com/t024.0fficial/",
      iconSrc: "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/instagram-logo.svg",
      fetchFollowerType: 'result',
      followerDataType: 'follower_count',
      fetchDateType: 'datetime',
      colors: ['#5851DB', '#6d67e1'],
    },
    {
      name: 'Spotify Followers',
      type: 'Followers',
      range: "three_month",
      end: new Date().toISOString().slice(0, 10),
      fetchURL: `/spotify/index?end=${end}&range=three_month`,
      iconSrc: "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/spotify-logo.svg",
      iconHref: "https://open.spotify.com/artist/0jxjOumN4dyPFTLUojSbNP",
      fetchFollowerType: 'posts',
      followerDataType: 'follower',
      fetchDateType: 'date',
      colors: ['#1DB954'],
    },
    {
      name: 'Spotify Listeners',
      type: 'Listeners',
      range: "three_month",
      end: new Date().toISOString().slice(0, 10),
      fetchURL: `/spotify/index?end=${end}&range=three_month`,
      iconSrc: "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/spotify-logo.svg",
      iconHref: "https://open.spotify.com/artist/0jxjOumN4dyPFTLUojSbNP",
      fetchFollowerType: 'posts',
      followerDataType: 'listener',
      fetchDateType: 'date',
      colors: ['#1DB954'],
    },
    {
      name: 'Tiktok Listeners',
      type: 'Followers',
      range: "three_month",
      end: new Date().toISOString().slice(0, 10),
      fetchURL: "/tiktok/chart/follower",
      iconSrc: "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/tiktok-logo.svg",
      iconHref: "https://www.tiktok.com/@t024.official",
      fetchFollowerType: 'result',
      followerDataType: 'tiktok_follower',
      fetchDateType: 'datetime',
      colors: ['#171616', '#464646'],
    },
    {
      name: 'Youtube Subscribes',
      type: 'Subscribers',
      range: "three_month",
      end: new Date().toISOString().slice(0, 10),
      fetchURL: "/youtube/stats/channel",
      iconSrc: "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/youtube-logo.svg",
      iconHref: "https://www.youtube.com/@t024.official",
      fetchFollowerType: 'result',
      followerDataType: 'subscriber',
      fetchDateType: 'datetime',
      colors: ['#ff0000'],
    },
    {
      name: 'Twitter Followers',
      type: 'Followers',
      range: "three_month",
      end: new Date().toISOString().slice(0, 10),
      fetchURL: `/twitter/index?end=${end}&range=three_month`,
      iconSrc: "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/twitter-logo.svg",
      iconHref: "https://twitter.com/t024_official",
      fetchFollowerType: 'posts',
      followerDataType: 'follower',
      fetchDateType: 'datetime',
      colors: ['#1DA1F2'],
    },



  ]
  const cardLoading = reactive({
    artist: true,
    member: true,
    trending: true,
  })
  const handleIncrement = () => {
    counterStore.increment()
  }
  const handleToAbout = () => {
    router.push({path: '/about'})
  }
  const fetchArtistInfo = async () => {
    try {
      cardLoading.artist = true
      const res = await axios.get(`/artist/info?mid=${mid.value}`, {setTimeout: 10000})
      artistInfo.value = res.data["results"]
      cardLoading.artist = false
    } catch (e) {
      console.error(e);
    }
  }

  const fetchMemberInfo = async () => {
    try {
      cardLoading.member = true
      const res = await axios.get(`/artist/members`, {setTimeout: 10000})
      memberInfo.value = res.data["results"]
      cardLoading.member = false
    } catch (e) {
      console.error(e);
    }
  } 

  const fetchTheQoo = async () => {
    try {
      cardLoading.trending = true
      const res = await axios.get(`/theqoo/hot?page=${page.value}&limit=${limit.value}&q=${q.value}`, {setTimeout: 10000})
      hotData.value = res.data["posts"]
      cardLoading.trending = false
    } catch (e) {
      console.error(e);
    }
  }


  const fetchAll = () => {
    fetchArtistInfo()
    fetchMemberInfo()
    fetchTheQoo()
  }

  const profile = await currentProfile()
  const { currentUser } = getAuth()

  if (!currentUser) {
    router.push('/auth/login')
  }

  if (!profile) {
    router.push('/auth/register/details')
  }

  onMounted(() => {
    fetchAll()
  })

</script>

<template>
  <v-container
    :class="['bg-grey-lighten-4']"
    fluid >
    <v-row
      class="mb-2"
      align="stretch"
    >
      <!-- Artist Info -->
      <v-col
      cols="12"
      md="6">
        <v-card 
          class="fill-height"
          :loading="cardLoading.artist"
          >
          <template v-slot:title>
            <span :class="['text-h5']">
              {{ $t("Summary") }}
            </span>
          </template>
          <template v-slot:text>
          <v-divider></v-divider>
          <br />
          <v-row>
            <v-col 
            align="center"
            justify="center"
            class="flex-grow-2"
            cols="12"
            sm="6">
              <v-avatar style="height:150px; width:150px;">
                <v-img
                    :src=artistInfo.image
                    class="img-design"
                ></v-img>
              </v-avatar>
            </v-col>
            <v-col
            cols="12"
            sm="6">
              <v-row>
                <v-col>
                  <v-card  class="pa-2 ma-2" variant="text" >
                    <span style="color: #757575;">
                      {{ $t("Artist") }}
                    </span>
                    <br />
                    <span :class="['text-body-1']">
                      {{ artistInfo.artist ? artistInfo.artist : 'N/A'}}
                    </span>
                  </v-card>
                </v-col>
                <v-col>
                  <v-card class="pa-2 ma-2" variant="text">
                <span style="color: #757575;">
                    {{ $t("Debut Year") }}
                    </span>
                    <br />
                    <span :class="['text-body-1']">
                      {{ artistInfo.debut_year ? artistInfo.debut_year : 'N/A' }}
                    </span>
                  </v-card>
                </v-col>
                <v-responsive width="100%"></v-responsive>
                <v-col>
                  <v-card class="pa-2 ma-2" variant="text">
                <span style="color: #757575;">
                    {{ $t("Country")}}
                    </span>
                    <br />
                    <img
                            src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/flags/kr.svg"
                            alt="kr-flag"
                            class="h-10 w-10"
                        >
                  </v-card>
                </v-col>

                <v-col>
                  <v-card class="pa-2 ma-2" variant="text">
                <span style="color: #757575;">
                    {{ $t("Birth")}}
                    </span>
                    <br />
                    <span :class="['text-body-1']">
                      {{  artistInfo.birth ? artistInfo.birth : "N/A" }}
                    </span>
                  </v-card>
                </v-col>
              </v-row>
            </v-col>
          </v-row>
          <v-divider></v-divider>
          <v-row>
            <v-col>
              <v-card class="pa-2 ma-2" variant="text">
                <span style="color: #757575;">
                {{ $t("Type") }}
                </span>
                <br />
                <span :class="['text-body-1']">
                  <span :class="['text-body-1']">
                    {{  artistInfo.type ? artistInfo.type[0] : "N/A" }}
                  </span>
                </span>
              </v-card>
            </v-col>
            <v-col>
              <v-card class="pa-2 ma-2" variant="text">
                <span style="color: #757575;">
                {{ $t("Members")}}
                </span>
                <br />
                    <span :class="['text-body-1']">
                {{    memberInfo ? memberInfo : "N/A" }}
                </span>
              </v-card>
            </v-col>
          </v-row>
          <v-divider></v-divider>
          <v-row>
            <v-col
            cols="6"
            sm="3">
              <v-card class="pa-2 ma-2" variant="text">
                <span style="color: #757575;">
                {{ $t("Label")}}
                </span>
                <br />
                <span :class="['text-body-1']">
                  {{    artistInfo.labels ? artistInfo.labels : "N/A" }}
                </span>
              </v-card>
            </v-col>
            <v-col
            cols="6"
            sm="3">
              <v-card class="pa-2 ma-2" variant="text">
                <span style="color: #757575;">
                {{ $t("Fandom")}}
                </span>
                <br />
                <span :class="['text-body-1']">
                  {{    artistInfo.fandom ? artistInfo.fandom : "N/A" }}
                </span>
              </v-card>
            </v-col>
            <v-col
            cols="6"
            sm="3">
              <v-card class="pa-2 ma-2" variant="text">
                <span style="color: #757575;">
                {{ $t("Color")}}
                </span>
                <br />
                <span :class="['text-body-1']">
                  {{    artistInfo.color ? artistInfo.color : "N/A" }}
                </span>
              </v-card>
            </v-col>
            <v-col
            cols="6"
            sm="3">
              <v-card class="pa-2 ma-2" variant="text">
                <span style="color: #757575;">
                {{ $t("Last Release")}}
                </span>
                <br />
                <span :class="['text-body-1']">
                  {{    artistInfo.last_release ? artistInfo.last_release : "N/A" }}
                </span>
              </v-card>
            </v-col>

          </v-row>

        </template>

        </v-card>
      </v-col>

      <!-- Trending Info -->
      <v-col
      cols="12"
      md="6">
        <v-card 
          class="fill-height"
          :loading="cardLoading.trending"
          >
          <template v-slot:title>
            <span :class="['text-h5']">
              {{  $t('Trending') }}
            </span>
          </template>
          <template v-slot:text>

          <v-divider></v-divider>
          <br />
          <v-card variant="text" v-if="hotData" v-for="item in hotData">

          </v-card>
          <v-card variant="text" v-else>
            No relevant data in 48 hours
          </v-card>
          
        </template>
        </v-card>

      </v-col>
    </v-row>
    <!-- Statistic-->
    <br />
  </v-container>
  <v-divider></v-divider>
    <v-container
    fluid
    style="background-color: #f8f7f2;">

    <v-card 
    style="background-color: #f8f7f2;"
    flat>
      <template v-slot:title>
        <span :class="['text-h4']">
          {{ $t('Top Statistics') }}
        </span>
      </template >
      <template v-slot:text>
        <v-slide-group
          show-arrows
          v-model="model"
          :class="['pa-4']"
          selected-class="bg-success"
        >
        <v-slide-group-item
          v-for="item in graphItems"
          :key="item.name"
        >
            <DB_TS_card
            :value="item"
            :class="['ma-4', 'rounded-xl', 'pa-2']"
            />
        </v-slide-group-item>
      </v-slide-group>

      </template>
    </v-card>
    </v-container>
</template>

<style>
  .card {
    min-width: 600px;
    min-height: 600px;
  }

</style>