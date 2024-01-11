import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import 'vuetify/dist/vuetify.min.css'
import './assets/css/bootstrap.min.css'
import './assets/css/styles.min.css'
import axios from 'axios'
import VueApexCharts from 'vue-apexcharts'
import i18n from './i18n'


Vue.config.productionTip = false
Vue.prototype.axios = axios;

Vue.use(VueApexCharts)
Vue.component('apexchart', VueApexCharts)
window.Apex.chart = { fontFamily: "Cairo, sans-serif" };

new Vue({
  router,
  store,
  vuetify,
  i18n,
  render: h => h(App)
}).$mount('#app')
