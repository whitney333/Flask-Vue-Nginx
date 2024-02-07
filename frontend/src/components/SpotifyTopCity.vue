<template>
  <div id="spotify-listener-city-chart">
    <v-row justify="end">
      <v-col cols="12">
        <div class="chart-latest-update">
            <span>Last updated
              <span>{{ this.latest_date }}</span>
            </span>
        </div>
      </v-col>
    </v-row>
    <apexchart
        ref="chart"
        width="80%"
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
  name: "SpotifyTopCity",
  components: {
    apexchart: VueApexCharts,
  },
  data: function () {
    return {
      latest_date: "",
      series: [],
      chartOptions: {
        chart: {
          height: '200%',
          type: 'bar',
        },
        dataLabels: {
          enabled: true,
          textAnchor: 'middle',
          dropShadow: {
            enabled: true
          },
          style: {
            colors: ['#ffffff'],
            fontSize: '14px'
          },
          formatter: function (val, opt) {
            return opt.w.globals.labels[opt.dataPointIndex]
          },
        },
        plotOptions: {
          bar: {
            distributed: true,
            borderRadius: 6,
            horizontal: true
          }
        },
        colors: ["#115f9a", "#00A9FF", "#315aee", "#3771d3", "#A0E9FF"],
        legend: {
          show: false
        },
        yaxis: {
          type: 'category',
          labels: {
            show: false,
            style: {
              fontSize: '12px',
              fontWeight: 'bold',
              fontFamily: 'Cairo',
            }
          },
          title: {
            text: 'Top Cities',
            style: {
              fontSize: '14px',
              fontFamily: 'Cairo, sans-serif',
              fontWeight: 600,
            },
          },
        },
        xaxis: {
          type: 'category',
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
            }
          },
          title: {
            text: 'Total Listeners',
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
          custom: function ({series, seriesIndex, dataPointIndex}) {
            return (
                '<div class="arrow_box">' +
                "<span>" +
                // w.globals.labels +
                "Listeners: " +
                (series[seriesIndex][dataPointIndex]).toLocaleString() +
                "</span>" +
                "</div>"
            );
          }
        },
      }
    }
  },
  methods: {
    async get_city() {
      const {data} = await this.axios.get('/api/spotify/top-city', {setTimeout: 10000})

      this.city = data['result']
      this.latest_date = data['result'][0]['date']
      // console.log(this.city)

      const formattedData = this.city.map((e, i) => {
            return {
              x: e.city,
              y: e.city_listener
            }
      })
      // console.log(formattedData)

      // update the series with axios data
      this.series = [
        {
          name: this.city,
          data: formattedData,
        }
      ]
    }
  },
  created() {
    this.get_city();
  }
}
</script>
<style scoped>
</style>
