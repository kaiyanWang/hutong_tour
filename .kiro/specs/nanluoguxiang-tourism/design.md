# Design Document: 南锣鼓巷旅游导览系统

## Overview

南锣鼓巷旅游导览系统采用前后端分离架构，前端使用Vue3框架构建单页应用（SPA），后端使用Django框架提供RESTful API服务。系统通过清晰的分层设计，实现胡同信息展示、POI浏览、路线推荐和搜索等核心功能。

### 技术栈选型

| 层级 | 技术选型 | 说明 |
|------|----------|------|
| 前端框架 | Vue 3 + Vite | 现代化前端框架，支持组合式API |
| UI组件 | Element Plus | Vue3生态的UI组件库 |
| 路由 | Vue Router 4 | 前端路由管理 |
| HTTP客户端 | Axios | API请求处理 |
| 后端框架 | Django 4.x | Python Web框架 |
| API框架 | Django REST Framework | RESTful API构建 |
| 数据库 | SQLite | 轻量级数据库，开发便捷 |
| 跨域处理 | django-cors-headers | 处理前后端跨域请求 |

## Architecture

### 系统架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                         用户浏览器                               │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Frontend (Vue3 + Vite)                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │   Views     │  │  Components │  │   Router    │              │
│  │  - Home     │  │  - Header   │  │  - /        │              │
│  │  - POIList  │  │  - POICard  │  │  - /pois    │              │
│  │  - POIDetail│  │  - RouteCard│  │  - /poi/:id │              │
│  │  - Routes   │  │  - Search   │  │  - /routes  │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
│                          │                                       │
│                    ┌─────┴─────┐                                │
│                    │   Axios   │                                │
│                    │  API层    │                                │
│                    └───────────┘                                │
└─────────────────────────────────────────────────────────────────┘
                                │
                          HTTP/JSON
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Backend (Django + DRF)                        │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                      URL Router                          │    │
│  │   /api/hutong/  /api/pois/  /api/routes/  /api/search/  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                          │                                       │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                     Views (ViewSets)                     │    │
│  │   HutongViewSet  POIViewSet  RouteViewSet  SearchView   │    │
│  └─────────────────────────────────────────────────────────┘    │
│                          │                                       │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    Serializers                           │    │
│  │   HutongSerializer  POISerializer  RouteSerializer      │    │
│  └─────────────────────────────────────────────────────────┘    │
│                          │                                       │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                      Models                              │    │
│  │      Hutong         POI         Route       RoutePOI    │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Database (SQLite)                           │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │
│   │ hutong   │  │   poi    │  │  route   │  │  route_poi   │   │
│   └──────────┘  └──────────┘  └──────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 项目目录结构

```
nanluoguxiang-tourism/
├── backend/                      # Django后端项目
│   ├── venv/                     # Python虚拟环境
│   ├── config/                   # Django项目配置
│   │   ├── __init__.py
│   │   ├── settings.py           # 项目设置
│   │   ├── urls.py               # 根URL配置
│   │   └── wsgi.py
│   ├── tourism/                  # 主应用
│   │   ├── __init__.py
│   │   ├── models.py             # 数据模型
│   │   ├── serializers.py        # 序列化器
│   │   ├── views.py              # 视图
│   │   ├── urls.py               # 应用URL
│   │   ├── admin.py              # 管理后台
│   │   └── migrations/           # 数据库迁移
│   ├── fixtures/                 # 初始数据
│   │   └── initial_data.json     # 南锣鼓巷预置数据
│   ├── manage.py
│   └── requirements.txt          # Python依赖
│
├── frontend/                     # Vue3前端项目
│   ├── node_modules/
│   ├── public/
│   │   └── images/               # 静态图片资源
│   ├── src/
│   │   ├── api/                  # API请求封装
│   │   │   └── index.js
│   │   ├── assets/               # 静态资源
│   │   ├── components/           # 公共组件
│   │   │   ├── AppHeader.vue
│   │   │   ├── AppFooter.vue
│   │   │   ├── POICard.vue
│   │   │   ├── RouteCard.vue
│   │   │   └── SearchBar.vue
│   │   ├── views/                # 页面视图
│   │   │   ├── HomeView.vue
│   │   │   ├── POIListView.vue
│   │   │   ├── POIDetailView.vue
│   │   │   └── RoutesView.vue
│   │   ├── router/               # 路由配置
│   │   │   └── index.js
│   │   ├── App.vue
│   │   └── main.js
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
│
└── README.md                     # 项目说明文档
```

## Components and Interfaces

### 后端API接口设计

#### 1. 胡同信息接口

```
GET /api/hutong/
```

**Response:**
```json
{
  "id": 1,
  "name": "南锣鼓巷",
  "description": "南锣鼓巷是北京最古老的街区之一...",
  "location": "北京市东城区",
  "history": "南锣鼓巷始建于元代...",
  "features": ["历史文化", "特色小店", "名人故居"],
  "image": "/images/nanluoguxiang.jpg",
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### 2. POI列表接口

```
GET /api/pois/
```

**Response:**
```json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "name": "茅盾故居",
      "type": "名人故居",
      "brief": "中国现代著名作家茅盾的故居",
      "thumbnail": "/images/poi/maodun.jpg",
      "location": "后圆恩寺胡同13号"
    }
  ]
}
```

#### 3. POI详情接口

```
GET /api/pois/{id}/
```

**Response:**
```json
{
  "id": 1,
  "name": "茅盾故居",
  "type": "名人故居",
  "description": "茅盾故居位于后圆恩寺胡同13号，是一座典型的北京四合院...",
  "location": "后圆恩寺胡同13号",
  "coordinates": {"lat": 39.9375, "lng": 116.4039},
  "images": ["/images/poi/maodun1.jpg", "/images/poi/maodun2.jpg"],
  "opening_hours": "9:00-17:00",
  "tips": "周一闭馆",
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### 4. 推荐路线列表接口

```
GET /api/routes/
```

**Response:**
```json
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "name": "经典文化游",
      "description": "探访名人故居，感受历史文化",
      "duration": "2小时",
      "distance": "1.5公里",
      "poi_count": 5
    }
  ]
}
```

#### 5. 路线详情接口

```
GET /api/routes/{id}/
```

**Response:**
```json
{
  "id": 1,
  "name": "经典文化游",
  "description": "探访名人故居，感受历史文化",
  "duration": "2小时",
  "distance": "1.5公里",
  "pois": [
    {"order": 1, "poi": {...}},
    {"order": 2, "poi": {...}}
  ]
}
```

#### 6. 搜索接口

```
GET /api/search/?q={keyword}
```

**Response:**
```json
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "name": "茅盾故居",
      "type": "名人故居",
      "brief": "中国现代著名作家茅盾的故居",
      "thumbnail": "/images/poi/maodun.jpg"
    }
  ]
}
```

### 前端组件设计

#### 1. AppHeader组件
- 显示系统Logo和标题
- 提供主导航菜单（首页、景点、路线）
- 集成搜索栏组件

#### 2. SearchBar组件
- 搜索输入框
- 搜索按钮
- 清空功能
- 搜索结果下拉展示

#### 3. POICard组件
- 展示POI缩略图
- 显示POI名称和类型标签
- 简短描述文字
- 点击跳转到详情页

#### 4. RouteCard组件
- 展示路线名称
- 显示预计时间和距离
- 包含的POI数量
- 点击展开路线详情

### 前端路由设计

| 路径 | 组件 | 说明 |
|------|------|------|
| `/` | HomeView | 首页，胡同概览 |
| `/pois` | POIListView | POI列表页 |
| `/poi/:id` | POIDetailView | POI详情页 |
| `/routes` | RoutesView | 推荐路线页 |

## Data Models

### 数据库ER图

```
┌─────────────────┐       ┌─────────────────┐
│     Hutong      │       │       POI       │
├─────────────────┤       ├─────────────────┤
│ id (PK)         │       │ id (PK)         │
│ name            │       │ hutong_id (FK)  │──┐
│ description     │◄──────│ name            │  │
│ location        │       │ type            │  │
│ history         │       │ description     │  │
│ features (JSON) │       │ brief           │  │
│ image           │       │ location        │  │
│ created_at      │       │ coordinates     │  │
└─────────────────┘       │ images (JSON)   │  │
                          │ opening_hours   │  │
                          │ tips            │  │
                          │ order           │  │
                          │ created_at      │  │
                          └─────────────────┘  │
                                    ▲          │
                                    │          │
┌─────────────────┐       ┌─────────┴─────────┐
│      Route      │       │     RoutePOI      │
├─────────────────┤       ├───────────────────┤
│ id (PK)         │       │ id (PK)           │
│ hutong_id (FK)  │──┐    │ route_id (FK)     │──┐
│ name            │  │    │ poi_id (FK)       │──┘
│ description     │  │    │ order             │
│ duration        │  │    └───────────────────┘
│ distance        │  │              ▲
│ created_at      │  │              │
└─────────────────┘  │              │
         │           │              │
         └───────────┴──────────────┘
```

### Django Models定义

```python
# tourism/models.py

from django.db import models

class Hutong(models.Model):
    """胡同信息模型"""
    name = models.CharField(max_length=100, verbose_name="胡同名称")
    description = models.TextField(verbose_name="详细介绍")
    location = models.CharField(max_length=200, verbose_name="地理位置")
    history = models.TextField(verbose_name="历史沿革")
    features = models.JSONField(default=list, verbose_name="特色标签")
    image = models.CharField(max_length=500, verbose_name="封面图片")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "胡同"
        verbose_name_plural = "胡同"

class POI(models.Model):
    """兴趣点模型"""
    TYPE_CHOICES = [
        ('historic', '历史古迹'),
        ('celebrity', '名人故居'),
        ('shop', '特色店铺'),
        ('food', '美食餐饮'),
        ('culture', '文化场所'),
        ('other', '其他'),
    ]
    
    hutong = models.ForeignKey(Hutong, on_delete=models.CASCADE, related_name='pois')
    name = models.CharField(max_length=100, verbose_name="名称")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="类型")
    description = models.TextField(verbose_name="详细介绍")
    brief = models.CharField(max_length=200, verbose_name="简短描述")
    location = models.CharField(max_length=200, verbose_name="具体位置")
    coordinates = models.JSONField(null=True, blank=True, verbose_name="坐标")
    images = models.JSONField(default=list, verbose_name="图片列表")
    opening_hours = models.CharField(max_length=100, blank=True, verbose_name="开放时间")
    tips = models.CharField(max_length=200, blank=True, verbose_name="游览提示")
    order = models.IntegerField(default=0, verbose_name="排序")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "兴趣点"
        verbose_name_plural = "兴趣点"
        ordering = ['order', 'id']

class Route(models.Model):
    """推荐路线模型"""
    hutong = models.ForeignKey(Hutong, on_delete=models.CASCADE, related_name='routes')
    name = models.CharField(max_length=100, verbose_name="路线名称")
    description = models.TextField(verbose_name="路线介绍")
    duration = models.CharField(max_length=50, verbose_name="预计时间")
    distance = models.CharField(max_length=50, verbose_name="路线长度")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "推荐路线"
        verbose_name_plural = "推荐路线"

class RoutePOI(models.Model):
    """路线-POI关联模型"""
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='route_pois')
    poi = models.ForeignKey(POI, on_delete=models.CASCADE)
    order = models.IntegerField(verbose_name="顺序")

    class Meta:
        verbose_name = "路线景点"
        verbose_name_plural = "路线景点"
        ordering = ['order']
        unique_together = ['route', 'poi']
```



## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### Property 1: 胡同信息完整性

*For any* 胡同信息API请求，返回的数据应包含name、description、location、features（非空列表）和image（非空字符串）字段。

**Validates: Requirements 1.1, 1.2, 1.3**

### Property 2: POI序列化完整性

*For any* POI对象，序列化后的数据应包含id、name、type、brief、location字段；详情序列化还应包含description（长度>=100字符）和images（至少1个元素）字段。

**Validates: Requirements 2.2, 3.1, 3.2, 3.3, 3.4**

### Property 3: POI列表排序

*For any* POI列表API响应，返回的POI应按order字段升序排列。

**Validates: Requirements 2.4**

### Property 4: 路线信息完整性

*For any* 路线对象，序列化后的数据应包含name、description、duration、distance字段，且pois列表按order字段排序。

**Validates: Requirements 4.2, 4.3, 4.5**

### Property 5: 搜索结果相关性

*For any* 搜索关键词q和返回的POI列表，每个返回的POI的name或description字段应包含关键词q（不区分大小写）。

**Validates: Requirements 5.1**

### Property 6: API响应格式一致性

*For any* 成功的API请求，响应Content-Type应为application/json；*For any* 无效请求（如不存在的资源ID），应返回4xx状态码和包含错误信息的JSON响应。

**Validates: Requirements 6.6, 6.7**

## Error Handling

### 后端错误处理

| 错误类型 | HTTP状态码 | 响应格式 |
|----------|------------|----------|
| 资源不存在 | 404 | `{"detail": "Not found."}` |
| 请求参数错误 | 400 | `{"detail": "错误描述"}` |
| 服务器内部错误 | 500 | `{"detail": "Internal server error"}` |

### 前端错误处理

1. **网络错误**: 显示"网络连接失败，请检查网络设置"提示
2. **API错误**: 根据状态码显示相应错误信息
3. **数据加载失败**: 显示重试按钮，允许用户重新加载
4. **404页面**: 当访问不存在的POI或路线时，显示友好的404页面

## Testing Strategy

### 单元测试

使用pytest进行Django后端单元测试：
- 模型测试：验证数据模型的字段和方法
- 序列化器测试：验证数据序列化的正确性
- 视图测试：验证API端点的响应

使用Vitest进行Vue前端单元测试：
- 组件测试：验证组件渲染和交互
- API模块测试：验证请求封装的正确性

### 属性测试

使用Hypothesis库进行Python属性测试：
- 每个属性测试运行至少100次迭代
- 测试标注格式：`# Feature: nanluoguxiang-tourism, Property N: 属性描述`

### 集成测试

- API集成测试：验证完整的请求-响应流程
- 前后端集成测试：验证数据流通的正确性

### 测试数据

- 使用Django fixtures加载测试数据
- 属性测试使用Hypothesis生成随机测试数据
