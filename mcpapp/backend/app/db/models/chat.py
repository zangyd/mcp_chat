from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, Float, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func, text
from app.db.base_class import Base
import enum

class MessageType(str, enum.Enum):
    """消息类型枚举"""
    USER = "user"  # 用户消息
    ASSISTANT = "assistant"  # AI助手消息
    SYSTEM = "system"  # 系统消息

class Message(Base):
    """聊天消息表"""
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="主键ID")
    session_id = Column(Integer, ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False, comment="所属会话ID")
    message_type = Column(String(50), nullable=False, comment="消息类型")
    content = Column(Text, nullable=False, comment="消息内容")
    message_metadata = Column(JSON, nullable=True, comment="消息元数据")
    created_at = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    is_active = Column(Boolean, nullable=False, server_default=text('1'), comment="是否有效")

    # 关联
    session = relationship("Session", back_populates="messages")

    def __repr__(self):
        return f"<Message {self.id}>"

    def get_metadata(self):
        """获取消息元数据"""
        return self.message_metadata

    def set_metadata(self, value):
        """设置消息元数据"""
        self.message_metadata = value

class Session(Base):
    """聊天会话表"""
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="主键ID")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="所属用户ID")
    title = Column(String(255), nullable=False, comment="会话标题")
    session_data = Column(JSON, nullable=True, comment="会话相关数据")
    created_at = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    is_active = Column(Boolean, nullable=False, server_default=text('1'), comment="是否有效")

    # 关联
    user = relationship("User", back_populates="sessions")
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")
    server_calls = relationship("ServerCall", back_populates="session", cascade="all, delete-orphan")

class MCPServer(Base):
    """MCP服务器信息表"""
    __tablename__ = "mcp_servers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="主键ID")
    name = Column(String(100), nullable=False, comment="服务器名称")
    description = Column(String(500), nullable=True, comment="服务器描述")
    host = Column(String(200), nullable=False, comment="服务器地址")
    port = Column(Integer, nullable=False, comment="服务器端口")
    status = Column(String(50), nullable=False, comment="服务器状态")
    capabilities = Column(JSON, nullable=True, comment="服务器能力描述")
    server_metadata = Column(JSON, nullable=True, comment="服务器元数据")
    response_time = Column(Float, nullable=True, comment="平均响应时间(ms)")
    success_rate = Column(Float, nullable=True, comment="成功率")
    server_load = Column(Float, nullable=True, comment="负载情况")
    created_at = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关联
    server_calls = relationship("ServerCall", back_populates="server", cascade="all, delete-orphan")

class ServerCall(Base):
    """服务器调用记录表"""
    __tablename__ = "server_calls"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="主键ID")
    server_id = Column(Integer, ForeignKey("mcp_servers.id", ondelete="CASCADE"), nullable=False, comment="服务器ID")
    session_id = Column(Integer, ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False, comment="关联的会话ID")
    message_id = Column(Integer, ForeignKey("chat_messages.id", ondelete="CASCADE"), nullable=True, comment="关联的消息ID")
    request_data = Column(JSON, nullable=True, comment="请求数据")
    response_data = Column(JSON, nullable=True, comment="响应数据")
    status = Column(String(50), nullable=False, comment="调用状态")
    error_message = Column(Text, nullable=True, comment="错误信息")
    response_time = Column(Float, nullable=True, comment="响应时间(ms)")
    created_at = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关联
    server = relationship("MCPServer", back_populates="server_calls")
    session = relationship("Session", back_populates="server_calls")
    message = relationship("Message", backref="server_calls") 