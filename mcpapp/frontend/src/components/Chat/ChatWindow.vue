<template>
  <div class="chat-window">
    <div class="chat-header">
      <h2>{{ currentSession?.title || '新的对话' }}</h2>
    </div>
    
    <div class="chat-messages" ref="messagesContainer">
      <div v-for="message in messages" :key="message.id" class="message" :class="message.messageType">
        <div class="message-content">
          {{ message.content }}
        </div>
        <div class="message-time">
          {{ formatTime(message.createdAt) }}
        </div>
      </div>
    </div>

    <div class="chat-input">
      <el-input
        v-model="userInput"
        type="textarea"
        :rows="3"
        placeholder="请输入消息..."
        @keyup.enter.ctrl="sendMessage"
      />
      <el-button 
        type="primary" 
        :loading="loading"
        @click="sendMessage"
      >
        发送
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, watch } from 'vue'
import { useChatStore } from '@/stores/chat'
import { storeToRefs } from 'pinia'
import { ElMessage } from 'element-plus'
import dayjs from 'dayjs'

const chatStore = useChatStore()
const { messages, currentSession, loading } = storeToRefs(chatStore)

const userInput = ref('')
const messagesContainer = ref<HTMLElement>()

// 发送消息
const sendMessage = async () => {
  if (!userInput.value.trim()) {
    ElMessage.warning('请输入消息内容')
    return
  }

  try {
    await chatStore.sendUserMessage(userInput.value)
    userInput.value = ''
  } catch (error) {
    console.error('发送消息失败:', error)
  }
}

// 格式化时间
const formatTime = (time: string) => {
  return dayjs(time).format('YYYY-MM-DD HH:mm:ss')
}

// 监听消息列表变化,自动滚动到底部
watch(messages, () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
})

// 组件挂载时滚动到底部
onMounted(() => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
})
</script>

<style scoped>
.chat-window {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
}

.chat-header {
  padding: 16px;
  border-bottom: 1px solid #eee;
  
  h2 {
    margin: 0;
    font-size: 18px;
    color: #333;
  }
}

.chat-messages {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
}

.message {
  margin-bottom: 16px;
  max-width: 80%;
  
  &.user {
    margin-left: auto;
    
    .message-content {
      background: #409EFF;
      color: #fff;
    }
  }
  
  &.assistant {
    margin-right: auto;
    
    .message-content {
      background: #f4f4f5;
      color: #333;
    }
  }
}

.message-content {
  padding: 12px 16px;
  border-radius: 8px;
  word-break: break-word;
}

.message-time {
  margin-top: 4px;
  font-size: 12px;
  color: #999;
  text-align: right;
}

.chat-input {
  padding: 16px;
  border-top: 1px solid #eee;
  
  .el-button {
    margin-top: 8px;
    width: 100%;
  }
}
</style> 