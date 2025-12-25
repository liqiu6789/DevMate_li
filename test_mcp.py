import asyncio
import sys
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_search_tool():
    # 关键修正：确保子进程能找到 src 模块
    env = os.environ.copy()
    env["PYTHONPATH"] = os.getcwd()

    # 1. 定义服务器参数
    server_params = StdioServerParameters(
        command=sys.executable, 
        args=["src/search_server.py"], 
        env=env 
    )

    print("🔌 Connecting to MCP Server...")
    
    try:
        # 2. 建立连接
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # 3. 初始化
                await session.initialize()
                
                # 4. 列出可用工具
                tools = await session.list_tools()
                print(f"\n🛠️  Available Tools: {[t.name for t in tools.tools]}")
                
                # 5. 调用搜索工具
                query = "Python 3.13 新特性"
                print(f"\n🚀 Calling 'search_web' with query: '{query}'...")
                
                result = await session.call_tool("search_web", arguments={"query": query})
                
                # 6. 打印结果
                print("\n📄 Search Results:")
                for content in result.content:
                    print(content.text)
                    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        # 打印更多调试信息，如果是 Connection closed，通常意味着 server 脚本报错了
        print("Tip: If you see 'Connection closed', it usually means src/search_server.py failed to start.")

if __name__ == "__main__":
    asyncio.run(test_search_tool())