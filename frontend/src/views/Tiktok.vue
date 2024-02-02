<template>
  <div class="main-content">
    <div class="section-stats">
      <div class="row align-items-center">
        <div class="col-xxl-12 col-xl-12 col-lg-12">
          <div class="row">
            <div class="col-lg-4">
              <div class="chart-box" id="tiktok-total-follower">
                <div class="section-header">
                  <v-img
                      src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/tiktok-logo.svg"
                      max-height="30px"
                      max-width="30px"
                      class="mr-3"
                  ></v-img>
                  <span>
                      {{ $t("Tiktok Followers") }}
                      <v-tooltip bottom color="grey lighten-4">
                        <template v-slot:activator="{ on, attrs }">
                          <v-icon
                              color="primary"
                              v-bind="attrs"
                              v-on="on"
                          >
                          mdi-information-outline
                          </v-icon>
                        </template>
                        <span>{{ $t("Number of followers on Tiktok") }}</span>
                      </v-tooltip>
                    </span>
                </div>
                <TiktokFollower/>
              </div>
            </div>
            <div class="col-lg-4">
              <div class="chart-box" id="tiktok-total-likes">
                <div class="section-header">
                  <v-img
                      src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/tiktok-logo.svg"
                      max-height="30px"
                      max-width="30px"
                      class="mr-3"
                  ></v-img>
                  <span>
                      {{ $t("Tiktok Total Likes") }}
                      <v-tooltip bottom color="grey lighten-4">
                        <template v-slot:activator="{ on, attrs }">
                          <v-icon
                              color="primary"
                              v-bind="attrs"
                              v-on="on"
                          >
                          mdi-information-outline
                          </v-icon>
                        </template>
                        <span>{{ $t("Number of likes on TikTok") }}</span>
                      </v-tooltip>
                    </span>
                </div>
                <TiktokTotalLikes/>
              </div>
            </div>
            <div class="col-lg-4">
              <div class="chart-box" id="tiktok-total-view">
                <div class="section-header">
                  <v-img
                      src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/tiktok-logo.svg"
                      max-height="30px"
                      max-width="30px"
                      class="mr-3"
                  ></v-img>
                  <span>
                      {{ $t("Tiktok Total Views") }}
                      <v-tooltip bottom color="grey lighten-4">
                        <template v-slot:activator="{ on, attrs }">
                          <v-icon
                              color="primary"
                              v-bind="attrs"
                              v-on="on"
                          >
                          mdi-information-outline
                          </v-icon>
                        </template>
                        <span>{{ $t("Number of views on TikTok") }}</span>
                      </v-tooltip>
                    </span>
                </div>
                <TiktokTotalViews/>
              </div>
            </div>
            <div class="col-lg-4">
              <div class="chart-box" id="tiktok-total-comment">
                <div class="section-header">
                  <v-img
                      src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/tiktok-logo.svg"
                      max-height="30px"
                      max-width="30px"
                      class="mr-3"
                  ></v-img>
                  <span>
                      {{ $t("Tiktok Total Comments") }}
                      <v-tooltip bottom color="grey lighten-4">
                        <template v-slot:activator="{ on, attrs }">
                          <v-icon
                              color="primary"
                              v-bind="attrs"
                              v-on="on"
                          >
                          mdi-information-outline
                          </v-icon>
                        </template>
                        <span>{{ $t("Number of comments on TikTok") }}</span>
                      </v-tooltip>
                    </span>
                </div>
                <TiktokTotalComment/>
              </div>
            </div>
            <div class="col-lg-4">
              <div class="chart-box" id="tiktok-total-share">
                <div class="section-header">
                  <v-img
                      src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/tiktok-logo.svg"
                      max-height="30px"
                      max-width="30px"
                      class="mr-3"
                  ></v-img>
                  <span>
                      {{ $t("Tiktok Total Shares") }}
                      <v-tooltip bottom color="grey lighten-4">
                        <template v-slot:activator="{ on, attrs }">
                          <v-icon
                              color="primary"
                              v-bind="attrs"
                              v-on="on"
                          >
                          mdi-information-outline
                          </v-icon>
                        </template>
                        <span>{{ $t("Number of shares on TikTok") }}</span>
                      </v-tooltip>
                    </span>
                </div>
                <TiktokTotalShare/>
              </div>
            </div>
            <div class="col-lg-4">
              <div class="chart-box" id="tiktok-total-save">
                <div class="section-header">
                  <v-img
                      src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/tiktok-logo.svg"
                      max-height="30px"
                      max-width="30px"
                      class="mr-3"
                  ></v-img>
                  <span>
                      {{ $t("Tiktok Total Saves") }}
                      <v-tooltip bottom color="grey lighten-4">
                        <template v-slot:activator="{ on, attrs }">
                          <v-icon
                              color="primary"
                              v-bind="attrs"
                              v-on="on"
                          >
                          mdi-information-outline
                          </v-icon>
                        </template>
                        <span>{{ $t("Number of saves on TikTok") }}</span>
                      </v-tooltip>
                    </span>
                </div>
                <TiktokTotalSaves/>
              </div>
            </div>
            <div class="col-lg-4">
              <div class="chart-box" id="tiktok-total-engagement">
                <div class="section-header">
                  <v-img
                      src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/tiktok-logo.svg"
                      max-height="30px"
                      max-width="30px"
                      class="mr-3"
                  ></v-img>
                  <span>
                      {{ $t("Tiktok Engagement Rate") }}
                      <v-tooltip bottom color="grey lighten-4">
                        <template v-slot:activator="{ on, attrs }">
                          <v-icon
                              color="primary"
                              v-bind="attrs"
                              v-on="on"
                          >
                          mdi-information-outline
                          </v-icon>
                        </template>
                        <span>{{ $t("Average engagement rate of TikTok videos") }}</span>
                      </v-tooltip>
                    </span>
                </div>
                <TiktokTotalEngagement/>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="section-overall">
      <div class="section-title">
        <h2>{{ $t('Hashtags Analytics') }}</h2>
      </div>
      <div class="row">
        <div class="col-lg-6 spacer">
          <div class="chart-box-2">
            <div class="section-header">
              <v-img
                  src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/hashtag.svg"
                  max-height="30px"
                  max-width="30px"
                  class="mr-3"
              ></v-img>
              <span>
                {{ $t('Top 10 Most-used Hashtags') }}
                  <v-tooltip bottom color="grey lighten-4">
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                      color="primary"
                      v-bind="attrs"
                      v-on="on"
                  >
                    mdi-information-outline
                  </v-icon>
                </template>
                <span>Daily trends of Spotify Followers</span>
              </v-tooltip>
                </span>
            </div>
            <div class="hash-list">
              <TiktokMostUsedHashtag/>
            </div>
          </div>
        </div>
        <div class="col-lg-6 spacer">
          <div class="chart-box-2">
            <div class="section-header">
              <v-img
                  src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/hashtag.svg"
                  max-height="30px"
                  max-width="30px"
                  class="mr-3"
              ></v-img>
              <span>
                {{ $t('Top 10 Most-engaged Hashtags') }}
                  <v-tooltip bottom color="grey lighten-4">
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                      color="primary"
                      v-bind="attrs"
                      v-on="on"
                  >
                    mdi-information-outline
                  </v-icon>
                </template>
                <span>Daily trends of Spotify Followers</span>
              </v-tooltip>
                </span>
            </div>
            <div class="hash-list">
              <TiktokMostEngagedHashtag/>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="section-campaign">
      <div class="section-title">
        <h2>{{ $t('All Videos') }}</h2>
      </div>
      <div class="filters">
        <v-row wrap justify="end">
          <v-col
              cols="3"
          >
            <v-select
                :items="select_items"
                label="Sort by"
                dense
                solo
                v-model="selected_cat"
                @input="filterSort"
                item-color="orange darken-1"
            ></v-select>
          </v-col>
        </v-row>
      </div>
      <div class="row">
        <div class="col-lg-4 col-md-6"
             v-for="(video, i) in TiktokPost"
        >
          <a v-bind:href="video.url" target="_blank">
            <div class="box3">
              <div class="box-img" :style="{backgroundImage: 'url(' + video.image +')'}"></div>
              <div class="box-body">
                <div class="infoStat">
                  <ul>
                    <v-tooltip right color="grey lighten-4">
                      <template v-slot:activator="{ on }">
                        <li class="stat4" v-on="on">{{ video.views | formatNumber }}</li>
                      </template>
                      <span>{{ $t('Views') }}: {{ (video.views).toLocaleString() }}</span>
                    </v-tooltip>
                    <v-tooltip right color="grey lighten-4">
                      <template v-slot:activator="{ on }">
                        <li class="stat3" v-on="on">{{ video.likes | formatNumber }}</li>
                      </template>
                      <span>{{ $t('Likes') }}: {{ (video.likes).toLocaleString() }}</span>
                    </v-tooltip>
                    <v-tooltip right color="grey lighten-4">
                      <template v-slot:activator="{ on }">
                        <li class="stat2" v-on="on">{{ video.comments | formatNumber }}</li>
                      </template>
                      <span>{{ $t('Comments') }}: {{ (video.comments).toLocaleString() }}</span>
                    </v-tooltip>
                    <v-tooltip right color="grey lighten-4">
                      <template v-slot:activator="{ on }">
                        <li class="stat1" v-on="on">{{ video.share | formatNumber }}</li>
                      </template>
                      <span>{{ $t('Shares') }}: {{ (video.share).toLocaleString() }}</span>
                    </v-tooltip>
                  </ul>
                </div>
                <span class="val-text">
                <v-tooltip right color="grey lighten-4">
                  <template v-slot:activator="{ on }">
                    <span>{{ (video.eng_rate.toFixed(2)) }}</span>
                    <span>%</span>
                  </template>
                  <span>{{ $t('Engagement Rate') }}</span>
                </v-tooltip>
              </span>
                <div class="date">
                  <span><img src="../assets/img/calendar-icon-red.svg" alt=""/>{{ video.publish_at }}</span>
                </div>
              </div>
            </div>
          </a>
        </div>
        <div class="col-12">
          <div class="button-block">
            <div class="filters">
              <v-row wrap justify="center">
                <v-col
                    cols="4"
                >
                  <v-btn
                      class="button"
                      large
                      icon
                      :disabled="this.page === 1"
                      @click="previousPage()"
                  >
                    <v-icon>
                      mdi-chevron-left
                    </v-icon>
                  </v-btn>
                  <v-btn
                      class="button"
                      large
                      icon
                      @click="loadMore()"
                      :disabled="this.page === (this.total_posts_count / this.perPage) + 1"
                  >
                    <v-icon>
                      mdi-chevron-right
                    </v-icon>
                  </v-btn>
                </v-col>
              </v-row>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import TiktokTotalLikes from "@/components/TiktokTotalLikes";
import TiktokTotalViews from "@/components/TiktokTotalViews";
import TiktokFollower from "@/components/TiktokFollower";
import TiktokMostUsedHashtag from "@/components/TiktokMostUsedHashtag";
import TiktokMostEngagedHashtag from "@/components/TiktokMostEngagedHashtag";
import TiktokTotalComment from "@/components/TiktokTotalComment";
import TiktokTotalShare from "@/components/TiktokTotalShare";
import TiktokTotalEngagement from "@/components/TiktokTotalEngagement";
import TiktokTotalSaves from "@/components/TiktokTotalSaves";

export default {
  name: "Tiktok",
  components: {
    TiktokTotalSaves,
    TiktokTotalEngagement,
    TiktokMostEngagedHashtag, TiktokMostUsedHashtag, TiktokFollower,
    TiktokTotalViews, TiktokTotalLikes, TiktokTotalComment, TiktokTotalShare},
  data() {
    return {
      page: 1,
      perPage: 9,
      sort: '',
      total_posts_count: '',
      TiktokPost: [],
      selected_cat: "",
      select_items: ["Date(Default)", "Most Likes", "Most Comments", "Most Engaged", "Most Shares"],
      //current & past week index
      current_video_num: "",
      current_like: "",
      current_comment: "",
      current_share: "",
      current_view: "",
      past_video_num: "",
      past_like: "",
      past_comment: "",
      past_share: "",
      past_view: ""
    }
  },
  methods: {
    async get_posts() {
      const {data} = await this.axios.get('http://localhost/api/tiktok/post?' + 'page=' + this.page + '&limit=' + this.perPage + '&sort=' + this.sort)
      this.page = data["result"]["page"]
      this.sort = data["result"]["sort"]
      this.total_posts_count = data["result"]["total_posts_count"]
      this.TiktokPost = data["result"]["posts"]
      // console.log(this.sort)
    },
    loadMore() {
      this.page++;
      if ((this.perPage * this.page) <= this.total_posts_count) {
        this.get_posts();
      }
    },
    previousPage() {
      this.page--
      if ((this.perPage * this.page) <= this.total_posts_count) {
        this.get_posts();
      }
    },
    filterSort() {
      if (this.selected_cat === 'Most Likes') {
        this.page = 1
        this.sort = 'like'
        this.get_posts();
      } else if (this.selected_cat === 'Most Comments') {
        this.page = 1
        this.sort = 'comment'
        this.get_posts();
      } else if (this.selected_cat === 'Date(Default)') {
        this.page = 1
        this.sort = 'date'
        this.get_posts();
      } else if (this.selected_cat === 'Most Engaged') {
        this.page = 1
        this.sort = 'engaged'
        this.get_posts();
      } else if (this.selected_cat === 'Most Shares') {
        this.page = 1
        this.sort = 'share'
        this.get_posts();
      }
    }
  },
  created() {
    this.get_posts();
    this.loadMore();
    this.previousPage();
    this.filterSort();
  },
  filters: {
    truncateText: (text) => {
      if (text.length > 60) {
        text = text.substring(0, 125) + "...";
      }
      return text;
    },
    formatNumber: function (num) {
      if (String(num).length < 4) {
        return num;
      } else if (String(num).length < 7) {
        return Math.floor(num / 1000) + 'K';
      } else if (String(num).length < 10) {
        return Math.floor(num / 1000000) + 'M';
      } else {
        return Math.floor(num / 1000000000) + 'B';
      }
    }
  }
}
</script>
<style scoped>
.chart-box {
  width:100%;
  height: 100%;
  padding: 20px 10px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  -webkit-border-radius: 8px;
}
.box3 .box-img:hover {
  /*-ms-transform: translate(-15px, -15px);*/
  /*transform: translate(-5px, -5px)*/
  transition: transform 0.6s ease;
  transform: translate(0, -5px);
}
.index-box {
  height: 100%;
  width: 100%;
  padding: 10px 20px;
  text-align: center;
  justify-content: center;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  -webkit-border-radius: 8px;
  /*padding-bottom: 20%;*/
}
.index-box .stat span {
  display: inline-block;
  font-size: 24px;
  font-weight: 700;
  white-space: nowrap;
  /*padding-top: 20%;*/
}
.index-box .stat span:after {
  content: '';
  display: inline-block;
  width: 16px;
  height: 19px;
  margin-left: 5px;
  background-repeat: no-repeat;
  background-position: center center
}
.index-box .stat span.up:after {
  background-image: url('../assets/img/rec-arrow-up.svg')
}
.index-box .stat span.down:after {
  background-image: url('../assets/img/rec-arrow-down.svg')
}
.index-box .stat span.same:after {
  background-image: url('../assets/img/rec-arrow-same.svg')
}
.index-box p {
  color: #767676;
  font-size: 16px;
  font-weight: 500;
  margin: 0;
  padding-top: 5px;
}
</style>