<template>
  <div id="bilibili-total-video-chart">
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
            <span>{{ $t("Last updated") }}
              <span>{{ this.latest_date }}</span>
            </span>
          </div>
          <div class="month_change_percentage">
            <div class="stat">
              <span class="up"
                    v-if="(((this.latest_video_count - this.past_month_video_count)/this.past_month_video_count)*100)>0">
                    +{{Number((((this.latest_video_count - this.past_month_video_count) / this.past_month_video_count) * 100).toFixed(2)).toLocaleString() }}%
              </span>
              <span class="down"
                    v-if="(((this.latest_video_count - this.past_month_video_count)/this.past_month_video_count)*100)<0">
                    {{Number((((this.latest_video_count - this.past_month_video_count) / this.past_month_video_count) * 100).toFixed(2)).toLocaleString() }}%
              </span>
              <span class="same"
                    v-if="(((this.latest_video_count - this.past_month_video_count)/this.past_month_video_count)*100)===0">
                    {{Number((((this.latest_video_count - this.past_month_video_count) / this.past_month_video_count) * 100).toFixed(2)).toLocaleString() }}%
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
  name: "BilibiliTotalVideo",
  components: {
    apexchart: VueApexCharts,
  },
  data() {
    return {
      series: [],
      selection: "one_month",
      latest_date: "",
      end: new Date().toISOString().slice(0, 10),
      latest_video_count: "",
      past_month_video_count: "",
      index_number: "",
      chartOptions: {
        chart: {
          id: 'bilibili-total-video',
          height: '100%',
          width: '100%',
          type: 'line',
          group: 'bilibili',
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
                "Total Videos" + ": " +
                (series[0][dataPointIndex]).toLocaleString() +
                "</li>" +
                "</span>" +
                "</ul>" +
                "</div>"
            );
          }
        },
        title: {
          style: {
            fontSize: '20px',
            fontWeight: 'bold',
            fontFamily: 'Cairo',
          },
          align: 'left'
        },
        yaxis: {
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
        colors: ['#1E88E5'],
        grid: {
          show: false
        }
      }
    }
  },
  methods: {
    async get_video_sum() {
      const {data} = await this.axios.get("/api/bilibili/chart", {setTimeout: 10000})

      this.result = data["result"]
      this.index_number = data["result"][data["result"].length - 1]["video_num"]
      // console.log(this.follower)

      let formattedData = this.result.map((e, i) => {
        return {
          x: e._id,
          y: e.video_num,
        };
      });
      // update the series with axios data
      this.series = [
        {
          name: "Total Video",
          data: formattedData,
        }
      ]
    },
    update_data(timeline) {
      this.selection = timeline

      this.axios.get("/api/bilibili/chart", {setTimeout: 10000})
          .then(res => {
            this.data = res["data"]["result"]
            this.latest_date = this.data[this.data.length - 1]["datetime"]
            this.one_month = this.data[this.data.length - 4]["datetime"]
            this.three_months = this.data[this.data.length - 12]["datetime"]
            // this.six_months = this.data[this.data.length - 24]["datetime"]
            // this.one_year = this.data[this.data.length - 48]["datetime"]

            this.latest_video_count = this.data[this.data.length - 1]["video_num"]
            this.past_month_video_count = this.data[this.data.length - 6]["video_num"]

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
    this.get_video_sum();
    this.update_data();
  }
}
</script>
<style scoped>
.chart-latest-update span {
  font-size: small;
  color: #9d9c9d;
}
.toolbar .month_change_percentage .stat span.update_date{
  display:inline-block;
  padding-left: 3px;
  font-size: small;
  color: #9d9c9d;
}
.toolbar .month_change_percentage .stat span{
    display:block;
    font-size:16px;
    font-weight:500;
    white-space:nowrap
}
.toolbar .month_change_percentage .stat span.up{
    content:'';
    display:inline-block;
    padding: 1px 3px;
    margin-left:5px;
    background-color: rgb(248 248 248 / 96%);
    border: 2px solid #00bf72;
    color: #00bf72;
    border-radius: 5px;
    background-repeat:no-repeat;
    background-position:center center
}
.month_change_percentage .stat span.down{
    content:'';
    display:inline-block;
    padding: 1px 3px;
    margin-left:5px;
    background-color: rgb(248 248 248 / 96%);
    border: 2px solid #bf0016;
    color: #BF0016FF;
    border-radius: 5px;
    background-repeat:no-repeat;
    background-position:center center
}
.month_change_percentage .stat span.same{
    content:'';
    display:inline-block;
    padding: 1px 3px;
    margin-left:5px;
    background-color: rgb(248 248 248 / 96%);
    border: 2px solid #252525;
    color: #252525;
    border-radius: 5px;
    background-repeat:no-repeat;
    background-position:center center
}
.toolbar .index_number {
  padding-left: 3px;
  padding-right: 10px;
  color: #000000;
  display: inline-flex;
  font-size: 24px;
  font-weight: bold;
  font-family: 'Cairo', sans-serif;
}
</style>