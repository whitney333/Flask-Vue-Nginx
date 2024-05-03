<template>
  <div id="post-category">
    <apexchart
        ref="chart"
        width="100%"
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
  name: "CategoryPercentage",
  components: {
    apexchart: VueApexCharts,
  },
  data() {
    return {
      post_param: 12,
      series: [],
      chartOptions: {
        chart: {
          width: 380,
          type: 'pie',
        },
        labels: [],
        responsive: [{
          breakpoint: 480,
          options: {
            chart: {
              width: 200
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
    async get_instagram_post_cat() {
      this.post_param = 12
      await this.axios.get("/api/instagram/post/topic-prc?"
       + "post=" + this.post_param, {setTimeout: 10000})
      .then(res =>{
        this.result = res.data['result']['post']
        console.log(this.result)

        //
        for (let i = 0; i < this.result.length; i++) {
          this.data.series.push(this.result[i].value);
          this.data.chartOptions.labels.push(this.result[i].key);
        }

        // Format data correctly
        let post_cat = this.result.map((e, i) => {
          return {
            x: e.category,
            y: e.percentage,
          };
        });
        console.log(post_cat)

        // update the series with axios data
        // this.series = [
        //   {
        //     name: 'Percentage',
        //     data: post_cat,
        //   }
        // ];
        // console.log(this.series)
      })
      .catch(err =>{
        console.log(err)
      })
    }
  },
  created() {
    this.get_instagram_post_cat();
  },
  mounted() {
    this.get_instagram_post_cat();
  }
}
</script>
<style scoped>
</style>