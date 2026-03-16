<script setup>
  import axios from '@/axios';
  import { useCounterStore } from '@/stores/counter';
  import { useArtistStore } from '@/stores/artist'
  import {watch, computed, onMounted, reactive, ref} from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  import DB_TS_card from '@/views/Dashboard/components/DB_TS_card.vue';
  import TopStats from '@/views/Dashboard/components/TopStats.vue'
  import { currentProfile } from '@/libs/current-profile';
  import { getAuth } from 'firebase/auth';

  const followedArtists = ref([])
  const artistInfo = ref([])
  const graphItems = ref([])
  const memberInfo = ref("")
  const hotData = ref([])
  const router = useRouter()
  //pinia store mid
  const artistStore = useArtistStore()
  // const mid = ref(null)
  const page = ref(1)
  const limit = ref(10)
  const end = new Date().toISOString().slice(0, 10);

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

  const fetchFollowedArtist = async () => {
    try {
      const auth = getAuth();
      const user = auth.currentUser;

      if (!user) {
        console.error("Not login yet!");
        return;
      }

      const token = await user.getIdToken();
      // console.log(token)
      const res = await axios.get("/user/v1/followed_artists", {
        headers: {
          Authorization: `Bearer ${token}`,
          timeout: 10000
        }
      });
      followedArtists.value = res.data.data;
      // console.log(followedArtists.value[0]["artist_id"])
      if (followedArtists.value.length > 0) {
        // fetch first artist_id
        const firstArtistId = followedArtists.value[0]["id"]
        artistStore.setArtistId(firstArtistId)
        // mid.value = firstArtistId
        cardLoading.artist = true

        console.log("🎯 first artistId:", firstArtistId)
        // await fetchArtistInfo(mid.value, token);
        // request artist information
        const artistInfoRes = await axios.get(`/artist/info?artist_id=${firstArtistId}`, {
          headers: {
            Authorization: `Bearer ${token}`
          }, timeout: 10000})
        artistInfo.value = artistInfoRes.data["data"][0]
        // console.log(artistInfo)
        cardLoading.artist = false
      }
    } catch (err) {
      console.error(err);
    }
  }


  const fetchArtistInfo = async (artistId, token=null) => {
    try {
      if (!artistId) {
        console.warn("artistId is undefined!")
        return
      }
      cardLoading.artist = true
      // console.log("Fetching artist info for:", artistId)

      // if no token
      if (!token) {
        const auth = getAuth();
        const user = auth.currentUser;
        token = await user.getIdToken();
      }

      const resp = await axios.get(`/artist/info?artist_id=${artistId}`, {
        headers: {
            Authorization: `Bearer ${token}`
        }, timeout: 10000})

      if (resp.data.data && resp.data.data.length > 0) {
        const artistData = resp.data.data[0]
        artistStore.setArtist({
          id: artistData._id || null,
          threads: artistData.threads || null,
          instagram_id: artistData.instagram_id || null,
          youtube_id: artistData.youtube_id || null,
          tiktok_id: artistData.tiktok_id || null,
          bilibili_id: artistData.bilibili_id || null,
          spotify_id: artistData.spotify_id || null,
          melon_id: artistData.melon_id || null,
          genie_id: artistData.genie_id || null,
          apple_id: artistData.apple_id || null,
        })
        artistInfo.value = artistData
      } else {
        artistInfo.value = null
        artistStore.reset()
      }
    } catch (e) {
      console.error(e);
    } finally {
      cardLoading.artist = false
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

  const fetchAll = () => {
    fetchFollowedArtist();
    // fetchMemberInfo()
    // fetchTheQoo()
  }

  const normalizeArtist = (raw) => {
    return {
      artistId: raw._id,
      mid: raw.artist_id,
      name: raw.artist,
      image: raw.image,

      platforms: {
        bilibili: raw.bilibili_id
            ? {id: raw.bilibili_id}
            : null,

        youtube: raw.youtube_id
            ? {id: raw.youtube_id}
            : null,

        instagram: raw.instagram_id
            ? {
              id: raw.instagram_id,
              username: raw.instagram_user
            }
            : null,

        tiktok: raw.tiktok_id
            ? {id: raw.tiktok_id}
            : null,

        spotify: raw.spotify_id
            ? {id: raw.spotify_id}
            : null,

        melon: raw.melon_id
            ? {id: raw.melon_id}
            : null,
      },

      // 保留原始資料（debug / 其他頁可用）
      raw,
    }
  }

  // const profile = await currentProfile()
  // const { currentUser } = getAuth()
  //
  // if (!currentUser) {
  //   router.push('/auth/login')
  // }
  //
  // if (!profile) {
  //   router.push('/auth/register/details')
  // }

  onMounted(() => {
    fetchAll()
  })


  // convert datetime into YYYY-MM-DD
  function formatDate(dateStr) {
    return new Date(dateStr).toISOString().slice(0, 10);
  }

  watch(() => artistStore.artistId, (newId) => {
    if (newId) {
      fetchArtistInfo(newId)
    }
  }, { immediate: true })

// watch mid & artistInfo, to update graphItems
  watch([() => artistStore.artistId, artistInfo], ([newMid, newInfo]) => {
    // if (!newMid || !newInfo) {
    //   graphItems.value = []
    //   return
    // }
    // clean old data
    graphItems.value.forEach(item => {
      if (item.series) {
        item.series.value = []
      }
    })
    const end = new Date().toISOString().slice(0, 10)

    graphItems.value =  [
      {
        name: 'Instagram Followers',
        platform: 'Instagram',
        platformKey: 'instagram_id',
        type: 'Followers',
        fetchURL: artistStore.artistId
            ? `/instagram/v1/follower?date_end=${end}&range=28d&artist_id=${artistStore.artistId}`
            : "",
        iconHref: artistInfo.value?.instagram_user
            ? `https://www.instagram.com/${artistInfo.value.instagram_user}`
            : "#",
        iconSrc: "https://cdn.revmishkan.com/dist/instagram-logo.svg",
        fetchFollowerType: 'data',
        followerDataType: 'follower',
        fetchDateType: 'datetime',
        colors: ['#5851DB', '#6d67e1'],
      },
      {
        name: 'Spotify Followers',
        platform: 'Spotify',
        platformKey: 'spotify_id',
        type: 'Followers',
        range: "28d",
        fetchURL: artistStore.artistId
            ? `/spotify/v1/follower?date_end=${end}&range=28d&artist_id=${artistStore.artistId}`
            : "",
        iconSrc: "https://cdn.revmishkan.com/dist/spotify-logo.svg",
        iconHref: artistInfo.value?.spotify_id
            ? `https://open.spotify.com/artist/${artistInfo.value.spotify_id}`
            : "#",
        fetchFollowerType: 'data',
        followerDataType: 'follower',
        fetchDateType: 'datetime',
        colors: ['#1DB954'],
      },
      {
        name: 'Spotify Listeners',
        platform: 'Spotify',
        platformKey: 'spotify_id',
        type: 'Listeners',
        range: "28d",
        fetchURL: `/spotify/v1/monthly-listener?date_end=${end}&range=28d&artist_id=${artistStore.artistId}`,
        iconSrc: "https://cdn.revmishkan.com/dist/spotify-logo.svg",
        iconHref: artistInfo.value?.spotify_id
            ? `https://open.spotify.com/artist/${artistInfo.value.spotify_id}`
            : "#",
        fetchFollowerType: 'data',
        followerDataType: 'monthly_listener',
        fetchDateType: 'datetime',
        colors: ['#1DB954'],
      },
      {
        name: 'Tiktok Followers',
        platform: 'Tiktok',
        platformKey: 'tiktok_id',
        type: 'Followers',
        range: "28d",
        fetchURL: `/tiktok/v1/follower?date_end=${end}&range=28d&artist_id=${artistStore.artistId}`,
        iconSrc: "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/tiktok-logo.svg",
        iconHref: artistInfo.value?.tiktok_id
            ? `https://www.tiktok.com/@${artistInfo.value.tiktok_id}`
            : "#",
        fetchFollowerType: 'data',
        followerDataType: 'follower',
        fetchDateType: 'datetime',
        colors: ['#171616', '#464646'],
      },
      {
        name: 'Youtube Subscribes',
        platform: 'Youtube',
        platformKey: 'youtube_id',
        type: 'Subscribers',
        range: "28d",
        fetchURL: `/youtube/v1/channel?date_end=${end}&range=28d&artist_id=${artistStore.artistId}`,
        iconSrc: "https://cdn.revmishkan.com/dist/youtube-logo.svg",
        iconHref: artistInfo.value?.youtube_id
            ? `https://www.youtube.com/channel/${artistInfo.value.youtube_id}`
            : "#",
        fetchFollowerType: 'data',
        followerDataType: 'follower',
        fetchDateType: 'datetime',
        colors: ['#ff0000'],
      }
    ]
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
                    v-if="artistInfo.image"
                    :src="artistInfo.image || 'https://blocks.astratic.com/img/general-img-square.png'"
                    class="img-design"
                    cover
                ></v-img>
                <v-img
                    v-else
                    src="https://blocks.astratic.com/img/general-img-square.png"
                    class="img-design"
                    cover
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
                      {{ artistInfo.artist ? artistInfo.artist : '-'}}
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
                      {{ artistInfo.debut_year ? artistInfo.debut_year : '-' }}
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
                    <span :class="['text-body-1']">
                      {{ artistInfo.nation ? artistInfo.nation : "-" }}
                    </span>
<!--                    <img-->
<!--                            src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/flags/kr.svg"-->
<!--                            alt="kr-flag"-->
<!--                            class="h-10 w-10"-->
<!--                        >-->
                  </v-card>
                </v-col>

                <v-col>
                  <v-card class="pa-2 ma-2" variant="text">
                <span style="color: #757575;">
                    {{ $t("Birth")}}
                    </span>
                    <br />
                    <span :class="['text-body-1']">
                      {{  artistInfo.birth ? formatDate(artistInfo.birth) : "-" }}
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
                    {{  artistInfo.type ? artistInfo.type[0] : "-" }}
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
                {{    memberInfo ? memberInfo : "-" }}
                </span>
              </v-card>
            </v-col>
          </v-row>
          <v-divider></v-divider>
          <v-row>
            <v-col
            cols="6"
            sm="4">
              <v-card class="pa-2 ma-2" variant="text">
                <span style="color: #757575;">
                {{ $t("Pronouns")}}
                </span>
                <v-tooltip location="bottom">
                  <template v-slot:activator="{ props: activatorProps }">
                    <v-icon
                        size="20"
                        class="mx-1"
                        v-bind="activatorProps"
                        icon="mdi-information-outline"
                    />
                  </template>
                  <span>
                    M = Male<br/>
                    F = Female<br/>
                    C = Group
                  </span>
                </v-tooltip>
                <br />
                <span :class="['text-body-1']">
                  {{    artistInfo.pronouns ? artistInfo.pronouns : "-" }}
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
                  {{    artistInfo.fandom ? artistInfo.fandom : "-" }}
                </span>
              </v-card>
            </v-col>
            <v-col
            cols="6"
            sm="4">
              <v-card class="pa-2 ma-2" variant="text">
                <span style="color: #757575;">
                {{ $t("Color")}}
                </span>
                <br />
                <span :class="['text-body-1']">
                  {{    artistInfo.color ? artistInfo.color : "-" }}
                </span>
              </v-card>
            </v-col>
          </v-row>
        </template>
        </v-card>
      </v-col>
      <!-- Campaign Overview -->
      <v-col
      cols="12"
      md="6">
        <v-card 
          class="fill-height"
          :loading="cardLoading.artist"
          >
          <template v-slot:title>
            <span :class="['text-h5']">
              {{  $t('Following Artists') }}
            </span>
          </template>
          <template v-slot:text>
            <v-list class="overflow-y-auto" style="max-height: 250px">
              <v-list-item
                  v-for="artist in followedArtists"
                  :key="artist.id"
                  class="artist-item"
                  :prepend-avatar="artist.image"
                  @click="fetchArtistInfo(artist.id)"
              >
                <v-list-item-title class="text-body-1 font-weight-medium">
                  {{ artist.english_name }}
                </v-list-item-title>
                <v-list-item-subtitle class="text-grey">
                  {{ artist.korean_name }}
                </v-list-item-subtitle>
              </v-list-item>
            </v-list>
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
    <br />
  </v-container>
  <v-divider></v-divider>
    <v-container
    fluid
    style="background-color: #f8f7f2;">
      <TopStats :graphItems="graphItems"/>
    </v-container>
</template>

<style>
.artist-item {
  transition: background-color 0.2s;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}
.artist-item:hover {
  background-color: rgba(255, 255, 255, 0.05);
  cursor: pointer;
}

</style>
