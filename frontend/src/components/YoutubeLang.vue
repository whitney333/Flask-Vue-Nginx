<template>
  <div id="youtube-audience-language">
    <apexchart
        ref="chart"
        width="100%"
        :options="chartOptions"
        :series="series"
        height="400"
    >
    </apexchart>
  </div>
</template>
<script>
import VueApexCharts from "vue-apexcharts";
export default {
  name: "YoutubeLang",
  components: {
    apexchart: VueApexCharts,
  },
  data() {
    return {
      series: [],
      chartOptions: {
        chart: {
          height: '356px',
          type: 'bar',
          toolbar: {
            show: true
          },
          zoom: {
            enabled: true
          }
        },
        dataLabels: {
          enabled: true,
          formatter: function (val) {
            return val + "%";
          },
          offsetY: -25,
          style: {
            fontSize: '12px',
            colors: ["#304758"]
          }
        },
        plotOptions: {
          bar: {
            borderRadius: 7,
            borderRadiusApplication: 'around',
            columnWidth: '50%',
            dataLabels: {
              position: 'top', // top, center, bottom
            },
          }
        },
        colors: ['#10a3ff'],
        // legend: {
        //   show: false
        // },
        yaxis: {
          show: true,
          title: {
            text: 'Percentage (%)',
            style: {
              fontSize: '14px',
              fontWeight: 'bold',
              fontFamily: 'Cairo',
            }
          }
        },
        xaxis: {
          trim: true,
          labels: {
            rotate: 90,
            style: {
              fontSize: '14px',
              fontWeight: 'bold',
              fontFamily: 'Cairo',
            }
          }
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
    async get_youtube_language() {
      await this.axios.get('http://localhost/api/youtube/stats/language',
          {setTimeout: 10000})
      .then( res => {
        this.languages = res.data['results']
        // Format data correctly
        let lang = this.languages.map((e, i) => {
          return {
            x: e.name,
            y: e.percentage,
          };
        });

        // update the series with axios data
        this.series = [
          {
            name: 'Probability',
            data: lang,
          }
        ];
      })
      .catch( err => {
        console.log(err)
      })
    }
  },
  created() {
    this.get_youtube_language();
  }
}
</script>
<style scoped>
</style>
