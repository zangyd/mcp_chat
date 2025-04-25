from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.db.session import get_db
from app.models.chat import (
    SessionCreate,
    SessionResponse,
    MessageCreate,
    MessageResponse,
    SessionStatus
)

router = APIRouter()

@router.get("/sessions", response_model=List[SessionResponse])
def get_sessions(
    db: Session = Depends(get_db),
    user_id: int = 1  # TODO: 从认证中获取用户ID
):
    """获取用户的会话列表"""
    sessions = db.execute(
        """
        SELECT id, user_id, title, status, created_at, updated_at 
        FROM chat_sessions 
        WHERE user_id = :user_id AND status != 'deleted'
        ORDER BY updated_at DESC
        """,
        {"user_id": user_id}
    ).fetchall()
    
    return [
        {
            "id": session.id,
            "title": session.title,
            "status": session.status,
            "created_at": session.created_at,
            "updated_at": session.updated_at
        }
        for session in sessions
    ]

@router.post("/sessions", response_model=SessionResponse)
def create_session(
    session: SessionCreate,
    db: Session = Depends(get_db),
    user_id: int = 1  # TODO: 从认证中获取用户ID
):
    """创建新的会话"""
    now = datetime.now()
    result = db.execute(
        """
        INSERT INTO chat_sessions (user_id, title, status, created_at, updated_at)
        VALUES (:user_id, :title, :status, :created_at, :updated_at)
        RETURNING id, title, status, created_at, updated_at
        """,
        {
            "user_id": user_id,
            "title": session.title,
            "status": SessionStatus.ongoing.value,
            "created_at": now,
            "updated_at": now
        }
    )
    new_session = result.fetchone()
    
    return {
        "id": new_session.id,
        "title": new_session.title,
        "status": new_session.status,
        "created_at": new_session.created_at,
        "updated_at": new_session.updated_at
    }

@router.get("/sessions/{session_id}/messages", response_model=List[MessageResponse])
def get_messages(
    session_id: int,
    db: Session = Depends(get_db),
    user_id: int = 1  # TODO: 从认证中获取用户ID
):
    """获取会话的消息列表"""
    # 验证会话归属
    session = db.execute(
        "SELECT id FROM chat_sessions WHERE id = :session_id AND user_id = :user_id",
        {"session_id": session_id, "user_id": user_id}
    ).fetchone()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
        
    messages = db.execute(
        """
        SELECT id, role, content, created_at
        FROM chat_messages 
        WHERE session_id = :session_id
        ORDER BY created_at ASC
        """,
        {"session_id": session_id}
    ).fetchall()
    
    return [
        {
            "id": message.id,
            "role": message.role,
            "content": message.content,
            "created_at": message.created_at
        }
        for message in messages
    ]

@router.post("/sessions/{session_id}/messages", response_model=MessageResponse)
async def send_message(
    session_id: int,
    message: MessageCreate,
    db: Session = Depends(get_db),
    user_id: int = 1  # TODO: 从认证中获取用户ID
):
    """发送新消息并获取助手回复"""
    # 验证会话归属和状态
    session = db.execute(
        """
        SELECT id, status 
        FROM chat_sessions 
        WHERE id = :session_id AND user_id = :user_id
        """,
        {"session_id": session_id, "user_id": user_id}
    ).fetchone()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.status != SessionStatus.ongoing.value:
        raise HTTPException(status_code=400, detail="Session is not active")
    
    # 保存用户消息
    now = datetime.now()
    result = db.execute(
        """
        INSERT INTO chat_messages (session_id, role, content, created_at)
        VALUES (:session_id, :role, :content, :created_at)
        RETURNING id, role, content, created_at
        """,
        {
            "session_id": session_id,
            "role": "user",
            "content": message.content,
            "created_at": now
        }
    )
    db.commit()
    
    user_message = result.fetchone()
    
    # TODO: 调用大模型获取回复
    assistant_reply = "这是一个测试回复"  # 临时占位
    
    # 保存助手回复
    result = db.execute(
        """
        INSERT INTO chat_messages (session_id, role, content, created_at)
        VALUES (:session_id, :role, :content, :created_at)
        RETURNING id, role, content, created_at
        """,
        {
            "session_id": session_id,
            "role": "assistant",
            "content": assistant_reply,
            "created_at": datetime.now()
        }
    )
    db.commit()
    
    assistant_message = result.fetchone()
    
    # 更新会话时间
    db.execute(
        "UPDATE chat_sessions SET updated_at = :now WHERE id = :session_id",
        {"now": datetime.now(), "session_id": session_id}
    )
    db.commit()
    
    return {
        "id": assistant_message.id,
        "role": assistant_message.role,
        "content": assistant_message.content,
        "created_at": assistant_message.created_at
    } 