<template>
  <div id="twitter-follower-chart">
    <div class="toolbar">
      <v-row justify="end">
        <v-col cols="12">
          <div class="index_number">
            <a href="https://twitter.com/t024_official">
              <v-img
                src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/twitter-logo.svg"
                max-height="30px"
                max-width="30px"
                class="mr-3"
            ></v-img>
            </a>
            {{ Number(this.index_number) | formatNumber }}
          </div>
          {{ $t("Followers") }}
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
  name: "HPTwitterFollower",
  components: {
    apexchart: VueApexCharts,
  },
  data() {
    return {
      series: [],
      range: "three_month",
      end: new Date().toISOString().slice(0, 10),
      latest_date: "",
      latest_follower_count: "",
      past_month_follower_count: "",
      index_number: "",
      chartOptions: {
        chart: {
          id: 'twitter-total-follower',
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
          enabled: false,
        },
        stroke: {
          curve: 'smooth',
          width: 3,
          dashArray: [0, 2]
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
          custom: function ({series, seriesIndex, dataPointIndex, w}) {
            var data = w.globals.initialSeries[seriesIndex].data[dataPointIndex];
            return (
                '<div class="arrow_box">' +
                new Date(data.x).toDateString() +
                "<ul>" +
                "<span>" +
                "<li>" +
                // w.globals.labels[dataPointIndex] +
                "Followers: " +
                (series[0][dataPointIndex]).toLocaleString() +
                "</li>" +
                "</span>" +
                "</ul>" +
                "</div>"
            );
          }
        },
        legend: {
          fontSize: '14px',
          fontWeight: 'bold',
          fontFamily: 'Cairo',
          position: 'top',
          horizontalAlign: 'left'
        },
        yaxis: [
          {
            tickAmount: 4,
            labels: {
              style: {
                fontSize: '12px',
                fontWeight: 'bold',
                fontFamily: 'Cairo',
              },
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
            }
          },
        ],
        colors: ['#1DA1F2'],
        grid: {
          show: false
        }
      },
    }
  },
  methods: {
    async get_twitter_follower() {
      await this.axios.get("/api/twitter/index?"
          + "end=" + this.end
          + "&range=" + this.range,
          {setTimeout: 10000})
      .then(res => {
        this.twitter_follower = res.data["posts"]
        this.index_number = res.data["posts"][res.data["posts"].length - 1]["follower"]

        let formattedData = this.twitter_follower.map((e, i) => {
          return {
            x: e.datetime,
            y: e.follower,
          };
        });
        // update the series with axios data
        this.series = [
          {
            name: "Followers",
            data: formattedData,
          }
        ]
      })
      .catch( err => {
        console.log(err)
      })
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
      this.get_twitter_follower();
  }
}
</script>
<style scoped>
</style>