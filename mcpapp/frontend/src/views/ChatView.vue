<template>
  <div class="chat-container">
    <el-container>
      <el-aside width="250px">
        <div class="session-list">
          <el-button type="primary" class="new-chat" @click="handleNewSession">
            新建会话
          </el-button>
          <el-scrollbar>
            <el-menu :default-active="currentSession?.id.toString()">
              <el-menu-item 
                v-for="session in sessions" 
                :key="session.id" 
                :index="session.id.toString()"
                @click="handleSelectSession(session)"
              >
                <el-icon><ChatLineRound /></el-icon>
                <span>{{ session.title || '新的会话' }}</span>
                <span class="session-time">{{ formatTime(session.created_at) }}</span>
              </el-menu-item>
            </el-menu>
          </el-scrollbar>
        </div>
      </el-aside>
      
      <el-container>
        <el-main>
          <div class="chat-main">
            <div class="chat-messages" ref="messagesContainer">
              <el-scrollbar>
                <div class="message-list">
                  <div 
                    v-for="message in messages" 
                    :key="message.id"
                    :class="['message', message.role]"
                  >
                    <div class="message-content">
                      {{ message.content }}
                    </div>
                    <div class="message-meta">
                      {{ formatTime(message.created_at) }}
                    </div>
                  </div>
                </div>
              </el-scrollbar>
            </div>
            
            <div class="chat-input">
              <el-input
                v-model="messageInput"
                type="textarea"
                :rows="3"
                placeholder="输入消息..."
                :disabled="!currentSession || loading"
                @keydown.enter.prevent="handleSendMessage"
              />
              <el-button 
                type="primary" 
                :loading="loading"
                :disabled="!currentSession || !messageInput.trim()"
                @click="handleSendMessage"
              >
                发送
              </el-button>
            </div>
          </div>
        </el-main>
      </el-container>
    </el-container>

    <!-- 错误提示 -->
    <el-dialog
      v-model="showError"
      title="错误"
      width="30%"
      @close="clearError"
    >
      <span>{{ error }}</span>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="clearError">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { ChatLineRound } from '@element-plus/icons-vue'
import { storeToRefs } from 'pinia'
import { useChatStore } from '@/stores/chat'
import type { Session } from '@/types/chat'
import dayjs from 'dayjs'

// 状态管理
const chatStore = useChatStore()
const { sessions, currentSession, messages, loading, error } = storeToRefs(chatStore)
const messageInput = ref('')
const messagesContainer = ref<HTMLElement | null>(null)

// 计算属性
const showError = computed({
  get: () => Boolean(error.value),
  set: (value) => {
    if (!value) {
      chatStore.clearError()
    }
  }
})

// 方法
const handleNewSession = () => {
  chatStore.createNewSession()
}

const handleSelectSession = (session: Session) => {
  chatStore.setCurrentSession(session)
}

const handleSendMessage = async () => {
  if (!messageInput.value.trim()) return
  
  const content = messageInput.value
  messageInput.value = ''
  
  await chatStore.sendUserMessage(content)
  scrollToBottom()
}

const formatTime = (time: string) => {
  return dayjs(time).format('YYYY-MM-DD HH:mm:ss')
}

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    const scrollbar = messagesContainer.value.querySelector('.el-scrollbar__wrap')
    if (scrollbar) {
      scrollbar.scrollTop = scrollbar.scrollHeight
    }
  }
}

const clearError = () => {
  chatStore.clearError()
}

// 监听消息变化，自动滚动到底部
watch(() => messages.value.length, scrollToBottom)

// 生命周期
onMounted(() => {
  chatStore.loadSessions()
})
</script>

<style scoped>
.chat-container {
  height: 100%;
}

.el-container {
  height: 100%;
}

.el-aside {
  background-color: #f5f7fa;
  border-right: 1px solid #e6e6e6;
}

.session-list {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.new-chat {
  margin: 16px;
}

.chat-main {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.chat-messages {
  flex: 1;
  overflow: hidden;
  padding: 20px;
}

.message-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.message {
  max-width: 80%;
  padding: 12px;
  border-radius: 8px;
}

.message.user {
  align-self: flex-end;
  background-color: #e6f7ff;
}

.message.assistant {
  align-self: flex-start;
  background-color: #f5f7fa;
}

.message.system {
  align-self: center;
  background-color: #fff0f0;
  font-style: italic;
}

.message-content {
  word-break: break-word;
}

.message-meta {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

.chat-input {
  padding: 20px;
  border-top: 1px solid #e6e6e6;
  display: flex;
  gap: 16px;
}

.chat-input .el-input {
  flex: 1;
}
</style>