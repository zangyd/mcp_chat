from typing import List, Optional, Any
from langchain.chat_models.base import BaseChatModel
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    BaseMessage,
    LLMResult,
    Generation
)

from app.core.config import settings
from app.db.models import Message, MessageType

class MockChatModel(BaseChatModel):
    """模拟的聊天模型实现"""
    
    def _generate(self, messages: List[BaseMessage], stop=None, **kwargs) -> LLMResult:
        """同步生成回复"""
        # 获取最后一条用户消息
        last_message = messages[-1].content if messages else ""
        response = f"这是对'{last_message}'的模拟回复。实际项目中，这里应该调用DeepSeek API获取回复。"
        return LLMResult(generations=[[Generation(text=response)]])
    
    async def _agenerate(self, messages: List[BaseMessage], stop=None, **kwargs) -> LLMResult:
        """异步生成回复"""
        # 获取最后一条用户消息
        last_message = messages[-1].content if messages else ""
        response = f"这是对'{last_message}'的模拟回复。实际项目中，这里应该调用DeepSeek API获取回复。"
        return LLMResult(generations=[[Generation(text=response)]])

    @property
    def _llm_type(self) -> str:
        """返回模型类型"""
        return "mock_chat_model"

class LLMService:
    """大语言模型服务"""

    def __init__(self):
        """初始化LLM服务"""
        self.llm = MockChatModel()

    def _convert_message_to_langchain(self, message: Message) -> BaseMessage:
        """将自定义消息转换为LangChain消息格式
        
        Args:
            message: 自定义消息对象

        Returns:
            BaseMessage: LangChain消息对象
        """
        if message.message_type == MessageType.USER:
            return HumanMessage(content=message.content)
        elif message.message_type == MessageType.ASSISTANT:
            return AIMessage(content=message.content)
        else:  # system
            return SystemMessage(content=message.content)

    def _convert_messages_to_langchain(
        self, 
        messages: List[Message]
    ) -> List[BaseMessage]:
        """将自定义消息列表转换为LangChain消息列表
        
        Args:
            messages: 自定义消息列表

        Returns:
            List[BaseMessage]: LangChain消息列表
        """
        return [
            self._convert_message_to_langchain(msg) 
            for msg in messages
        ]

    async def get_response(
        self, 
        message: str,
        history: Optional[List[Message]] = None
    ) -> str:
        """获取大模型回复
        
        Args:
            message: 用户输入的消息
            history: 历史消息列表

        Returns:
            str: 大模型的回复内容
        """
        try:
            # 构建消息历史
            messages: List[BaseMessage] = []
            
            # 添加系统提示语
            if settings.SYSTEM_PROMPT:
                messages.append(SystemMessage(content=settings.SYSTEM_PROMPT))
            
            # 添加历史消息
            if history:
                messages.extend(self._convert_messages_to_langchain(history))
            
            # 添加当前用户消息
            messages.append(HumanMessage(content=message))
            
            # 调用大模型获取回复
            response = await self.llm.agenerate([messages])
            
            # 提取回复内容
            if response.generations:
                return response.generations[0][0].text
        except Exception as e:
            print(f"Error calling LLM: {e}")
        
        return f"这是对'{message}'的模拟回复。实际项目中，这里应该调用DeepSeek API获取回复。" 