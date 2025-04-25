from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.services.chat import ChatService
from app.schemas.chat import (
    SessionCreate,
    SessionResponse,
    MessageCreate,
    MessageResponse
)

router = APIRouter()

@router.get("/sessions", response_model=List[SessionResponse])
def get_sessions(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(deps.get_db),
    current_user_id: int = Depends(deps.get_current_user_id)
):
    """获取用户的会话列表"""
    chat_service = ChatService(db)
    sessions = chat_service.get_user_sessions(current_user_id, skip, limit)
    return sessions

@router.post("/sessions", response_model=SessionResponse)
def create_session(
    session: SessionCreate,
    db: Session = Depends(deps.get_db),
    current_user_id: int = Depends(deps.get_current_user_id)
):
    """创建新会话"""
    chat_service = ChatService(db)
    return chat_service.create_session(current_user_id, session.title)

@router.get("/sessions/{session_id}/messages", response_model=List[MessageResponse])
def get_messages(
    session_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(deps.get_db),
    current_user_id: int = Depends(deps.get_current_user_id)
):
    """获取会话消息列表"""
    chat_service = ChatService(db)
    messages = chat_service.get_session_messages(session_id, skip, limit)
    return messages

@router.post("/sessions/{session_id}/messages", response_model=MessageResponse)
async def send_message(
    session_id: int,
    message: MessageCreate,
    db: Session = Depends(deps.get_db),
    current_user_id: int = Depends(deps.get_current_user_id)
):
    """发送消息"""
    chat_service = ChatService(db)
    return await chat_service.send_message(session_id, message.content) 