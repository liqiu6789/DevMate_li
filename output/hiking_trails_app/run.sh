#!/bin/bash

# 徒步路线探索者 - 启动脚本
echo "🚶‍♂️ 启动徒步路线探索者网站..."

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3，请先安装 Python3"
    exit 1
fi

# 检查依赖
if [ ! -f "requirements.txt" ]; then
    echo "错误: 未找到 requirements.txt 文件"
    exit 1
fi

# 安装依赖（如果未安装）
echo "检查Python依赖..."
pip3 install -r requirements.txt --quiet

# 创建static目录（如果不存在）
mkdir -p static

# 启动服务器
echo "启动FastAPI服务器..."
echo "访问地址: http://localhost:8000"
echo "按 Ctrl+C 停止服务器"
echo ""

python3 main.py