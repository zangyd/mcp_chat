<template>
  <div class="chat-input">
    <div class="input-container">
      <el-input
        v-model="inputContent"
        type="textarea"
        :rows="3"
        :placeholder="placeholder"
        resize="none"
        @keydown.enter.prevent="handleEnter"
      />
      <div class="input-actions">
        <el-tooltip content="上传文件">
          <el-button
            :icon="Upload"
            circle
            @click="handleUpload"
          />
        </el-tooltip>
        <el-button
          type="primary"
          :loading="sending"
          @click="handleSend"
        >
          发送
        </el-button>
      </div>
    </div>
    <div class="tools-panel" v-if="showTools">
      <div class="tools-header">
        <h4>可用工具</h4>
        <el-button
          link
          type="primary"
          @click="showTools = false"
        >
          收起
        </el-button>
      </div>
      <div class="tools-list">
        <el-card
          v-for="tool in tools"
          :key="tool.name"
          class="tool-card"
          shadow="hover"
        >
          <template #header>
            <div class="tool-header">
              <span>{{ tool.name }}</span>
              <el-button
                link
                type="primary"
                @click="handleUseTool(tool)"
              >
                使用
              </el-button>
            </div>
          </template>
          <p>{{ tool.description }}</p>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Upload } from '@element-plus/icons-vue'
import type { MCPTool } from '@/types/chat'

const props = defineProps<{
  placeholder?: string
  sending?: boolean
  tools?: MCPTool[]
}>()

const emit = defineEmits<{
  (e: 'send', content: string): void
  (e: 'upload'): void
  (e: 'use-tool', tool: MCPTool): void
}>()

const inputContent = ref('')
const showTools = ref(false)

const handleSend = () => {
  if (!inputContent.value.trim()) return
  emit('send', inputContent.value)
  inputContent.value = ''
}

const handleEnter = (e: KeyboardEvent) => {
  if (e.shiftKey) return
  handleSend()
}

const handleUpload = () => {
  emit('upload')
}

const handleUseTool = (tool: MCPTool) => {
  emit('use-tool', tool)
}
</script>

<style scoped lang="scss">
.chat-input {
  border-top: 1px solid var(--el-border-color);
  padding: 1rem;
  
  .input-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    
    .input-actions {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
  }
  
  .tools-panel {
    margin-top: 1rem;
    
    .tools-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1rem;
      
      h4 {
        margin: 0;
      }
    }
    
    .tools-list {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 1rem;
      
      .tool-card {
        .tool-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
      }
    }
  }
}
</style>