<template>
  <v-data-table
      :headers="headers"
      :items="chart"
      item-key="song"
      :items-per-page=5
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
                        :csv-title="year + '-' + 'W' + week_param + '-' + 'Digital-Charts'"
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
    <template v-slot:item.rank_change="{ item }">
      <v-chip
          :color="getColor(item.rank_change)"
          dark
          small
      >
        {{ item.rank_change }}
      </v-chip>
    </template>
  </v-data-table>
</template>
<script>
import VueJsonToCsv from "vue-json-to-csv";

export default {
  name: "WeekChartMelon",
  components: {
    toCsv: VueJsonToCsv
  },
  data: function () {
    return {
      chart: [],
      date: "",
      year: "",
      weekNumber: "",
      week_param: "",
      platform: 'melon',
      param: "",
      search: "",
      headers: [
        {
          text: 'Rank',
          value: 'rank',
          align: 'start',
          width: 80
        },
        {
          text: 'Rank Change',
          value: 'rank_change',
          align: 'start',
          width: 150
        },
        {
          text: 'Artist',
          value: 'artist',
          align: 'start',
          width: 200
        },
        {
          text: 'Song',
          value: 'title',
          align: 'start',
          width: 700
        }
      ],
      year_list: ["2024", "2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016"],
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

      this.weekNumber = (Math.ceil(days / 7)) - 1;
      if (this.weekNumber === 0) {
        this.weekNumber === 1
      } else if (this.weekNumber < 0) {
        this.weekNumber === 1
      } else {
        this.weekNumber === this.weekNumber
      }

      const {data} = await this.axios.get('http://localhost/api/weekly/music-charts?' + 'year=' + this.year + '&week=' + this.weekNumber + '&pl=' + this.platform, {setTimeout: 10000})

      this.chart = data["posts"]
      // this.week = data['result'][0]['week']
      // console.log(this.weekNumber)
    },
    filterText(value, search, item) {
      return value != null &&
          search != null &&
          search.toString().toLocaleLowerCase() &&
          typeof value === 'string' &&
          value.toString().toLocaleLowerCase().indexOf(search) !== -1
    },
    async get_data() {
      this.param = this.selected_week.split(" ")[1]
      const {data} = await this.axios.get('http://localhost/api/weekly/music-charts?' + 'year=' + this.selected_year + '&week=' + this.param + '&pl=' + this.platform, {setTimeout: 10000})

      this.chart = data["posts"]
      // console.log(this.chart)
    },
    getColor(text) {
      if (text.search(new RegExp(/^[a-zA-Z]+$/)) !== -1) {
        return '#8f50fd'
      } else if (text.search(new RegExp(/^\+[a-zA-Z]+-[a-zA-Z]+/)) !== -1) {
        return '#006efd'
      } else if (text.search(new RegExp(/^\+[0-9]+/)) !== -1) {
        return '#39c295'
      } else if (text.search(new RegExp(/^\-[0-9]+/)) !== -1) {
        return '#ee5164'
      } else {
        return '#838383'
      }
    }
  },
  created() {
    this.get_default();
    this.get_data();
    this.filterText();
    this.getColor();
  },
  mounted:
      function () {
        this.get_default(() => {
          this.get_data();
        })
      }
}
</script>
<style scoped>
</style>