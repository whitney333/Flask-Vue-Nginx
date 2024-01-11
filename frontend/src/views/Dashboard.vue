<template>
  <div class="main-body">
    <div class="main-content">
      <div class="section-halved">
        <div class="half-section right-border profile-section">
          <div class="section-header mb-35">
            <h3>{{ $t("Summary") }}</h3>
          </div>
          <div class="section-body">
            <div class="row">
              <div class="col-md-12">
                <div class="profile-box">
                  <v-list-item>
                    <v-avatar style="height:130px; width:130px; margin-right:15px">
                      <v-img
                          src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/artist-profile/1297-t024.webp"
                          class="img-design"
                      ></v-img>
                    </v-avatar>
                    <v-spacer/>
                    <v-list-item-content>
                      <v-list-item-title>{{ $t("Artist") }}</v-list-item-title>
                      <div class="h6 pb-3">{{ artist_info["artist"] }}</div>
                      <v-list-item-title>{{ $t("Country") }}</v-list-item-title>
                      <span class="rounded-lg">
                       <img
                           src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/flags/kr.svg"
                           alt="kr-flag"
                           height="30px"
                       >
                      </span>
                    </v-list-item-content>
                    <v-list-item-content>
                      <v-list-item-title>{{ $t("Debut Year") }}</v-list-item-title>
                      <div class="h6 pb-3" v-if="artist_info['debut_year'] != null">
                        {{ artist_info['debut_year'] }}
                      </div>
                      <div class="h6 pb-3" v-else>
                        {{ 'N/A' }}
                      </div>
                      <v-list-item-title>{{ $t("Birth") }}</v-list-item-title>
                      <div class="h6 pb-3" v-if="artist_info['birth'] != null">
                        {{ artist_info["birth"] }}
                      </div>
                      <div class="h6 pb-3" v-else>
                        {{ 'N/A' }}
                      </div>
                    </v-list-item-content>
                  </v-list-item>
                  <v-divider></v-divider>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title>{{ $t("Type") }}</v-list-item-title>
                      <div class="h6 pb-3"
                           v-if="artist_info['type'] != null"
                           v-for="(type, index) in artist_info['type']"
                      >
                        {{ type }}
                      </div>
                      <div class="h6 pb-3" v-else>
                        {{ 'N/A' }}
                      </div>
                    </v-list-item-content>
                    <v-list-item-content>
                      <v-list-item-title>{{ $t("Members") }}</v-list-item-title>
                      <span class="h6 pb-3"
                            v-for="(artist, index) in member_info"
                            :key="index"
                            v-if="member_info != null">
                        {{ artist["artist"] }}
                      </span>
                      <span class="h6 pb-3" v-else>
                        {{ 'N/A' }}
                      </span>
                    </v-list-item-content>
                  </v-list-item>
                  <v-divider></v-divider>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title>{{ $t("Label") }}</v-list-item-title>
                      <div class="h6" v-if="artist_info['labels'] != null">
                        {{ artist_info['labels'] }}
                      </div>
                      <div class="h6" v-else>
                        {{ 'N/A' }}
                      </div>
                    </v-list-item-content>
                    <v-list-item-content>
                      <v-list-item-title>{{ $t("Fandom") }}</v-list-item-title>
                      <div class="h6" v-if="artist_info['fandom'] != null">
                        {{ artist_info["fandom"] }}
                      </div>
                      <div class="h6" v-else>
                        {{ 'N/A' }}
                      </div>
                    </v-list-item-content>
                    <v-list-item-content>
                      <v-list-item-title>{{ $t("Color") }}</v-list-item-title>
                      <div class="h6" v-if="artist_info['color'] != null">
                        {{ artist_info["color"] }}
                      </div>
                      <div class="h6" v-else>
                        {{ 'N/A' }}
                      </div>
                    </v-list-item-content>
                    <v-list-item-content>
                      <v-list-item-title>{{ $t("Last Release") }}</v-list-item-title>
                      <div class="h6" v-if="artist_info['last_release'] != null">
                        {{ artist_info["last_release"] }}
                      </div>
                      <div class="h6" v-else>
                        {{ 'N/A' }}
                      </div>
                    </v-list-item-content>
                  </v-list-item>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="half-section hot-section">
          <div class="section-header mb-35">
            <h3>{{ $t("Trending") }}</h3>
          </div>
          <div class="row align-items-center">
            <div class="col-md-6">
                <div
                    class="chart-box-text-1"
                    v-if="hot_data"
                    style="height: 355px; overflow-y: scroll"
                >
                      <span
                          class="no_data"
                          v-if="!hot_data.length"
                      >
                      No relevant data in 48 hours
                      </span>
                  <ul
                      v-for="item in hot_data"
                      :key="item.title"
                  >
                    <v-list>
                      <li
                          class="font-weight-black text-left"
                      >
                        <a :href="item.url">
                          {{ item.title }}
                        </a>
                      </li>
                    </v-list>
                  </ul>
                </div>
              </div>
            <div class="col-md-6">
              <TheqooSentiment/>
            </div>
          </div>
        </div>
      </div>
      <!--  <hello-world />-->
      <div class="section-overall">
        <div class="section-title">
          <h2>Top Statistics</h2>
        </div>
        <div class="row align-items-center">
          <div class="col-md-12">
            <div
                class="card-box"
                style="width:auto; height: auto; overflow-x: scroll"
            >
              <div class="col-xl-3 col-lg-4 col-md-4">
                <v-card class="rounded-card">
                  <HPInstagramFollower/>
                </v-card>
              </div>
              <div class="col-xl-3 col-lg-4 col-md-4">
                <v-card class="rounded-card">
                  <HPSpotifyFollower/>
                </v-card>
              </div>
              <div class="col-xl-3 col-lg-4 col-md-4">
                <v-card class="rounded-card">
                  <HPSpotifyMonthlyListener/>
                </v-card>
              </div>
              <div class="col-xl-3 col-lg-4 col-md-4">
                <v-card class="rounded-card">
                  <HPTiktokFollower/>
                </v-card>
              </div>
              <div class="col-xl-3 col-lg-4 col-md-4">
                <v-card class="rounded-card">
                  <HPYoutubeSubscriber/>
                </v-card>
              </div>
              <div class="col-xl-3 col-lg-4 col-md-4">
                <v-card class="rounded-card">
                  <HPTwitterFollower/>
                </v-card>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import HelloWorld from "@/components/HelloWorld";
import HPInstagramFollower from "@/components/HPInstagramFollower";
import HPSpotifyFollower from "@/components/HPSpotifyFollower";
import HPSpotifyMonthlyListener from "@/components/HPSpotifyMonthlyListener";
import HPTiktokFollower from "@/components/HPTiktokFollower";
import HPYoutubeSubscriber from "@/components/HPYoutubeSubscriber";
import TheqooSentiment from "@/components/TheqooSentiment";
import HPTwitterFollower from "@/components/HPTwitterFollower";

export default {
  name: "Dashboard",
  components: {
    HPTwitterFollower,
    TheqooSentiment,
    HPYoutubeSubscriber,
    HPTiktokFollower,
    HPSpotifyMonthlyListener,
    HPSpotifyFollower,
    HPInstagramFollower,
      HelloWorld,
  },
  data() {
    return {
      artist_info: "",
      member_info: "",
      hot_data: [],
      page: 1,
      limit: 10,
      q: "뉴진스"
    }
  },
  methods: {
    async getArtistInfo() {
      await this.axios.get("http://localhost/api/artist/info",
          {setTimeout: 10000})
      .then(res => {
        this.artist_info = res.data[0]
        // console.log(this.artist_info['artist'])
      })
      .catch(err => {
        console.log(err);
      })
    },
    async getMemberInfo() {
      await this.axios.get("http://localhost/api/artist/members",
          {setTimeout: 10000})
      .then(res => {
        this.member_info = res.data["result"]
        console.log(this.member_info)
      })
      .catch(err => {
        console.log(err);
      })
    },
    async getTheQoo() {
      await this.axios.get("http://localhost/api/theqoo/hot?page=" + this.page +
          "&limit=" + this.limit + "&q=" + this.q, {setTimeout: 10000})
      .then(res => {
        this.hot_data = res.data["posts"]
        console.log(this.hot_data)
      })
      .catch(err => {
        console.log(err)
      })
    }
  },
  created() {
    this.getArtistInfo();
    this.getMemberInfo();
    this.getTheQoo();
  }
}
</script>
<style scoped>
.profile-box {
  height: auto;
  width: 100%;
  padding: 10px 20px;
/*text-align: center;*/
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  -webkit-border-radius: 8px
}
.profile-box p{
  color: #767676;
  font-size: 13px;
  font-weight: 500;
  margin: 0;
  padding-top: 5px;
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
.top-stat-box {
  width:100%;
  height: 100%;
  padding: 5px 5px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  -webkit-border-radius: 8px;
}
.half-section.hot-section ul {
  border-top: 1px solid #ddd;
  padding: 0 10px;
  margin-top: 4px;
  list-style: none;
  display: flex;
  flex-direction: row;
  align-items: center
}
.card-box {
  display: flex;
}
.rounded-card {
  border-radius: 25px;
}
.rounded-card:hover {
  box-shadow: 0 0 11px rgba(33,33,33,.2);
}
</style>