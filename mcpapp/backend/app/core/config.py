from typing import List, Union, Dict, Any, Optional
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator, Field, PostgresDsn, field_validator
from urllib.parse import quote_plus

class Settings(BaseSettings):
    PROJECT_NAME: str = "MCP Server 智能聊天系统"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "基于大模型的智能聊天系统"
    API_V1_STR: str = "/api/v1"
    
    # CORS配置
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # 数据库配置
    MYSQL_HOST: str = Field(default="localhost")
    MYSQL_PORT: str = Field(default="3306")
    MYSQL_USER: str = Field(default="root")
    MYSQL_PASSWORD: str = Field(default="Autotest@2024")
    MYSQL_DATABASE: str = Field(default="mcp_chat")

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        """获取数据库连接URI"""
        encoded_password = quote_plus(self.MYSQL_PASSWORD)
        return f"mysql+pymysql://{self.MYSQL_USER}:{encoded_password}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}?charset=utf8mb4"

    # Redis配置
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0

    # JWT配置
    SECRET_KEY: str = "your-secret-key"  # 在生产环境中应该使用环境变量
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天

    # DeepSeek配置
    DEEPSEEK_API_KEY: str = Field(default="your-api-key-here")
    DEEPSEEK_API_BASE: str = "https://api.deepseek.com/v1"
    DEEPSEEK_MODEL_NAME: str = "deepseek-chat"
    SYSTEM_PROMPT: str = """你是一个专业的AI助手，可以帮助用户解决各种问题。
请注意：
1. 保持专业和友好的态度
2. 给出准确和有帮助的回答
3. 如果不确定，诚实地表示不知道
4. 避免有害或不当的内容
5. 尊重用户的隐私
"""

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()