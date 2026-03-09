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
