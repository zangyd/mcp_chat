from datetime import datetime
from typing import Any, Dict
from sqlalchemy import Column, DateTime, Integer
from app.db.base_class import Base

class BaseModel(Base):
    """
    基础模型类，包含所有模型共用的字段
    """
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="主键ID")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment="更新时间")
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns} 