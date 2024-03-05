<template>
  <div id="instagram-most-mentioned">
    <div class="toolbar">
      <v-row justify="end">
        <v-col cols="12">
          <v-btn
              outlined
              small
              color="blue-grey lighten-1"
              dark
              rounded
              elevation="1"
              class="mr-3"
              @click="getRecentTens()"
          >
            Latest 10 Posts (Default)
          </v-btn>
          <v-btn
              outlined
              small
              color="blue-grey lighten-1"
              dark
              rounded
              elevation="1"
              class="mr-3"
              @click="getRecentThirtys()"
          >
            Latest 30 Posts
          </v-btn>
          <v-btn
              small
              outlined
              color="blue-grey lighten-1"
              dark
              rounded
              elevation="1"
              class="mr-3"
              @click="getOveralls()"
          >
            All Posts
          </v-btn>
        </v-col>
      </v-row>
    </div>
    <v-divider/>
    <div class="row">
      <div class="col-lg-6" v-for="(user, index) in TopTenUsed">
        <v-chip
            class="mr-7"
            color="deep-purple accent-2"
            v-bind:href='user.url'
            text-color="white"
        >
          <v-icon left>
            mdi-at
          </v-icon>
          {{ user.user }}
        </v-chip>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "InstagramMention",
  components: {
    apexchart: VueApexCharts,
  },
  data: function () {
    return {
      TopTenUsed: [],
      series: [],
    }
  },
  methods: {
    async getRecentTens() {
      const {data} = await this.$axios.get('/api/instagram/mentions/recent-ten-posts')
      this.TopTenUsed = data["result"]
      // console.log(this.TopTenUsed)

      // Format data correctly
      let tags = this.TopTenUsed.map((e, i) => {
        return {
          x: e.user,
          y: e.count,
        };
      });

      // update the series with axios data
      this.series = [
        {
          name: 'Counts',
          data: tags,
        }
      ];

    },
    async getRecentThirtys() {
      const {data} = await this.$axios.get('/api/instagram/mentions/recent-thirty-posts')
      this.TopTenUsed = data["result"]
      // console.log(this.TopTenUsed)

      // Format data correctly
      let tags = this.TopTenUsed.map((e, i) => {
        return {
          x: e.user,
          y: e.count,
        };
      });

      // update the series with axios data
      this.series = [
        {
          name: 'Counts',
          data: tags,
        }
      ];

    },
    async getOveralls() {
      const {data} = await this.$axios.get('/api/instagram/mentions/overall-posts')
      this.TopTenUsed = data["result"]
      // console.log(this.TopTenUsed)

      // Format data correctly
      let tags = this.TopTenUsed.map((e, i) => {
        return {
          x: e.user,
          y: e.count,
        };
      });

      // update the series with axios data
      this.series = [
        {
          name: 'Counts',
          data: tags,
        }
      ];

    },
  },
  created() {
    this.getRecentTens();
    this.getRecentThirtys();
    this.getOveralls();
  },
  mounted: //set latest 10 posts as default
      function () {
        this.getRecentTens(() => {
          this.getRecentThirtys();
          this.getOveralls();
        })
      }
}
</script>
<style scoped>
</style>