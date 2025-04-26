from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class User(Base):
    """用户表"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="主键ID")
    username = Column(String(50), unique=True, nullable=False, comment="用户名")
    email = Column(String(100), unique=True, nullable=False, comment="邮箱")
    hashed_password = Column(String(200), nullable=False, comment="加密后的密码")
    is_active = Column(Boolean, default=True, comment="是否激活")
    is_superuser = Column(Boolean, default=False, comment="是否是超级用户")
    avatar = Column(String(200), nullable=True, comment="头像URL")
    phone = Column(String(20), unique=True, nullable=True, comment="手机号")
    full_name = Column(String(100), nullable=True, comment="全名")
    created_at = Column(DateTime, nullable=False, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关联
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan") 