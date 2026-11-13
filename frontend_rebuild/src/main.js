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
import { loadGoogleAnalytics } from '@/libs/siteScripts.js'
import 'flag-icons/css/flag-icons.min.css'

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

// Google Analytics: only when VITE_GA4_ID is set. Set up synchronously (before the first
// route) so the first page view is queued; gtag.js itself loads async, so a blocker that
// blocks it cannot stop the app. The loader's file name is neutral on purpose (see siteScripts.js).
if (loadGoogleAnalytics(import.meta.env.VITE_GA4_ID)) {
  router.afterEach((to) => {
    if (typeof window.gtag === 'function') {
      // public share URLs carry a secret token: report the route pattern, never the real URL
      const pagePath = to.meta.public
        ? (to.matched[to.matched.length - 1]?.path || '/share')
        : to.fullPath
      window.gtag('event', 'page_view', {
        page_path: pagePath,
        // the share page title is the (confidential) event name, so send a fixed one
        page_title: to.meta.public ? 'Shared report' : document.title,
        page_location: to.meta.public ? `${window.location.origin}${pagePath}` : window.location.href
      })
    }
  })
}

const authStore = useAuthStore()
authStore.init()

app.mount('#app');
