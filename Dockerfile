# 使用官方 Python 3.13 Slim 镜像作为基础
FROM python:3.13-slim

# 设置工作目录
WORKDIR /app

# 安装 uv
# 使用官方推荐的安装脚本，或者直接复制预编译的二进制文件（更简单）
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 1. 先复制依赖文件 (利用 Docker 缓存层)
COPY pyproject.toml uv.lock ./

# 2. 安装依赖
# --frozen: 严格按照 uv.lock 安装
# --no-cache: 减小镜像体积
RUN uv sync --frozen --no-cache

# 3. 复制项目代码
COPY . .

# 设置环境变量，确保 Python 使用 uv 创建的虚拟环境
ENV PATH="/app/.venv/bin:$PATH"

# 容器启动命令
# 使用 -u (unbuffered) 确保日志实时输出
CMD ["python", "-u", "main.py"]