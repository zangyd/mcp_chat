import axios from 'axios'
import type { AxiosInstance } from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'
import { useAuthStore } from '@/stores/auth'

// 创建axios实例
const service: AxiosInstance = axios.create({
  baseURL: '/',  // 修改baseURL，因为Vite已经配置了/api前缀
  timeout: 15000,
  withCredentials: true
})

// 请求拦截器
service.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    // 如果有token，添加到请求头
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    
    // 如果是FormData，让浏览器自动设置Content-Type
    if (config.data instanceof FormData) {
      delete config.headers['Content-Type']
    }
    
    // 调试信息
    console.log('Request Config:', {
      url: config.url,
      method: config.method,
      headers: config.headers,
      data: config.data
    })
    return config
  },
  (error) => {
    console.error('Request Error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  (response) => {
    // 调试信息
    console.log('Response Data:', response.data)
    return response.data
  },
  (error) => {
    console.error('Response Error:', error)
    console.error('Error Config:', error.config)
    console.error('Error Response:', error.response)
    
    if (error.response) {
      switch (error.response.status) {
        case 401:
          // 未授权，清除token并跳转到登录页
          const authStore = useAuthStore()
          authStore.clearToken()
          router.push({
            path: '/login',
            query: { redirect: router.currentRoute.value.fullPath }
          })
          ElMessage.error('登录已过期，请重新登录')
          break
          
        case 403:
          ElMessage.error('没有权限访问该资源')
          break
          
        case 404:
          ElMessage.error('请求的资源不存在')
          break
          
        case 500:
          ElMessage.error('服务器错误')
          break
          
        default:
          ElMessage.error(error.response.data?.detail || '请求失败')
      }
    } else if (error.request) {
      ElMessage.error('网络错误，请检查网络连接')
    } else {
      ElMessage.error('请求配置错误')
    }
    
    return Promise.reject(error)
  }
)

export default service 