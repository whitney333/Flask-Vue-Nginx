<template>
  <v-data-table
      :headers="headers"
      :items="campaigns_list"
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
</template>
<script>

export default {
  name: "CampaignReport",
  data() {
    return {
      headers: [
        { text: 'Date',
          value: 'POST_DATE.date',
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
          width: '3%'
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
          width: '3%'
        }
      ],
      packages: [],
      campaigns_list: [],
      search: "",
      mid: "1297",
      props: {
        campaignId: {
          type: String,
          required: true
        }
      },
    }
  },
  methods: {
    async get_campaign_package() {
      await this.axios.get("http://localhost/api/campaign?"
          + "mid=" + this.mid
          + "&cid=" + this.campaignId,
          {setTimeout: 10000})
        .then(res => {
          this.packages = res.data["results"]["posts"]
          // console.log(this.packages)
          this.packages.forEach((package_) => {
            package_.forEach((campaign) => {
              this.campaigns_list.push(campaign)
            })
          })
          console.log(this.campaigns_list)
          console.log(typeof(this.campaigns_list))
        })
        .catch(err => {
          console.log(err)
        })
    },
    filterText(value, search, item) {
      return value != null &&
          search != null &&
          search.toString().toLocaleLowerCase() &&
          typeof value === 'string' &&
          value.toString().toLocaleLowerCase().indexOf(search) !== -1
    },
  },
  created() {
    this.get_campaign_package();
    this.filterText();
  },
}
</script>
<style scoped>
</style>