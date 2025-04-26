import { defineStore } from 'pinia'
import type { Session, Message, ChatState, CreateSessionRequest, SendMessageRequest } from '@/types/chat'
import { chatApi } from '@/api/chat'
import { ElMessageBox } from 'element-plus'

export const useChatStore = defineStore('chat', {
  state: (): ChatState => ({
    sessions: [],
    currentSession: null,
    messages: [],
    error: null,
    loading: false
  }),

  getters: {
    currentMessages: (state): Message[] => state.messages,
    hasError: (state): boolean => state.error !== null
  },

  actions: {
    // 加载会话列表
    async loadSessions() {
      this.loading = true
      try {
        const sessions = await chatApi.getSessions()
        this.sessions = sessions
        if (sessions.length > 0 && !this.currentSession) {
          this.currentSession = sessions[0]
          await this.loadMessages(sessions[0].id)
        }
        this.error = null
      } catch (error) {
        this.error = error instanceof Error ? error.message : '加载会话失败'
      } finally {
        this.loading = false
      }
    },

    // 创建新会话
    async createNewSession() {
      this.loading = true
      try {
        const session = await chatApi.createSession({
          title: '新的会话'
        })
        this.sessions.push(session)
        this.currentSession = session
        this.messages = []
        this.error = null
      } catch (error) {
        this.error = error instanceof Error ? error.message : '创建会话失败'
      } finally {
        this.loading = false
      }
    },

    // 设置当前会话
    async setCurrentSession(session: Session) {
      this.loading = true
      try {
        this.currentSession = session
        await this.loadMessages(session.id)
        this.error = null
      } catch (error) {
        this.error = error instanceof Error ? error.message : '切换会话失败'
      } finally {
        this.loading = false
      }
    },

    // 加载会话消息
    async loadMessages(sessionId: number) {
      this.loading = true
      try {
        const messages = await chatApi.getMessages(sessionId)
        this.messages = messages
        this.error = null
      } catch (error) {
        this.error = error instanceof Error ? error.message : '加载消息失败'
      } finally {
        this.loading = false
      }
    },

    // 发送用户消息
    async sendUserMessage(content: string) {
      if (!this.currentSession) return
      
      this.loading = true
      try {
        const messages = await chatApi.sendMessage(this.currentSession.id, { content })
        // 将返回的消息列表添加到当前消息列表中
        this.messages.push(...messages)
        this.error = null
      } catch (error) {
        this.error = error instanceof Error ? error.message : '发送消息失败'
      } finally {
        this.loading = false
      }
    },

    // 删除会话
    async deleteSession(sessionId: number) {
      try {
        // 弹出确认框
        await ElMessageBox.confirm('确定要删除这个会话吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })

        this.loading = true
        await chatApi.deleteSession(sessionId)
        
        // 从列表中移除
        this.sessions = this.sessions.filter(s => s.id !== sessionId)
        
        // 如果删除的是当前会话，切换到第一个会话
        if (this.currentSession?.id === sessionId) {
          if (this.sessions.length > 0) {
            await this.setCurrentSession(this.sessions[0])
          } else {
            this.currentSession = null
            this.messages = []
          }
        }
        
        this.error = null
      } catch (error) {
        if (error !== 'cancel') {
          this.error = error instanceof Error ? error.message : '删除会话失败'
        }
      } finally {
        this.loading = false
      }
    },

    // 清除错误
    clearError() {
      this.error = null
    }
  }
})