<template>
  <div
    class="chat-message"
    :class="[
      message.role,
      { 'sending': message.status === 'sending' }
    ]"
  >
    <div class="message-avatar">
      <el-avatar :icon="message.role === 'user' ? 'User' : 'Assistant'" />
    </div>
    <div class="message-content">
      <div class="message-header">
        <span class="role">{{ message.role === 'user' ? '用户' : 'AI助手' }}</span>
        <span class="time">{{ formatTime(message.timestamp) }}</span>
      </div>
      <div class="message-body" v-html="formatContent(message.content)" />
      <div v-if="message.status === 'error'" class="message-error">
        <el-alert
          title="消息发送失败"
          type="error"
          show-icon
          :closable="false"
        >
          <template #default>
            <el-button size="small" @click="$emit('retry', message)">
              重试
            </el-button>
          </template>
        </el-alert>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Message } from '@/types/chat'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const props = defineProps<{
  message: Message
}>()

const emit = defineEmits<{
  (e: 'retry', message: Message): void
}>()

const formatTime = (timestamp: string) => {
  return new Date(timestamp).toLocaleString()
}

const formatContent = (content: string) => {
  // 使用marked处理Markdown，并用DOMPurify清理HTML
  return DOMPurify.sanitize(marked(content))
}
</script>

<style scoped lang="scss">
.chat-message {
  display: flex;
  margin: 1rem 0;
  padding: 1rem;
  gap: 1rem;
  
  &.user {
    background-color: var(--el-bg-color-page);
  }
  
  &.assistant {
    background-color: var(--el-bg-color);
  }
  
  &.sending {
    opacity: 0.7;
  }
  
  .message-avatar {
    flex-shrink: 0;
  }
  
  .message-content {
    flex-grow: 1;
    
    .message-header {
      display: flex;
      justify-content: space-between;
      margin-bottom: 0.5rem;
      
      .role {
        font-weight: bold;
      }
      
      .time {
        color: var(--el-text-color-secondary);
        font-size: 0.9em;
      }
    }
    
    .message-body {
      line-height: 1.6;
      
      :deep(pre) {
        background-color: var(--el-bg-color-page);
        padding: 1rem;
        border-radius: 4px;
        overflow-x: auto;
      }
      
      :deep(code) {
        background-color: var(--el-bg-color-page);
        padding: 0.2em 0.4em;
        border-radius: 3px;
      }
    }
    
    .message-error {
      margin-top: 0.5rem;
    }
  }
}
</style>