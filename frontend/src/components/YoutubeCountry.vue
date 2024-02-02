<template>
  <div id="youtube-audience-country">
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
  name: "YoutubeCountry",
  components: {
    apexchart: VueApexCharts,
  },
  data() {
    return {
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
          enabled: true,
          formatter: function (val) {
            return val + "%";
          },
          offsetY: 0,
          offsetX: 600,
          style: {
            fontSize: '12px',
            colors: ["#304758"]
          }
        },
        colors: ['#863af6', '#18E7F2', '#8EDB21', '#F29518', '#D4526E',
          '#4CAF50', '#5653FE', '#F86624', '#A5978B', '#2983FF'],
        // fill: {
        //   type: 'solid',
          // gradient: {
          //   shade: 'dark',
          //   type: "horizontal",
          //   shadeIntensity: 0.5,
          //   gradientToColors: undefined, // optional, if not defined - uses the shades of same color in series
          //   inverseColors: true,
          //   opacityFrom: 1,
          //   opacityTo: 1,
          //   stops: [0, 50, 100],
          //   colorStops: []
          // }
        // },
        grid: {
          show: true,
          yaxis: {
            lines: {
              show: true
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
            },
            dataLabels: {
              position: 'top', // top, center, bottom
            },
          }
        },
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
          type: 'numeric',
          max: 100,
          tickAmount: 5,
          axisBorder: {
            show: false
          }
        },
        tooltip: {
          theme: 'light',
          custom: function ({series, seriesIndex, dataPointIndex, w}) {
            // var data = w.globals.initialSeries[seriesIndex].data[dataPointIndex];
            return (
                '<div class="arrow_box">' +
                "<ul>" +
                "<span>" +
                "<li>" +
                w.globals.labels[dataPointIndex] +
                ": " +
                (series[seriesIndex][dataPointIndex]) +
                "%" +
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
    async get_youtube_country() {
      await this.axios.get('http://localhost/api/youtube/stats/country',
          {setTimeout: 10000})
      .then(res => {
        this.countries = res.data['result']
        // Format data correctly
        let country = this.countries.map((e, i) => {
          return {
            x: e.Name,
            y: e.percentage,
          };
        });

        // update the series with axios data
        this.series = [
          {
            name: 'Probability',
            data: country,
          }
        ];
      })
      .catch(err => {
        console.log(err)
      })
    }
  },
  created() {
    this.get_youtube_country();
  }
}
</script>
<style scoped>
</style>