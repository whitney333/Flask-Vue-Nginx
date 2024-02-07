<template>
  <div class="data-table">
    <v-data-table
        dense
        :headers="headers"
        :items="chart"
        item-key="artist"
        :custom-filter="filterText"
        items-per-page="5"
        :search="search"
    >
     <template v-slot:top>
        <v-row class="align-center ">
          <v-col cols="12" lg="4">
            <v-list-item>
              <v-list-item-content>
                <v-text-field
                    solo
                    filled
                    dense
                    v-model="search"
                    label="Search..."
                ></v-text-field>
              </v-list-item-content>
              <v-spacer/>
            </v-list-item>
          </v-col>
          <v-col cols="12" lg="8">
            <v-list-item>
              <v-list-item-content class="mr-3">
                <v-select
                    :items="year_list"
                    label="Year"
                    dense
                    filled
                    solo
                    v-model="selected_year"
                    item-color="orange darken-1"
                ></v-select>
              </v-list-item-content>
              <v-list-item-content class="mr-3">
                <v-select
                    :items="week_list"
                    solo
                    label="Week"
                    dense
                    filled
                    v-model="selected_week"
                    item-color="orange darken-1"
                ></v-select>
              </v-list-item-content>
              <v-list-item-content class="mr-3">
                <v-row>
                  <v-col cols="12" lg="12">
                    <v-btn
                        dark
                        outlined
                        small
                        color="deep-purple darken-1"
                        @click="get_data()"
                        class="mb-3 mr-3"
                    >{{ $t("Send") }} <i class="mdi mdi-send" aria-hidden="true"></i>
                    </v-btn>
                    <toCsv
                        :json-data="chart"
                        :csv-title="year + '-' + 'W' + week + '-' + 'Digital-Charts'"
                    >
                      <v-btn class="mb-3"
                             dark
                             small
                             color="deep-purple darken-1">
                        CSV {{ $t('Export') }} <i class="mdi mdi-file-export" aria-hidden="true"></i>
                      </v-btn>
                    </toCsv>
                  </v-col>
                </v-row>
              </v-list-item-content>
            </v-list-item>
          </v-col>
        </v-row>
      </template>
    </v-data-table>
  </div>
</template>
<script>
import VueJsonToCsv from "vue-json-to-csv";
export default {
  name: "MPTheShow",
  components: {
    toCsv: VueJsonToCsv
  },
  data() {
    return {
      chart: [],
      week: "",
      search: "",
      headers: [
        {
          text: 'Rank',
          value: 'rank',
          align: 'start',
          width: '1%'
        },
        {
          text: 'Artist',
          value: 'artist',
          align: 'start',
          width: '5%'
        },
        {
          text: 'Song',
          value: 'song',
          align: 'start',
          width: '15%'
        },
        {
          text: 'Total Score',
          value: 'total_score',
          align: 'start',
          width: '1%'
        }
      ]
    }
  },
  methods: {
    async get_default() {
      this.year = new Date().getFullYear()
      var currentDate = new Date();
      var startDate = new Date(currentDate.getFullYear(), 0, 1);
      var days = Math.floor((currentDate - startDate) / (24 * 60 * 60 * 1000));

      this.weekNumber = (Math.ceil(days / 7)) - 2;
      await this.axios.get("/api/music-broadcast/show-champion/chart?"
        + "year=" + this.year
        + "&week=" + this.weekNumber, {setTimeout: 10000})
      .then(res => {
        this.chart = res.data['result']
        this.week = res.data['result'][0]['week']
      })
      .catch(err => {
        console.log(err)
      })
    },
    async get_theshow() {
      this.param = this.selected_week.split(" ")[1]
      await this.axios.get("/api/music-broadcast/show-champion/chart?"
        + "year=" + this.selected_year
        + "&week=" + this.param, {setTimeout: 10000})
      .then(res => {
        this.chart = res.data['result']
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
    this.get_default();
    this.get_theshow();
    this.filterText();
  }
}
</script>
<style scoped>
</style>