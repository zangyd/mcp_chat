from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class MessageType(str, Enum):
    """消息类型枚举"""
    USER = "user"  # 用户消息
    ASSISTANT = "assistant"  # AI助手消息
    SYSTEM = "system"  # 系统消息

class SessionStatus(int, Enum):
    """会话状态枚举"""
    DELETED = 0  # 已删除
    ONGOING = 1  # 进行中
    COMPLETED = 2  # 已完成

class MessageRole(str, Enum):
    """消息角色枚举"""
    USER = "user"  # 用户
    ASSISTANT = "assistant"  # 助手
    SYSTEM = "system"  # 系统

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

    model_config = ConfigDict(from_attributes=True)

class MessageBase(BaseModel):
    """消息基础模型"""
    content: str

class MessageCreate(MessageBase):
    """创建消息请求模型"""
    pass

class MessageResponse(MessageBase):
    """消息响应模型"""
    id: int
    role: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Message(MessageBase):
    """消息模型"""
    id: int
    session_id: int
    role: MessageRole
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Session(SessionBase):
    """会话模型"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class SessionList(BaseModel):
    """会话列表响应模型"""
    total: int
    sessions: List[Session]

class MessageList(BaseModel):
    """消息列表响应模型"""
    total: int
    messages: List[Message]

class Session(Base):
    """
    聊天会话模型
    """
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="主键ID")
    title = Column(String(200), nullable=False, comment="会话标题")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, comment="所属用户ID")
    session_data = Column(JSON, nullable=True, comment="会话相关数据")
    created_at = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关联关系
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ChatSession {self.title}>"

class Message(Base):
    """
    聊天消息模型
    """
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="主键ID")
    session_id = Column(Integer, ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False, index=True, comment="会话ID")
    content = Column(Text, nullable=False, comment="消息内容")
    role = Column(String(20), nullable=False, comment="消息角色")
    created_at = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")
    
    # 关联关系
    session = relationship("Session", back_populates="messages")

    def __repr__(self):
        return f"<ChatMessage {self.role}: {self.content[:20]}...>" 