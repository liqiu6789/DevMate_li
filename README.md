# DevMate - 智能编程助手 🤖

DevMate 是一个 AI 驱动的全能编程助手，专为解决开发中的实际问题而生。它结合了 **RAG (检索增强生成)** 和 **MCP (Model Context Protocol)** 技术，能够查阅内部文档规范，实时搜索互联网最新技术，并自动生成符合规范的高质量代码。

## ✨ 核心特性

- **🧠 智能决策**: 基于 LangGraph 的 ReAct Agent，自主规划任务路径。
- **📚 知识增强 (RAG)**: 集成 ChromaDB，自动查阅并遵守本地开发规范（如变量命名、API 格式）。
- **🌐 联网搜索 (MCP)**: 通过 MCP 协议连接 Tavily 搜索，获取最新技术文档和 API 用法。
- **✍️ 自动编码**: 具备文件系统读写能力，可生成完整的多文件项目（如 FastAPI + HTML 网站）。
- **📦 容器化交付**: 提供 Docker 支持，一键启动完整环境。

## 🛠️ 技术栈

- **Language**: Python 3.13
- **Package Manager**: [uv](https://github.com/astral-sh/uv) (极速 Python 包管理)
- **Framework**: LangChain, LangGraph
- **Search Protocol**: Model Context Protocol (MCP)
- **Vector DB**: ChromaDB
- **LLM**: OpenAI / DeepSeek (可通过配置切换)

## 🚀 快速开始

### 方式一：Docker 一键运行 (推荐)

如果你已安装 Docker，这是最快的方式。

1. **配置环境变量**
   复制 `.env.example` 为 `.env`，并填入你的 API Key：
   ```bash
   # Windows PowerShell
   copy .env.example .env
   # Linux/Mac
   cp .env.example .env
   ```

2. **启动服务**
   ```bash
   docker compose up -d
   ```

3. **进入交互**
   ```bash
   docker attach devmate-app
   # 或者
   docker compose run --rm devmate
   ```

### 方式二：本地开发运行

1. **前置要求**
   - Python 3.13+
   - 安装 `uv`: `pip install uv` (或参考官方文档)

2. **安装依赖**
   ```bash
   uv sync
   ```

3. **初始化向量数据库**
   首次运行前，需将文档摄入数据库：
   ```bash
   uv run -m src.rag
   ```

4. **启动 Agent**
   ```bash
   uv run main.py
   ```

## 📂 项目结构

```
DevMate/
├── src/                # 核心源代码
│   ├── agent.py        # Agent 定义与工具绑定 (LangGraph)
│   ├── rag.py          # RAG 摄入与检索逻辑
│   ├── search_server.py # MCP 搜索服务
│   └── config.py       # 配置管理
├── output/             # Agent 生成代码的输出目录 (安全沙箱)
├── docs/               # RAG 知识库文档 (存放内部规范)
├── main.py             # CLI 启动入口
├── Dockerfile          # 容器构建文件
└── pyproject.toml      # 项目依赖配置
```

## 📝 典型使用场景

启动 Agent 后，你可以尝试以下指令：

> "我想构建一个简单的徒步路线推荐网站，使用 FastAPI 和原生 HTML。"

Agent 将会：
1. 🔍 查阅 `docs/` 下的内部规范。
2. 🌐 搜索徒步地图 API 的用法。
3. 💻 在 `output/` 目录下生成 `main.py`, `index.html` 等文件。
4. ✅ 确保变量名以 `dm_secret_` 开头（依据内部规范）。

---
*Built for the Future of Coding.*
