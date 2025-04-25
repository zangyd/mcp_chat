import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/chat'
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue')
    },
    {
      path: '/chat',
      name: 'chat',
      component: () => import('@/views/ChatView.vue'),
      meta: { requiresAuth: true }
    }
  ]
})

// 路由守卫
router.beforeEach(async (to, from) => {
  const authStore = useAuthStore()
  
  // 如果需要认证
  if (to.meta.requiresAuth) {
    // 没有token，跳转到登录页
    if (!authStore.token) {
      return {
        path: '/login',
        query: { redirect: to.fullPath }
      }
    }
    
    // 有token但没有用户信息，尝试获取用户信息
    if (!authStore.userInfo) {
      try {
        await authStore.fetchUserInfo()
      } catch (error) {
        return {
          path: '/login',
          query: { redirect: to.fullPath }
        }
      }
    }
  }
})

export default router