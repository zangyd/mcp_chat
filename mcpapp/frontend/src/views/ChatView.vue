<template>
  <div class="chat-container">
    <el-container>
      <el-aside width="300px">
        <div class="session-list">
          <el-button type="primary" class="new-chat" @click="handleNewSession">
            <el-icon><Plus /></el-icon>
            新建会话
          </el-button>
          <el-empty
            v-if="!sessions.length"
            description="暂无会话"
          >
            <el-button type="primary" @click="handleNewSession">
              创建第一个会话
            </el-button>
          </el-empty>
          <el-scrollbar v-else>
            <el-menu :default-active="currentSession?.id.toString()">
              <el-menu-item 
                v-for="session in sessions" 
                :key="session.id" 
                :index="session.id.toString()"
                @click="handleSelectSession(session)"
              >
                <div class="session-item">
                  <div class="session-info">
                    <el-icon class="session-icon"><ChatLineRound /></el-icon>
                    <div class="session-text">
                      <el-tooltip
                        :content="session.title || '新的会话'"
                        placement="top"
                        :show-after="1000"
                      >
                        <span class="session-title">{{ session.title || '新的会话' }}</span>
                      </el-tooltip>
                      <span class="session-time">{{ formatTime(session.created_at) }}</span>
                    </div>
                  </div>
                  <div class="session-actions">
                    <el-dropdown trigger="click" @command="handleSessionCommand($event, session)">
                      <el-button type="info" text>
                        <el-icon size="18"><More /></el-icon>
                      </el-button>
                      <template #dropdown>
                        <el-dropdown-menu>
                          <el-dropdown-item command="rename">
                            <el-icon><EditPen /></el-icon>
                            重命名
                          </el-dropdown-item>
                          <el-dropdown-item command="export">
                            <el-icon><Download /></el-icon>
                            导出记录
                          </el-dropdown-item>
                          <el-dropdown-item
                            command="delete"
                            divided
                            class="danger"
                          >
                            <el-icon><Delete /></el-icon>
                            删除
                          </el-dropdown-item>
                        </el-dropdown-menu>
                      </template>
                    </el-dropdown>
                  </div>
                </div>
              </el-menu-item>
            </el-menu>
          </el-scrollbar>
        </div>
      </el-aside>
      
      <el-container>
        <el-main>
          <div class="chat-main">
            <div v-if="!currentSession" class="chat-empty">
              <el-empty description="请选择或创建一个会话">
                <el-button type="primary" @click="handleNewSession">
                  创建新会话
                </el-button>
              </el-empty>
            </div>
            <template v-else>
              <div class="chat-messages" ref="messagesContainer">
                <el-empty 
                  v-if="!messages.length"
                  description="暂无消息"
                />
                <el-scrollbar v-else>
                  <div class="message-list">
                    <div 
                      v-for="message in messages" 
                      :key="message.id"
                      :class="['message', message.message_type]"
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
                  :disabled="loading"
                  @keydown.enter.prevent="handleSendMessage"
                />
                <el-button 
                  type="primary" 
                  :loading="loading"
                  :disabled="!messageInput.trim()"
                  @click="handleSendMessage"
                >
                  发送
                </el-button>
              </div>
            </template>
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
import { ChatLineRound, More, EditPen, Download, Delete, Plus } from '@element-plus/icons-vue'
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
const handleNewSession = async () => {
  await chatStore.createNewSession()
}

const handleSelectSession = (session: Session) => {
  chatStore.setCurrentSession(session)
}

const handleSessionCommand = async (command: string, session: Session) => {
  switch (command) {
    case 'rename':
      // TODO: 实现重命名功能
      break
    case 'export':
      // TODO: 实现导出功能
      break
    case 'delete':
      await chatStore.deleteSession(session.id)
      break
  }
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
onMounted(async () => {
  await chatStore.loadSessions()
  // 如果没有会话，自动创建一个
  if (!sessions.value.length) {
    await handleNewSession()
  }
})
</script>

<style scoped>
.chat-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.el-container {
  flex: 1;
  height: 100%;
}

.el-aside {
  background-color: var(--el-bg-color-page);
  border-right: 1px solid var(--el-border-color-light);
  display: flex;
  flex-direction: column;
}

.session-list {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 16px;
}

.new-chat {
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  height: 40px;
}

.session-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: 8px;
  border-radius: 6px;
  transition: all 0.3s;
}

.session-info {
  display: flex;
  align-items: center;
  gap: 12px;
  flex: 1;
  min-width: 0;
}

.session-icon {
  flex-shrink: 0;
  font-size: 18px;
}

.session-text {
  display: flex;
  flex-direction: column;
  min-width: 0;
  flex: 1;
}

.session-title {
  font-size: 14px;
  font-weight: 500;
  color: var(--el-text-color-primary);
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  line-height: 1.4;
}

.session-time {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  line-height: 1.2;
}

.session-actions {
  display: flex;
  align-items: center;
  opacity: 0.6;
  transition: opacity 0.2s;
  margin-left: 8px;
}

.el-menu-item {
  height: auto !important;
  line-height: 1.5 !important;
  padding: 4px !important;
  margin-bottom: 4px;
}

.el-menu-item.is-active .session-item {
  background-color: var(--el-color-primary-light-9);
}

.el-menu-item:hover .session-item {
  background-color: var(--el-fill-color-light);
}

.el-menu-item:hover .session-actions {
  opacity: 1;
}

.session-actions .el-button {
  padding: 8px;
  height: auto;
}

.session-actions .el-icon {
  margin-right: 0;
}

.el-dropdown-menu .el-icon {
  margin-right: 8px;
  font-size: 16px;
}

.danger {
  color: var(--el-color-danger);
}

.danger .el-icon {
  color: var(--el-color-danger);
}

.el-dropdown-item {
  display: flex;
  align-items: center;
  padding: 8px 16px;
}

.el-menu {
  border-right: none;
  background: none;
}

.chat-main {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.chat-empty {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
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
  padding: 12px;
  border-radius: 8px;
  max-width: 80%;
}

.message.user {
  align-self: flex-end;
  background-color: #e6f7ff;
}

.message.assistant {
  align-self: flex-start;
  background-color: #f5f5f5;
}

.message-content {
  white-space: pre-wrap;
  word-break: break-word;
}

.message-meta {
  font-size: 12px;
  color: #999;
  margin-top: 8px;
}

.chat-input {
  padding: 20px;
  border-top: 1px solid #e6e6e6;
  display: flex;
  gap: 16px;
}

.el-input {
  flex: 1;
}
</style>