from datetime import datetime, timedelta
from typing import Any, Union
from passlib.context import CryptContext
from jose import jwt

from app.core.config import settings

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码
    
    Args:
        plain_password: 明文密码
        hashed_password: 加密后的密码

    Returns:
        bool: 密码是否匹配
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """获取密码哈希值
    
    Args:
        password: 明文密码

    Returns:
        str: 加密后的密码
    """
    return pwd_context.hash(password)

def create_access_token(
    subject: Union[str, Any],
    expires_delta: timedelta = None
) -> str:
    """创建访问令牌
    
    Args:
        subject: 令牌主题（通常是用户ID）
        expires_delta: 过期时间

    Returns:
        str: JWT令牌
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {
        "exp": expire,
        "sub": str(subject)
    }
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm="HS256"
    )
    
    return encoded_jwt 