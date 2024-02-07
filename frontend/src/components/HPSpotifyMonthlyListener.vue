<template>
  <div id="spotify-monthly-listener-chart">
    <div class="toolbar">
      <v-row justify="end">
        <v-col cols="12">
          <div class="index_number">
            <a href="https://open.spotify.com/artist/0jxjOumN4dyPFTLUojSbNP">
              <v-img
                src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/spotify-logo.svg"
                max-height="30px"
                max-width="30px"
                class="mr-3"
            ></v-img>
            </a>
            {{ Number(this.index_number) | formatNumber }}
          </div>
          {{ $t("Monthly Listeners") }}
        </v-col>
      </v-row>
    </div>
    <apexchart
        ref="chart"
        :options="chartOptions"
        :series="series"
        width="100%"
        height="100%"
    >
    </apexchart>
  </div>
</template>
<script>
import VueApexCharts from "vue-apexcharts";

export default {
  name: "HPSpotifyMonthlyListener",
  components: {
    apexchart: VueApexCharts,
  },
  data() {
    return {
      series: [],
      range: "three_month",
      end: new Date().toISOString().slice(0, 10),
      latest_listener_count: "",
      past_month_listener_count: "",
      index_number: "",
      latest_date: "",
      chartOptions: {
        chart: {
          height: '100%',
          width: '100%',
          type: 'area',
          toolbar: {
            tools: {
              download: false,
              selection: false,
              zoom: false,
              zoomin: false,
              zoomout: false,
              pan: false,
              reset: false
            }
          }
        },
        dataLabels: {
          enabled: false
        },
        stroke: {
          curve: 'smooth',
          width: 3,
        },
        xaxis: {
          // categories: [],
          type: 'datetime',
          labels: {
            format: 'MM/dd',
            rotate: -45,
            trim: true,
            style: {
              fontSize: '12px',
              fontWeight: 'bold',
              fontFamily: 'Cairo',
            }
          },
          tickAmount: 4,
          tooltip: {
            enabled: false
          }
        },
        tooltip: {
          theme: 'light',
          x: {
            show: false
          },
          custom: function ({series, seriesIndex, dataPointIndex, w}) {
            var data = w.globals.initialSeries[seriesIndex].data[dataPointIndex];
            return (
                '<div class="arrow_box">' +
                new Date(data.x).toDateString() +
                "<ul>" +
                "<span>" +
                "<li>" +
                // w.globals.labels[dataPointIndex] +
                "Total Listeners: " +
                (series[0][dataPointIndex]).toLocaleString() +
                "</li>" +
                "</span>" +
                "</ul>" +
                "</div>"
            );
          }
        },
        title: {
          // text: 'Followers',
          style: {
            fontSize: '20px',
            fontWeight: 'bold',
            fontFamily: 'Cairo',
          },
          align: 'left'
        },
        yaxis: {
          tickAmount: 4,
          labels: {
            formatter: function (value) {
              if (String(value).length < 4) {
                return Number(value).toLocaleString();
              } else if (String(value).length < 7) {
                return Number(value / 1000).toLocaleString() + 'K';
              } else if (String(value).length < 10) {
                return Number(value / 1000000).toLocaleString() + 'M';
              } else {
                return Number(value / 1000000000).toLocaleString() + 'B';
              }
            },
            style: {
              fontSize: '12px',
              fontWeight: 'bold',
              fontFamily: 'Cairo',
            }
          }
        },
        colors: ['#1DB954'],
        grid: {
          show: false
        }
      }
    }
  },
  methods: {
    async get_spotify_listener() {
    const {data} = await this.axios.get("/api/spotify/index?" + "end=" + this.end + "&range=" + this.range,
        {setTimeout: 10000})

    this.range = data["range"]
    this.follower = data["posts"]
    this.index_number = data["posts"][data["posts"].length - 1]["listener"]
    // console.log(this.follower)

      let formattedData = this.follower.map((e, i) => {
        return {
          x: e.date,
          y: e.listener,
        };
      });
      // update the series with axios data
      this.series = [
        {
          name: "Monthly Listeners",
          data: formattedData,
        }
      ]
    },
  },
  filters: {
    formatNumber: function (value) {
      if (String(value).length < 4) {
        return Number(value).toLocaleString();
      } else if (String(value).length < 7) {
        return Number(value / 1000).toLocaleString() + 'K';
      } else if (String(value).length < 10) {
        return Number(value / 1000000).toLocaleString() + 'M';
      } else {
        return Number(value / 1000000000).toLocaleString() + 'B';
      }
    }
  },
  created() {
    this.get_spotify_listener();
  }
}
</script>
<style scoped>
.toolbar .index_number {
  padding-left: 20px;
  padding-right: 10px;
  color: #000000;
  display: inline-flex;
  font-size: 24px;
  font-weight: bold;
  font-family: 'Cairo', sans-serif;
}
</style>