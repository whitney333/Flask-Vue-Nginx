import { createApp } from 'vue';
import './assets/main.css'
import App from './App.vue'
import router from './router'
import VueApexCharts from 'vue3-apexcharts'
// import i18n from './i18n'
import { createPinia } from 'pinia'
import { createI18n } from 'vue-i18n';
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'
import initI18n from './i18n'; // Path to your i18n setup file

// window.Apex.chart = { fontFamily: "Cairo, sans-serif" };

const vuetify = createVuetify({
    components,
    directives,
})

const setupApp = async () => {
    const i18n = await initI18n();
    
    const app = createApp(App);

    app.use(router);
    app.use(vuetify);
    app.use(VueApexCharts);
    app.use(i18n);
    app.use(createPinia())
    app.mount('#app');
    }

setupApp();

