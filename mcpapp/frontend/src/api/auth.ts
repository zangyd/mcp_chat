import request from '@/utils/request'

export interface LoginData {
  email: string
  password: string
}

export interface TokenResponse {
  access_token: string
}

export interface UserInfo {
  id: number
  email: string
  username: string
}

// 用户登录
export const login = (data: LoginData) => {
  const formData = new FormData()
  formData.append('username', data.email)
  formData.append('password', data.password)
  return request.post<TokenResponse>('/api/v1/auth/login', formData)
}

// 获取当前用户信息
export const getCurrentUser = () => {
  return request.get<UserInfo>('/api/v1/auth/me')
}

// 用户注册
export const register = (data: LoginData & { username: string }) => {
  return request.post<TokenResponse>('/api/v1/auth/register', data)
} 