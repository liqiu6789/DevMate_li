import asyncio
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
from src.config import settings

# 1. 初始化 MCP Server
# "devmate-search" 是服务名称
mcp = FastMCP("devmate-search")

# 2. 初始化 Tavily 客户端
tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)

# 3. 定义工具 (Tool)
# 使用装饰器 @mcp.tool 注册这个函数，让它变成 MCP 可调用的工具
@mcp.tool()
async def search_web(query: str, max_results: int = 3) -> str:
    """
    使用 Tavily 搜索引擎搜索互联网。
    当用户询问当前事件、技术文档或任何不在本地知识库中的信息时使用。
    
    Args:
        query: 搜索关键词
        max_results: 返回结果的数量，默认为 3
    """
    print(f"[MCP Server] Searching for: {query}")
    try:
        # 调用 Tavily API
        response = tavily_client.search(query, max_results=max_results)
        
        # 格式化结果
        results = []
        for result in response.get("results", []):
            title = result.get("title", "No Title")
            url = result.get("url", "#")
            content = result.get("content", "")
            results.append(f"Title: {title}\nURL: {url}\nContent: {content}\n---")
            
        return "\n".join(results)
        
    except Exception as e:
        return f"Error performing search: {str(e)}"

# 4. 运行服务器
if __name__ == "__main__":
    # 使用 stdio 模式运行 (标准输入输出通信)
    mcp.run()