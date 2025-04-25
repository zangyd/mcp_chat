import request from '@/utils/request'
import type { Session, Message } from '@/types/chat'

const baseUrl = '/api/v1'

// 获取会话列表
export const getSessions = () => {
  return request.get<Session[]>(`${baseUrl}/chat/sessions`)
}

// 创建新会话
export const createSession = () => {
  return request.post<Session>(`${baseUrl}/chat/sessions`, {
    title: '新的会话'
  })
}

// 获取会话消息列表
export const getMessages = (sessionId: number) => {
  return request.get<Message[]>(`${baseUrl}/chat/sessions/${sessionId}/messages`)
}

// 发送消息
export const sendMessage = (sessionId: number, content: string) => {
  return request.post<Message>(`${baseUrl}/chat/sessions/${sessionId}/messages`, {
    content
  })
}