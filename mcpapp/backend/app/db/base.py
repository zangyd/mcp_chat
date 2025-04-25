from typing import Any
from datetime import datetime
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import Column, DateTime, Integer

@as_declarative()
class Base:
    """
    SQLAlchemy 模型的基类
    """
    id: Any
    __name__: str

    # 通用字段
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 生成表名
    @declared_attr
    def __tablename__(cls) -> str:
        """
        将类名转换为蛇形命名的表名
        例如: UserProfile -> user_profile
        """
        return cls.__name__.lower()

    def dict(self) -> dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns} 