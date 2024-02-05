<template>
  <div id="instagram-most-used-hashtag">
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
  name: "InstagramMostUsedHashtag",
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
          // text inside bars
          enabled: false,
          // textAnchor: 'top',
          // style: {
          //   colors: ['#ffffff'],
          //   fontSize: '14px'
          // },
          // formatter: function (val, opt) {
          //   return opt.w.globals.labels[Number(opt.dataPointIndex)]
          // },
          // offsetX: 0,
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
            gradientToColors: ['#ffcf92'], // optional, if not defined - uses the shades of same color in series
            inverseColors: true,
            opacityFrom: 1,
            opacityTo: 1,
            stops: [0, 50, 100],
            colorStops: []
          }
        },
        colors: ['#dd4ee5'],
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
            text: 'Occurrence',
            offsetX: 0,
            offsetY: 0,
            style: {
              color: undefined,
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
      const {data} = await this.axios.get('/api/instagram/hashtags/most-used/recent-ten-posts')
      this.TopTenUsed = data["result"]
      // console.log(this.TopTenUsed)

      // Format data correctly
      let hashtags = this.TopTenUsed.map((e, i) => {
        return {
          x: e._id,
          y: e.count,
        };
      });

      // update the series with axios data
      this.series = [
        {
          name: 'Counts',
          data: hashtags,
        }
      ];

    },
    async getRecentThirtys() {
      const {data} = await this.axios.get('/api/instagram/hashtags/most-used/recent-thirty-posts')
      this.TopTenUsed = data["result"]
      // console.log(this.TopTenUsed)

      // Format data correctly
      let hashtags = this.TopTenUsed.map((e, i) => {
        return {
          x: e._id,
          y: e.count,
        };
      });

      // update the series with axios data
      this.series = [
        {
          name: 'Counts',
          data: hashtags,
        }
      ];

    },
    async getOveralls() {
      const {data} = await this.axios.get('/api/instagram/hashtags/most-used/overall-posts')
      this.TopTenUsed = data["result"]
      // console.log(this.TopTenUsed)

      // Format data correctly
      let hashtags = this.TopTenUsed.map((e, i) => {
        return {
          x: e._id,
          y: e.count,
        };
      });

      // update the series with axios data
      this.series = [
        {
          name: 'Counts',
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
</style>