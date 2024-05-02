<template>
  <div class="main-body">
    <div class="main-content">
      <div class="section-stats">
        <div class="row align-items-center">
          <div class="col-xxl-12 col-xl-12 col-lg-12">
            <!-- Instagram Basic Numbers -->
            <div class="row">
              <div class="col-lg-4">
                <div class="chart-box" id="instagram-total-follower">
                  <div class="section-header">
                    <v-img
                        src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/instagram-logo.svg"
                        max-height="30px"
                        max-width="30px"
                        class="mr-3"
                    ></v-img>
                    <span>
                      {{ $t('Instagram Follower') }}
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
                        <span>{{ $t("Number of followers on Instagram") }}</span>
                      </v-tooltip>
                    </span>
                  </div>
                  <InstagramFollower/>
                </div>
              </div>
              <div class="col-lg-4">
                <div class="chart-box" id="instagram-threads-follower">
                  <div class="section-header">
                    <v-img
                        src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/instagram-logo.svg"
                        max-height="30px"
                        max-width="30px"
                        class="mr-3"
                    ></v-img>
                    <span>
                      {{ $t('Instagram Threads Follower') }}
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
                        <span>{{ $t("Number of followers on Instagram Threads") }}</span>
                      </v-tooltip>
                    </span>
                  </div>
                  <InstagramThreadsFollower/>
                </div>
              </div>
              <div class="col-lg-4">
                <div class="chart-box" id="instagram-total-post">
                  <div class="section-header">
                    <v-img
                        src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/instagram-logo.svg"
                        max-height="30px"
                        max-width="30px"
                        class="mr-3"
                    ></v-img>
                    <span>
                      {{ $t('Instagram Posts') }}
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
                        <span>{{ $t("Number of posts on Instagram") }}</span>
                      </v-tooltip>
                    </span>
                  </div>
                  <InstagramTotalPost/>
                </div>
              </div>
              <div class="col-lg-4">
                <div class="chart-box" id="instagram-total-like">
                  <div class="section-header">
                    <v-img
                        src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/instagram-logo.svg"
                        max-height="30px"
                        max-width="30px"
                        class="mr-3"
                    ></v-img>
                    <span>
                      {{ $t('Instagram Likes') }}
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
                        <span>{{ $t("Number of likes on Instagram") }}</span>
                      </v-tooltip>
                    </span>
                  </div>
                  <InstagramTotalLike/>
                </div>
              </div>
              <div class="col-lg-4">
                <div class="chart-box" id="instagram-total-comment">
                  <div class="section-header">
                    <v-img
                        src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/instagram-logo.svg"
                        max-height="30px"
                        max-width="30px"
                        class="mr-3"
                    ></v-img>
                    <span>
                      {{ $t('Instagram Comments') }}
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
                        <span>{{ $t("Number of comments on Instagram") }}</span>
                      </v-tooltip>
                    </span>
                  </div>
                  <InstagramTotalComment/>
                </div>
              </div>
              <div class="col-lg-4">
                <div class="chart-box" id="instagram-total-er">
                  <div class="section-header">
                    <v-img
                        src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/instagram-logo.svg"
                        max-height="30px"
                        max-width="30px"
                        class="mr-3"
                    ></v-img>
                    <span>
                      {{ $t('Instagram Engagement Rate') }}
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
                        <span>{{ $t("Average engagement rate of Instagram posts") }}</span>
                      </v-tooltip>
                    </span>
                  </div>
                  <InstagramTotalEngagement/>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!--TODO-->
      <!-- Instagram Audience Demographic -->
      <!-- public API: ?__a=1&__d=dis fail    -->
<!--      <div class="section-overall">-->
<!--        <div class="section-title">-->
<!--          <h2>Know Your Audience</h2>-->
<!--        </div>-->
<!--        <div class="row">-->
<!--          <div class="col-lg-4 spacer">-->
<!--            <div class="chart-box-2">-->
<!--              <div class="section-header">-->
<!--                <h3>Gender</h3>-->
<!--                <button class="dots"></button>-->
<!--              </div>-->
<!--              <div class="chart">-->
<!--                <img src="../assets/img/chart08.svg" alt=""/>-->
<!--              </div>-->
<!--            </div>-->
<!--          </div>-->
<!--          <div class="col-lg-8 spacer">-->
<!--            <div class="chart-box-2">-->
<!--              <div class="section-header">-->
<!--                <h3>Gender by Age</h3>-->
<!--                <button class="dots"></button>-->
<!--              </div>-->
<!--              <div class="chart">-->
<!--                <span><img src="../assets/img/chart09.svg" alt=""/></span>-->
<!--              </div>-->
<!--            </div>-->
<!--          </div>-->
<!--        </div>-->
<!--        <div class="row">-->
<!--          <div class="col-lg-8 spacer">-->
<!--            <div class="chart-box-2">-->
<!--              <div class="section-header">-->
<!--                <h3>Fan Location</h3>-->
<!--                <button class="dots"></button>-->
<!--              </div>-->
<!--              <div class="row">-->
<!--                <div class="col-md-6">-->
<!--                  <div class="listing-title">-->
<!--                    <h5>Top Countries</h5>-->
<!--                    <a href="#">View more</a>-->
<!--                  </div>-->
<!--                  <div class="listing-block">-->
<!--                    <p><img src="../assets/img/indonesia-flag.svg" alt=""/>Indonesia</p>-->
<!--                    <span>21.11%</span>-->
<!--                    <div class="percent-bar">-->
<!--                      <div class="percent-value green" style="width: 21.11%;"></div>-->
<!--                    </div>-->
<!--                  </div>-->
<!--                  <div class="listing-block">-->
<!--                    <p><img src="../assets/img/south-korea-flag.svg" alt=""/>South Korea</p>-->
<!--                    <span>11.44%</span>-->
<!--                    <div class="percent-bar">-->
<!--                      <div class="percent-value green" style="width: 11.44%;"></div>-->
<!--                    </div>-->
<!--                  </div>-->
<!--                  <div class="listing-block">-->
<!--                    <p><img src="../assets/img/philippines-flag.svg" alt=""/>Philippines</p>-->
<!--                    <span>8.91%</span>-->
<!--                    <div class="percent-bar">-->
<!--                      <div class="percent-value green" style="width: 8.91%;"></div>-->
<!--                    </div>-->
<!--                  </div>-->
<!--                  <div class="listing-block">-->
<!--                    <p><img src="../assets/img/united-states-of-america-flag.svg" alt=""/>United States</p>-->
<!--                    <span>6.80%</span>-->
<!--                    <div class="percent-bar">-->
<!--                      <div class="percent-value green" style="width: 6.80%;"></div>-->
<!--                    </div>-->
<!--                  </div>-->
<!--                </div>-->
<!--                <div class="col-md-6">-->
<!--                  <div class="listing-title">-->
<!--                    <h5>Top Cities</h5>-->
<!--                    <a href="#">View more</a>-->
<!--                  </div>-->
<!--                  <div class="listing-block">-->
<!--                    <p><img src="../assets/img/south-korea-flag.svg" alt=""/>Seoul</p>-->
<!--                    <span>5.98%</span>-->
<!--                    <div class="percent-bar">-->
<!--                      <div class="percent-value orange" style="width: 21.11%;"></div>-->
<!--                    </div>-->
<!--                  </div>-->
<!--                  <div class="listing-block">-->
<!--                    <p><img src="../assets/img/indonesia-flag.svg" alt=""/>Jakarta</p>-->
<!--                    <span>2.46%</span>-->
<!--                    <div class="percent-bar">-->
<!--                      <div class="percent-value orange" style="width: 2.46%;"></div>-->
<!--                    </div>-->
<!--                  </div>-->
<!--                  <div class="listing-block">-->
<!--                    <p><img src="../assets/img/thailand-flag.svg" alt=""/>Bangkok</p>-->
<!--                    <span>1.61%</span>-->
<!--                    <div class="percent-bar">-->
<!--                      <div class="percent-value orange" style="width: 1.61%;"></div>-->
<!--                    </div>-->
<!--                  </div>-->
<!--                  <div class="listing-block">-->
<!--                    <p><img src="../assets/img/japan-flag.svg" alt=""/>Tokyo</p>-->
<!--                    <span>1.06%</span>-->
<!--                    <div class="percent-bar">-->
<!--                      <div class="percent-value orange" style="width: 1.06%;"></div>-->
<!--                    </div>-->
<!--                  </div>-->
<!--                </div>-->
<!--              </div>-->
<!--            </div>-->
<!--          </div>-->
<!--          <div class="col-lg-4 spacer">-->
<!--            <div class="chart-box-2">-->
<!--              <div class="section-header">-->
<!--                <h3>Fan Language</h3>-->
<!--                <button class="dots"></button>-->
<!--              </div>-->
<!--              <div class="row">-->
<!--                <div class="col-12">-->
<!--                  <div class="listing-title placeholder">-->
<!--                  </div>-->
<!--                  <div class="listing-block">-->
<!--                    <p>English</p>-->
<!--                    <span>42.20%</span>-->
<!--                    <div class="percent-bar">-->
<!--                      <div class="percent-value teal" style="width: 42.20%;"></div>-->
<!--                    </div>-->
<!--                  </div>-->
<!--                  <div class="listing-block">-->
<!--                    <p>Indonesian</p>-->
<!--                    <span>8.85%</span>-->
<!--                    <div class="percent-bar">-->
<!--                      <div class="percent-value teal" style="width: 8.85%;"></div>-->
<!--                    </div>-->
<!--                  </div>-->
<!--                  <div class="listing-block">-->
<!--                    <p>Spanish</p>-->
<!--                    <span>8.01%</span>-->
<!--                    <div class="percent-bar">-->
<!--                      <div class="percent-value teal" style="width: 8.01%;"></div>-->
<!--                    </div>-->
<!--                  </div>-->
<!--                  <div class="listing-block">-->
<!--                    <p>Korean</p>-->
<!--                    <span>7.70%</span>-->
<!--                    <div class="percent-bar">-->
<!--                      <div class="percent-value teal" style="width: 7.70%;"></div>-->
<!--                    </div>-->
<!--                  </div>-->
<!--                </div>-->
<!--              </div>-->
<!--            </div>-->
<!--          </div>-->
<!--        </div>-->
<!--      </div>-->
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
                <InstagramMostUsedHashtag/>
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
                <InstagramMostEngagedHashtag/>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- post categories analytics -->
      <div class="section-category">
        <div class="section-title">
          <h2>{{ $t('Topic Analytics') }}</h2>
        </div>
        <div class="row">
<!--          <div class="col-lg-6 spacer">-->
<!--            <div class="chart-box-2">-->
<!--              <div class="section-header">-->
<!--                <v-img-->
<!--                    src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/hashtag.svg"-->
<!--                    max-height="30px"-->
<!--                    max-width="30px"-->
<!--                    class="mr-3"-->
<!--                ></v-img>-->
<!--                <span>-->
<!--                {{ $t('Post Categories(%)') }}-->
<!--                  <v-tooltip bottom color="grey lighten-4">-->
<!--                <template v-slot:activator="{ on, attrs }">-->
<!--                  <v-icon-->
<!--                      color="primary"-->
<!--                      v-bind="attrs"-->
<!--                      v-on="on"-->
<!--                  >-->
<!--                    mdi-information-outline-->
<!--                  </v-icon>-->
<!--                </template>-->
<!--                <span></span>-->
<!--              </v-tooltip>-->
<!--                </span>-->
<!--              </div>-->
<!--              <div class="hash-list">-->
<!--                <CategoryPercentage/>-->
<!--              </div>-->
<!--            </div>-->
<!--          </div>-->
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
                {{ $t('Engagement Rate by Categories') }}
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
                <span></span>
              </v-tooltip>
                </span>
              </div>
              <div class="hash-list">
                <CategoryBar/>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="section-latest-posts">
        <div class="section-title">
          <h2>{{ $t('All Posts') }}</h2>
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
        <!--TODO Add Loading skeleton-->
<!--          <div class="col-xl-3 col-lg-6 col-md-6" v-if="!InstaPost.length">-->
<!--            <v-skeleton-loader-->
<!--                type="image, list-item-two-line"-->
<!--            >-->
<!--            </v-skeleton-loader>-->
<!--          </div>-->
          <div class="col-xl-3 col-lg-6 col-md-6" v-for="(post, index) in InstaPost"
               v-if="index < total_posts_count" :key="index">
            <a v-bind:href="post.url" target="_blank">
              <div class="box2" :style="{backgroundImage: 'url(' + post.image +')'}">
                <div class="box-body">
                  <div class="infoStat">
                    <ul>
                      <v-tooltip top color="grey lighten-4">
                        <template v-slot:activator="{ on }">
                          <li class="stat3" v-on="on">{{ post.like_count | formatNumber }}</li>
                        </template>
                        <span>{{ $t('Likes') }}: {{ (post.like_count).toLocaleString() }}</span>
                      </v-tooltip>
                      <v-tooltip bottom color="grey lighten-4">
                        <template v-slot:activator="{ on }">
                          <li class="stat2" v-on="on">{{ post.comment_count | formatNumber }}</li>
                        </template>
                        <span>{{ $t('Comments') }}: {{ (post.comment_count).toLocaleString() }}</span>
                      </v-tooltip>
                    </ul>
                    <div class="right-side">
                      <span class="num">{{ (post.RowTotal / current_follower * 100).toFixed(2) }}%</span>
                      <span class="date">{{ post.post_date }}</span>
                    </div>
                  </div>
                </div>
                <div class="box-overlay pa-4">
                  <v-chip-group column>
                      <div class="text-post-category"
                           v-for='(category, index) in post["cat"]'>
                        <v-chip
                            color="blue lighten-4"
                            class="mr-3"
                        >
                          {{ category }}
                        </v-chip>
                      </div>

                  </v-chip-group>
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
  </div>
</template>
<script>
import InstagramFollower from "@/components/InstagramFollower";
import InstagramTotalPost from "@/components/InstagramTotalPost";
import InstagramTotalLike from "@/components/InstagramTotalLike";
import InstagramTotalComment from "@/components/InstagramTotalComment";
import InstagramTotalEngagement from "@/components/InstagramTotalEngagement";
import InstagramMostUsedHashtag from "@/components/InstagramMostUsedHashtag";
import InstagramMostEngagedHashtag from "@/components/InstagramMostEngagedHashtag";
import InstagramThreadsFollower from "@/components/InstagramThreadsFollower";
import CategoryPercentage from "@/components/CategoryPercentage";
import CategoryBar from "@/components/CategoryBar";
// import InstagramMention from "@/components/InstagramMention";

export default {
  name: "Instagram",
  components: {
    CategoryBar,
    CategoryPercentage,
    InstagramThreadsFollower,
    InstagramMostEngagedHashtag,
    InstagramMostUsedHashtag,
    InstagramTotalEngagement,
    InstagramTotalComment, InstagramTotalLike,
    InstagramTotalPost, InstagramFollower},
    data() {
    return {
      InstaPost: [],
      overlay: false,
      page: 1,
      perPage: 16,
      sort: "",
      selected_cat: "",
      allLoaded: false,
      total_posts_count: "",
      subTotalNum: "",
      current_follower: "",
      past_follower: "",
      current_media: "",
      past_media: "",
      update_date: "",
      select_items: ["Date(Default)", "Most Likes",
                    "Most Comments", "Most Engaged"],
    }
  },
  methods: {
    async getInstaPost() {
      const {data} = await this.axios.get('/api/instagram/post?' + 'page=' + this.page + '&limit=' + this.perPage + '&sort=' + this.sort)
      this.page = data["result"]["page"]
      this.sort = data["result"]["sort"]
      this.total_posts_count = data["result"]["total_posts_count"]
      this.InstaPost = data["result"]["posts"]
      // console.log(this.sort)
      //calculate subtotals
      const SubTotals = {};
      const columns = ['comment_count', 'like_count'];

      this.InstaPost.forEach(b => {
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
      // console.log(this.subTotalNum)
    },
    async getIndex() {
      const {data} = await this.axios.get("/api/instagram/index")
      this.current_follower = data["result"][0]["follower_count"]
      this.past_follower = data["result"][6]["follower_count"]
      this.current_media = data["result"][0]["media_count"]
      this.past_media = data["result"][6]["media_count"]
      this.update_date = data["result"][0]["date"]
      // console.log(this.current_follower)
    },
    loadMore() {
      this.page++;
      let total_page = Math.ceil(this.total_posts_count/this.perPage)
      // console.log(total_page)
      if ((this.page) <= total_page) {
        this.getInstaPost();
      }
    },
    previousPage() {
      this.page--
      let total_page = Math.ceil(this.total_posts_count/this.perPage)
      if ((this.page) <= total_page) {
        this.getInstaPost();
      }
    },
    filterSort() {
      if (this.selected_cat === 'Most Likes') {
        this.page = 1
        this.sort = 'like'
        this.getInstaPost();
      } else if (this.selected_cat === 'Most Comments') {
        this.page = 1
        this.sort = 'comment'
        this.getInstaPost();
      } else if (this.selected_cat === 'Date(Default)') {
        this.page = 1
        this.sort = 'date'
        this.getInstaPost();
      } else if (this.selected_cat === 'Most Engaged') {
        this.page = 1
        this.sort = 'engaged'
        this.getInstaPost();
      }
    },
  },
  created() {
    this.getInstaPost();
    this.getIndex();
    this.loadMore();
    this.previousPage();
    this.filterSort();
  },
  filters: {
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
.chart-box {
  width:100%;
  height: 100%;
  padding: 20px 10px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  -webkit-border-radius: 8px;
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
  padding-bottom: 20%;
}

.index-box .stat span {
  display: inline-block;
  font-size: 24px;
  font-weight: 700;
  white-space: nowrap;
  padding-top: 10%;
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
.box2:hover .box-overlay {
  opacity: 1;
  background-color: rgba(0,0,0,.5);
  border-radius:6px;
  -webkit-border-radius:6px;
  padding:15px
}
.box-overlay {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  height: 100%;
  width: 100%;
  opacity: 0;
  transition: .5s ease;
  background-color: rgba(0,0,0,.5);
}
.text-post-category {
  font-weight: bold;
  font-family: 'Cairo', sans-serif;
  margin-bottom: -1rem;
  color: white;
  font-size: 20px;
  position: relative;
  top: 70%;
  left: 50%;
  transform: translate(-50%, -50%);
  -ms-transform: translate(-50%, -50%);
  text-align: center;
}
/*.button {*/
/*  color: white;*/
/*  font-size: 20px;*/
/*  font-weight: 700;*/
/*  background-color: #ffa2a2;*/
/*  border: none;*/
/*  padding: 14px 28px;*/
/*  border-radius: 22px;*/
/*  cursor: pointer;*/
/*}*/
/*.button:hover {*/
/*  background-color: #fdadad;*/
/*}*/
/*.button:focus {*/
/*  outline: none;*/
/*}*/
/*.button:active {*/
/*  background-color: #ef8c8c;*/
/*}*/
</style>