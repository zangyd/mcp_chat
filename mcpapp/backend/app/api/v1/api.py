from fastapi import APIRouter

from app.api.v1 import auth, chat

api_router = APIRouter()

# 添加认证相关路由
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# 添加聊天相关路由
api_router.include_router(chat.router, prefix="/chat", tags=["chat"]) 