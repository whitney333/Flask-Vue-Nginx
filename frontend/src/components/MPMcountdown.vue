<template>
  <div class="data-table">
    <v-data-table
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
                        @click="get_mcountdown()"
                        class="mb-3 mr-3"
                    >{{ $t("Send") }} <i class="mdi mdi-send" aria-hidden="true"></i>
                    </v-btn>
                    <toCsv
                        :json-data="chart"
                        :csv-title="year + '-' + 'W' + week + '-' + 'Mcountdown'"
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
  name: "MPMcountdown",
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
          text: 'Artist',
          value: 'artist',
          align: 'start',
          width: 150
        },
        {
          text: 'Song',
          value: 'title',
          align: 'start',
          width: 200
        },
        {
          text: 'Total Score',
          value: 'totalScore',
          align: 'start',
          width: 100
        },
        {
          text: 'Sound Score',
          value: 'soundScore',
          align: 'start',
          width: 100
        },
        {
          text: 'Album Score',
          value: 'albumScore',
          align: 'start',
          width: 100
        },
        {
          text: 'SNS Score',
          value: 'globalSNS',
          align: 'start',
          width: 100
        },
        {
          text: 'Global Vote Score',
          value: 'globalVote',
          align: 'start',
          width: 100
        },
        {
          text: 'Broadcast Score',
          value: 'broadcastScore',
          align: 'start',
          width: 100
        },
        {
          text: 'Live Vote Score',
          value: 'liveVote',
          align: 'start',
          width: 100
        }
      ],
      year_list: ["2022", "2023", "2024"],
      week_list: [
        "Week 1", "Week 2", "Week 3", "Week 4", "Week 5", "Week 6", "Week 7", "Week 8", "Week 9", "Week 10",
        "Week 11", "Week 12", "Week 13", "Week 14", "Week 15", "Week 16", "Week 17", "Week 18", "Week 19", "Week 20",
        "Week 21", "Week 22", "Week 23", "Week 24", "Week 25", "Week 26", "Week 27", "Week 28", "Week 29", "Week 30",
        "Week 31", "Week 32", "Week 33", "Week 34", "Week 35", "Week 36", "Week 37", "Week 38", "Week 39", "Week 40",
        "Week 41", "Week 42", "Week 43", "Week 44", "Week 45", "Week 46", "Week 47", "Week 48", "Week 49", "Week 50",
        "Week 51", "Week 52", "Week 53"
      ],
      selected_year: "",
      selected_week: ""
    }
  },
  methods: {
    async get_default() {
      this.year = new Date().getFullYear()
      var currentDate = new Date();
      var startDate = new Date(currentDate.getFullYear(), 0, 1);
      var days = Math.floor((currentDate - startDate) / (24 * 60 * 60 * 1000));

      this.weekNumber = (Math.ceil(days / 7)) - 2;
      await this.axios.get("http://localhost/api/music-broadcast/mcountdown/chart?"
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
    async get_mcountdown() {
      this.param = this.selected_week.split(" ")[1]
      await this.axios.get("http://localhost/api/music-broadcast/mcountdown/chart?"
        + "year=" + this.selected_year
        + "&week=" + this.param, {setTimeout: 10000})
      .then(res => {
        this.chart = res.data['result']
        this.week = res.data['result'][0]['week']
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
    this.get_mcountdown();
    this.filterText();
  }
}
</script>
<style scoped>
</style>