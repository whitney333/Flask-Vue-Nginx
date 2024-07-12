import { createApp } from 'vue';
import App from './App.vue'
import router from './router'
import VueApexCharts from 'vue3-apexcharts'
// import i18n from './i18n'
import { createPinia } from 'pinia'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'

const app = createApp(App)

window.Apex.chart = { fontFamily: "Cairo, sans-serif" };

const vuetify = createVuetify({
    components,
    directives,
})

app.use(router);
app.use(vuetify);
app.use(VueApexCharts);
// app.use(i18n);
app.use(createPinia())

app.component('apexchart', VueApexCharts);

app.mount('#app');
