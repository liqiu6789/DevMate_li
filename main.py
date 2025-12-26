import os
import sys
from langchain_core.messages import HumanMessage, SystemMessage
from src.config import settings
from src.agent import create_agent

# 确保环境变量注入（为了 LangSmith）
os.environ["LANGCHAIN_TRACING_V2"] = "true" if settings.LANGCHAIN_TRACING_V2 else "false"
os.environ["LANGCHAIN_API_KEY"] = settings.LANGCHAIN_API_KEY
os.environ["LANGCHAIN_PROJECT"] = settings.LANGCHAIN_PROJECT

def main():
    print("🤖 DevMate Starting...")
    
    # 1. 创建 Agent
    agent_app, system_prompt = create_agent()
    
    print("✅ Agent ready! (Type 'exit' to quit)")
    print("--------------------------------------------------")
    
    # 2. 交互循环
    # 初始化对话历史，带上 System Prompt
    messages = [SystemMessage(content=system_prompt)]
    
    while True:
        try:
            user_input = input("\n👤 User: ").strip()
            if user_input.lower() in ["exit", "quit", "q"]:
                print("Bye!")
                break
            if not user_input:
                continue
                
            # 添加用户消息
            messages.append(HumanMessage(content=user_input))
            
            # 3. 调用 Agent
            # stream_mode="updates" 可以看到每一步的动作
            print("\n🤖 DevMate is thinking...")
            
            # 使用 invoke 运行图
            final_state = agent_app.invoke({"messages": messages})
            
            # 获取最新的 AI 回复
            last_msg = final_state["messages"][-1]
            print(f"\n🤖 Agent: {last_msg.content}")
            
            # 更新对话历史（LangGraph 每次返回完整的 state，我们需要维护上下文）
            # 在简单的 demo 中，我们可以直接用 final_state["messages"] 作为下一轮的输入
            messages = final_state["messages"]
            
        except KeyboardInterrupt:
            print("\nAborted.")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main()