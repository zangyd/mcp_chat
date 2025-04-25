from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.chat import Session as ChatSession, Message, MessageRole, SessionStatus
from app.db.crud.chat import ChatCRUD
from app.services.llm import LLMService

class ChatService:
    """聊天服务"""
    
    def __init__(self, db: Session):
        self.db = db
        self.crud = ChatCRUD(db)
        self.llm = LLMService()

    def get_user_sessions(
        self, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 10
    ) -> List[ChatSession]:
        """获取用户的会话列表"""
        return self.crud.get_user_sessions(user_id, skip, limit)

    def create_session(self, user_id: int, title: str = "新会话") -> ChatSession:
        """创建新会话"""
        return self.crud.create_session(user_id, title)

    def get_session(self, session_id: int) -> Optional[ChatSession]:
        """获取指定会话"""
        return self.crud.get_session(session_id)

    def delete_session(self, session_id: int) -> bool:
        """删除(软删除)指定会话"""
        return self.crud.update_session_status(session_id, SessionStatus.DELETED)

    def get_session_messages(
        self, 
        session_id: int, 
        skip: int = 0, 
        limit: int = 50
    ) -> List[Message]:
        """获取会话消息列表"""
        return self.crud.get_session_messages(session_id, skip, limit)

    async def send_message(self, session_id: int, content: str) -> Message:
        """发送消息并获取AI回复"""
        # 保存用户消息
        user_message = self.crud.create_message(
            session_id=session_id,
            content=content,
            role=MessageRole.USER
        )

        # 获取AI回复
        ai_response = await self.llm.get_response(content)

        # 保存AI回复
        ai_message = self.crud.create_message(
            session_id=session_id,
            content=ai_response,
            role=MessageRole.ASSISTANT
        )

        return ai_message 