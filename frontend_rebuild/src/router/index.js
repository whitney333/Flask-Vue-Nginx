import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import AboutView from '@/views/AboutView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Dashboard',
      component: Dashboard
    },
    {
      path: '/about',
      name: 'About',
      component: AboutView
    },
    {
      path: '/sns/instagram',
      name: 'Instagram',
      component: AboutView
    },
    {
    path: '/sns/youtube',
    name: 'Youtube',
    component: AboutView,
    },
    {
      path: '/sns/tiktok',
      name: 'TikTok',
      component: AboutView,
    },  
    {
      path: '/sns/bilibili',
      name: 'Bilibili',
      component: AboutView,
      meta: {
        requireAuth: true,
        keepAlive: true
      }
    },
    {
      path: '/works/music',
      name: 'Music',
      component: AboutView,
      meta: {
        requireAuth: true,
        keepAlive: true
      }
    },
    {
      path: '/campaign/analytics',
      name: 'Campaign Analytics',
      component: AboutView,
    }
  ]
})

export default router
