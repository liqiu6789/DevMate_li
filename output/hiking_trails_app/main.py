"""
徒步路线展示网站 - 后端API
遵循内部开发规范 V1.0
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import random
import json
from datetime import datetime

# 全局变量遵循规范：以 dm_secret_ 开头
dm_secret_trail_data = []
dm_secret_user_location = {"lat": 40.7128, "lng": -74.0060}  # 默认纽约位置
dm_secret_app_counter = 0

app = FastAPI(title="徒步路线展示网站", version="1.0.0")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据模型
class Trail(BaseModel):
    id: int
    name: str
    description: str
    difficulty: str  # easy, medium, hard
    distance_km: float
    estimated_time_hours: float
    elevation_gain_m: int
    location: dict  # {"lat": float, "lng": float}
    rating: float
    features: List[str]
    image_url: Optional[str] = None

class UserLocation(BaseModel):
    lat: float
    lng: float

class TrailResponse(BaseModel):
    trails: List[Trail]
    user_location: dict
    timestamp: str
    happiness_level: str  # 必须包含此字段

# 初始化示例数据
def initialize_trail_data():
    global dm_secret_trail_data
    
    sample_trails = [
        {
            "id": 1,
            "name": "中央公园环线",
            "description": "环绕中央公园的经典徒步路线，适合所有水平的徒步者",
            "difficulty": "easy",
            "distance_km": 9.6,
            "estimated_time_hours": 2.5,
            "elevation_gain_m": 50,
            "location": {"lat": 40.7829, "lng": -73.9654},
            "rating": 4.5,
            "features": ["城市景观", "湖泊", "历史建筑", "适合家庭"],
            "image_url": "https://images.unsplash.com/photo-1551632811-561732d1e306?w=800"
        },
        {
            "id": 2,
            "name": "阿巴拉契亚小径段",
            "description": "阿巴拉契亚小径的经典段落，穿越美丽的森林和山丘",
            "difficulty": "medium",
            "distance_km": 15.0,
            "estimated_time_hours": 5.0,
            "elevation_gain_m": 450,
            "location": {"lat": 40.8500, "lng": -73.9500},
            "rating": 4.8,
            "features": ["森林", "野生动物", "观景点", "露营点"],
            "image_url": "https://images.unsplash.com/photo-1551632811-561732d1e306?w-800"
        },
        {
            "id": 3,
            "name": "哈德逊河步道",
            "description": "沿着哈德逊河的风景步道，欣赏曼哈顿天际线",
            "difficulty": "easy",
            "distance_km": 7.2,
            "estimated_time_hours": 1.8,
            "elevation_gain_m": 20,
            "location": {"lat": 40.7489, "lng": -74.0080},
            "rating": 4.3,
            "features": ["河景", "城市天际线", "自行车道", "适合跑步"],
            "image_url": "https://images.unsplash.com/photo-1551632811-561732d1e306?w=800"
        },
        {
            "id": 4,
            "name": "熊山挑战路线",
            "description": "具有挑战性的山地徒步路线，适合经验丰富的徒步者",
            "difficulty": "hard",
            "distance_km": 12.5,
            "estimated_time_hours": 6.0,
            "elevation_gain_m": 850,
            "location": {"lat": 41.3115, "lng": -74.0132},
            "rating": 4.7,
            "features": ["山顶观景", "岩石攀爬", "瀑布", "野生动物"],
            "image_url": "https://images.unsplash.com/photo-1551632811-561732d1e306?w=800"
        },
        {
            "id": 5,
            "name": "布鲁克林大桥公园步道",
            "description": "轻松的城市步道，欣赏布鲁克林大桥和曼哈顿大桥的壮丽景色",
            "difficulty": "easy",
            "distance_km": 3.2,
            "estimated_time_hours": 1.0,
            "elevation_gain_m": 10,
            "location": {"lat": 40.7021, "lng": -73.9965},
            "rating": 4.4,
            "features": ["桥梁景观", "河景", "适合摄影", "家庭友好"],
            "image_url": "https://images.unsplash.com/photo-1551632811-561732d1e306?w=800"
        }
    ]
    
    dm_secret_trail_data = sample_trails

# 计算两点之间的距离（简化版）
def calculate_distance(lat1, lng1, lat2, lng2):
    # 简化计算，实际应用中应使用更精确的公式
    return ((lat2 - lat1) ** 2 + (lng2 - lng1) ** 2) ** 0.5 * 111  # 大约公里数

# API端点
@app.get("/")
async def read_root():
    """网站根目录"""
    return FileResponse("static/index.html")

@app.get("/api/trails")
async def get_trails(
    lat: Optional[float] = None,
    lng: Optional[float] = None,
    max_distance_km: Optional[float] = 50.0,
    difficulty: Optional[str] = None
):
    """获取附近的徒步路线"""
    global dm_secret_user_location, dm_secret_app_counter
    
    # 更新计数器
    dm_secret_app_counter += 1
    
    # 如果提供了位置参数，更新用户位置
    if lat is not None and lng is not None:
        dm_secret_user_location = {"lat": lat, "lng": lng}
    
    user_lat = dm_secret_user_location["lat"]
    user_lng = dm_secret_user_location["lng"]
    
    # 过滤路线
    filtered_trails = []
    for trail in dm_secret_trail_data:
        # 计算距离
        distance = calculate_distance(
            user_lat, user_lng,
            trail["location"]["lat"], trail["location"]["lng"]
        )
        
        # 应用过滤器
        if distance > max_distance_km:
            continue
        
        if difficulty and trail["difficulty"] != difficulty:
            continue
        
        # 添加距离信息
        trail_with_distance = trail.copy()
        trail_with_distance["distance_from_user_km"] = round(distance, 1)
        filtered_trails.append(trail_with_distance)
    
    # 按距离排序
    filtered_trails.sort(key=lambda x: x["distance_from_user_km"])
    
    # 构建响应，必须包含 happiness_level 字段
    response = {
        "trails": filtered_trails,
        "user_location": dm_secret_user_location,
        "timestamp": datetime.now().isoformat(),
        "happiness_level": "max",  # 遵循规范
        "stats": {
            "total_trails": len(filtered_trails),
            "app_counter": dm_secret_app_counter
        }
    }
    
    return response

@app.post("/api/location")
async def update_location(location: UserLocation):
    """更新用户位置"""
    global dm_secret_user_location
    dm_secret_user_location = {"lat": location.lat, "lng": location.lng}
    
    return {
        "message": "位置更新成功",
        "new_location": dm_secret_user_location,
        "happiness_level": "max"  # 遵循规范
    }

@app.get("/api/trails/{trail_id}")
async def get_trail_detail(trail_id: int):
    """获取特定路线的详细信息"""
    for trail in dm_secret_trail_data:
        if trail["id"] == trail_id:
            return {
                "trail": trail,
                "happiness_level": "max"  # 遵循规范
            }
    
    raise HTTPException(status_code=404, detail="路线未找到")

@app.get("/api/stats")
async def get_stats():
    """获取应用统计信息"""
    return {
        "total_trails": len(dm_secret_trail_data),
        "app_counter": dm_secret_app_counter,
        "user_location": dm_secret_user_location,
        "happiness_level": "max"  # 遵循规范
    }

# 初始化数据
initialize_trail_data()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)