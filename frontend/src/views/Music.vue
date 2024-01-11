<template>
  <div class="main-content">
    <div class="section-spotify-stat">
      <div class="section-title">
        <h2>{{ $t("Popularity of Spotify Top Tracks") }}</h2>
      </div>
      <div class="row">
        <div class="col-lg-6">
          <div class="chart-box">
            <div class="section-header">
              <v-img
                  src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/spotify-logo.svg"
                  max-height="30px"
                  max-width="30px"
                  class="mr-3"
              ></v-img>
              <span>
              {{ $t('By Region') }}
              <v-tooltip bottom color="grey lighten-4" max-width="250px">
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                      color="primary"
                      dark
                      v-bind="attrs"
                      v-on="on"
                  >
                    mdi-information-outline
                  </v-icon>
                </template>
                <span>The ratio of artist's followers to monthly listeners. (Number of followers/ monthly listeners)</span>
              </v-tooltip>
              </span>
            </div>
            <SpotifyRegionTopTrack/>
          </div>
        </div>
        <div class="col-lg-6">
          <div class="chart-box">
            <div class="section-header">
              <v-img
                  src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/spotify-logo.svg"
                  max-height="30px"
                  max-width="30px"
                  class="mr-3"
              ></v-img>
              <span>
              {{ $t('By Country') }}
              <v-tooltip bottom color="grey lighten-4" max-width="250px">
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                      color="primary"
                      dark
                      v-bind="attrs"
                      v-on="on"
                  >
                    mdi-information-outline
                  </v-icon>
                </template>
                <span>The ratio of artist's followers to monthly listeners. (Number of followers/ monthly listeners)</span>
              </v-tooltip>
              </span>
            </div>
            <SpotifyTopTrack/>
          </div>
        </div>
      </div>
    </div>
    <div class="section-overall bg-color2">
      <div class="section-title">
        <h2>{{ $t("Fan Engagement") }}</h2>
      </div>
      <div class="row">
        <div class="col-lg-4">
          <div class="chart-box">
            <div class="section-header">
              <v-img
                  src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/spotify-logo.svg"
                  max-height="30px"
                  max-width="30px"
                  class="mr-3"
              ></v-img>
              <span>
                {{ $t('Spotify Followers') }}
                <v-tooltip bottom color="grey lighten-4" max-width="250px">
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                      color="primary"
                      v-bind="attrs"
                      v-on="on"
                  >
                    mdi-information-outline
                  </v-icon>
                </template>
                <span>Number of followers on Spotify</span>
              </v-tooltip>
              </span>
            </div>
            <SpotifyFollower/>
          </div>
        </div>
        <div class="col-lg-4">
          <div class="chart-box">
            <div class="section-header">
              <v-img
                  src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/spotify-logo.svg"
                  max-height="30px"
                  max-width="30px"
                  class="mr-3"
              ></v-img>
              <span>
                {{ $t('Spotify Monthly Listeners') }}
                <v-tooltip bottom color="grey lighten-4" max-width="250px">
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                      color="primary"
                      dark
                      v-bind="attrs"
                      v-on="on"
                  >
                    mdi-information-outline
                  </v-icon>
                </template>
                <span>Number of Spotify monthly listeners in the past 28 days</span>
              </v-tooltip>
              </span>
            </div>
            <SpotifyMonthlyListener/>
          </div>
        </div>
        <div class="col-lg-4">
          <div class="chart-box">
            <div class="section-header">
              <v-img
                  src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/spotify-logo.svg"
                  max-height="30px"
                  max-width="30px"
                  class="mr-3"
              ></v-img>
              <span>
              {{ $t('Spotify Fan Conversion Rate') }}
              <v-tooltip bottom color="grey lighten-4" max-width="250px">
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                      color="primary"
                      dark
                      v-bind="attrs"
                      v-on="on"
                  >
                    mdi-information-outline
                  </v-icon>
                </template>
                <span>The ratio of artist's followers to monthly listeners. (Number of followers/ monthly listeners)</span>
              </v-tooltip>
              </span>
            </div>
            <SpotifyFanConversion/>
          </div>
        </div>
        <div class="col-lg-4">
          <div class="chart-box">
            <div class="section-header">
              <v-img
                  src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/spotify-logo.svg"
                  max-height="30px"
                  max-width="30px"
                  class="mr-3"
              ></v-img>
              <span>
              {{ $t("Spotify Top Cities") }}
              <v-tooltip bottom color="grey lighten-4" max-width="250px">
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                      color="primary"
                      dark
                      v-bind="attrs"
                      v-on="on"
                  >
                    mdi-information-outline
                  </v-icon>
                </template>
                <span>Top 5 cities with the most monthly listeners</span>
              </v-tooltip>
              </span>
            </div>
            <SpotifyTopCity/>
          </div>
        </div>
        <div class="col-lg-4">
          <div class="chart-box">
            <div class="section-header">
              <v-img
                  src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/spotify-logo.svg"
                  max-height="30px"
                  max-width="30px"
                  class="mr-3"
              ></v-img>
              <span>
              {{ $t('Spotify Popularity Index') }}
              <v-tooltip bottom color="grey lighten-4" max-width="250px">
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                      color="primary"
                      dark
                      v-bind="attrs"
                      v-on="on"
                  >
                    mdi-information-outline
                  </v-icon>
                </template>
                <span>An index on a scale of 0-100 showing an artist's popularity relative to others on Spotify</span>
              </v-tooltip>
              </span>
            </div>
            <SpotifyPopularity/>
          </div>
        </div>
        <div class="col-lg-4">
          <div class="chart-box">
            <div class="section-header">
              <v-img
                  src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/melon.svg"
                  max-height="40px"
                  max-width="40px"
              ></v-img>
              <span>
              {{ $t('Melon Follower') }}
              <v-tooltip bottom color="grey lighten-4" max-width="250px">
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                      color="primary"
                      dark
                      v-bind="attrs"
                      v-on="on"
                  >
                    mdi-information-outline
                  </v-icon>
                </template>
                <span>Number of followers on Melon</span>
              </v-tooltip>
              </span>
            </div>
            <MelonFollower/>
          </div>
        </div>
        <!-- YouTube Top Artist -->
      </div>
    </div>
    <div class="section-overall">
      <div class="section-title">
        <h2>{{ $t('Weekly Music Charts Overview') }}</h2>
      </div>
      <div class="row">
        <div class="col-lg-12 spacer">
          <div class="overview-box">
            <div class="box-upper">
              <div v-if="this.selected_chart === 'Spotify (스포티파이)'">
                <v-img
                    src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/spotify-logo.svg"
                    alt="spotify-logo"
                    max-width="40px"
                    max-height="40px"
                    class="mr-2"
                ></v-img>
              </div>
              <div v-else-if="this.selected_chart === 'YouTube (유튜브)'">
                <v-img
                    src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/youtube-logo.svg"
                    alt="youtube-logo"
                    max-width="40px"
                    max-height="40px"
                    class="mr-2"
                ></v-img>
              </div>
              <div v-else-if="this.selected_chart === 'Billboard Top 200 (빌보드)'">
                <v-img
                    src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/billboard-logo.svg"
                    alt="billboard-logo"
                    max-width="40px"
                    max-height="40px"
                    class="mr-2"
                ></v-img>
              </div>
              <div v-else-if="this.selected_chart === 'Melon (멜론)'">
                <v-img
                    src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/melon.svg"
                    alt="melon-logo"
                    max-width="40px"
                    max-height="40px"
                    class="mr-2"
                ></v-img>
              </div>
              <div v-else-if="this.selected_chart === 'Genie (지니뮤직)'">
                <img
                    src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/Genie_music_logo.svg"
                    alt="genie-logo"
                    height="40px"
                    class="mr-2"
                >
              </div>
              <div v-else-if="this.selected_chart === 'QQ Music'">
                <img
                    src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/QQ_music_logo.svg"
                    alt="qq-logo"
                    height="40px"
                    class="mr-2"
                >
              </div>
              <h3> {{ this.selected_chart }}</h3>
              <v-spacer/>
              <!--  dropdown menu of music broadcast programs  -->
              <v-row style="flex-direction: row-reverse">
                <v-col cols="6" lg="6" class="align-content-end">
                  <v-select
                      :items="music_platform"
                      label="Select Platform"
                      dense
                      filled
                      rounded
                      v-model="selected_chart"
                      item-color="orange darken-1"
                  ></v-select>
                </v-col>
              </v-row>
            </div>
            <div class="box-body" style="width:auto; height: auto; overflow-y: scroll">
              <div v-if="this.selected_chart === 'Spotify (스포티파이)'">
                <WeekChartSpotify/>
              </div>
              <div v-else-if="this.selected_chart === 'YouTube (유튜브)'">
                <WeekChartYoutube/>
              </div>
              <div v-else-if="this.selected_chart === 'Billboard Top 200 (빌보드)'">
                <WeekChartBillboard/>
              </div>
              <div v-else-if="this.selected_chart === 'Melon (멜론)'">
                <WeekChartMelon/>
              </div>
              <div v-else-if="this.selected_chart === 'Genie (지니뮤직)'">
                <WeekChartGenie/>
              </div>
              <div v-else-if="this.selected_chart === 'QQ Music'">
                <WeekChartQQ/>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import SpotifyFollower from "@/components/SpotifyFollower";
import SpotifyMonthlyListener from "@/components/SpotifyMonthlyListener";
import SpotifyFanConversion from "@/components/SpotifyFanConversion";
import SpotifyTopCity from "@/components/SpotifyTopCity";
import SpotifyPopularity from "@/components/SpotifyPopularity";
import MelonFollower from "@/components/MelonFollower";
import WeekChartSpotify from "@/components/WeekChartSpotify";
import WeekChartYoutube from "@/components/WeekChartYoutube";
import WeekChartBillboard from "@/components/WeekChartBillboard";
import WeekChartMelon from "@/components/WeekChartMelon";
import WeekChartGenie from "@/components/WeekChartGenie";
import SpotifyTopTrack from "@/components/SpotifyTopTrack";
import SpotifyRegionTopTrack from "@/components/SpotifyRegionTopTrack";
import WeekChartQQ from "@/components/WeekChartQQ";

export default {
  name: "Music",
  components: {
    WeekChartQQ,
    SpotifyRegionTopTrack,
    SpotifyTopTrack,
    WeekChartGenie,
    WeekChartMelon,
    WeekChartBillboard,
    WeekChartYoutube,
    WeekChartSpotify,
    MelonFollower,
    SpotifyPopularity, SpotifyTopCity, SpotifyFanConversion,
    SpotifyMonthlyListener, SpotifyFollower
  },
  data() {
    return {
      index: "",
      selected_cat: "",
      programs: ["Inkigayo (인기가요)", "The Show (더 쇼)", "Show Champion (쇼 챔피언)",
          "M countdown (엠 카운트다운)", "Music Center (쇼!음악중심)", "Music Bank (뮤직뱅크)"],
      selected_chart: "",
      music_platform: ["Spotify (스포티파이)", "YouTube (유튜브)", "Billboard Top 200 (빌보드)",
          "Melon (멜론)", "Genie (지니뮤직)", "QQ Music"],
    }
  },
  methods: {
    get_default_weekly_chart() {
      this.selected_chart = "Spotify (스포티파이)"
    }
  },
  created() {
    this.get_default_weekly_chart();
  }
}
</script>
<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR&display=swap');
.chart-box {
  width: auto;
  height: 100%;
  padding: 20px 10px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  -webkit-border-radius: 8px;
}
.box-upper {
  display:flex;
  align-items:center;
  padding:0 0 3px;
  border-bottom:1px solid #d9d9db;
}
.box-upper h3 {
  display: flex;
}

/* width */
::-webkit-scrollbar {
  width: 5px;
  height: 5px;
}

/* Track */
::-webkit-scrollbar-track {
  background: #ffffff;
}

/* Handle */
::-webkit-scrollbar-thumb {
  background: rgb(183, 181, 181);
  border-radius: 7px;
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: #605f5f;
}
.track-box{
    height:100%;
    width:100%;
    padding:10px;
    background-color:#fff;
    border:1px solid #ddd;
    border-radius:8px;
    -webkit-border-radius:8px
}
</style>