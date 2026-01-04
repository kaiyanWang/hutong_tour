# 南锣鼓巷智慧导览系统

基于 Django + Web 的胡同旅游导览系统。

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py migrate

# 初始化示例数据
python manage.py init_data

# 启动服务
python manage.py runserver
```

访问 http://127.0.0.1:8000

## 后台管理

访问 http://127.0.0.1:8000/admin

- 用户名: admin
- 密码: admin123

## 功能模块

- 胡同概览：展示南锣鼓巷基本信息
- POI景点：10个核心景点详情
- 推荐路线：2条游览路线
- 搜索功能：按名称搜索景点
- 收藏功能：收藏喜欢的景点

## 技术栈

- 后端: Django 5.x
- 数据库: SQLite
- 前端: Bootstrap 5 + Bootstrap Icons
