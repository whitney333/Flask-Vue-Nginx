<template>
  <div id="instagram-most-engaged-hashtag">
    <div class="toolbar">
      <v-row justify="end">
        <v-col cols="12">
          <v-btn
              outlined
              small
              color="blue-grey lighten-1"
              dark
              rounded
              elevation="1"
              class="mr-3"
              @click="getRecentTens()"
          >
            Latest 10 Posts (Default)
          </v-btn>
          <v-btn
              outlined
              small
              color="blue-grey lighten-1"
              dark
              rounded
              elevation="1"
              class="mr-3"
              @click="getRecentThirtys()"
          >
            Latest 30 Posts
          </v-btn>
          <v-btn
              small
              outlined
              color="blue-grey lighten-1"
              dark
              rounded
              elevation="1"
              class="mr-3"
              @click="getOveralls()"
          >
            All Posts
          </v-btn>
        </v-col>
      </v-row>
    </div>
    <apexchart
        ref="chart"
        width="100%"
        :options="chartOptions"
        :series="series"
        height="350"
    >
    </apexchart>
  </div>
</template>
<script>
import VueApexCharts from 'vue-apexcharts'
export default {
  name: "InstagramMostEngagedHashtag",
  components: {
    apexchart: VueApexCharts,
  },
  data: function () {
    return {
      series: [],
      chartOptions: {
        chart: {
          height: '356px',
          type: 'bar',
        },
        dataLabels: {
          enabled: false,
        },
        plotOptions: {
          bar: {
            borderRadius: 7,
            borderRadiusApplication: 'around',
            horizontal: true,
            columnWidth: '50%',
          }
        },
        fill: {
          type: 'gradient',
          gradient: {
            // shade: 'dark',
            type: "horizontal",
            shadeIntensity: 0.5,
            gradientToColors: ['#ab93ff'], // optional, if not defined - uses the shades of same color in series
            inverseColors: true,
            opacityFrom: 1,
            opacityTo: 1,
            stops: [0, 50, 100],
            colorStops: []
          }
        },
        colors: ['#10a3ff'],
        // legend: {
        //   show: false
        // },
        yaxis: {
          type: 'category',
          labels: {
            show: true,
            trim: true,
            style: {
              colors: [],
              fontSize: '14px',
              fontFamily: 'Cairo, sans-serif',
              fontWeight: 400,
              // cssClass: 'apexcharts-xaxis-label',
            },
          }
        },
        xaxis: {
          labels: {
            show: true,
            formatter: (value) => {
              return Number(value).toLocaleString()
            }
          },
          title: {
            text: 'Engage Percentage',
            offsetX: 0,
            offsetY: 0,
            style: {
              fontSize: '14px',
              fontFamily: 'Cairo, sans-serif',
              fontWeight: 600,
              // cssClass: 'apexcharts-xaxis-title',
            },
          },
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
    async getRecentTens() {
      const {data} = await this.axios.get('/api/instagram/hashtags/most-engaged/recent-ten-posts')
      this.TopTenUsed = data["result"]
      // console.log(this.TopTenUsed)

      // Format data correctly
      let hashtags = this.TopTenUsed.map((e, i) => {
        return {
          x: e._id,
          y: e.eng_rate_per_hashtag,
        };
      });

      // update the series with axios data
      this.series = [
        {
          name: 'Probability',
          data: hashtags,
        }
      ];

    },
    async getRecentThirtys() {
      const {data} = await this.axios.get('/api/instagram/hashtags/most-engaged/recent-thirty-posts')
      this.TopTenUsed = data["result"]
      // console.log(this.TopTenUsed)

      // Format data correctly
      let hashtags = this.TopTenUsed.map((e, i) => {
        return {
          x: e._id,
          y: e.eng_rate_per_hashtag,
        };
      });

      // update the series with axios data
      this.series = [
        {
          name: 'Probability',
          data: hashtags,
        }
      ];

    },
    async getOveralls() {
      const {data} = await this.axios.get('/api/instagram/hashtags/most-engaged/overall-posts')
      this.TopTenUsed = data["result"]
      // console.log(this.TopTenUsed)

      // Format data correctly
      let hashtags = this.TopTenUsed.map((e, i) => {
        return {
          x: e._id,
          y: e.eng_rate_per_hashtag,
        };
      });

      // update the series with axios data
      this.series = [
        {
          name: 'Probability',
          data: hashtags,
        }
      ];

    },
  },
  created() {
    this.getRecentTens();
    this.getRecentThirtys();
    this.getOveralls();
  },
  mounted: //set latest 10 posts as default
      function () {
        this.getRecentTens(() => {
        this.getRecentThirtys();
        this.getOveralls();
     })
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