from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.chat import Session as ChatSession, Message, MessageRole

class ChatCRUD:
    """聊天相关数据库操作类"""

    def __init__(self, db: Session):
        self.db = db

    def get_session(self, session_id: int) -> Optional[ChatSession]:
        """获取单个会话"""
        result = self.db.execute(
            text("""
            SELECT id, user_id, title, session_data, created_at, updated_at
            FROM chat_sessions
            WHERE id = :session_id
            """),
            {"session_id": session_id}
        ).fetchone()
        
        if result:
            return {
                "id": result.id,
                "user_id": result.user_id,
                "title": result.title,
                "session_data": result.session_data,
                "created_at": result.created_at,
                "updated_at": result.updated_at
            }
        return None

    def get_user_sessions(self, user_id: int, skip: int = 0, limit: int = 10) -> List[ChatSession]:
        """获取用户的会话列表"""
        results = self.db.execute(
            text("""
            SELECT id, user_id, title, session_data, created_at, updated_at
            FROM chat_sessions
            WHERE user_id = :user_id
            ORDER BY updated_at DESC
            LIMIT :limit OFFSET :skip
            """),
            {
                "user_id": user_id,
                "limit": limit,
                "skip": skip
            }
        ).fetchall()
        
        return [
            {
                "id": result.id,
                "user_id": result.user_id,
                "title": result.title,
                "session_data": result.session_data,
                "created_at": result.created_at,
                "updated_at": result.updated_at
            }
            for result in results
        ]

    def create_session(self, user_id: int, title: str) -> ChatSession:
        """创建新会话"""
        result = self.db.execute(
            text("""
            INSERT INTO chat_sessions (user_id, title)
            VALUES (:user_id, :title)
            RETURNING id, user_id, title, session_data, created_at, updated_at
            """),
            {
                "user_id": user_id,
                "title": title
            }
        ).fetchone()
        
        self.db.commit()
        
        return {
            "id": result.id,
            "user_id": result.user_id,
            "title": result.title,
            "session_data": result.session_data,
            "created_at": result.created_at,
            "updated_at": result.updated_at
        }

    def get_session_messages(self, session_id: int, skip: int = 0, limit: int = 50) -> List[Message]:
        """获取会话消息列表"""
        results = self.db.execute(
            text("""
            SELECT id, session_id, content, role, created_at
            FROM chat_messages
            WHERE session_id = :session_id
            ORDER BY created_at ASC
            LIMIT :limit OFFSET :skip
            """),
            {"session_id": session_id, "limit": limit, "skip": skip}
        ).fetchall()
        
        return [
            {
                "id": result.id,
                "session_id": result.session_id,
                "content": result.content,
                "role": result.role,
                "created_at": result.created_at
            }
            for result in results
        ]

    def create_message(self, session_id: int, content: str, role: MessageRole) -> Message:
        """创建新消息"""
        result = self.db.execute(
            text("""
            INSERT INTO chat_messages (session_id, content, role)
            VALUES (:session_id, :content, :role)
            RETURNING id, session_id, content, role, created_at
            """),
            {
                "session_id": session_id,
                "content": content,
                "role": role
            }
        ).fetchone()
        
        self.db.commit()
        
        return {
            "id": result.id,
            "session_id": result.session_id,
            "content": result.content,
            "role": result.role,
            "created_at": result.created_at
        } 