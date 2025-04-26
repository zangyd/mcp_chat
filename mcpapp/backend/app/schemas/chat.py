from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel
from app.db.models.chat import MessageType

class SessionBase(BaseModel):
    """会话基础模型"""
    title: str = "新会话"

class SessionCreate(SessionBase):
    """创建会话请求模型"""
    pass

class SessionResponse(SessionBase):
    """会话响应模型"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    last_message: Optional[str] = None
    message_count: Optional[int] = 0
    session_data: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

class MessageBase(BaseModel):
    """消息基础模型"""
    content: str

class MessageCreate(MessageBase):
    """创建消息请求模型"""
    metadata: Optional[Dict[str, Any]] = None

class MessageResponse(MessageBase):
    """消息响应模型"""
    id: int
    session_id: int
    message_type: str
    created_at: datetime
    updated_at: datetime
    message_metadata: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

class DeleteResponse(BaseModel):
    """删除响应模型"""
    success: bool
    message: str 