import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # LLM Settings
    AI_BASE_URL: str
    API_KEY: str
    MODEL_NAME: str = "gpt-4o-mini"
    EMBEDDING_MODEL_NAME: str = "text-embedding-3-small"

    # Search Tool Settings
    TAVILY_API_KEY: str

    # Observability
    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_API_KEY: str = ""
    LANGCHAIN_PROJECT: str = "devmate-project"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # 忽略多余的环境变量
    )

# 实例化配置对象，供其他模块导入使用
settings = Settings()

# 验证配置加载（可选，调试用）
if __name__ == "__main__":
    print(f"Loaded config for model: {settings.MODEL_NAME}")
    print(f"Base URL: {settings.AI_BASE_URL}")