from typing import Dict, List, Optional
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from app.llm.deepseek_llm import DeepSeekLLM

class IntentRecognitionService:
    def __init__(self):
        self.llm = DeepSeekLLM()
        self.prompt_template = PromptTemplate(
            input_variables=["user_input"],
            template="""
            分析用户输入，识别其意图。将意图分类为以下类别之一：
            1. 信息查询
            2. 任务执行
            3. 工具调用
            4. 闲聊对话

            用户输入: {user_input}
            
            以JSON格式返回：
            1. 意图类别
            2. 置信度（0-1）
            3. 关键词列表
            4. 可能需要的MCP工具
            """
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)

    async def analyze_intent(self, user_input: str) -> Dict:
        """分析用户输入的意图"""
        result = await self.chain.arun(user_input=user_input)
        # 解析LLM返回的JSON字符串
        try:
            import json
            return json.loads(result)
        except:
            return {
                "intent_type": "unknown",
                "confidence": 0.0,
                "keywords": [],
                "required_tools": []
            }

    async def get_required_tools(self, intent_data: Dict) -> List[str]:
        """根据意图数据获取所需的MCP工具列表"""
        return intent_data.get("required_tools", [])