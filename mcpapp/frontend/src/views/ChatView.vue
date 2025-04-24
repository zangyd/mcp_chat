<template>
  <div class="chat-container">
    <el-container>
      <el-aside width="300px">
        <ChatSessionList
          :sessions="sessions"
          :active-session-id="currentSessionId"
          @new-session="handleNewSession"
          @select-session="handleSelectSession"
          @rename-session="handleRenameSession"
          @export-session="handleExportSession"
          @delete-session="handleDeleteSession"
        />
      </el-aside>
      <el-main>
        <div v-if="currentSession" class="chat-main">
          <div class="chat-header">
            <h2>{{ currentSession.title }}</h2>
            <div class="header-actions">
              <el-button
                :icon="Refresh"
                circle
                @click="handleRefresh"
              />
              <el-button
                :icon="Setting"
                circle
                @click="showSettings = true"
              />
            </div>
          </div>
          <div class="chat-messages" ref="messagesRef">
            <el-scrollbar>
              <div class="messages-container">
                <ChatMessage
                  v-for="message in currentSession.messages"
                  :key="message.id"
                  :message="message"
                  @retry="handleRetry"
                />
              </div>
            </el-scrollbar>
          </div>
          <ChatInput
            :sending="sending"
            :tools="availableTools"
            placeholder="输入消息，Shift + Enter换行"
            @send="handleSend"
            @upload="handleUpload"
            @use-tool="handleUseTool"
          />
        </div>
        <div v-else class="empty-state">
          <el-empty description="选择或创建一个会话开始聊天" />
          <el-button type="primary" @click="handleNewSession">
            新建会话
          </el-button>
        </div>
      </el-main>
    </el-container>

    <!-- 设置对话框 -->
    <el-dialog
      v-model="showSettings"
      title="会话设置"
      width="500px"
    >
      <el-form label-position="top">
        <el-form-item label="会话名称">
          <el-input v-model="sessionTitle" />
        </el-form-item>
        <el-form-item label="模型设置">
          <el-select v-model="modelSettings.temperature" style="width: 100%">
            <el-option label="更精确" :value="0.3" />
            <el-option label="平衡" :value="0.7" />
            <el-option label="更有创造力" :value="1" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showSettings = false">取消</el-button>
        <el-button type="primary" @click="handleSaveSettings">
          保存
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'
import { Refresh, Setting } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { ChatSession, Message, MCPTool } from '@/types/chat'
import ChatSessionList from '@/components/ChatSessionList.vue'
import ChatMessage from '@/components/ChatMessage.vue'
import ChatInput from '@/components/ChatInput.vue'
import { useChatStore } from '@/stores/chat'

const chatStore = useChatStore()
const messagesRef = ref<HTMLElement>()
const showSettings = ref(false)
const sending = ref(false)
const sessionTitle = ref('')
const modelSettings = ref({
  temperature: 0.7
})

// 从store获取会话列表
const sessions = computed(() => chatStore.sessions)
const currentSessionId = computed(() => chatStore.currentSessionId)
const currentSession = computed(() => 
  sessions.value.find(s => s.id === currentSessionId.value)
)
const availableTools = computed(() => chatStore.availableTools)

// 监听消息变化，自动滚动到底部
watch(
  () => currentSession.value?.messages,
  async () => {
    await nextTick()
    if (messagesRef.value) {
      const scrollbar = messagesRef.value.querySelector('.el-scrollbar__wrap')
      if (scrollbar) {
        scrollbar.scrollTop = scrollbar.scrollHeight
      }
    }
  },
  { deep: true }
)

// 处理会话相关操作
const handleNewSession = () => {
  chatStore.createSession()
}

const handleSelectSession = (id: string) => {
  chatStore.setCurrentSession(id)
}

const handleRenameSession = async (id: string) => {
  try {
    const { value: newTitle } = await ElMessageBox.prompt(
      '请输入新的会话名称',
      '重命名会话',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputValue: currentSession.value?.title
      }
    )
    if (newTitle) {
      chatStore.renameSession(id, newTitle)
    }
  } catch {}
}

const handleExportSession = (id: string) => {
  const session = sessions.value.find(s => s.id === id)
  if (!session) return
  
  const content = JSON.stringify(session, null, 2)
  const blob = new Blob([content], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `${session.title}.json`
  link.click()
  URL.revokeObjectURL(url)
}

const handleDeleteSession = async (id: string) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除这个会话吗？此操作不可恢复。',
      '删除会话',
      {
        type: 'warning'
      }
    )
    chatStore.deleteSession(id)
  } catch {}
}

// 处理消息相关操作
const handleSend = async (content: string) => {
  if (!currentSessionId.value) return
  
  sending.value = true
  try {
    await chatStore.sendMessage({
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date().toISOString()
    })
  } catch (error) {
    ElMessage.error('发送消息失败')
  } finally {
    sending.value = false
  }
}

const handleRetry = async (message: Message) => {
  if (!currentSessionId.value) return
  
  sending.value = true
  try {
    await chatStore.retryMessage(message)
  } catch (error) {
    ElMessage.error('重试失败')
  } finally {
    sending.value = false
  }
}

const handleUpload = () => {
  // 实现文件上传逻辑
}

const handleUseTool = (tool: MCPTool) => {
  // 实现工具使用逻辑
}

const handleRefresh = () => {
  // 实现刷新逻辑
}

const handleSaveSettings = () => {
  if (!currentSessionId.value) return
  
  chatStore.updateSessionSettings(currentSessionId.value, {
    title: sessionTitle.value,
    modelSettings: modelSettings.value
  })
  showSettings.value = false
}

// 监听设置对话框的显示状态
watch(showSettings, (visible) => {
  if (visible && currentSession.value) {
    sessionTitle.value = currentSession.value.title
    // 加载其他设置
  }
})
</script>

<style scoped lang="scss">
.chat-container {
  height: 100vh;
  
  :deep(.el-container) {
    height: 100%;
  }
  
  .el-aside {
    border-right: 1px solid var(--el-border-color);
  }
  
  .chat-main {
    height: 100%;
    display: flex;
    flex-direction: column;
    
    .chat-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem;
      border-bottom: 1px solid var(--el-border-color);
      
      h2 {
        margin: 0;
      }
      
      .header-actions {
        display: flex;
        gap: 0.5rem;
      }
    }
    
    .chat-messages {
      flex-grow: 1;
      overflow: hidden;
      
      .messages-container {
        padding: 1rem;
      }
    }
  }
  
  .empty-state {
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 2rem;
  }
}
</style>