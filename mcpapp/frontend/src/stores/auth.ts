import { ref } from 'vue'
import { defineStore } from 'pinia'
import { login as loginApi, register as registerApi, getCurrentUser, type LoginData } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref<{
    id: number
    email: string
    username: string
  } | null>(null)
  
  // 设置token
  const setToken = (newToken: string) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }
  
  // 清除token
  const clearToken = () => {
    token.value = ''
    localStorage.removeItem('token')
    userInfo.value = null
  }
  
  // 登录
  const login = async (data: LoginData) => {
    try {
      const res = await loginApi(data)
      setToken(res.access_token)
      await fetchUserInfo()
    } catch (error: any) {
      clearToken()
      throw error
    }
  }
  
  // 注册
  const register = async (data: LoginData & { username: string }) => {
    const res = await registerApi(data)
    setToken(res.access_token)
    await fetchUserInfo()
  }
  
  // 获取用户信息
  const fetchUserInfo = async () => {
    if (!token.value) return
    try {
      userInfo.value = await getCurrentUser()
    } catch (error) {
      clearToken()
      throw error
    }
  }
  
  // 登出
  const logout = () => {
    clearToken()
  }
  
  return {
    token,
    userInfo,
    login,
    register,
    logout,
    fetchUserInfo
  }
}) 