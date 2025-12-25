import os
from langchain_openai import ChatOpenAI
from src.config import settings

# 关键：手动将配置注入环境变量，LangChain 才能识别
os.environ["LANGCHAIN_TRACING_V2"] = "true" if settings.LANGCHAIN_TRACING_V2 else "false"
os.environ["LANGCHAIN_API_KEY"] = settings.LANGCHAIN_API_KEY
os.environ["LANGCHAIN_PROJECT"] = settings.LANGCHAIN_PROJECT

def test_llm_connection():
    print(f"Testing connection with model: {settings.MODEL_NAME}...")
    
    try:
        # 初始化 ChatOpenAI
        llm = ChatOpenAI(
            base_url=settings.AI_BASE_URL,
            api_key=settings.API_KEY,
            model=settings.MODEL_NAME,
            temperature=0.7
        )
        
        # 发送简单请求
        response = llm.invoke("你好，你是谁")
        
        print("\n✅ Success! LLM Response:")
        print(response.content)
        print("\nCheck your LangSmith project to see if this trace appeared.")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    test_llm_connection()