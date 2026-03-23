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
import { AllCommunityModule, ModuleRegistry } from 'ag-grid-community';
import "/node_modules/ag-grid-community/styles/ag-theme-quartz.css";
// window.Apex.chart = { fontFamily: "Cairo, sans-serif" };
import { useAuthStore } from "@/stores/auth"

const vuetify = createVuetify({
    components,
    directives,
})

firebase()
const app = createApp(App);
const pinia = createPinia();


// register ag-grid
ModuleRegistry.registerModules([AllCommunityModule]);

pinia.use(piniaPluginPersistedstate);

app.use(router);
app.use(vuetify);
app.use(VueApexCharts);
app.use(i18n);
app.use(pinia);

if (import.meta.env.VITE_GA4_ID) {
  router.afterEach((to) => {
    if (typeof window.gtag === 'function') {
      window.gtag('event', 'page_view', {
        page_path: to.fullPath,
        page_title: document.title,
        page_location: window.location.href
      })
    }
  })
}

const authStore = useAuthStore()
authStore.init()

app.mount('#app');
