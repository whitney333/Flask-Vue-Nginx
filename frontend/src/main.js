import { createApp } from 'vue';
import './assets/main.css'
import App from './App.vue'
import router from './router'
import VueApexCharts from 'vue3-apexcharts'
import firebase from './firebase';
import { createPinia } from 'pinia'
import { createI18n } from 'vue-i18n';
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'
import i18n from './i18n'; // Path to your i18n setup file
import PrimeVue from 'primevue/config';
import Aura from '@primevue/themes/aura';
import 'primeicons/primeicons.css';

// window.Apex.chart = { fontFamily: "Cairo, sans-serif" };

const vuetify = createVuetify({
    components,
    directives,
})

firebase()
const app = createApp(App);

app.use(PrimeVue, {
    theme: {
        preset: Aura,
        options: {
            prefix: 'p',
            darkModeSelector: 'light',
            cssLayer: false
        }
    }
});
app.use(router);
app.use(vuetify);
app.use(VueApexCharts);
app.use(i18n);
app.use(createPinia())
app.mount('#app');


