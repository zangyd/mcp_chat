from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.db.models.chat import Session as ChatSession, Message, MessageType
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
        sessions = self.crud.get_user_sessions(user_id, skip, limit)
        # 为每个会话添加最后一条消息和消息数量
        for session in sessions:
            last_message = self.crud.get_session_last_message(session.id)
            if last_message:
                session.last_message = last_message.content
            message_count = self.crud.get_session_message_count(session.id)
            session.message_count = message_count
        return sessions

    def create_session(self, user_id: int, title: str = "新会话") -> ChatSession:
        """创建新会话"""
        return self.crud.create_session(user_id, title)

    def get_session(self, session_id: int) -> Optional[ChatSession]:
        """获取指定会话"""
        return self.crud.get_session(session_id)

    def delete_session(self, session_id: int) -> bool:
        """删除(软删除)指定会话"""
        return self.crud.update_session_status(session_id, False)

    def get_session_messages(
        self, 
        session_id: int, 
        skip: int = 0, 
        limit: int = 50
    ) -> List[Message]:
        """获取会话消息列表"""
        return self.crud.get_session_messages(session_id, skip, limit)

    async def send_message(
        self, 
        session_id: int, 
        content: str, 
        metadata: Optional[Dict[str, Any]] = None
    ) -> List[Message]:
        """发送消息并获取AI回复
        
        Args:
            session_id: 会话ID
            content: 消息内容
            metadata: 元数据
            
        Returns:
            List[Message]: 包含用户消息和AI回复的消息列表
        """
        # 创建用户消息
        user_message = self.crud.create_message(
            session_id=session_id,
            content=content,
            message_type=MessageType.USER.value,  # 使用枚举值的字符串表示
            metadata=metadata
        )
        
        # 获取会话历史消息作为上下文
        context = [
            {"role": msg.message_type, "content": msg.content}
            for msg in self.crud.get_session_messages(session_id, limit=10)
        ]
        
        # 调用LLM获取回复
        assistant_reply = await self.llm.get_llm_response(content, context)
        
        # 创建助手回复消息
        assistant_message = self.crud.create_message(
            session_id=session_id,
            content=assistant_reply,
            message_type=MessageType.ASSISTANT.value  # 使用枚举值的字符串表示
        )
        
        # 更新会话最后活动时间
        session = self.crud.get_session(session_id)
        if session:
            session.updated_at = func.now()
            self.db.commit()
        
        return [user_message, assistant_message] 