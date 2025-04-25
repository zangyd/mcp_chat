from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, Text, JSON, ForeignKey, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class ServerStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class CallStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"

class MCPServer(Base):
    __tablename__ = "mcp_servers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, comment="服务器名称")
    description = Column(Text, nullable=True, comment="服务器描述")
    status = Column(SQLAlchemyEnum(ServerStatus), default=ServerStatus.ACTIVE, comment="服务器状态")
    config = Column(JSON, nullable=True, comment="服务器配置")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")

    # 关联关系
    calls = relationship("ServerCall", back_populates="server", cascade="all, delete-orphan")

class ServerCall(Base):
    __tablename__ = "server_calls"

    id = Column(Integer, primary_key=True, index=True)
    server_id = Column(Integer, ForeignKey("mcp_servers.id"), nullable=False, comment="服务器ID")
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False, comment="会话ID")
    tool_name = Column(String(100), nullable=False, comment="工具名称")
    parameters = Column(JSON, nullable=True, comment="调用参数")
    result = Column(JSON, nullable=True, comment="调用结果")
    status = Column(SQLAlchemyEnum(CallStatus), default=CallStatus.PENDING, comment="调用状态")
    error_message = Column(Text, nullable=True, comment="错误信息")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")

    # 关联关系
    server = relationship("MCPServer", back_populates="calls")
    session = relationship("ChatSession") 