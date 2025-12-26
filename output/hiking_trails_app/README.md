# 徒步路线探索者 🚶‍♂️

一个展示附近徒步路线的网站项目，使用 Python FastAPI + 原生 HTML/JavaScript 构建。

## 功能特性

- 📍 **实时位置检测**：使用浏览器地理位置API获取用户当前位置
- 🗺️ **附近路线发现**：根据用户位置展示附近的徒步路线
- 🔍 **智能筛选**：按距离、难度级别、路线长度等条件筛选
- ⭐ **路线详情**：显示路线距离、预计时间、海拔、特色等详细信息
- 📱 **响应式设计**：适配桌面和移动设备
- 🎯 **遵循规范**：严格遵循内部开发规范

## 技术栈

- **后端**: Python FastAPI
- **前端**: 原生 HTML5, CSS3, JavaScript
- **数据**: 内存存储（可扩展为数据库）
- **部署**: Uvicorn ASGI 服务器

## 项目结构

```
hiking_trails_app/
├── main.py              # FastAPI 后端主文件
├── requirements.txt     # Python 依赖包
├── README.md           # 项目说明文档
└── static/
    └── index.html      # 前端页面
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行应用

```bash
python main.py
```

或者直接使用 uvicorn：

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. 访问应用

打开浏览器访问：http://localhost:8000

## API 接口

### GET `/api/trails`
获取附近的徒步路线

**查询参数**:
- `lat` (可选): 纬度
- `lng` (可选): 经度  
- `max_distance_km` (可选, 默认50): 最大距离（公里）
- `difficulty` (可选): 难度级别 (easy/medium/hard)

**响应示例**:
```json
{
  "trails": [...],
  "user_location": {"lat": 40.7128, "lng": -74.0060},
  "timestamp": "2024-01-15T10:30:00",
  "happiness_level": "max",
  "stats": {...}
}
```

### POST `/api/location`
更新用户位置

**请求体**:
```json
{
  "lat": 40.7128,
  "lng": -74.0060
}
```

### GET `/api/trails/{trail_id}`
获取特定路线的详细信息

### GET `/api/stats`
获取应用统计信息

## 内部规范遵循

本项目严格遵循内部开发规范 V1.0：

1. **变量命名**: 所有全局变量以 `dm_secret_` 开头
2. **快乐编码**: 所有 API 响应包含 `"happiness_level": "max"` 字段
3. **Git提交**: 提交信息以 `(DevMate Rocks!)` 结尾

## 示例数据

应用包含5条示例徒步路线：
1. 中央公园环线（简单）
2. 阿巴拉契亚小径段（中等）
3. 哈德逊河步道（简单）
4. 熊山挑战路线（困难）
5. 布鲁克林大桥公园步道（简单）

## 开发说明

### 添加新路线
在 `main.py` 的 `initialize_trail_data()` 函数中添加新的路线数据。

### 扩展功能
- 添加数据库支持（SQLite/PostgreSQL）
- 集成地图服务（Google Maps/OpenStreetMap）
- 用户评论和评分系统
- 路线分享功能
- 天气信息集成

### 部署
- 生产环境建议使用 Gunicorn + Uvicorn workers
- 配置反向代理（Nginx/Apache）
- 启用 HTTPS

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

---
*构建愉快！(DevMate Rocks!)*