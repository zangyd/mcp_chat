import type { ChatSession, Message, MCPTool } from '@/types/chat'
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

export const chatApi = {
  async getSessions(): Promise<ChatSession[]> {
    const response = await api.get('/chat/sessions')
    return response.data
  },

  async createSession(): Promise<ChatSession> {
    const response = await api.post('/chat/sessions', {
      title: '新会话'
    })
    return response.data
  },

  async updateSession(id: string, data: Partial<ChatSession>): Promise<void> {
    await api.patch(`/chat/sessions/${id}`, data)
  },

  async deleteSession(id: string): Promise<void> {
    await api.delete(`/chat/sessions/${id}`)
  },

  async sendMessage(sessionId: string, message: Message): Promise<Message> {
    const response = await api.post(`/chat/sessions/${sessionId}/messages`, message)
    return response.data
  },

  async getAvailableTools(): Promise<MCPTool[]> {
    const response = await api.get('/mcp/tools')
    return response.data
  }
}