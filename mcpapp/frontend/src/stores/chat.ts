import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Session, Message } from '@/types/chat'
import { ElMessage } from 'element-plus'
import { createSession, getSessions, getMessages, sendMessage } from '@/api/chat'

export const useChatStore = defineStore('chat', () => {
  // 状态
  const sessions = ref<Session[]>([])
  const currentSession = ref<Session | null>(null)
  const messages = ref<Message[]>([])
  const loading = ref(false)
  const error = ref('')

  // 方法
  const loadSessions = async () => {
    try {
      loading.value = true
      const response = await getSessions()
      sessions.value = response.data
      if (sessions.value.length > 0) {
        await setCurrentSession(sessions.value[0])
      }
    } catch (err) {
      error.value = '加载会话列表失败'
      ElMessage.error('加载会话列表失败')
    } finally {
      loading.value = false
    }
  }

  const createNewSession = async () => {
    try {
      loading.value = true
      const response = await createSession()
      const newSession = response.data
      sessions.value.unshift(newSession)
      await setCurrentSession(newSession)
    } catch (err) {
      error.value = '创建新会话失败'
      ElMessage.error('创建新会话失败')
    } finally {
      loading.value = false
    }
  }

  const setCurrentSession = async (session: Session) => {
    try {
      loading.value = true
      currentSession.value = session
      messages.value = []
      const response = await getMessages(session.id)
      messages.value = response.data
    } catch (err) {
      error.value = '加载会话消息失败'
      ElMessage.error('加载会话消息失败')
      currentSession.value = null
    } finally {
      loading.value = false
    }
  }

  const sendUserMessage = async (content: string) => {
    if (!currentSession.value) {
      ElMessage.warning('请先选择或创建一个会话')
      return
    }

    loading.value = true
    error.value = ''

    try {
      // 添加用户消息到列表
      const userMessage: Message = {
        id: Date.now().toString(),
        session_id: currentSession.value.id,
        content,
        role: 'user',
        created_at: new Date().toISOString()
      }
      messages.value.push(userMessage)

      // 发送消息到后端
      const response = await sendMessage(currentSession.value.id, content)
      const assistantMessage = response.data

      // 添加助手回复到列表
      messages.value.push(assistantMessage)
    } catch (err) {
      error.value = '发送消息失败'
      ElMessage.error('发送消息失败')
      // 移除临时添加的用户消息
      messages.value.pop()
    } finally {
      loading.value = false
    }
  }

  const clearError = () => {
    error.value = ''
  }

  return {
    // 状态
    sessions,
    currentSession,
    messages,
    loading,
    error,
    // 方法
    loadSessions,
    createNewSession,
    setCurrentSession,
    sendUserMessage,
    clearError
  }
})