<script setup>
  import axios from '@/axios';
  import { useCounterStore } from '@/stores/counter';
  import { reactive, ref } from 'vue';
  import AreaCharts from '../components/AreaCharts.vue'
  import { useRoute, useRouter } from 'vue-router';
import HPFollower from '@/components/HPFollower.vue';
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
      fetchURL: "/api/instagram/chart/follower",
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
      fetchURL: `/api/spotify/index?end=${end}&range=three_month`,
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
      fetchURL: `/api/spotify/index?end=${end}&range=three_month`,
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
      fetchURL: "/api/tiktok/chart/follower",
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
      fetchURL: "/api/youtube/stats/channel",
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
      fetchURL: `/api/twitter/index?end=${end}&range=three_month`,
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
      const res = await axios.get(`/api/artist/info?mid=${mid.value}`, {setTimeout: 10000})
      artistInfo.value = res.data["results"]
      console.log("artistInfo : ", artistInfo);
      cardLoading.artist = false
    } catch (e) {
      console.error(e);
    }
  }

  const fetchMemberInfo = async () => {
    try {
      cardLoading.member = true
      const res = await axios.get(`/api/artist/members`, {setTimeout: 10000})
      memberInfo.value = res.data["results"]
      console.log("memberInfo : ", memberInfo);
      cardLoading.member = false
    } catch (e) {
      console.error(e);
    }
  }

  const fetchTheQoo = async () => {
    try {
      cardLoading.trending = true
      const res = await axios.get(`/api/theqoo/hot?page=${page.value}&limit=${limit.value}&q=${q.value}`, {setTimeout: 10000})
      hotData.value = res.data["posts"]
      console.log("hotData : ", res.data);
      cardLoading.trending = false
    } catch (e) {
      console.error(e);
    }
  }


  const fetchAll = async () => {
    await fetchArtistInfo()
    await fetchMemberInfo()
    await fetchTheQoo()
    console.log("// fetchAll Done");
  }

  fetchAll()

</script>

<template>
  <v-container
    class="bgcolor"
    fluid >
    <v-row
      class="mb-2"
      align="stretch"
    >
      <!-- Artist Info -->
      <v-col>
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
            class="flex-grow-2">
              <v-avatar style="height:150px; width:150px;">
                <v-img
                    :src=artistInfo.image
                    class="img-design"
                ></v-img>
              </v-avatar>
            </v-col>
            <v-col  class="flex-grow-2">
              <v-row>
                <v-col>
                  <v-card  class="pa-2 ma-2" variant="text">
                    {{ $t("Artist") }}:
                    <br />
                    <span :class="['font-weight-bold', 'text-body-1']">
                      {{ artistInfo.artist ? artistInfo.artist : 'N/A'}}
                    </span>
                  </v-card>
                </v-col>
                <v-col>
                  <v-card class="pa-2 ma-2" variant="text">
                    {{ $t("Debut Year") }}:
                    <br />
                    <span :class="['font-weight-bold', 'text-body-1']">
                      {{ artistInfo.debut_year ? artistInfo.debut_year : 'N/A' }}
                    </span>
                  </v-card>
                </v-col>
                <v-responsive width="100%"></v-responsive>
                <v-col>
                  <v-card class="pa-2 ma-2" variant="text">
                    {{ $t("Country")}}:
                    <br />
                    <img
                            src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/flags/kr.svg"
                            alt="kr-flag"
                            height="30px"
                        >
                  </v-card>
                </v-col>

                <v-col>
                  <v-card class="pa-2 ma-2" variant="text">
                    {{ $t("Birth")}}:
                    <br />
                    <span :class="['font-weight-bold', 'text-body-1']">
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
                {{ $t("Type") }}:
                <br />
                <span :class="['font-weight-bold', 'text-body-1']">
                  <span :class="['font-weight-bold', 'text-body-1']">
                    {{  artistInfo.type ? artistInfo.type[0] : "N/A" }}
                  </span>
                </span>
              </v-card>
            </v-col>
            <v-col>
              <v-card class="pa-2 ma-2" variant="text">
                {{ $t("Members")}}:
                <br />
                   <span :class="['font-weight-bold', 'text-body-1']">
                {{    memberInfo ? memberInfo : "N/A" }}
                </span>
              </v-card>
            </v-col>
          </v-row>
          <v-divider></v-divider>
          <v-row>
            <v-col>
              <v-card class="pa-2 ma-2" variant="text">
                {{ $t("Label")}}:
                <br />
                <span :class="['font-weight-bold', 'text-body-1']">
                  {{    artistInfo.labels ? artistInfo.labels : "N/A" }}
                </span>
              </v-card>
            </v-col>
            <v-col>
              <v-card class="pa-2 ma-2" variant="text">
                {{ $t("Fandom")}}:
                <br />
                <span :class="['font-weight-bold', 'text-body-1']">
                  {{    artistInfo.fandom ? artistInfo.fandom : "N/A" }}
                </span>
              </v-card>
            </v-col>
            <v-col>
              <v-card class="pa-2 ma-2" variant="text">
                {{ $t("Color")}}:
                <br />
                <span :class="['font-weight-bold', 'text-body-1']">
                  {{    artistInfo.color ? artistInfo.color : "N/A" }}
                </span>
              </v-card>
            </v-col>
            <v-col>
              <v-card class="pa-2 ma-2" variant="text">
                {{ $t("Last Release")}}:
                <br />
                <span :class="['font-weight-bold', 'text-body-1']">
                  {{    artistInfo.last_release ? artistInfo.last_release : "N/A" }}
                </span>
              </v-card>
            </v-col>

          </v-row>

        </template>

        </v-card>
      </v-col>


      <!-- Trending Info -->
      <v-col>
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
     <v-divider></v-divider>
     <br />
    <v-card style="background-color: #f8f7f2;">
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

            <HPFollower
            :type="item.type"
            :class="['ma-4', 'rounded-xl', 'pa-2']"
            :fetchURL="item.fetchURL"
            :iconHref="item.iconHref"
            :iconSrc="item.iconSrc"
            :fetchFollowerType="item.fetchFollowerType"
            :followerDataType="item.followerDataType"
            :fetchDateType="item.fetchDateType"
            :colors="item.colors"
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

  .bgcolor {
    background-color: #F5F5F5;
  }

</style>