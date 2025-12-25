import os
import shutil
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from src.config import settings

# 定义向量数据库的持久化路径
PERSIST_DIRECTORY = "./chroma_db"

def ingest_docs():
    """读取 docs/ 目录下的文档并存入向量数据库"""
    
    # 1. 检查文档目录是否存在
    if not os.path.exists("docs"):
        print("❌ 目录 'docs' 不存在，请先创建并放入文档。")
        return

    # 2. 加载文档
    print("📂 Loading documents...")
    loader = DirectoryLoader("docs", glob="**/*.md", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"})
    docs = loader.load()
    print(f"   Found {len(docs)} documents.")

    if not docs:
        return

    # 3. 切分文档
    print("✂️ Splitting documents...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(docs)
    print(f"   Split into {len(splits)} chunks.")

    # 4. 初始化 Embedding 模型
    embeddings = OpenAIEmbeddings(
        base_url=settings.AI_BASE_URL,
        api_key=settings.API_KEY,
        model=settings.EMBEDDING_MODEL_NAME
    )

    # 5. 存入 ChromaDB
    # 如果数据库已存在，先清空以便重新索引（可选，开发阶段方便）
    if os.path.exists(PERSIST_DIRECTORY):
        shutil.rmtree(PERSIST_DIRECTORY)
        print("   Cleared existing database.")

    print("💾 Saving to vector database...")
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )
    print("✅ Ingestion complete!")

def query_knowledge_base(query: str, k: int = 2):
    """
    查询向量数据库
    :param query: 用户问题
    :param k: 返回最相关的文档块数量
    :return: 相关的文档列表
    """
    embeddings = OpenAIEmbeddings(
        base_url=settings.AI_BASE_URL,
        api_key=settings.API_KEY,
        model=settings.EMBEDDING_MODEL_NAME
    )
    
    # 加载已存在的数据库
    vectorstore = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embeddings
    )
    
    print(f"\n🔍 Searching for: '{query}'")
    results = vectorstore.similarity_search(query, k=k)
    
    return results

# --- 测试代码 ---
if __name__ == "__main__":
    # 1. 先执行摄入（如果已经摄入过，这步可以注释掉）
    ingest_docs()
    
    # 2. 测试查询
    test_query = "变量命名有什么要求？"
    hits = query_knowledge_base(test_query)
    
    print("\n📝 Search Results:")
    for i, doc in enumerate(hits):
        print(f"--- Result {i+1} ---")
        print(doc.page_content)
        print("------------------")