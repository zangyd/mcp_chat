export interface Session {
  id: number
  user_id: number
  title: string
  session_data?: any
  created_at: string
  updated_at: string
}

export interface Message {
  id: string
  session_id: number
  content: string
  role: 'user' | 'assistant' | 'system'
  created_at: string
}

export interface ChatState {
  sessions: Session[]
  currentSession: Session | null
  messages: Message[]
  loading: boolean
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