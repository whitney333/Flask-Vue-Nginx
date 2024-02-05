<template>
  <div class="main-content">
    <div class="section-stats">
      <div class="row align-items-center">
        <div class="col-xxl-12 col-xl-12 col-lg-12">
          <div class="row">
            <div class="col-lg-4">
              <div class="chart-box" id="bilibili-total-video">
                <div class="section-header">
                  <v-img
                      src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/bilibili-logo.svg"
                      max-height="30px"
                      max-width="30px"
                      class="mr-3"
                  ></v-img>
                  <span>
                      {{ $t("Bilibili Total Videos") }}
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
                        <span>{{ $t("Number of related (keyword) videos on Bilibili") }}</span>
                      </v-tooltip>
                    </span>
                </div>
                <BilibiliTotalVideo/>
              </div>
            </div>
            <div class="col-lg-4">
              <div class="chart-box" id="bilibili-total-view">
                <div class="section-header">
                  <v-img
                      src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/bilibili-logo.svg"
                      max-height="30px"
                      max-width="30px"
                      class="mr-3"
                  ></v-img>
                  <span>
                      {{ $t("Bilibili Total Views") }}
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
                        <span>{{ $t("Number of related (keyword) video views on Bilibili") }}</span>
                      </v-tooltip>
                    </span>
                </div>
                <BilibiliTotalView/>
              </div>
            </div>
            <div class="col-lg-4">
              <div class="chart-box" id="bilibili-total-like">
                <div class="section-header">
                  <v-img
                      src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/bilibili-logo.svg"
                      max-height="30px"
                      max-width="30px"
                      class="mr-3"
                  ></v-img>
                  <span>
                      {{ $t("Bilibili Total Likes") }}
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
                        <span>{{ $t("Number of related (keyword) video likes on Bilibili") }}</span>
                      </v-tooltip>
                    </span>
                </div>
                <BilibiliTotalLike/>
              </div>
            </div>
            <div class="col-lg-4">
              <div class="chart-box" id="bilibili-total-comment">
                <div class="section-header">
                  <v-img
                      src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/bilibili-logo.svg"
                      max-height="30px"
                      max-width="30px"
                      class="mr-3"
                  ></v-img>
                  <span>
                      {{ $t("Bilibili Total Comments") }}
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
                        <span>{{ $t("Number of related (keyword) video comments on Bilibili") }}</span>
                      </v-tooltip>
                    </span>
                </div>
                <BilibiliTotalComment/>
              </div>
            </div>
            <div class="col-lg-4">
              <div class="chart-box" id="bilibili-total-share">
                <div class="section-header">
                  <v-img
                      src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/bilibili-logo.svg"
                      max-height="30px"
                      max-width="30px"
                      class="mr-3"
                  ></v-img>
                  <span>
                      {{ $t("Bilibili Total Shares") }}
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
                        <span>{{ $t("Number of related (keyword) video shares on Bilibili") }}</span>
                      </v-tooltip>
                    </span>
                </div>
                <BilibiliTotalShare/>
              </div>
            </div>
            <div class="col-lg-4">
              <div class="chart-box" id="bilibili-total-danmu">
                <div class="section-header">
                  <v-img
                      src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/bilibili-logo.svg"
                      max-height="30px"
                      max-width="30px"
                      class="mr-3"
                  ></v-img>
                  <span>
                      {{ $t("Bilibili Total Bullet Chats") }}
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
                        <span>{{ $t("Number of related (keyword) video bullet chats on Bilibili") }}</span>
                      </v-tooltip>
                    </span>
                </div>
                <BilibiliTotalDanmu/>
              </div>
            </div>
            <div class="col-lg-4">
              <div class="chart-box" id="bilibili-total-coin">
                <div class="section-header">
                  <v-img
                      src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/bilibili-logo.svg"
                      max-height="30px"
                      max-width="30px"
                      class="mr-3"
                  ></v-img>
                  <span>
                      {{ $t("Bilibili Total Coins") }}
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
                        <span>{{ $t("Number of related (keyword) video coins on Bilibili") }}</span>
                      </v-tooltip>
                    </span>
                </div>
                <BilibiliTotalCoin/>
              </div>
            </div>
            <div class="col-lg-4">
              <div class="chart-box" id="bilibili-total-collect">
                <div class="section-header">
                  <v-img
                      src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/bilibili-logo.svg"
                      max-height="30px"
                      max-width="30px"
                      class="mr-3"
                  ></v-img>
                  <span>
                      {{ $t("Bilibili Total Collects") }}
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
                        <span>{{ $t("Number of related (keyword) video collects on Bilibili") }}</span>
                      </v-tooltip>
                    </span>
                </div>
                <BilibiliTotalCollect/>
              </div>
            </div>
            <div class="col-lg-4">
              <div class="chart-box" id="bilibili-total-engagement ">
                <div class="section-header">
                  <v-img
                      src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/bilibili-logo.svg"
                      max-height="30px"
                      max-width="30px"
                      class="mr-3"
                  ></v-img>
                  <span>
                      {{ $t("Bilibili Engagement Rate") }}
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
                        <span>{{ $t("Average engagement rate of related (keyword) videos on Bilibili") }}</span>
                      </v-tooltip>
                    </span>
                </div>
                <BilibiliTotalEngagement/>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="section-campaign">
      <div class="section-title">
        <h2>{{ $t('Featured Videos') }}</h2>
        <div class="filters">
          <v-row wrap justify="end">
            <v-col
                cols="3"
            >
              <v-select
                  :items="select_items"
                  label="Sort By"
                  dense
                  solo
                  v-model="selected_cat"
                  @input="filterSort"
                  item-color="orange darken-1"
              ></v-select>
            </v-col>
          </v-row>
        </div>
      </div>
      <div class="row">
        <div class="col-lg-3 col-md-6" v-for="(video, index) in videos"
             v-if="index < total_posts_count" :key="index">
          <div class="box">
            <div class="img">
              <div class="box-img" v-if="video.image" :style="{backgroundImage: 'url(' + video.image +')'}">
              </div>
            </div>
            <div class="box-body">
              <a v-bind:href="video.url" target="_blank">
                <div class="title">
                  <v-tooltip top color="grey lighten-4" max-width="250px">
                    <template v-slot:activator="{ on, attrs }">
                      <h4 v-bind="attrs" v-on="on">{{ video.title | truncateText }}</h4>
                    </template>
                    <span> {{ video.title }}</span>
                  </v-tooltip>
                  <span><img src="@/assets/img/calendar-icon-red.svg" alt=""/>{{ video.upload_date }}</span>
                </div>
              </a>
              <div class="infoStat">
                <ul>
                  <v-tooltip bottom color="grey lighten-4">
                    <template v-slot:activator="{ on }">
                      <li class="stat4" v-on="on">{{ video.view | formatNumber }}</li>
                    </template>
                    <span>Views: {{ (video.view).toLocaleString() }}</span>
                  </v-tooltip>
                  <v-tooltip bottom color="grey lighten-4">
                    <template v-slot:activator="{ on }">
                      <li class="stat3" v-on="on">{{ video.like | formatNumber }}</li>
                    </template>
                    <span>Likes: {{ (video.like).toLocaleString() }}</span>
                  </v-tooltip>
                  <v-tooltip bottom color="grey lighten-4">
                    <template v-slot:activator="{ on }">
                      <li class="stat5" v-on="on">{{ video.share | formatNumber }}</li>
                    </template>
                    <span>Shares: {{ (video.share).toLocaleString() }}</span>
                  </v-tooltip>
                  <v-tooltip bottom color="grey lighten-4">
                    <template v-slot:activator="{ on }">
                      <li class="stat8" v-on="on">{{ video.coin | formatNumber }}</li>
                    </template>
                    <span>Coins: {{ (video.coin).toLocaleString() }}</span>
                  </v-tooltip>
                  <v-tooltip bottom color="grey lighten-4">
                    <template v-slot:activator="{ on }">
                      <li class="stat7" v-on="on">{{ video.danmu | formatNumber }}</li>
                    </template>
                    <span>Danmus: {{ (video.danmu).toLocaleString() }}</span>
                  </v-tooltip>
                  <v-tooltip bottom color="grey lighten-4">
                    <template v-slot:activator="{ on }">
                      <li class="stat1" v-on="on">{{ video.collect | formatNumber }}</li>
                    </template>
                    <span>Collects: {{ (video.collect).toLocaleString() }}</span>
                  </v-tooltip>
                </ul>
                <span>
                  {{ (video.RowTotal / video.view * 100).toFixed(2) }}
                  <span>%</span>
                </span>
              </div>
            </div>
          </div>
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
import BilibiliTotalView from "@/components/BilibiliTotalView";
import BilibiliTotalVideo from "@/components/BilibiliTotalVideo";
import BilibiliTotalLike from "@/components/BilibiliTotalLike";
import BilibiliTotalComment from "@/components/BilibiliTotalComment";
import BilibiliTotalShare from "@/components/BilibiliTotalShare";
import BilibiliTotalDanmu from "@/components/BilibiliTotalDanmu";
import BilibiliTotalCoin from "@/components/BilibiliTotalCoin";
import BilibiliTotalCollect from "@/components/BilibiliTotalCollect";
import BilibiliTotalEngagement from "@/components/BilibiliTotalEngagement";
export default {
  name: "Bilibili",
    components: {
    BilibiliTotalEngagement,
    BilibiliTotalCollect,
    BilibiliTotalCoin,
    BilibiliTotalDanmu,
    BilibiliTotalShare, BilibiliTotalComment, BilibiliTotalLike, BilibiliTotalVideo, BilibiliTotalView},
  data() {
    return {
      page: 1,
      perPage: 20,

      //video info
      videos: [],
      sort: "",
      total_posts_count: "",
      select_items: ["Date(Default)", "Most Likes", "Most Comments", "Most Coins", "Most Collects", "Most Shares",
                     "Most Danmus", "Most Views"],
      subTotalNum: "",
      eng_rate: ""
    }
  },
  methods: {
    async getBilibiliPost() {
      const {data} = await this.axios.get('/api/bilibili/post?' + 'page=' + this.page + '&limit=' + this.perPage + '&sort=' + this.sort)
      this.page = data["page"]
      this.sort = data["sort"]
      this.total_posts_count = data["total_posts_count"]
      this.videos = data["posts"]
      // console.log(this.videos)

      let SubTotals = {};
      let columns = ['coin', 'collect', 'like', 'comment', 'share', 'danmu'];

      this.videos.forEach(b => {
        let rowTotal = 0;
        columns.forEach(i => {
          if (b[i] === undefined) {
            return;
          }

          SubTotals[i] = SubTotals[i] || 0;
          SubTotals[i] += b[i];
          rowTotal += b[i];
        })
        b.RowTotal = rowTotal;
      });

      // Calculate RowTotal for ColumnsTotals
      columns.forEach(i => {
        SubTotals.RowTotal = SubTotals.RowTotal || 0;
        SubTotals.RowTotal += SubTotals[i];
      })
      this.subTotalNum = SubTotals.RowTotal
      console.log(this.subTotalNum)
    },
    loadMore() {
      this.page++;
      if ((this.perPage * this.page) <= this.total_posts_count) {
        this.getBilibiliPost();
      }
    },
    previousPage() {
      this.page--
      if ((this.perPage * this.page) <= this.total_posts_count) {
        this.getBilibiliPost();
      }
    },
    filterSort() {
      if (this.selected_cat === 'Most Likes') {
        this.page = 1
        this.sort = 'like'
        this.getBilibiliPost();
      } else if (this.selected_cat === 'Most Comments') {
        this.page = 1
        this.sort = 'comment'
        this.getBilibiliPost();
      } else if (this.selected_cat === 'Date(Default)') {
        this.page = 1
        this.sort = 'date'
        this.getBilibiliPost();
      } else if (this.selected_cat === 'Most Shares') {
        this.page = 1
        this.sort = 'share'
        this.getBilibiliPost();
      } else if (this.selected_cat === 'Most Coins') {
        this.page = 1
        this.sort = 'coin'
        this.getBilibiliPost();
      } else if (this.selected_cat === 'Most Collects') {
        this.page = 1
        this.sort = 'collect'
        this.getBilibiliPost();
      } else if (this.selected_cat === 'Most Danmus') {
        this.page = 1
        this.sort = 'danmu'
        this.getBilibiliPost();
      } else if (this.selected_cat === 'Most Views') {
        this.page = 1
        this.sort = 'view'
        this.getBilibiliPost();
      }
    }
  },
  created() {
    this.getBilibiliPost();
    this.loadMore();
    this.previousPage();
    this.filterSort();
  },
  filters:{
    truncateText: (text) => {
      if (text.length > 8) {
        text = text.substring(0, 8) + "...";
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
  },
}
</script>
<style scoped>
.box .img {
  position: relative;
  margin: auto;
  overflow: hidden;
  width: auto;
  border-radius: 8px;
}
.box .img .box-img {
  max-width: 100%;
  transition: all 0.3s;
  display: block;
  width: 100%;
  height: auto;
  transform: scale(1);
}
.box .img .box-img:hover {
  border-radius: 8px;
  transform: scale(1.1);
}
.chart-box {
  width:100%;
  height: 100%;
  padding: 20px 10px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  -webkit-border-radius: 8px;
}
</style>