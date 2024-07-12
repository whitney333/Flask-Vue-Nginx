import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '@/views/AboutView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Dashboard',
      component: HomeView
    },
    {
      path: '/about',
      name: 'About',
      component: AboutView
    },
    {
      path: '/sns',
      name: 'Sns',
      component: HomeView
    },
    {
      path: '/works',
      name: 'Works',
      component: HomeView
    },
    {
      path: '/campaign',
      name: 'Campaign',
      component: HomeView
    }
  ]
})

export default router