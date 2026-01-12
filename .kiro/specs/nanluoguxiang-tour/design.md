# Design Document

## Overview

南锣鼓巷胡同智慧导览系统采用前后端分离架构，后端使用Django REST Framework提供统一的API服务，前端分为Vue3 Web应用和微信原生小程序两个客户端。系统使用SQLite数据库存储数据，通过百度地图API提供地图展示功能。

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         客户端层                                  │
├─────────────────────────────┬───────────────────────────────────┤
│   Vue3 Web Client           │   WeChat MiniProgram              │
│   - Element UI              │   - 原生组件                       │
│   - Axios                   │   - wx.request                    │
│   - Vue Router              │   - 页面路由                       │
│   - Baidu Map JS API        │   - Baidu Map SDK                 │
│   AK: TfGPBvI...            │   AK: GJmkGJ3...                  │
└─────────────────────────────┴───────────────────────────────────┘
                              │
                              │ HTTP/HTTPS (RESTful API)
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Django Backend                              │
├─────────────────────────────────────────────────────────────────┤
│   - Django REST Framework                                        │
│   - Token Authentication                                         │
│   - CORS Headers                                                 │
│   - Admin Panel (admin/admin123)                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      SQLite Database                             │
│   - User, Hutong, POI, Route, RoutePOI, Favorite                │
└─────────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### Backend Components

#### 1. Django Apps Structure
```
backend/
├── manage.py
├── requirements.txt
├── hutong_tour/          # 项目配置
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── api/                  # API应用
│   ├── models.py         # 数据模型
│   ├── serializers.py    # 序列化器
│   ├── views.py          # 视图
│   ├── urls.py           # 路由
│   └── admin.py          # 管理后台
└── db.sqlite3
```

#### 2. API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | /api/register/ | 用户注册 | No |
| POST | /api/login/ | 用户登录 | No |
| POST | /api/logout/ | 用户登出 | Yes |
| GET | /api/hutong/ | 获取胡同概览 | No |
| GET | /api/pois/ | 获取POI列表 | No |
| GET | /api/pois/{id}/ | 获取POI详情 | No |
| GET | /api/pois/search/?q={keyword} | 搜索POI | No |
| GET | /api/routes/ | 获取路线列表 | No |
| GET | /api/routes/{id}/ | 获取路线详情 | No |
| GET | /api/favorites/ | 获取收藏列表 | Yes |
| POST | /api/favorites/ | 添加收藏 | Yes |
| DELETE | /api/favorites/{poi_id}/ | 取消收藏 | Yes |
| GET | /api/pois/{id}/is_favorite/ | 检查是否已收藏 | Yes |

### Frontend Components (Vue3)

```
frontend/
├── package.json
├── vite.config.js
├── index.html
├── src/
│   ├── main.js
│   ├── App.vue
│   ├── router/
│   │   └── index.js
│   ├── api/
│   │   └── index.js        # Axios配置和API调用
│   ├── stores/
│   │   └── user.js         # Pinia用户状态
│   ├── views/
│   │   ├── Home.vue        # 首页/胡同概览
│   │   ├── POIList.vue     # POI列表
│   │   ├── POIDetail.vue   # POI详情
│   │   ├── RouteList.vue   # 路线列表
│   │   ├── RouteDetail.vue # 路线详情
│   │   ├── Favorites.vue   # 收藏列表
│   │   ├── Login.vue       # 登录
│   │   └── Register.vue    # 注册
│   └── components/
│       ├── NavBar.vue      # 导航栏
│       ├── POICard.vue     # POI卡片
│       ├── BaiduMap.vue    # 百度地图组件
│       └── SearchBar.vue   # 搜索栏
```

### MiniProgram Components

```
miniprogram/
├── app.js
├── app.json
├── app.wxss
├── project.config.json
├── utils/
│   ├── api.js              # API请求封装
│   └── auth.js             # 认证工具
├── pages/
│   ├── index/              # 首页
│   ├── poi-list/           # POI列表
│   ├── poi-detail/         # POI详情
│   ├── route-list/         # 路线列表
│   ├── route-detail/       # 路线详情
│   ├── favorites/          # 收藏列表
│   ├── login/              # 登录
│   └── register/           # 注册
└── components/
    ├── poi-card/           # POI卡片组件
    └── nav-bar/            # 导航栏组件
```

## Data Models

### Entity Relationship Diagram

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│    User      │       │   Hutong     │       │    POI       │
├──────────────┤       ├──────────────┤       ├──────────────┤
│ id (PK)      │       │ id (PK)      │       │ id (PK)      │
│ username     │       │ name         │       │ name         │
│ password     │       │ introduction │       │ category     │
│ created_at   │       │ history      │       │ description  │
└──────────────┘       │ image        │       │ brief        │
       │               │ latitude     │       │ images       │
       │               │ longitude    │       │ latitude     │
       │               └──────────────┘       │ longitude    │
       │                                      │ address      │
       │                                      │ hutong_id(FK)│
       │               ┌──────────────┐       └──────────────┘
       │               │    Route     │              │
       │               ├──────────────┤              │
       │               │ id (PK)      │              │
       │               │ name         │              │
       │               │ description  │              │
       │               │ duration     │              │
       │               │ hutong_id(FK)│              │
       │               └──────────────┘              │
       │                      │                      │
       │               ┌──────────────┐              │
       │               │  RoutePOI    │              │
       │               ├──────────────┤              │
       │               │ id (PK)      │──────────────┘
       │               │ route_id(FK) │
       │               │ poi_id (FK)  │
       │               │ order        │
       │               └──────────────┘
       │
       │               ┌──────────────┐
       └───────────────│  Favorite    │
                       ├──────────────┤
                       │ id (PK)      │
                       │ user_id (FK) │
                       │ poi_id (FK)  │
                       │ created_at   │
                       └──────────────┘
```

### Django Models Definition

```python
from django.db import models
from django.contrib.auth.models import User

class Hutong(models.Model):
    name = models.CharField(max_length=100)
    introduction = models.TextField()
    history = models.TextField()
    image = models.URLField()
    latitude = models.FloatField()
    longitude = models.FloatField()

class POI(models.Model):
    CATEGORY_CHOICES = [
        ('historic', '历史古迹'),
        ('shop', '特色店铺'),
        ('food', '美食餐饮'),
        ('culture', '文化场所'),
        ('scenic', '景观'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    brief = models.CharField(max_length=200)
    images = models.JSONField(default=list)  # 存储图片URL列表
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=200)
    hutong = models.ForeignKey(Hutong, on_delete=models.CASCADE, related_name='pois')

class Route(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField()  # 预计时长(分钟)
    hutong = models.ForeignKey(Hutong, on_delete=models.CASCADE, related_name='routes')

class RoutePOI(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='route_pois')
    poi = models.ForeignKey(POI, on_delete=models.CASCADE)
    order = models.IntegerField()

    class Meta:
        ordering = ['order']

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    poi = models.ForeignKey(POI, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'poi']
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Registration Validation

*For any* registration request, the system should create a user account if and only if the username is unique AND the password matches the confirm password. Otherwise, the registration should be rejected with an appropriate error.

**Validates: Requirements 1.1, 1.2, 1.3**

### Property 2: Login Authentication

*For any* login request with credentials (username, password), the system should return a valid token if and only if the user exists AND the password is correct. Otherwise, the login should be rejected.

**Validates: Requirements 1.4, 1.5**

### Property 3: Logout Invalidation

*For any* authenticated user session, after logout, the previously valid token should no longer be accepted for authenticated requests.

**Validates: Requirements 1.6**

### Property 4: Hutong Data Completeness

*For any* hutong retrieved from the API, the response should contain all required fields: name, introduction, history, image, latitude, and longitude.

**Validates: Requirements 2.1**

### Property 5: POI List Data Completeness

*For any* POI in the list response, the POI should contain: name, category, brief description, and at least one image URL.

**Validates: Requirements 3.1**

### Property 6: POI Detail Data Completeness

*For any* POI detail retrieved by ID, the response should contain all required fields: name, category, description, images, latitude, longitude, and address.

**Validates: Requirements 3.3**

### Property 7: Search Result Relevance

*For any* search query keyword and POI in the database, if the keyword is contained in the POI name (case-insensitive), then that POI should appear in the search results.

**Validates: Requirements 3.5, 6.1**

### Property 8: Route Data Completeness

*For any* route in the list response, the route should contain: name, duration, and POI count. For route detail, it should also include description and ordered list of POIs.

**Validates: Requirements 4.1, 4.3**

### Property 9: Favorite Round-Trip

*For any* authenticated user and POI, adding the POI to favorites then checking favorites list should include that POI. Removing the POI from favorites then checking favorites list should not include that POI.

**Validates: Requirements 5.1, 5.2, 5.4**

### Property 10: Favorite Status Consistency

*For any* authenticated user and POI, the is_favorite endpoint should return true if and only if the POI is in the user's favorites list.

**Validates: Requirements 5.5**

### Property 11: Authentication Required for Protected Endpoints

*For any* request to a protected endpoint (favorites operations) without a valid token, the system should reject the request with 401 Unauthorized.

**Validates: Requirements 5.3, 8.4**

## Error Handling

### Backend Error Responses

| Status Code | Scenario | Response Format |
|-------------|----------|-----------------|
| 400 | Invalid request data | `{"error": "error message"}` |
| 401 | Unauthorized access | `{"error": "Authentication required"}` |
| 404 | Resource not found | `{"error": "Resource not found"}` |
| 409 | Conflict (duplicate) | `{"error": "Username already exists"}` |
| 500 | Server error | `{"error": "Internal server error"}` |

### Frontend Error Handling

- Display user-friendly error messages using Element UI Message component
- Redirect to login page when receiving 401 response
- Show loading state during API calls
- Handle network errors gracefully

### MiniProgram Error Handling

- Use wx.showToast for error messages
- Navigate to login page on authentication errors
- Show loading indicator using wx.showLoading

## Testing Strategy

### Unit Tests

Unit tests will verify specific examples and edge cases:

1. **User Registration Tests**
   - Test successful registration with valid data
   - Test registration rejection with duplicate username
   - Test registration rejection with mismatched passwords

2. **User Login Tests**
   - Test successful login returns token
   - Test login rejection with wrong password
   - Test login rejection with non-existent user

3. **POI API Tests**
   - Test POI list returns all POIs
   - Test POI detail returns complete data
   - Test search returns matching results
   - Test search with no matches returns empty list

4. **Route API Tests**
   - Test route list returns all routes
   - Test route detail includes ordered POIs

5. **Favorite API Tests**
   - Test add favorite requires authentication
   - Test add favorite succeeds for authenticated user
   - Test remove favorite works correctly
   - Test favorites list returns user's favorites only

### Property-Based Tests

Property-based tests will use Python's `hypothesis` library to verify universal properties:

- Minimum 100 iterations per property test
- Each test tagged with: **Feature: nanluoguxiang-tour, Property {number}: {property_text}**

### Test Configuration

```python
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*

# For hypothesis
hypothesis_profile = default
```

### Test Data

Initial test data will include:
- 1 Hutong (南锣鼓巷)
- 8+ POIs with complete information
- 2+ Routes with POI associations
- Test users for authentication tests
