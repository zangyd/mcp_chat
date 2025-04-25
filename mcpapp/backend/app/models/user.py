from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    """用户基础模型"""
    email: EmailStr
    username: str

class UserCreate(UserBase):
    """用户创建模型"""
    password: str

class UserResponse(UserBase):
    """用户响应模型"""
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class UserUpdate(UserBase):
    """更新用户请求模型"""
    password: Optional[str] = None

class User(UserBase):
    """用户响应模型"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    """Token响应模型"""
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Token数据模型"""
    sub: Optional[str] = None
    exp: Optional[datetime] = None 