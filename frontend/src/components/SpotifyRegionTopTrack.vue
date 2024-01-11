<template>
  <div id="spotify-region-top-track-chart">
    <div class="toolbar">
      <v-row justify="end">
        <v-col cols="8">
          <div class="index_number">
            {{ selected_track }}
          </div>
        </v-col>
        <v-col cols="4" lg="4" class="align-content-end">
          <v-select
              :items="track_list"
              label="Select Track"
              dense
              filled
              rounded
              v-model="selected_track"
              item-color="orange darken-1"
              v-on:change="fetch_top_track_by_region"
          ></v-select>
        </v-col>
        <v-col cols="12">
          <div class="chart-latest-update">
            <span>Last updated
              <span>{{ this.latest_date }}</span>
            </span>
          </div>
        </v-col>
      </v-row>
    </div>
    <apexchart
        ref="chart"
        width="100%"
        height="100%"
        :options="chartOptions"
        :series="series"
    >
    </apexchart>
  </div>
</template>
<script>
import VueApexCharts from "vue-apexcharts";

export default {
  name: "SpotifyRegionTopTrack",
  components: {
    apexchart: VueApexCharts,
  },
  data() {
    return {
      index_number: "",
      latest_date: "",
      series: [],
      track_list: [],
      top_one_song: "fox",
      selected_track: "",
      chartOptions: {
        chart: {
          height: '100%',
          width: '100%',
          type: 'radar',
          dropShadow: {
            enabled: true,
            blur: 1,
            left: 1,
            top: 1
          }
        },
        stroke: {
          width: 2
        },
        plotOptions: {
          radar: {
            size: 100,
            polygons: {
              strokeColors: '#202850',
              strokeWidth: 1,
              connectorColors: ['#808080'],
              fill: {
                colors: ['#ffffff', '#f8f8f8']
              }
            }
          }
        },
        fill: {
          opacity: 0.1
        },
        colors: ['#FF4560'],
        markers: {
          size: 5,
          hover: {
            size: 8
          },
          colors: ['#fff'],
          strokeColor: '#FF4560',
          strokeWidth: 2,
        },
        dataLabels: {
          enabled: true,
          background: {
            enabled: true,
            borderRadius: 2,
          }
        },
        tooltip: {
          y: {
            formatter: function(val) {
              return val
            }
          }
        },
        xaxis: {
          labels: {
            show: true,
            style: {
              color: ["#101d4d"],
              fontSize: "20px",
              fontFamily: "Cairo"
            }
          },
          categories: ['Asia', 'North America', 'South America', 'Oceania', 'Europe']
        },
        yaxis: {
          show: true,
          tickAmount: 5,
          min: 0,
          max: 100,
          labels: {
            formatter: function(val, i) {
              if (i % 2 === 0) {
                return val
              } else {
                return ''
              }
            },
            style: {
              fontSize: '16px',
              fontWeight: 'bold',
              fontFamily: 'Cairo',
            }
          }
        }
      },
    }
  },
  methods: {
    async get_default_top_track_by_region() {
      await this.axios.get('http://localhost/api/spotify/top-track/region?'
          + "track=" + this.top_one_song,
          {setTimeout: 10000})
      .then( res => {
        this.tracks = res.data['result'][0]["track_info"]
        this.track_list = res.data["track_select_list"][0]["track"]

        const formattedData = this.tracks.map((e, i) => {
          return {
            x: e.region,
            y: e.agg_popularity
          }
        })
        // update the series with axios data
        this.series = [
          {
            name: this.tracks,
            data: formattedData,
          }
        ]
        console.log(this.series)
      })
      .catch( err => {
        console.log(err)
      })
    },
    async fetch_top_track_by_region() {
      await this.axios.get('http://localhost/api/spotify/top-track/region?'
          + "track=" + this.selected_track,
          {setTimeout: 10000})
      .then( res => {
        this.tracks = res.data['result'][0]["track_info"]
        this.track_list = res.data["track_select_list"][0]["track"]
        console.log(this.track_list)
        console.log(this.tracks)

        const formattedData = this.tracks.map((e, i) => {
          return {
            x: e.region,
            y: e.agg_popularity
          }
        })
        // update the series with axios data
        this.series = [
          {
            name: this.tracks,
            data: formattedData,
          }
        ]
      })
      .catch( err => {
        console.log(err)
      })
    },
    async get_top_song() {
      let _date = new Date()
      this.end_date = _date.toISOString().split('T')[0]

      await this.axios.get("http://localhost/api/spotify/top-track?"
          + "end=" + this.end_date
          + "&country=" + "KR"
          + "&drange=" + "",
          {setTimeout: 5000})
      .then(res => {
        this.top_one_song = res.data["posts"][0]["top_track"][0]["track"]
      })
      .catch(err => {
        console.log(err)
      })
    }
  },
  created() {
    this.get_top_song();
    this.get_default_top_track_by_region();
    this.fetch_top_track_by_region();
  },
  mounted: {
    function() {
      this.get_default_top_track_by_region();
      this.fetch_top_track_by_region();
    }
  },
  computed: {
    function() {
      this.get_top_song();
    }
  },
}
</script>
<style scoped>
</style>