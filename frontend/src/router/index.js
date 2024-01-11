import Vue from 'vue'
import VueRouter from 'vue-router'
import Instagram from "@/views/Instagram";
import Dashboard from '../views/Dashboard.vue';
import Bilibili from '../views/Bilibili.vue';
import Tiktok from '../views/Tiktok';
import Campaign from "../views/Campaign";
import CampaignAnalytics from "../views/CampaignAnalytics";
import CreateCampaign from "../views/CreateCampaign";
import Music from "../views/Music";
import News from "../views/News";
import Sns from "../views/Sns";
import Works from "../views/Works";
import Youtube from "../views/Youtube";
import Login from "@/views/Login";


Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: {
      showNav: true
    }
  },
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: {
      requireAuth: true,
    }
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/sns',
    name: 'Sns',
    component: Sns,
    meta: {
      requireAuth: true,
      keepAlive: true
    }
  },
  {
    path: '/sns-bilibili',
    name: 'Bilibili',
    component: Bilibili,
    meta: {
      requireAuth: true,
      keepAlive: true
    }
  },
  {
    path: '/sns-instagram',
    name: 'Instagram',
    component: Instagram,
    meta: {
      requireAuth: true,
      keepAlive: true
    }
  },
  {
    path: '/sns-tiktok',
    name: 'Tiktok',
    component: Tiktok,
    meta: {
      requireAuth: true,
      keepAlive: true
    }
  },
  {
    path: '/sns-youtube',
    name: 'Youtube',
    component: Youtube,
    meta: {
      requireAuth: true,
      keepAlive: true
    }
  },
  {
    path: '/campaign',
    name: 'Campaign',
    component: Campaign,
    meta: {
      requireAuth: true,
      keepAlive: true
    }
  },
  {
    path: '/campaign-analytics',
    name: 'CampaignAnalytics',
    component: CampaignAnalytics,
    meta: {
      requireAuth: true,
      keepAlive: true
    }
  }, {
    path: '/create-campaign',
    name: ' CreateCampaign',
    component: CreateCampaign,
    meta: {
      requireAuth: true,
      keepAlive: true
    }
  },
  {
    path: '/works/music',
    name: 'Music',
    component: Music,
    meta: {
      requireAuth: true,
      keepAlive: true
    }
  },
  {
    path: '/works',
    name: 'Works',
    component: Works,
    meta: {
      requireAuth: true,
      keepAlive: true
    }
  },
  {
    path: '/news',
    name: 'News',
    component: News,
    meta: {
      requireAuth: true,
      keepAlive: true
    }
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  if (to.meta.requireAuth) { // 判断该路由是否需要登录权限
    if (localStorage.getItem('token')) { // 通过localStorage获取当前的token是否存在
      next()
    } else {
      next({
        path: '/login',
        query: { redirect: to.fullPath } // 将跳转的路由path作为参数，登录成功后跳转到该路由
      })
    }
  } else {
    next()
  }
})

export default router
