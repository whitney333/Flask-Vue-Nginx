import { createApp } from 'vue';
import './assets/main.css'
import App from './App.vue'
import router from './router'
import VueApexCharts from 'vue3-apexcharts'
import firebase from './firebase';
import { createPinia } from 'pinia'
import piniaPluginPersistedstate  from 'pinia-plugin-persistedstate'
import { createI18n } from 'vue-i18n';
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'
import i18n from './i18n'; // Path to your i18n setup file
import './assets/tailwind.css'; // Import Tailwind

// window.Apex.chart = { fontFamily: "Cairo, sans-serif" };

const vuetify = createVuetify({
    components,
    directives,
})

firebase()
const app = createApp(App);
const pinia = createPinia();

pinia.use(piniaPluginPersistedstate);

app.use(router);
app.use(vuetify);
app.use(VueApexCharts);
app.use(i18n);
app.use(pinia);
app.mount('#app');


