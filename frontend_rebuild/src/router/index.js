import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '@/views/DashboardView.vue'
import AboutView from '@/views/AboutView.vue'
import TrendingArtistsView from '@/views/TrendingArtistsView.vue'
import ArtistView from '@/views/ArtistView.vue'
import SNS_InstaView from '@/views/SNS/SNS_InstaView.vue'
import SNS_TiktokView from '@/views/SNS/SNS_TiktokView.vue'
import SNS_YoutubeView from '@/views/SNS/SNS_YoutubeView.vue'
import SNS_BilibiliView from '@/views/SNS/SNS_BilibiliView.vue'
import MusicView from '@/views/Works/MusicView.vue'
import LoginView from '@/views/LoginView.vue'
import { getAuth, onAuthStateChanged } from 'firebase/auth'
import AnalyticsView from '@/views/Campaign/AnalyticsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: '',
      redirect: { path: "/dashboard" },
      component: DashboardView,
      meta: {
        requireAuth: true,
      }
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: DashboardView,
      meta: {
        requireAuth: true,
      }
    },
    {
      path: '/about',
      name: 'About',
      component: AboutView
    },
    {
      path: '/auth',
      name: 'Auth',
      children: [
        {
          path: 'login',
          name: 'Login',
          component: LoginView
        }
      ]

    },
    {
      path: '/sns',
      name: 'Sns',
      children: [
        
        {
          path: 'instagram',
          name: 'Instagram',
          component: SNS_InstaView,
          meta: {
            requireAuth: true,
          }

        },
        {
          path: 'youtube',
          name: 'Youtube',
          component: SNS_YoutubeView,
          meta: {
            requireAuth: true,
          }

        },
        {
          path: 'tiktok',
          name: 'TikTok',
          component: SNS_TiktokView,
          meta: {
            requireAuth: true,
          }
        },  
        {
          path: 'bilibili',
          name: 'Bilibili',
          component: SNS_BilibiliView,
          meta: {
            requireAuth: true,
          }
        }
      ]

    },
    {
      path: '/works',
      name: 'Works',
      children: [
        {
          path: 'music',
          name: 'Music',
          component: MusicView,
          meta: {
            requireAuth: true,
          }
        },
      ]
    },
    {
      path: '/campaign',
      name: 'Campaign',
      children: [
        {
          path: 'analytics',
          name: 'Campaign Analytics',
          component: AnalyticsView,
          meta: {
            requireAuth: true,
          }    
        },
      ]
    },
    {
      path: '/trending-artists',
      name: 'Trending Artists',
      component: TrendingArtistsView,
      meta: {
        requireAuth: true,
      }

    },
    {
      path: '/artist/:artistId/:artistName',
      name: 'Artist',
      component: ArtistView,
      meta: {
        requireAuth: true,
      }

    }
  ]
})

const getCurrentUser = () => {
  return new Promise((resolve, reject) => {
    const auth = getAuth()
    const removeListener = onAuthStateChanged(
      auth,
      (user) => {
        removeListener();
        resolve(user)
      },
      reject
    )
  })
}

router.beforeEach(async (to, from, next) => {
  if (to.matched.some((record) => record.meta.requireAuth)) {
    if (await getCurrentUser()) {
      next();
    } else {
      // alert("you dont have access!")
      next("/auth/login")
    }
  } else {
    next()
  }
})

export default router
