<template>
  <div id="tiktok-total-save-chart">
    <div class="toolbar">
      <v-row justify="end">
        <v-col cols="12">
          <div class="index_number">
            {{ Number(this.index_number) | formatNumber }}
          </div>
          <v-btn
              outlined
              x-small
              color="blue-grey lighten-1"
              dark
              rounded
              elevation="1"
              class="mr-3"
              @click="update_data('one_month')" :class="{active: selection==='one_month'}"
          >
            1M
          </v-btn>
          <v-btn
              outlined
              x-small
              color="blue-grey lighten-1"
              dark
              rounded
              elevation="1"
              class="mr-3"
              @click="update_data('three_months')" :class="{active: selection==='three_months'}"
          >
            3M
          </v-btn>
          <v-btn
              x-small
              outlined
              color="blue-grey lighten-1"
              dark
              rounded
              elevation="1"
              class="mr-3"
              @click="update_data('six_months')" :class="{active: selection==='six_months'}"
          >
            6M
          </v-btn>
          <v-btn
              x-small
              outlined
              color="blue-grey lighten-1"
              dark
              rounded
              elevation="1"
              class="mr-3"
              @click="update_data('one_year')" :class="{active: selection==='one_year'}"
          >
            1Y
          </v-btn>
        </v-col>
        <v-col cols="12">
          <div class="chart-latest-update">
            <span>{{ $t('Last updated') }}
              <span>{{ this.latest_date }}</span>
            </span>
          </div>
          <div class="month_change_percentage">
            <div class="stat">
              <span class="up"
                    v-if="(((this.latest_save_count - this.past_month_save_count)/this.past_month_save_count)*100)>0">
                    +{{Number((((this.latest_save_count - this.past_month_save_count) / this.past_month_save_count) * 100).toFixed(2)).toLocaleString() }}%
              </span>
              <span class="down"
                    v-if="(((this.latest_save_count - this.past_month_save_count)/this.past_month_save_count)*100)<0">
                    {{Number((((this.latest_save_count - this.past_month_save_count) / this.past_month_save_count) * 100).toFixed(2)).toLocaleString() }}%
              </span>
              <span class="same"
                    v-if="(((this.latest_save_count - this.past_month_save_count)/this.past_month_save_count)*100)===0">
                    {{Number((((this.latest_save_count - this.past_month_save_count) / this.past_month_save_count) * 100).toFixed(2)).toLocaleString() }}%
              </span>
              <span class="update_date">{{ $t('Past Month') }}</span>
            </div>
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
  name: "TiktokTotalSaves",
  components: {
    apexchart: VueApexCharts,
  },
  data() {
    return {
      series: [],
      selection: 'one_month',
      latest_date: '',
      latest_save_count: '',
      past_month_save_count: '',
      chartOptions: {
        chart: {
          id: 'tiktok-total-save',
          height: '100%',
          width: '100%',
          type: 'line',
          group: 'tiktok',
          toolbar: {
            tools: {
              download: true,
              selection: true,
              zoom: true,
              zoomin: false,
              zoomout: false,
              pan: true,
              reset: true
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
                "Total Saves: " +
                (series[0][dataPointIndex]).toLocaleString() +
                "</li>" +
                "</span>" +
                "<span>" +
                "<li>" +
                "Saves per video: " +
                (series[1][dataPointIndex]).toLocaleString() +
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
          {
            opposite: true,
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
        colors: ['#000000', '#000000'],
        grid: {
          show: false
        }
      }
    }
  },
  methods: {
    async get_tiktok_total_saves() {
      const {data} = await this.axios.get("/api/tiktok/chart", {setTimeout: 10000})
      this.tiktok_total_saves = data["result"]
      this.index_number = data["result"][data["result"].length - 1]["total_save"]
      // console.log(this.tiktok_total_views)

      let formattedData = this.tiktok_total_saves.map((e, i) => {
        return {
          x: e._id,
          y: e.total_save,
        };
      });
      let formattedData1 = this.tiktok_total_saves.map((e, i) => {
        return {
          x: e._id,
          y: e.avg_save,
        };
      });
      // update the series with axios data
      this.series = [
        {
          name: "Saves",
          data: JSON.parse(JSON.stringify(formattedData)),
        },
        {
          name: "Saves per video",
          data: JSON.parse(JSON.stringify(formattedData1)),
        },
      ]
    },
    update_data(timeline) {
      this.selection = timeline

      this.axios.get("/api/tiktok/chart", {setTimeout: 10000})
          .then(res => {
            this.data = res["data"]["result"]
            this.latest_date = this.data[this.data.length - 1]["datetime"]
            this.one_month = this.data[this.data.length - 30]["datetime"]
            this.three_months = this.data[this.data.length - 90]["datetime"]
            // this.six_months = this.data[this.data.length - 180]["datetime"]
            // this.one_year = this.data[this.data.length - 365]["datetime"]

            this.latest_save_count = this.data[this.data.length - 1]["total_share"]
            this.past_month_save_count = this.data[this.data.length - 6]["total_share"]

            // console.log(this.latest_date)
            // console.log(this.one_month)
            // console.log(this.three_months)
            // console.log(this.six_months)
            // console.log(this.one_year)
            // console.log(new Date(this.one_month).getTime())
          })
          .catch(err => {
            console.log(err);
          })

      switch (timeline) {
        case 'one_month':
          this.$refs.chart.zoomX(
              new Date(this.one_month).getTime(),
              new Date(this.latest_date).getTime()
          )
              break
        case 'three_months':
          this.$refs.chart.zoomX(
              new Date(this.three_months).getTime(),
              new Date(this.latest_date).getTime()
          )
              break
        case 'six_months':
          this.$refs.chart.zoomX(
              new Date(this.six_months).getTime(),
              new Date(this.latest_date).getTime()
          )
              break
        case 'one_year':
          this.$refs.chart.zoomX(
              new Date(this.one_year).getTime(),
              new Date(this.latest_date).getTime()
          )
      }
    },
  },
  created() {
    this.get_tiktok_total_saves();
    this.update_data();
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
}
</script>
<style scoped>
</style>