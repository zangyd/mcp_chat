from typing import List, Optional, Any, Dict
import json
import aiohttp
from langchain.chat_models.base import BaseChatModel
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    BaseMessage,
    LLMResult,
    Generation
)
from pydantic import BaseModel, Field

from app.core.config import settings
from app.db.models import Message, MessageType

class DeepSeekMessage(BaseModel):
    """DeepSeek消息模型"""
    role: str = Field(..., description="消息角色：system/user/assistant")
    content: str = Field(..., description="消息内容")

class DeepSeekChatModel(BaseChatModel):
    """DeepSeek聊天模型实现"""
    
    api_base: str = "https://api.deepseek.com/v1"
    model_name: str = "deepseek-chat"
    
    def __init__(
        self,
        api_base: str = "https://api.deepseek.com/v1",
        model_name: str = "deepseek-chat",
        api_key: str = None,
        **kwargs: Any,
    ):
        """初始化DeepSeek聊天模型
        
        Args:
            api_base: API基础URL
            model_name: 模型名称
            api_key: API密钥
            **kwargs: 其他参数
        """
        super().__init__(**kwargs)
        self.api_base = api_base
        self.model_name = model_name
        self._api_key = api_key or settings.DEEPSEEK_API_KEY
        
    @property
    def api_key(self) -> str:
        """获取API Key"""
        return self._api_key
        
    @api_key.setter
    def api_key(self, value: str):
        """设置API Key"""
        self._api_key = value
        
    def _convert_messages_to_dict(self, messages: List[BaseMessage] | BaseMessage) -> List[Dict]:
        """将LangChain消息转换为DeepSeek API格式
        
        Args:
            messages: LangChain消息或消息列表
            
        Returns:
            List[Dict]: DeepSeek API消息格式
        """
        message_dicts = []
        
        # 如果传入的是单个消息，转换为列表
        if isinstance(messages, BaseMessage):
            messages = [messages]
        # 如果传入的是列表的列表，取第一个列表
        elif isinstance(messages, list) and messages and isinstance(messages[0], list):
            messages = messages[0]
            
        for message in messages:
            if isinstance(message, SystemMessage):
                role = "system"
            elif isinstance(message, HumanMessage):
                role = "user"
            elif isinstance(message, AIMessage):
                role = "assistant"
            else:
                raise ValueError(f"Got unknown message type: {type(message)}")
            
            message_dicts.append({
                "role": role,
                "content": message.content
            })
        return message_dicts
    
    def _create_chat_completion(
        self,
        messages: List[BaseMessage],
        **kwargs: Any,
    ) -> str:
        """调用DeepSeek API获取回复
        
        Args:
            messages: 消息列表
            **kwargs: 其他参数
            
        Returns:
            str: 模型回复
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model_name,
            "messages": self._convert_messages_to_dict(messages),
            **kwargs
        }
        
        # 同步调用API
        import requests
        response = requests.post(
            f"{self.api_base}/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code != 200:
            raise ValueError(
                f"Error calling DeepSeek API: {response.status_code} {response.text}"
            )
            
        return response.json()["choices"][0]["message"]["content"]
    
    async def _acreate_chat_completion(
        self,
        messages: List[BaseMessage],
        **kwargs: Any,
    ) -> str:
        """异步调用DeepSeek API获取回复
        
        Args:
            messages: 消息列表
            **kwargs: 其他参数
            
        Returns:
            str: 模型回复
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model_name,
            "messages": self._convert_messages_to_dict(messages),
            **kwargs
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                json=data
            ) as response:
                if response.status != 200:
                    text = await response.text()
                    raise ValueError(
                        f"Error calling DeepSeek API: {response.status} {text}"
                    )
                    
                result = await response.json()
                return result["choices"][0]["message"]["content"]
    
    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> LLMResult:
        """同步生成回复
        
        Args:
            messages: 消息列表
            stop: 停止词列表
            **kwargs: 其他参数
            
        Returns:
            LLMResult: 生成结果
        """
        response = self._create_chat_completion(messages, stop=stop, **kwargs)
        return LLMResult(generations=[[Generation(text=response)]])
    
    async def _agenerate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> LLMResult:
        """异步生成回复
        
        Args:
            messages: 消息列表
            stop: 停止词列表
            **kwargs: 其他参数
            
        Returns:
            LLMResult: 生成结果
        """
        response = await self._acreate_chat_completion(messages, stop=stop, **kwargs)
        return LLMResult(generations=[[Generation(text=response)]])

    @property
    def _llm_type(self) -> str:
        """返回模型类型"""
        return "deepseek_chat_model"

class LLMService:
    """LLM服务类"""
    
    def __init__(self):
        self.api_base = settings.DEEPSEEK_API_BASE
        self.api_key = settings.DEEPSEEK_API_KEY
        self.model_name = settings.DEEPSEEK_MODEL_NAME
    
    async def get_llm_response(
        self,
        message: str,
        context: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """
        获取大模型回复
        
        Args:
            message: 用户输入的消息
            context: 历史上下文消息列表
            
        Returns:
            str: 大模型的回复内容
        """
        # 构建请求数据
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": "你是一个智能助手，请用简洁专业的方式回答问题。"},
                *([{"role": msg["role"], "content": msg["content"]} 
                   for msg in (context or [])]),
                {"role": "user", "content": message}
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            # 发送请求到DeepSeek API
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_base}/chat/completions",
                    json=payload,
                    headers=headers
                ) as response:
                    if response.status != 200:
                        error_msg = await response.text()
                        raise Exception(f"DeepSeek API error: {error_msg}")
                    
                    data = await response.json()
                    return data["choices"][0]["message"]["content"]
        except Exception as e:
            # 如果API调用失败，返回一个友好的错误消息
            error_message = f"抱歉，我现在无法正常回复。错误信息：{str(e)}"
            return error_message

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
            # 构建消息列表
            messages = []
            
            # 添加系统提示语
            if settings.SYSTEM_PROMPT:
                messages.append(SystemMessage(content=settings.SYSTEM_PROMPT))
            
            # 添加历史消息
            if history:
                messages.extend(self._convert_messages_to_langchain(history))
            
            # 添加当前用户消息
            messages.append(HumanMessage(content=message))
            
            # 调用大模型获取回复
            result = await self._acreate_chat_completion(messages)
            
            # 提取回复内容
            if result and isinstance(result, str):
                return result
            
            raise ValueError("No response from LLM")
        except Exception as e:
            print(f"Error calling LLM: {e}")
            raise 