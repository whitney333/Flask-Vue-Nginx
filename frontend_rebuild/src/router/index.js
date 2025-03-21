import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '@/views/Dashboard/DashboardView.vue'
import TrendingArtistsView from '@/views/TrendingArtists/TrendingArtistsView.vue'
import ArtistView from '@/views/TrendingArtists/ArtistView.vue'
import SNS_InstaView from '@/views/SNS/SNS_InstaView.vue'
import SNS_TiktokView from '@/views/SNS/SNS_TiktokView.vue'
import SNS_YoutubeView from '@/views/SNS/SNS_YoutubeView.vue'
import SNS_BilibiliView from '@/views/SNS/SNS_BilibiliView.vue'
import SNS_Layout from '@/layouts/SNS_Layout.vue'
import Auth_Layout from '@/layouts/Auth_Layout.vue'
import Work_MusicView from '@/views/Works/Work_MusicView.vue'
import LoginView from '@/views/Auth/LoginView.vue'
import { getAuth, onAuthStateChanged } from 'firebase/auth'
import Campaign_AnalyticsView from '@/views/Campaign/Campaign_AnalyticsView.vue'
import RegisterView from '@/views/Auth/RegisterView.vue'
import RegisterDetailsView from '@/views/Auth/RegisterDetailsView.vue'
import Works_Layout from '@/layouts/Works_Layout.vue'
import Campaign_PostsView from '@/views/Campaign/Campaign_PostsView.vue'
import Campaign_CreatePostView from '@/views/Campaign/Campaign_CreatePostView.vue'

const routes = [
    { path: '/', name: '', redirect: { path: "/dashboard" }, component: DashboardView,  meta: {requireAuth: true,}},
    { path: '/dashboard',  name: 'Dashboard',  component: DashboardView, meta: { requireAuth: true }},
    { path: '/auth', name: 'Auth',  component: Auth_Layout, 
      children: [
        { path: 'login', name: 'Login', component: LoginView }, 
        { path: 'register', name: 'Create Account', component: RegisterView},
        { path: 'register/details', name: 'Account Details', component: RegisterDetailsView, meta: { requireAuth: true, }}
      ]
    },
    { path: '/sns', name: 'Sns', component: SNS_Layout, meta: { requireAuth: true, },
      children: [
        { path: 'instagram', name: 'Instagram', component: SNS_InstaView, meta: { requireAuth: true,}},
        { path: 'youtube', name: 'Youtube', component: SNS_YoutubeView, meta: { requireAuth: true,}},
        { path: 'tiktok', name: 'TikTok', component: SNS_TiktokView, meta: { requireAuth: true, }},
        { path: 'bilibili', name: 'Bilibili', component: SNS_BilibiliView, meta: { requireAuth: true,}}
      ],
    },
    { path: '/works', name: 'Works', component: Works_Layout, meta: { requireAuth: true,},
      children: [
        { path: 'music', name: 'Music', component: Work_MusicView, },
      ]
    },
    { path: '/campaign', name: 'Campaign', component: Works_Layout, meta: { requireAuth: true,},
      children: [
        { path: 'analytics', name: 'Campaign Analytics', component: Campaign_AnalyticsView, meta: { requireAuth: true,}},
        { path: 'posts', name: 'Campaign Posts', component: Campaign_PostsView, meta: { requireAuth: true }},
        {path: 'posts/create', name: 'Campaign Create Posts', component: Campaign_CreatePostView, meta: { requireAuth: true }}
      ]
    },
    { path: '/trending-artists', name: 'Trending Artists', component: TrendingArtistsView, meta: { requireAuth: true, }},
    { path: '/artist/:artistId/:artistName', name: 'Artist', component: ArtistView, meta: { requireAuth: true,}}
  ]

  const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
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
    if (await getCurrentUser()) {
      next("/dashboard")
      // next()
    } else {
      next()
    }
  }
})

export default router
