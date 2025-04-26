export interface Session {
  id: number
  user_id: number
  title: string
  session_data?: Record<string, any>
  last_message?: string | null
  message_count?: number
  created_at: string
  updated_at?: string
}

export interface Message {
  id: number
  session_id: number
  message_type: 'user' | 'assistant' | 'system'
  content: string
  message_metadata?: Record<string, any>
  created_at: string
}

export interface ChatState {
  sessions: Session[]
  currentSession: Session | null
  messages: Message[]
  error: string | null
}

export interface ChatSession {
  id: string
  title: string
  messages: Message[]
  createdAt: string
  updatedAt: string
}

export interface MCPTool {
  name: string
  description: string
  parameters: Record<string, any>
}

export interface MCPServer {
  name: string
  description: string
  status: 'active' | 'inactive'
  tools: MCPTool[]
}

export interface ApiResponse<T> {
  code: number
  message: string
  data: T
}

export interface PaginatedResponse<T> {
  total: number
  items: T[]
  page: number
  pageSize: number
}

export interface CreateSessionRequest {
  title: string
}

export interface SendMessageRequest {
  content: string
  metadata?: Record<string, any>
}