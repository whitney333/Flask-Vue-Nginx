<template>
  <div id="tiktok-most-used-hashtag">
    <div class="toolbar">
      <v-row justify="end">
        <v-col cols="12">
          <v-btn
              outlined
              small
              rounded
              color="blue-grey lighten-1"
              dark
              elevation="1"
              class="mr-3"
              @click="getRecentTens()"
          >
            {{ $t('Latest 10 Posts(Default)') }}
          </v-btn>
          <v-btn
              outlined
              small
              rounded
              color="blue-grey lighten-1"
              dark
              elevation="1"
              class="mr-3"
              @click="getRecentThirtys()"
          >
            {{ $t('Latest 30 Posts') }}
          </v-btn>
          <v-btn
              small
              outlined
              rounded
              color="blue-grey lighten-1"
              dark
              elevation="1"
              class="mr-3"
              @click="getOveralls()"
          >
            {{ $t('All Posts') }}
          </v-btn>
        </v-col>
      </v-row>
    </div>
    <apexchart
        ref="sample"
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
  name: "TiktokMostUsedHashtag",
  components: {
    apexchart: VueApexCharts,
  },
  data: function () {
    return {
      series: [],
      chartOptions: {
        noData: {
          text: 'Loading...'
        },
        chart: {
          height: '356px',
          type: 'bar',
        },
        dataLabels: {
          enabled: false,
        //   textAnchor: 'middle',
        //   style: {
        //     colors: ['#ffffff'],
        //     fontSize: '14px'
        //   },
          formatter: function (val, opt) {
            return opt.w.globals.labels[Number(opt.dataPointIndex)]
          },
        //   offsetX: 0,
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
              cssClass: 'apexcharts-xaxis-label',
            },
            // formatter: (value) => {
            //   return Number(value).toLocaleString()
            // }
          },
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
      },
      selection: '1W'
    }
  },
  methods: {
    async getRecentTens() {
      const {data} = await this.axios.get('http://localhost/api/tiktok/hashtags/most-used/recent-ten-posts')
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
      const {data} = await this.axios.get('http://localhost/api/tiktok/hashtags/most-used/recent-thirty-posts')
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
      chart.updateSeries(this.series)
    },
    async getOveralls() {
      const {data} = await this.axios.get('http://localhost/api/tiktok/hashtags/most-used/overall-posts')
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
      chart.updateSeries(this.series)
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
@import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
</style>