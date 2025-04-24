import { defineStore } from 'pinia'
import type { ChatSession, Message, MCPTool } from '@/types/chat'
import { chatApi } from '@/api/chat'

export const useChatStore = defineStore('chat', {
  state: () => ({
    sessions: [] as ChatSession[],
    currentSessionId: null as string | null,
    availableTools: [] as MCPTool[],
    loading: false
  }),

  getters: {
    currentSession: (state) => 
      state.sessions.find(s => s.id === state.currentSessionId)
  },

  actions: {
    async initStore() {
      try {
        const [sessions, tools] = await Promise.all([
          chatApi.getSessions(),
          chatApi.getAvailableTools()
        ])
        this.sessions = sessions
        this.availableTools = tools
      } catch (error) {
        console.error('Failed to initialize store:', error)
      }
    },

    setCurrentSession(id: string) {
      this.currentSessionId = id
    },

    async createSession() {
      try {
        const newSession = await chatApi.createSession()
        this.sessions.push(newSession)
        this.currentSessionId = newSession.id
      } catch (error) {
        console.error('Failed to create session:', error)
        throw error
      }
    },

    async renameSession(id: string, title: string) {
      try {
        await chatApi.updateSession(id, { title })
        const session = this.sessions.find(s => s.id === id)
        if (session) {
          session.title = title
        }
      } catch (error) {
        console.error('Failed to rename session:', error)
        throw error
      }
    },

    async deleteSession(id: string) {
      try {
        await chatApi.deleteSession(id)
        const index = this.sessions.findIndex(s => s.id === id)
        if (index !== -1) {
          this.sessions.splice(index, 1)
        }
        if (this.currentSessionId === id) {
          this.currentSessionId = this.sessions[0]?.id || null
        }
      } catch (error) {
        console.error('Failed to delete session:', error)
        throw error
      }
    },

    async sendMessage(message: Message) {
      if (!this.currentSessionId) return

      try {
        const session = this.sessions.find(s => s.id === this.currentSessionId)
        if (!session) return

        // 添加用户消息
        session.messages.push({
          ...message,
          status: 'sending'
        })

        // 发送到服务器并等待回复
        const response = await chatApi.sendMessage(this.currentSessionId, message)

        // 更新消息状态
        const msgIndex = session.messages.findIndex(m => m.id === message.id)
        if (msgIndex !== -1) {
          session.messages[msgIndex].status = 'sent'
        }

        // 添加助手回复
        session.messages.push(response)
      } catch (error) {
        console.error('Failed to send message:', error)
        // 更新消息状态为错误
        const session = this.sessions.find(s => s.id === this.currentSessionId)
        if (session) {
          const msgIndex = session.messages.findIndex(m => m.id === message.id)
          if (msgIndex !== -1) {
            session.messages[msgIndex].status = 'error'
          }
        }
        throw error
      }
    },

    async retryMessage(message: Message) {
      if (!this.currentSessionId) return

      try {
        const session = this.sessions.find(s => s.id === this.currentSessionId)
        if (!session) return

        // 更新消息状态
        const msgIndex = session.messages.findIndex(m => m.id === message.id)
        if (msgIndex !== -1) {
          session.messages[msgIndex].status = 'sending'
        }

        // 重新发送消息
        const response = await chatApi.sendMessage(this.currentSessionId, message)

        // 更新消息状态
        if (msgIndex !== -1) {
          session.messages[msgIndex].status = 'sent'
        }

        // 添加助手回复
        session.messages.push(response)
      } catch (error) {
        console.error('Failed to retry message:', error)
        throw error
      }
    },

    async updateSessionSettings(id: string, settings: any) {
      try {
        await chatApi.updateSession(id, settings)
        const session = this.sessions.find(s => s.id === id)
        if (session) {
          Object.assign(session, settings)
        }
      } catch (error) {
        console.error('Failed to update session settings:', error)
        throw error
      }
    }
  }
})