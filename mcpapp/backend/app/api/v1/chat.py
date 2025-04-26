from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.services.chat import ChatService
from app.schemas.chat import (
    SessionCreate,
    SessionResponse,
    MessageCreate,
    MessageResponse,
    DeleteResponse
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

@router.post("/sessions/{session_id}/messages", response_model=List[MessageResponse])
async def send_message(
    session_id: int,
    message: MessageCreate,
    db: Session = Depends(deps.get_db),
    current_user_id: int = Depends(deps.get_current_user_id)
):
    """发送消息并获取回复
    
    Args:
        session_id: 会话ID
        message: 消息内容
        db: 数据库会话
        current_user_id: 当前用户ID
        
    Returns:
        List[MessageResponse]: [用户消息, AI回复消息]
    """
    chat_service = ChatService(db)
    return await chat_service.send_message(session_id, message.content)

@router.delete("/sessions/{session_id}", response_model=DeleteResponse)
async def delete_session(
    session_id: int,
    db: Session = Depends(deps.get_db),
    current_user_id: int = Depends(deps.get_current_user_id)
):
    """删除会话
    
    Args:
        session_id: 会话ID
        db: 数据库会话
        current_user_id: 当前用户ID
        
    Returns:
        DeleteResponse: 删除结果
    
    Raises:
        HTTPException: 会话不存在或无权限删除
    """
    chat_service = ChatService(db)
    
    # 检查会话是否存在
    session = chat_service.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
        
    # 检查是否有权限删除
    if session.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="无权限删除此会话")
    
    # 删除会话
    success = chat_service.delete_session(session_id)
    if not success:
        raise HTTPException(status_code=500, detail="删除会话失败")
        
    return {"success": True, "message": "会话已删除"} 