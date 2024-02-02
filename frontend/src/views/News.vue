<template>
  <div class="main-body">
    <div class="main-content">
      <div class="section-overall bg-color2">
        <div class="row">
          <div class="col-lg-4 spacer">
            <div class="chart-box-2">
              <div class="section-header">
                <h3>Sentiment</h3>
                <button class="dots"></button>
              </div>
              <div class="chart">
                <img src="@/assets/img/chart13.svg" alt=""/>
              </div>
            </div>
          </div>
          <div class="col-lg-4 spacer">
            <div class="chart-box-2">
              <div class="section-header">
                <h3>Source</h3>
                <button class="dots"></button>
              </div>

            </div>
          </div>
          <div class="col-lg-4 spacer">
            <div class="chart-box-2">
              <div class="section-header">
                <h3>Sentiment by Source</h3>
                <button class="dots"></button>
              </div>
              <div class="chart">
                <img src="@/assets/img/chart15.svg" alt=""/>
              </div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-12">
            <div class="table-holder">

            </div>
          </div>
        </div>
      </div>
      <div class="section-overall">
        <div class="section-title">
          <h2>Keywords Analysis</h2>
        </div>
        <div class="row">
          <div class="col-12">
            <!-- TODO ADD KEYWORDS CHART-->
          </div>
        </div>
      </div>
      <div class="section-overall bg-color2">
        <div class="row">
          <div class="col-lg-6 spacer">
            <div class="chart-box-2">
              <div class="chart">
                <GoogleTrendRisingQuery/>
              </div>
            </div>
          </div>
          <div class="col-lg-6 spacer">
            <div class="chart-box-2">
              <div class="chart">
                <GoogleTrendWebRisingQuery/>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import GoogleTrendRisingQuery from "@/components/GoogleTrendRisingQuery";
import GoogleTrendWebRisingQuery from "@/components/GoogleTrendWebRisingQuery";
export default {
  name: "News",
  components: {GoogleTrendWebRisingQuery, GoogleTrendRisingQuery}
}
</script>
<style scoped>
</style>