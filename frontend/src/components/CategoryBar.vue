<template>
  <div id="post-category-by-eng-rate">
    <div class="toolbar">
    <v-row justify="start">
      <v-col cols="12">
        <v-list-item>
          <v-list-item-content class="mr-3">
            <v-select
                :items="all_post_limit"
                label="Select range"
                dense
                outlined
                v-model="selected_post_limit"
                item-color="orange darken-1"
                @click="update_data()"
            ></v-select>
          </v-list-item-content>
        </v-list-item>
      </v-col>
    </v-row>
  </div>
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
  name: "CategoryBar",
  components: {
    apexchart: VueApexCharts,
  },
  data() {
    return {
      selected_post_limit: "",
      post_limit: 10,
      all_post_limit: ["Latest 10 Posts", "Latest 30 Posts", "Overall"],
      series: [],
      chartOptions: {
        chart: {
          height: '356px',
          type: 'bar',
        },
        dataLabels: {
          // text inside bars
          enabled: false,
        },
        plotOptions: {
          bar: {
            borderRadius: 7,
            borderRadiusApplication: 'around',
            horizontal: true,
            columnWidth: '50%',
            distributed: true
          }
        },
        colors: ['#5BBCFF', '#FFFAB7', '#FFD1E3', '#7EA1FF', '#0C356A',
          '#80BCBD', '#AAD9BB', '#D5F0C1', '#0174BE', '#FFC436'],
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
    async get_default() {
      this.post_limit = 10
      await this.axios.get("/api/instagram/post/cat?"
          + "cat=" + this.post_limit, {setTimeout: 10000})
          .then(res => {
            this.result = res.data['result']['cat']
            // console.log(this.result)

            let _eng_rate_by_cat = this.result.map((e, i) => {
              return {
                x: e._id,
                y: e.eng_rate_by_cat,
              };
            });

            // update the series with axios data
            this.series = [
              {
                name: 'Engagement Rate',
                data: _eng_rate_by_cat,
              }
            ];
            // console.log(this.series)

          })
          .catch(err => {
            console.log(err)
          })
    },
    async update_data() {
      if (this.selected_post_limit === "Latest 10 Posts") {
        console.log(this.selected_post_limit)
        this.post_limit = 10
        await this.axios.get("/api/instagram/post/cat?"
            + "cat=" + this.post_limit, {setTimeout: 10000})
            .then(res => {
              this.result = res.data['result']['cat']
              // console.log(this.result)

              let _eng_rate_by_cat = this.result.map((e, i) => {
                return {
                  x: e._id,
                  y: e.eng_rate_by_cat,
                };
              });

              // update the series with axios data
              this.series = [
                {
                  name: 'Engagement Rate',
                  data: _eng_rate_by_cat,
                }
              ];
              // console.log(this.series)

            })
            .catch(err => {
              console.log(err)
            })
      } else if (this.selected_post_limit === "Latest 30 Posts") {
        console.log(this.selected_post_limit)
        this.post_limit = 30
        await this.axios.get("/api/instagram/post/cat?"
            + "cat=" + this.post_limit, {setTimeout: 10000})
            .then(res => {
              this.result = res.data['result']['cat']
              // console.log(this.result)

              let _eng_rate_by_cat = this.result.map((e, i) => {
                return {
                  x: e._id,
                  y: e.eng_rate_by_cat,
                };
              });

              // update the series with axios data
              this.series = [
                {
                  name: 'Engagement Rate',
                  data: _eng_rate_by_cat,
                }
              ];
              // console.log(this.series)

            })
            .catch(err => {
              console.log(err)
            })
      } else {
        console.log(this.selected_post_limit)
        this.post_limit = 0
        await this.axios.get("/api/instagram/post/cat?"
            + "cat=" + this.post_limit, {setTimeout: 10000})
            .then(res => {
              this.result = res.data['result']['cat']
              // console.log(this.result)

              let _eng_rate_by_cat = this.result.map((e, i) => {
                return {
                  x: e._id,
                  y: e.eng_rate_by_cat,
                };
              });

              // update the series with axios data
              this.series = [
                {
                  name: 'Engagement Rate',
                  data: _eng_rate_by_cat,
                }
              ];
              // console.log(this.series)

            })
            .catch(err => {
              console.log(err)
            })
      }
    }
  },
  created() {
    this.get_default();
  },
  computed() {
    this.update_data();
  }
}
</script>
<style scoped>
</style>
