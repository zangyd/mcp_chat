from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.chat import SessionStatus

class Session(Base):
    """聊天会话表"""
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, index=True, comment="用户ID")
    title = Column(String(100), nullable=False, comment="会话标题")
    status = Column(SQLEnum(SessionStatus), nullable=False, default=SessionStatus.ongoing, comment="会话状态")
    created_at = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关联消息
    messages = relationship("Message", back_populates="session")

class Message(Base):
    """聊天消息表"""
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False, index=True, comment="会话ID")
    role = Column(String(20), nullable=False, comment="消息角色(user/assistant)")
    content = Column(String(4000), nullable=False, comment="消息内容")
    created_at = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")

    # 关联会话
    session = relationship("Session", back_populates="messages") 