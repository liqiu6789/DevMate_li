import os
import sys
import asyncio
from typing import Annotated, Literal, TypedDict
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from src.config import settings
from src.rag import query_knowledge_base

# --- 1. 定义工具集 ---

# (A) RAG 检索工具
@tool
def search_local_docs(query: str) -> str:
    """
    查阅本地知识库/内部文档。
    当用户询问关于'内部规范'、'项目特定规则'、'自定义库用法'等问题时，必须优先使用此工具。
    """
    results = query_knowledge_base(query)
    if not results:
        return "本地文档中未找到相关内容。"
    
    formatted = "\n\n".join([f"[文档片段]:\n{doc.page_content}" for doc in results])
    return formatted

# (B) 文件写入工具

@tool
def write_file(file_path: str, content: str) -> str:
    """
    将内容写入到 'output' 目录下的指定文件。
    ...
    """
    # 强制加上 output/ 前缀
    if not file_path.startswith("output/"):
        file_path = os.path.join("output", file_path)
    try:
        # --- 修复开始 ---
        # 获取父目录
        directory = os.path.dirname(file_path)
        # 只有当 directory 不为空时，才尝试创建目录
        if directory:
            os.makedirs(directory, exist_ok=True)
        # --- 修复结束 ---
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

# (C) MCP 网络搜索工具的封装
# 由于 MCP Client 是异步且有状态的 (Context Manager)，我们需要一种特殊方式来调用它。
# 为了简化面试项目，我们在这里使用一个简化的同步包装器，或者在 Agent 运行时动态绑定。
# 这里我们采用一种直接调用的方式（每次调用启动一次 Client，效率略低但实现简单稳定）。

@tool
def search_web(query: str) -> str:
    """
    使用 Tavily 搜索互联网最新信息。
    当本地文档无法回答，或者需要查询通用技术知识（如 Python 最新语法、库的用法）时使用。
    """
    async def _run_mcp():
        # 设置环境变量以确保子进程能找到 src
        env = os.environ.copy()
        env["PYTHONPATH"] = os.getcwd()
        
        server_params = StdioServerParameters(
            command=sys.executable,
            args=["src/search_server.py"],
            env=env
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool("search_web", arguments={"query": query})
                return "\n".join([c.text for c in result.content])

    try:
        return asyncio.run(_run_mcp())
    except Exception as e:
        return f"Web search failed: {str(e)}"

# --- 2. 构建 Agent ---

def create_agent():
    # 1. 准备工具列表
    tools = [search_local_docs, write_file, search_web]
    
    # 2. 初始化 LLM
    llm = ChatOpenAI(
        base_url=settings.AI_BASE_URL,
        api_key=settings.API_KEY,
        model=settings.MODEL_NAME,
        temperature=0
    )
    
    # 3. 绑定工具
    llm_with_tools = llm.bind_tools(tools)
    
    # 4. 定义系统提示词
    SYSTEM_PROMPT = SYSTEM_PROMPT = """你是一个全能编程助手 DevMate。
你的目标是帮助用户快速构建原型、编写代码并生成项目文件。

核心决策原则：
1. **行动优先**: 面对宽泛的构建请求（如“做一个网站”），不要陷入无休止的技术调研。**立即选择一套最简单的默认技术栈（Python FastAPI + 原生 HTML）**，并开始编写代码。

2. **知识检索与严格合规**:
   - 涉及具体实现细节（如 API 用法）时，才使用 [search_web]。搜到第一个可用示例就停止。
   - 涉及项目规范时，**必须**查阅 [search_local_docs]。
   - **关键指令**: 生成的代码必须 **100% 严格遵守** 查到的内部规范（例如：全局变量前缀必须是 `dm_secret_`，API 响应必须包含特定字段等）。违反规范的代码是不可接受的。

3. **文件落地与隔离**:
   - 必须使用 [write_file] 将代码写入文件。
   - **项目隔离**: 请为每个生成的项目创建一个具有描述性的子目录（例如 `output/hiking_app/`），将所有文件放在该目录下，避免不同项目的文件混淆。
   - **一次性交付**: 在一轮交互中，连续调用多次 [write_file] 把所有必要文件（如 main.py, index.html）都写完，不要分批次问用户。

4. **禁止啰嗦**: 文件写完后，直接回复“任务完成”并展示文件列表，不要反问用户意见。

5. **自我修正**: 如果遇到工具报错，尝试修复参数重试。如果连续失败两次，则放弃该步骤并告知用户。
"""

    # 5. 构建 LangGraph 图
    # 这是一个标准的 ReAct 模式图
    
    from langgraph.graph import MessagesState
    
    # 定义节点函数
    def call_model(state: MessagesState):
        messages = state["messages"]
        # 如果是第一条消息，且没有 SystemPrompt，可以在这里插入（简化起见，我们假设外部会在 messages[0] 传入 System 这里的逻辑略）
        # 更好的方式是在 invoke 时传入 system message
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}

    # 构建图
    workflow = StateGraph(MessagesState)
    
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", ToolNode(tools))
    
    workflow.add_edge(START, "agent")
    
    # 条件边：如果 LLM 决定调用工具，走 tools 节点；否则结束
    def should_continue(state: MessagesState):
        messages = state["messages"]
        last_message = messages[-1]
        if last_message.tool_calls:
            return "tools"
        return END
        
    workflow.add_conditional_edges("agent", should_continue)
    workflow.add_edge("tools", "agent") # 工具执行完回环给 agent 继续思考
    
    app = workflow.compile()
    return app, SYSTEM_PROMPT