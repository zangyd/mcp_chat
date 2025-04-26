from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import text, func
from app.db.models.chat import Session as ChatSession, Message, MessageType

class ChatCRUD:
    """聊天相关数据库操作类"""

    def __init__(self, db: Session):
        self.db = db

    def get_session(self, session_id: int) -> Optional[ChatSession]:
        """获取单个会话"""
        return self.db.query(ChatSession)\
            .filter(ChatSession.id == session_id)\
            .filter(ChatSession.is_active == True)\
            .first()

    def get_user_sessions(self, user_id: int, skip: int = 0, limit: int = 10) -> List[ChatSession]:
        """获取用户的会话列表"""
        return self.db.query(ChatSession)\
            .filter(ChatSession.user_id == user_id)\
            .filter(ChatSession.is_active == True)\
            .order_by(ChatSession.updated_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()

    def create_session(self, user_id: int, title: str) -> ChatSession:
        """创建新会话"""
        session = ChatSession(user_id=user_id, title=title)
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def get_session_messages(self, session_id: int, skip: int = 0, limit: int = 50) -> List[Message]:
        """获取会话消息列表"""
        return self.db.query(Message)\
            .filter(Message.session_id == session_id)\
            .filter(Message.is_active == True)\
            .order_by(Message.created_at.asc())\
            .offset(skip)\
            .limit(limit)\
            .all()

    def get_session_last_message(self, session_id: int) -> Optional[Message]:
        """获取会话的最后一条消息"""
        return self.db.query(Message)\
            .filter(Message.session_id == session_id)\
            .filter(Message.is_active == True)\
            .order_by(Message.created_at.desc())\
            .first()

    def get_session_message_count(self, session_id: int) -> int:
        """获取会话的消息数量"""
        return self.db.query(func.count(Message.id))\
            .filter(Message.session_id == session_id)\
            .filter(Message.is_active == True)\
            .scalar() or 0

    def create_message(self, session_id: int, content: str, message_type: MessageType, metadata: Optional[Dict[str, Any]] = None) -> Message:
        """创建新消息"""
        message = Message(
            session_id=session_id,
            content=content,
            message_type=message_type,
            message_metadata=metadata if metadata else {}
        )
        
        self.db.add(message)
        
        # 更新会话的更新时间
        session = self.get_session(session_id)
        if session:
            session.updated_at = func.now()
        
        self.db.commit()
        self.db.refresh(message)
        return message

    def update_session_status(self, session_id: int, is_active: bool = True) -> bool:
        """更新会话状态（软删除）
        
        Args:
            session_id: 会话ID
            is_active: 是否激活，False表示删除
            
        Returns:
            bool: 更新是否成功
        """
        try:
            session = self.get_session(session_id)
            if not session:
                return False
                
            # 更新会话状态
            session.is_active = is_active
            session.updated_at = func.now()
            
            # 如果是删除操作，同时更新所有相关消息的状态
            if not is_active:
                self.db.query(Message)\
                    .filter(Message.session_id == session_id)\
                    .update({"is_active": False})
            
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Error updating session status: {e}")
            return False 