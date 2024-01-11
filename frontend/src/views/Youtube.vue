<template>
  <div class="main-content">
    <div class="section-stats">
      <div class="row align-items-center">
        <div class="col-xxl-12 col-xl-12 col-lg-12">
          <div class="row align-items-end">
            <div class="row">
              <div class="col-lg-4">
                <div class="chart-box" id="youtube-total-sub">
                  <div class="section-header">
                    <v-img
                        src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/youtube-logo.svg"
                        max-height="30px"
                        max-width="30px"
                        class="mr-3"
                    ></v-img>
                    <span>
                      {{ $t('YouTube Subscribers') }}
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
                        <span>Tooltip</span>
                      </v-tooltip>
                    </span>
                  </div>
                  <YoutubeSubscriber/>
                </div>
              </div>
              <div class="col-lg-4">
                <div class="chart-box" id="youtube-total-video">
                  <div class="section-header">
                    <v-img
                        src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/youtube-logo.svg"
                        max-height="30px"
                        max-width="30px"
                        class="mr-3"
                    ></v-img>
                    <span>
                      {{ $t('YouTube Total Channel Videos') }}
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
                        <span>Tooltip</span>
                      </v-tooltip>
                    </span>
                  </div>
                  <YoutubeTotalVideo/>
                </div>
              </div>
              <div class="col-lg-4">
                <div class="chart-box" id="youtube-total-channel-view">
                  <div class="section-header">
                    <v-img
                        src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/youtube-logo.svg"
                        max-height="30px"
                        max-width="30px"
                        class="mr-3"
                    ></v-img>
                    <span>
                      {{ $t('YouTube Total Channel Video Views') }}
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
                        <span>Tooltip</span>
                      </v-tooltip>
                    </span>
                  </div>
                  <YoutubeTotalChannelView/>
                </div>
              </div>
              <div class="col-lg-4">
                <div class="chart-box" id="youtube-total-video-view">
                  <div class="section-header">
                    <v-img
                        src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/youtube-logo.svg"
                        max-height="30px"
                        max-width="30px"
                        class="mr-3"
                    ></v-img>
                    <span>
                      {{ $t('YouTube Total Video Views') }}
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
                        <span>Tooltip</span>
                      </v-tooltip>
                    </span>
                  </div>
                  <YoutubeTotalVideoView/>
                </div>
              </div>
              <div class="col-lg-4">
                <div class="chart-box" id="youtube-total-video-like">
                  <div class="section-header">
                    <v-img
                        src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/youtube-logo.svg"
                        max-height="30px"
                        max-width="30px"
                        class="mr-3"
                    ></v-img>
                    <span>
                      {{ $t('YouTube Total Video Likes') }}
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
                        <span>Tooltip</span>
                      </v-tooltip>
                    </span>
                  </div>
                  <YoutubeTotalLike/>
                </div>
              </div>
              <div class="col-lg-4">
                <div class="chart-box" id="youtube-total-video-comment">
                  <div class="section-header">
                    <v-img
                        src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/youtube-logo.svg"
                        max-height="30px"
                        max-width="30px"
                        class="mr-3"
                    ></v-img>
                    <span>
                      {{ $t('YouTube Total Video Comments') }}
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
                        <span>Tooltip</span>
                      </v-tooltip>
                    </span>
                  </div>
                  <YoutubeTotalComment/>
                </div>
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
                        <span>Tooltip</span>
                      </v-tooltip>
                </span>
              </div>
              <div class="hash-list">
                <YoutubeMostUsedHashtag/>
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
                        <span>Tooltip</span>
                      </v-tooltip>
                </span>
              </div>
              <div class="hash-list">
                <YoutubeMostEngagedHashtag/>
              </div>
            </div>
        </div>
      </div>
    </div>
    <div class="section-overall bg-color2">
      <div class="section-title">
        <h2>Know Your Audience</h2>
      </div>
      <div class="row">
        <div class="col-lg-8 spacer">
          <div class="chart-box-2">
            <div class="section-header">
              <h3>Fan Location</h3>
            </div>
            <div class="row">
              <YoutubeCountry/>
            </div>
          </div>
        </div>
        <div class="col-lg-4 spacer">
          <div class="chart-box-2">
            <div class="section-header">
              <h3>Fan Language</h3>
            </div>
            <div class="row">
              <div class="col-12">
                <YoutubeLang/>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="section-campaign bg-color2">
      <div class="section-title">
        <h2>All Videos</h2>
      </div>
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
      <div class="row">
        <div class="col-lg-4 col-md-6" v-for="(video, index) in YTPost" :key="video.code">
          <div class="box">
            <div class="img">
              <div class="box-img" :style="{backgroundImage: 'url(' + video.image +')'}">
              </div>
            </div>
            <div class="box-body" >
              <a v-bind:href="video.url" target="_blank">
              <div class="title">
                <v-tooltip top color="grey lighten-4" max-width="250px">
                  <template v-slot:activator="{ on, attrs }">
                    <h4 v-bind="attrs" v-on="on">{{ video.title | truncateText }}</h4>
                  </template>
                  <span> {{ video.title }}</span>
                </v-tooltip>
                <span><img src="../assets/img/calendar-icon-red.svg" alt=""/>{{ video.publish_at }}</span>
              </div>
              </a>
              <div class="infoStat">
                <ul>
                  <v-tooltip top color="grey lighten-4">
                    <template v-slot:activator="{ on }">
                      <li class="stat4" v-on="on">{{ video.view_count | formatNumber }}</li>
                    </template>
                    <span>Views: {{ (video.view_count).toLocaleString() }}</span>
                  </v-tooltip>
                  <v-tooltip top color="grey lighten-4">
                    <template v-slot:activator="{ on }">
                      <li class="stat3" v-on="on">{{ video.like_count | formatNumber }}</li>
                    </template>
                    <span>Likes: {{ (video.like_count).toLocaleString() }}</span>
                  </v-tooltip>
                  <v-tooltip top color="grey lighten-4">
                    <template v-slot:activator="{ on }">
                      <li class="stat2" v-on="on">{{ video.comment_count | formatNumber }}</li>
                    </template>
                    <span>Comments: {{ (video.comment_count).toLocaleString() }}</span>
                  </v-tooltip>
                </ul>
                <span class="left_side">
                  {{ (video.eng_rate).toFixed(2) }}
                  <span>%</span>
                  <template>
                    <div v-for="comment in vd_comments" :key="comment.vid">
                      <span v-if="comment.vid === video.code" >
                        <v-row>
                          <v-col cols="12" lg="12" class="ma-0">
                            <span class="positive_label" style="font-size:14px;">
                              <img
                                  src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/happy-emoji-svgrepo-com.svg"
                                  alt="positive-img"
                                  height="20px"
                              >
                                {{ comment.pos_perc }}%
                            </span>
                            <span class="neutral_label" style="font-size:14px;">
                          <img
                              src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/confused-emoji-svgrepo-com.svg"
                              alt="neutral-img"
                              height="20px"
                          >
                          {{ comment.neu_perc }}%
                        </span>
                            <span class="negative_label" style="font-size:14px;">
                          <img
                              src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/angry-emoji-svgrepo-com.svg"
                              alt="negative-img"
                              height="20px"
                          >
                          {{ comment.neg_perc }}%
                        </span>
                          </v-col>
                        </v-row>
                      </span>
                    </div>
                  </template>
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
import YoutubeSubscriber from "@/components/YoutubeSubscriber";
import YoutubeTotalVideo from "@/components/YoutubeTotalVideo";
import YoutubeTotalChannelView from "@/components/YoutubeTotalChannelView";
import YoutubeTotalVideoView from "@/components/YoutubeTotalVideoView";
import YoutubeTotalLike from "@/components/YoutubeTotalLike";
import YoutubeTotalComment from "@/components/YoutubeTotalComment";
import YoutubeMostUsedHashtag from "@/components/YoutubeMostUsedHashtag";
import YoutubeMostEngagedHashtag from "@/components/YoutubeMostEngagedHashtag";
import YoutubeLang from "@/components/YoutubeLang";
import YoutubeCountry from "@/components/YoutubeCountry";
export default {
  name: "Youtube",
  components: {
    YoutubeCountry,
    YoutubeLang,
    YoutubeMostEngagedHashtag,
    YoutubeMostUsedHashtag,
    YoutubeTotalComment,
    YoutubeTotalLike, YoutubeTotalVideoView, YoutubeTotalChannelView, YoutubeTotalVideo, YoutubeSubscriber
  },
  data() {
    return {
      view_count: "",
      subscriber_count: "",
      video_count: "",
      index_update_time: "",
      past_view_count: "",
      past_subscriber_count: "",
      past_video_count: "",
      video_subtotal: "",
      videos: [],
      YTPost: [],
      vd_comments: [],
      drange: 10,
      page: 1,
      perPage: 12,
      selected_cat: "",
      select_items: ["Date(Default)", "Most Likes", "Most Comments", "Most Engaged", "Most Watched"],
      sort: "",
      total_posts_count: "",
    }
  },
  methods: {
    async get_youtube_post() {
      const {data} = await this.axios.get('http://localhost/api/youtube/post?' + 'page=' + this.page + '&limit=' + this.perPage + '&sort=' + this.sort)
      this.page = data["result"]["page"]
      this.sort = data["result"]["sort"]
      this.total_posts_count = data["result"]["total_posts_count"]
      this.YTPost = data["result"]["posts"]
      // console.log(this.YTPost)

      const SubTotals = {Name: SubTotals};
      const columns = ['commentCount', 'likeCount'];

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
      this.video_subtotal = SubTotals.RowTotal
      // console.log(this.video_subtotal)
    },
    async get_youtube_comment() {
      const {data} = await this.axios.get("http://localhost/api/youtube/comment?"
          + 'page=' + this.page
          + '&limit=' + this.perPage
          + '&drange=' + this.drange, {setTimeout: 10000})
      this.page = data["result"]["page"]
      this.drange = data["result"]["drange"]
      // this.total_posts = data["result"]["total_posts_count"]
      this.vd_comments = data["result"]["posts"]

      console.log(this.vd_comments)
    },
    loadMore() {
      this.page++;
      let total_page = Math.ceil(this.total_posts_count/this.perPage)
      if ((this.page) <= total_page) {
        this.get_youtube_post();
      }
    },
    previousPage() {
      this.page--;
      let total_page = Math.ceil(this.total_posts_count/this.perPage)
      if ((this.page) <= total_page) {
        this.get_youtube_post();
      }
    },
    filterSort() {
      if (this.selected_cat === 'Most Likes') {
        this.page = 1
        this.sort = 'like'
        this.get_youtube_post();
      } else if (this.selected_cat === 'Most Comments') {
        this.page = 1
        this.sort = 'comment'
        this.get_youtube_post();
      } else if (this.selected_cat === 'Date(Default)') {
        this.page = 1
        this.sort = 'date'
        this.get_youtube_post();
      } else if (this.selected_cat === 'Most Engaged') {
        this.page = 1
        this.sort = 'engaged'
        this.get_youtube_post();
      } else if (this.selected_cat === 'Most Watched') {
        this.page = 1
        this.sort = 'view'
        this.get_youtube_post();
      }
    }
  },
  created() {
    this.get_youtube_post();
    this.filterSort();
    this.loadMore();
    this.previousPage();
    this.get_youtube_comment();
  },
  filters: {
    truncateText: (text) => {
      if (text.length > 13) {
        text = text.substring(0, 13) + "...";
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
.box .box-body .info ul {
    flex: 0 0 50%;
    max-width: 35%;
    padding: 0;
    margin: 0;
    list-style: none;
}
.box .box-body .info span.left_side {
  margin-left: 50px;
}
</style>