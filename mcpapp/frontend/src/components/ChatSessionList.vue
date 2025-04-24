<template>
  <div class="chat-session-list">
    <div class="list-header">
      <h3>会话列表</h3>
      <el-button
        type="primary"
        :icon="Plus"
        circle
        @click="$emit('new-session')"
      />
    </div>
    <el-scrollbar>
      <div class="sessions">
        <el-card
          v-for="session in sessions"
          :key="session.id"
          class="session-card"
          :class="{ active: session.id === activeSessionId }"
          shadow="hover"
          @click="$emit('select-session', session.id)"
        >
          <div class="session-info">
            <h4>{{ session.title }}</h4>
            <p class="time">{{ formatTime(session.updatedAt) }}</p>
          </div>
          <div class="session-actions">
            <el-dropdown trigger="click" @command="handleCommand($event, session.id)">
              <el-button :icon="More" circle />
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="rename">重命名</el-dropdown-item>
                  <el-dropdown-item command="export">导出记录</el-dropdown-item>
                  <el-dropdown-item
                    command="delete"
                    divided
                    class="danger"
                  >
                    删除
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-card>
      </div>
    </el-scrollbar>
  </div>
</template>

<script setup lang="ts">
import { Plus, More } from '@element-plus/icons-vue'
import type { ChatSession } from '@/types/chat'

const props = defineProps<{
  sessions: ChatSession[]
  activeSessionId?: string
}>()

const emit = defineEmits<{
  (e: 'new-session'): void
  (e: 'select-session', id: string): void
  (e: 'rename-session', id: string): void
  (e: 'export-session', id: string): void
  (e: 'delete-session', id: string): void
}>()

const formatTime = (timestamp: string) => {
  const date = new Date(timestamp)
  const now = new Date()
  
  if (date.toDateString() === now.toDateString()) {
    return date.toLocaleTimeString()
  }
  return date.toLocaleDateString()
}

const handleCommand = (command: string, sessionId: string) => {
  switch (command) {
    case 'rename':
      emit('rename-session', sessionId)
      break
    case 'export':
      emit('export-session', sessionId)
      break
    case 'delete':
      emit('delete-session', sessionId)
      break
  }
}
</script>

<style scoped lang="scss">
.chat-session-list {
  height: 100%;
  display: flex;
  flex-direction: column;
  
  .list-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    border-bottom: 1px solid var(--el-border-color);
    
    h3 {
      margin: 0;
    }
  }
  
  .sessions {
    padding: 1rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    
    .session-card {
      cursor: pointer;
      
      &.active {
        border-color: var(--el-color-primary);
      }
      
      :deep(.el-card__body) {
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
      
      .session-info {
        h4 {
          margin: 0;
          margin-bottom: 0.5rem;
        }
        
        .time {
          margin: 0;
          font-size: 0.9em;
          color: var(--el-text-color-secondary);
        }
      }
    }
  }
}

.danger {
  color: var(--el-color-danger);
}
</style>