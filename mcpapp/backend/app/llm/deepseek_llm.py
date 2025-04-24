from typing import Any, List, Mapping, Optional
from langchain.llms.base import LLM
from langchain.callbacks.manager import CallbackManagerForLLMRun
import requests
from app.core.config import settings

class DeepSeekLLM(LLM):
    """DeepSeek LLM wrapper for LangChain."""
    
    model_name: str = settings.DEEPSEEK_MODEL_NAME
    temperature: float = 0.7
    max_tokens: int = 1000

    @property
    def _llm_type(self) -> str:
        return "deepseek"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Call the DeepSeek API and return the response."""
        headers = {
            "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
            "Content-Type": "application/json",
        }

        data = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        if stop:
            data["stop"] = stop

        response = requests.post(
            f"{settings.DEEPSEEK_API_BASE}/chat/completions",
            headers=headers,
            json=data,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }