import type { Session, Message, CreateSessionRequest, SendMessageRequest } from '@/types/chat'
import request from '@/utils/request'

const baseUrl = '/api/v1/chat'

export const chatApi = {
  // 获取会话列表
  getSessions(): Promise<Session[]> {
    return request.get(`${baseUrl}/sessions`)
  },

  // 创建新会话
  createSession(data: CreateSessionRequest): Promise<Session> {
    return request.post(`${baseUrl}/sessions`, data)
  },

  // 重命名会话
  renameSession(sessionId: number, sessionName: string): Promise<Session> {
    return request.put(`${baseUrl}/sessions/${sessionId}`, { session_name: sessionName })
  },

  // 删除会话
  deleteSession(sessionId: number): Promise<void> {
    return request.delete(`${baseUrl}/sessions/${sessionId}`)
  },

  // 获取会话消息
  getMessages(sessionId: number): Promise<Message[]> {
    return request.get(`${baseUrl}/sessions/${sessionId}/messages`)
  },

  // 发送消息
  sendMessage(sessionId: number, data: SendMessageRequest): Promise<Message> {
    return request.post(`${baseUrl}/sessions/${sessionId}/messages`, data)
  }
}

export const exportSession = async (sessionId: number): Promise<Blob> => {
  const response = await request.get(`${baseUrl}/sessions/${sessionId}/export`, {
    responseType: 'blob'
  })
  return response.data
}