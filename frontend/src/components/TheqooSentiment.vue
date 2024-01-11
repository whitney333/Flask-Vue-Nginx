<template>
  <div id="sentiment-chart">
    <apexchart
      type="donut"
      :options="chartOptions"
      :series="series"
      width="100%"
      height="100%"
    ></apexchart>
  </div>
</template>
<script>
import VueApexCharts from "vue-apexcharts";
export default {
  name: "TheqooSentiment",
  components: {
    apexchart: VueApexCharts
  },
  data() {
    return {
      series: [10, 45, 45],
      chartOptions: {
        chart: {
          type: 'donut',
        },
        height: '100%',
        width: '100%',
        plotOptions: {
          pie: {
            startAngle: 0,
            endAngle: 360,
            customScale: 1.2,
            dataLabels: {
              offset: 0,
              minAngleToShowLabel: 10
            },
            donut: {
              size: '100%',
              background: 'transparent',
              labels: {
                show: true,
                // name: {
                //   show: true,
                //   fontSize: '20px',
                //   fontFamily: 'Helvetica, Arial, sans-serif',
                //   fontWeight: 600,
                //   color: undefined,
                //   offsetY: 0,
                //   formatter: function (val) {
                //     return val
                //   }
                // },
                // value: {
                //   show: true,
                //   fontSize: '16px',
                //   fontFamily: 'Helvetica, Arial, sans-serif',
                //   fontWeight: 400,
                //   color: undefined,
                //   offsetY: 16,
                //   formatter: function (val) {
                //     return val
                //   }
                // }
              }
            }
          }
        },
        dataLabels: {
          enabled: false,
        },
        colors: ['#981111', '#ec802a', '#27ad0c'],
        legend: {
          position: 'bottom',
          horizontalAlign: 'center',
          itemMargin: {
            horizontal: 15,
            vertical: 0
          },
        },
        responsive: [{
          breakpoint: 300,
          options: {
            chart: {
              width: 300
            },
            legend: {
              position: 'bottom'
            }
          }
        }]
      }
    }
  },
  methods: {

  },
  created() {

  }
}
</script>
<style scoped>
</style>