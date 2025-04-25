from datetime import timedelta
from typing import Optional
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db import models
from app.models.user import UserCreate, Token
from app.utils.security import (
    verify_password,
    get_password_hash,
    create_access_token
)

class AuthService:
    """认证服务"""
    
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> Optional[models.User]:
        """通过邮箱获取用户
        
        Args:
            email: 用户邮箱

        Returns:
            Optional[models.User]: 用户对象
        """
        return self.db.query(models.User).filter(
            models.User.email == email
        ).first()

    def get_user_by_id(self, user_id: int) -> Optional[models.User]:
        """通过ID获取用户
        
        Args:
            user_id: 用户ID
            
        Returns:
            Optional[User]: 用户对象，不存在则返回None
        """
        return self.db.query(models.User).filter(
            models.User.id == user_id
        ).first()

    def authenticate_user(
        self,
        email: str,
        password: str
    ) -> Optional[models.User]:
        """验证用户
        
        Args:
            email: 用户邮箱
            password: 用户密码

        Returns:
            Optional[models.User]: 验证成功返回用户对象，失败返回None
        """
        user = self.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def create_user(self, user_in: UserCreate) -> models.User:
        """创建新用户
        
        Args:
            user_in: 用户创建请求模型

        Returns:
            models.User: 创建的用户对象
        """
        # 创建用户对象
        db_user = models.User(
            email=user_in.email,
            username=user_in.username,
            hashed_password=get_password_hash(user_in.password),
            is_active=True
        )
        
        # 保存到数据库
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        
        return db_user

    def create_token(self, user_id: int) -> Token:
        """创建访问令牌
        
        Args:
            user_id: 用户ID

        Returns:
            Token: 令牌对象
        """
        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        
        access_token = create_access_token(
            user_id,
            expires_delta=access_token_expires
        )
        
        return Token(access_token=access_token) 