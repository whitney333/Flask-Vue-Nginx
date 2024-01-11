<template>
  <div id="spotify-top-track-chart">
    <!--  dropdown menu of music broadcast programs  -->
    <div class="toolbar">
      <v-row justify="start">
        <v-col cols="8">
          <div class="index_number">
            <v-img
                src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/medal-gold.svg"
                max-height="30"
                max-width="30"
            >
            </v-img>
            {{ this.top_one }}
          </div>
          <div class="chart-latest-update">
            <span>Last updated
              <span>{{ this.latest_date }}</span>
            </span>
          </div>
        </v-col>
        <v-col cols="4" lg="4" class="align-content-end">
          <v-select
              :items="country_list"
              label="Select Country"
              dense
              filled
              rounded
              v-model="selected_country"
              item-color="orange darken-1"
              :item-text="text"
              :item-value="value"
              v-on:change="fetch_top_track"
          ></v-select>
        </v-col>
      </v-row>
    </div>
    <apexchart
        ref="chart"
        width="90%"
        height="350"
        :options="chartOptions"
        :series="series"
    >
    </apexchart>
  </div>
</template>
<script>
import VueApexCharts from "vue-apexcharts";
export default {
  name: "SpotifyTopTrack",
  components: {
    apexchart: VueApexCharts,
  },
  data: function () {
    return {
      drange: "1d",
      end_date: new Date().toISOString().slice(0, 10),
      selected_country: "",
      country: "KR",
      country_list: [
        {value: "KR", text: "South Korea"},
        {value: "HK", text: "Hong Kong"},
        {value: "IN", text: "India"},
        {value: "ID", text: "Indonesia"},
        {value: "JP", text: "Japan"},
        {value: "MY", text: "Malaysia"},
        {value: "MO", text: "Macao"},
        {value: "PH", text: "Philippines"},
        {value: "TW", text: "Taiwan"},
        {value: "TH", text: "Thailand"},
        {value: "VN", text: "Vietnam"}, //Asia
        {value: "CA", text: "Canada"},
        {value: "US", text: "United States"},
        {value: "BR", text: "Brazil"},
        {value: "MX", text: "Mexico"}, // North America & South America
        {value: "IT", text: "Italy"},
        {value: "FR", text: "France"},
        {value: "DE", text: "Germany"},
        {value: "ES", text: "Spain"},
        {value: "GB", text: "United Kingdom"}, //Europe
        {value: "AU", text: "Australia"}], //Oceania
      selection: "",
      top_one: "",
      latest_date: "",
      series: [],
      chartOptions: {
        chart: {
          height: '100%',
          weight: '100%',
          type: 'bar',
          stacked: false,
          toolbar: {
            offsetX: 50
          }
        },
        dataLabels: {
          enabled: true
        },
        fill: {
          type: 'gradient',
          gradient: {
            shade: 'dark',
            type: "horizontal",
            shadeIntensity: 0.5,
            gradientToColors: undefined, // optional, if not defined - uses the shades of same color in series
            inverseColors: true,
            opacityFrom: 1,
            opacityTo: 1,
            stops: [0, 50, 100],
            colorStops: []
          }
        },
        grid: {
          show: false,
          yaxis: {
            lines: {
              show: false
            }
          },
        },
        plotOptions: {
          bar: {
            borderRadius: 7,
            borderRadiusApplication: 'around',
            horizontal: true,
            columnWidth: '50%',
            colors: {
              backgroundBarColors: ['#eeeeee'],
              backgroundBarRadius: 10
            }
          }
        },
        colors: ['#863af6', '#18E7F2', '#8EDB21', '#F29518'],
        legend: {
          show: false
        },
        yaxis: {
          type: 'category',
          labels: {
            show: true,
            align: 'right',
            minWidth: 0,
            maxWidth: 200,
            trim: true,
            style: {
              colors: [],
              fontSize: '14px',
              fontFamily: 'Cairo, sans-serif',
              fontWeight: 400,
              cssClass: 'apexcharts-yaxis-label',
            },
          },
          // display axis border
          axisBorder: {
            show: false
          }
        },
        xaxis: {
          type: 'category',
          max: 100,
          tickAmount: 5,
          axisBorder: {
            show: false
          }
        },
        tooltip: {
          theme: 'light',
          custom: function ({series, seriesIndex, dataPointIndex, w}) {
            var data = w.globals.initialSeries[seriesIndex].data[dataPointIndex];
            return (
                '<div class="arrow_box">' +
                "<ul>" +
                "<span>" +
                "<li>" +
                // w.globals.labels[dataPointIndex] +
                w.globals.labels[dataPointIndex] +
                ": " +
                (series[seriesIndex][dataPointIndex]).toLocaleString() +
                "</li>" +
                "</span>" +
                "</ul>" +
                "</div>"
            );
          }
        }
      }
    }
  },
  methods: {
    async get_default_top_track() {
      let _date = new Date()
      this.end_date = _date.toISOString().split('T')[0]

      const {data} = await this.axios.get("http://localhost/api/spotify/top-track?"
          + "end=" + this.end_date
          + "&country=" + this.country
          + "&drange=" + this.drange,
          {setTimeout: 10000})
      this.tracks = data["posts"][0]["top_track"]
      this.latest_date = data["posts"][0]["datetime"]
      this.top_one = data["posts"][0]["top_track"][0]["track"]
      console.log(this.tracks)

      // Format data correctly
      let top_tracks = this.tracks.map((e, i) => {
        return {
          x: e.track,
          y: e.popularity,
        };
      });

      // update the series with axios data
      this.series = [
        {
          name: 'Tracks',
          data: top_tracks,
        }
      ];
    },
    async fetch_top_track() {
      let _date = new Date()
      this.end_date = _date.toISOString().split('T')[0]

      const {data} = await this.axios.get("http://localhost/api/spotify/top-track?"
          + "end=" + this.end_date
          + "&country=" + this.selected_country
          + "&drange=" + this.drange,
          {setTimeout: 10000})
      this.tracks = data["posts"][0]["top_track"]
      this.latest_date = data["posts"][0]["datetime"]
      this.top_one = data["posts"][0]["top_track"][0]["track"]
      console.log(this.tracks)

      // Format data correctly
      let top_tracks = this.tracks.map((e, i) => {
        return {
          x: e.track,
          y: e.popularity,
        };
      });

      // update the series with axios data
      this.series = [
        {
          name: 'Tracks',
          data: top_tracks,
        }
      ];
    }
  },
  created() {
    this.get_default_top_track();
    this.fetch_top_track();
  },
  mounted: //set kr as default
      function () {
        this.get_default_top_track(() => {
          this.fetch_top_track();
        })
      }
}
</script>
<style scoped>
</style>