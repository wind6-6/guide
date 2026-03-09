import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../pages/Recommend/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { title: '景点推荐' }
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../pages/User/LoginView.vue'),
    meta: { title: '登录', public: true }
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('../pages/User/RegisterView.vue'),
    meta: { title: '注册', public: true }
  },
  {
    path: '/recommend',
    name: 'recommend',
    component: () => import('../pages/Recommend/RecommendView.vue'),
    meta: { title: '旅游推荐' }
  },
  {
    path: '/route-plan',
    name: 'routePlan',
    component: () => import('../pages/RoutePlan/RoutePlanView.vue'),
    meta: { title: '路线规划' }
  },
  {
    path: '/place-query',
    name: 'placeQuery',
    component: () => import('../pages/PlaceQuery/PlaceQueryView.vue'),
    meta: { title: '场所查询' }
  },
  {
    path: '/diary',
    name: 'diary',
    component: () => import('../pages/Diary/DiaryView.vue'),
    meta: { title: '旅游日记' }
  },
  {
    path: '/food',
    name: 'food',
    component: () => import('../pages/Food/FoodView.vue'),
    meta: { title: '美食推荐' }
  },
  {
    path: '/user',
    name: 'user',
    component: () => import('../pages/User/UserCenterView.vue'),
    meta: { title: '用户中心' }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = to.meta.title + ' - 个性化旅游系统'
  }
  
  // 检查是否需要登录
  const token = sessionStorage.getItem('token')
  if (!to.meta.public && !token) {
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
  } else {
    next()
  }
})

export default router
