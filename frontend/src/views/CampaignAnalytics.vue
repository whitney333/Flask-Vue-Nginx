<template>
  <div class="main-body">
    <div class="main-content">
      <div class="section-overall">
        <div class="section-title">
          <h2>Report</h2>
        </div>
        <div class="row align-items-center">
          <div class="col-lg-4 col-md-3"
               v-for="(campaign, index) in campaigns"
          >
            <v-dialog
                transition="dialog-bottom-transition"
                max-width="1080"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-card>
                  <v-card-text>
                    <p>Begin at: {{ campaign["start_date"] }}</p>
                    <h6>Target Region:</h6>
                    <p class="text-h6 text--primary"
                       v-for='(region, index) in campaign["region"]'>
                      <span class="resp-list">
                        {{ addComma(campaign["region"], region, index) }}
                      </span>
                    </p>
                    <h6>Target Language:</h6>
                    <p class="text-h6 text--primary"
                       v-for='(lang, index) in campaign["language"]'>
                      <span class="resp-list">
                        {{ addComma(campaign["language"], lang, index) }}&nbsp;
                      </span>
                    </p>
                    <h6>Cost:</h6>
                    <p class="text-h6 text--primary">
                      {{ campaign["budget"] }}&nbsp;
                    </p>
                    <h6>Total Reach:</h6>
                    <p class="text-h6 text--primary">
                      {{ (campaign["total_reach"]).toLocaleString() }}&nbsp;
                    </p>
                  </v-card-text>
                  <v-btn
                      block
                      text
                      color="teal accent-4"
                      v-bind="attrs"
                      v-on="on"
                      @click="sendCid(campaign.cid)"
                  >
                    Explore
                  </v-btn>
                </v-card>
              </template>
              <!-- Dialog popup -->
              <template v-slot:default="dialog">
                <v-card>
                  <v-toolbar
                      color="deep-purple darken-1"
                      dark
                  >
                    <p>Campaign ID: {{ campaign["cid"] }}</p>
                  </v-toolbar>
                  <v-data-table
                      :headers="headers"
                      :items="packages"
                      :items-per-page=5
                      :search="search"
                      class="elevation-1"
                  >
                    <template v-slot:top>
                      <v-row class="align-center">
                        <v-col cols="12" lg="4">
                          <v-list-item>
                            <v-list-item-content>
                              <v-text-field
                                  outlined
                                  dense
                                  v-model="search"
                                  label="Search..."
                              ></v-text-field>
                            </v-list-item-content>
                            <v-spacer/>
                          </v-list-item>
                        </v-col>
                      </v-row>
                    </template>
                  </v-data-table>
                  <v-card-actions class="justify-end">
                    <v-btn
                        text
                        @click="dialog.value = false"
                    >Close
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </template>
            </v-dialog>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
// import CampaignReport from "@/components/CampaignReport";
export default {
  name: "CampaignAnalytics",
  data() {
    return {
      mid: "1297",
      campaigns: [],
      headers: [
        { text: 'Date',
          value: 'POST_DATE',
          width: '5%'
        },
        {
          text: 'Account',
          align: 'start',
          sortable: true,
          value: 'ACCOUNT_NAME',
          width: '5%',
        },
        { text: 'Platform',
          value: 'PLATFORM',
          width: '6%'
        },
        { text: 'Follower',
          value: 'FOLLOWER',
          width: '3%',
          formatter: this.formatterEx
        },
        { text: 'Region',
          align: 'start',
          value: 'REGION',
          width: '3%'
        },
        { text: 'Language',
          value: 'LANGUAGE',
          width: '3%'
        },
        { text: 'Likes',
          value: 'LIKES',
          width: '3%'
        },
        { text: 'Comments',
          value: 'COMMENTS',
          width: '2%'
        }
      ],
      packages: [],
      search: "",
    }
  },
  methods: {
   async get_campaign_package() {
      await this.axios.get("/api/artist/campaign",
          {setTimeout: 10000})
        .then(res => {
          this.campaigns = res.data["result"]
          // this.mid = res.data["result"]
          // console.log(this.campaigns)
        })
        .catch(err => {
          console.log(err)
        })
    },
    async sendCid(cid) {
     this.cid = cid;
     console.log(this.cid)
     await this.axios.get("/api/campaign?"
         + "mid=" + this.mid
         + "&cid=" + cid,
         {setTimeout: 10000})
         .then(res => {
           this.packages = res.data["results"]["posts"]
           console.log(this.packages)
           // this.packages.forEach((package_) => {
           //   package_.forEach((campaign) => {
           //     this.campaigns_list.push(campaign)
           //   })
           // })
           // console.log(this.campaigns_list)
           // console.log(typeof(this.campaigns_list))
         })
         .catch(err => {
           console.log(err)
         })
   },
    addComma(result, val, idx) {
     if(idx < result.length - 1) {
       return val + ","
     }
     return val
    },
  },
  created() {
    this.get_campaign_package();
    this.sendCid();
    this.addComma();
  }
}
</script>
<style scoped>
p.text-h6.text--primary {
  display: inline-block;
  padding-right: 5px;
}
</style>
