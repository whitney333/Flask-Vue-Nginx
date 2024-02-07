<template>
  <div id="google-chart">
    <apexchart
        :options="chartOptions"
        :series="series"
        ref="chart"
        height="500"
    >
    </apexchart>
  </div>
</template>
<script>
import VueApexCharts from "vue-apexcharts";
export default {
  name: "GoogleTrendRisingQuery",
  components: {
    apexchart: VueApexCharts
  },
  data() {
    return {
      series: [],
      chartOptions: {
        noData: {
          text: 'Loading...',
          align: 'center',
          verticalAlign: 'middle',
          style: {
            color: '#525050',
            fontSize: '18px',
            fontWeight: 'bold',
            fontFamily: 'Cairo'
          }
        },
        chart: {
          height: '100%',
          width: '100%',
          type: 'bar',
          toolbar: {
            show: true
          }
        },
        dataLabels: {
          enabled: false
        },
        plotOptions: {
          bar: {
            horizontal: true,
            columnWidth: '50%',
            borderRadius: 5
          }
        },
        yaxis: {
          categories: [],
          labels: {
            show: true,
            formatter: function (str) {
              const n = 10
              return str.length > n ? str.substr(0, n - 1) + '...' : str
            },
          style: {
            fontSize: '16px'
          }
        }
        },
        xaxis: {
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
              fontSize: '14px'
            }
          }
        },
        tooltip: {
          theme: 'light',
          x: {
            show: true
          },
          custom: function ({series, seriesIndex, dataPointIndex, w}) {
            return (
                '<div class="arrow_box">' +
                "<span>" +
                w.globals.labels[dataPointIndex] +
                ": " +
                (series[seriesIndex][dataPointIndex]).toLocaleString() +
                "</span>" +
                "</div>"
            );
          }
        },
        title: {
          text: "YouTube Rising Query",
          style: {
            fontSize: '24px',
            fontWeight: 'bold',
            fontFamily: 'Cairo',
          },
          align: 'left'
        },
        grid: {
          show: true,
          position: 'back',
          borderColor: '#90A4AE'
        },
        fill: {
          type: 'gradient',
          gradient: {
            // shade: 'dark',
            type: "horizontal",
            shadeIntensity: 0.5,
            gradientToColors: ['#FFBE98'], // optional, if not defined - uses the shades of same color in series
            inverseColors: true,
            opacityFrom: 1,
            opacityTo: 1,
            stops: [0, 50, 100],
            colorStops: []
          }
        },
        colors: ['#dd4ee5'],
      }
    }
  },
  methods: {
    async get_rising_query() {
      await this.axios.get("/api/google-trends/youtube-rising-query",
          {setTimeout: 10000})
      .then(res => {
        this.rising_query = res["data"]

        let formattedData = this.rising_query.map((e, i) => {
        return {
          x: e.query,
          y: e.value,
        }
        });
          // update the series with axios data
        this.series = [
            {
              name: "Rising Query",
              data: formattedData,
            }
        ]
      })
      .catch(err => {
        console.log(err)
      })
    }
  },
  created() {
    this.get_rising_query();
  },
  filters: {
    truncateText: (text) => {
      if (text.length > 6) {
        text = text.substring(0, 6) + "...";
      }
      return text;
    }
  }
}
</script>
<style scoped>
</style>