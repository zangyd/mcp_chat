from typing import Optional, List, Dict, Any
import aiohttp
from app.core.config import settings

async def get_llm_response(
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
        "model": settings.DEEPSEEK_MODEL_NAME,
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
        "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        # 发送请求到DeepSeek API
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{settings.DEEPSEEK_API_BASE}/chat/completions",
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