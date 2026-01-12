# Implementation Plan: 南锣鼓巷胡同智慧导览系统

## Overview

本实现计划将系统分为三个主要部分：Django后端、Vue3 Web前端、微信小程序。采用增量开发方式，先完成后端API，再实现两个前端客户端。

## Tasks

- [x] 1. Django后端项目初始化
  - [x] 1.1 创建Django项目和虚拟环境
    - 创建venv虚拟环境
    - 安装Django、djangorestframework、django-cors-headers
    - 创建hutong_tour项目和api应用
    - 配置settings.py（CORS、REST Framework、SQLite）
    - _Requirements: 8.1, 8.3, 8.6_

  - [x] 1.2 创建数据模型
    - 实现Hutong、POI、Route、RoutePOI、Favorite模型
    - 执行数据库迁移
    - 创建超级用户admin/admin123
    - _Requirements: 8.5_

  - [x] 1.3 配置Django Admin
    - 注册所有模型到Admin
    - 配置Admin显示字段
    - _Requirements: 8.5_

- [x] 2. 用户认证API实现
  - [x] 2.1 实现用户注册API
    - 创建注册序列化器和视图
    - 验证用户名唯一性和密码匹配
    - _Requirements: 1.1, 1.2, 1.3_

  - [x] 2.2 实现用户登录API
    - 创建登录视图，返回Token
    - 验证用户凭据
    - _Requirements: 1.4, 1.5_

  - [x] 2.3 实现用户登出API
    - 创建登出视图，删除Token
    - _Requirements: 1.6_

  - [x] 2.4 编写认证API属性测试
    - **Property 1: Registration Validation**
    - **Property 2: Login Authentication**
    - **Property 3: Logout Invalidation**
    - **Validates: Requirements 1.1-1.6**

- [x] 3. 胡同和POI API实现
  - [x] 3.1 实现胡同概览API
    - 创建Hutong序列化器和视图
    - 返回胡同基本信息
    - _Requirements: 2.1_

  - [x] 3.2 实现POI列表和详情API
    - 创建POI序列化器（列表和详情）
    - 实现POI列表视图
    - 实现POI详情视图
    - _Requirements: 3.1, 3.3_

  - [x] 3.3 实现POI搜索API
    - 实现按名称搜索功能
    - 支持模糊匹配
    - _Requirements: 3.5, 6.1, 6.2, 6.3_

  - [x] 3.4 编写POI API属性测试
    - **Property 4: Hutong Data Completeness**
    - **Property 5: POI List Data Completeness**
    - **Property 6: POI Detail Data Completeness**
    - **Property 7: Search Result Relevance**
    - **Validates: Requirements 2.1, 3.1, 3.3, 3.5**

- [x] 4. 路线API实现
  - [x] 4.1 实现路线列表和详情API
    - 创建Route序列化器（包含POI数量）
    - 实现路线列表视图
    - 实现路线详情视图（包含有序POI列表）
    - _Requirements: 4.1, 4.3_

  - [x] 4.2 编写路线API属性测试
    - **Property 8: Route Data Completeness**
    - **Validates: Requirements 4.1, 4.3**

- [x] 5. 收藏功能API实现
  - [x] 5.1 实现收藏列表API
    - 创建Favorite序列化器
    - 实现获取用户收藏列表视图
    - 需要Token认证
    - _Requirements: 5.4_

  - [x] 5.2 实现添加和删除收藏API
    - 实现添加收藏视图
    - 实现删除收藏视图
    - 实现检查是否已收藏视图
    - _Requirements: 5.1, 5.2, 5.3, 5.5_

  - [x] 5.3 编写收藏API属性测试
    - **Property 9: Favorite Round-Trip**
    - **Property 10: Favorite Status Consistency**
    - **Property 11: Authentication Required for Protected Endpoints**
    - **Validates: Requirements 5.1-5.5, 8.4**

- [x] 6. 初始化南锣鼓巷数据
  - [x] 6.1 创建数据初始化脚本
    - 创建南锣鼓巷胡同数据
    - 创建至少8个POI数据（包含真实景点信息）
    - 创建至少2条推荐路线
    - _Requirements: 3.6, 4.5_

- [x] 7. Checkpoint - 后端API完成
  - 确保所有API测试通过
  - 验证Admin后台可正常访问
  - 如有问题请询问用户

- [x] 8. Vue3 Web前端项目初始化
  - [x] 8.1 创建Vue3项目
    - 使用Vite创建Vue3项目
    - 安装Element Plus、Vue Router、Pinia、Axios
    - 配置项目结构
    - _Requirements: 7.1_

  - [x] 8.2 配置API请求和路由
    - 配置Axios实例和拦截器
    - 配置Vue Router路由
    - 创建Pinia用户状态管理
    - _Requirements: 7.1_

- [-] 9. Web前端页面实现
  - [x] 9.1 实现导航栏和布局组件
    - 创建NavBar组件（包含登录状态显示）
    - 创建基础布局
    - _Requirements: 7.1, 7.4_

  - [x] 9.2 实现用户认证页面
    - 创建Login登录页面
    - 创建Register注册页面
    - 实现表单验证和提交
    - _Requirements: 1.1-1.6, 7.1_

  - [x] 9.3 实现首页和胡同概览
    - 创建Home首页组件
    - 集成百度地图显示胡同位置
    - 使用Web端AK: TfGPBvIrhd5l1qpC8wluqEB9ZZ2AOcCs
    - _Requirements: 2.1, 2.2, 2.3_

  - [x] 9.4 实现POI列表和详情页面
    - 创建POIList页面（含搜索功能）
    - 创建POICard组件
    - 创建POIDetail页面（含地图和收藏按钮）
    - _Requirements: 3.1-3.5, 5.1, 5.2, 5.5, 6.1-6.3_

  - [x] 9.5 实现路线列表和详情页面
    - 创建RouteList页面
    - 创建RouteDetail页面（含地图路线展示）
    - _Requirements: 4.1-4.4_

  - [x] 9.6 实现收藏页面
    - 创建Favorites页面
    - 显示用户收藏的POI列表
    - _Requirements: 5.4_

- [x] 10. Checkpoint - Web前端完成
  - 确保所有页面功能正常
  - 验证与后端API交互正确
  - 如有问题请询问用户

- [x] 11. 微信小程序项目初始化
  - [x] 11.1 创建小程序项目结构
    - 配置app.json页面路由
    - 配置app.wxss全局样式
    - 创建utils/api.js请求封装
    - _Requirements: 7.3_

- [x] 12. 小程序页面实现
  - [x] 12.1 实现首页和胡同概览
    - 创建index首页
    - 集成百度地图小程序SDK
    - 使用小程序端AK: GJmkGJ3hoOKqsZHhGNukaTkcusjcyoIn
    - _Requirements: 2.1, 2.2, 2.4_

  - [x] 12.2 实现用户认证页面
    - 创建login登录页面
    - 创建register注册页面
    - 实现Token存储
    - _Requirements: 1.1-1.6_

  - [x] 12.3 实现POI列表和详情页面
    - 创建poi-list页面（含搜索）
    - 创建poi-detail页面（含地图和收藏）
    - _Requirements: 3.1-3.5, 5.1, 5.2, 5.5, 6.1-6.3_

  - [x] 12.4 实现路线列表和详情页面
    - 创建route-list页面
    - 创建route-detail页面
    - _Requirements: 4.1-4.4_

  - [x] 12.5 实现收藏页面
    - 创建favorites页面
    - _Requirements: 5.4_

- [x] 13. Final Checkpoint - 系统集成完成
  - 确保Web端和小程序端功能完整
  - 验证所有核心功能正常运行
  - 如有问题请询问用户

## Notes

- All tasks including property-based tests are required
- 后端使用Python hypothesis库进行属性测试
- Web前端使用百度地图JavaScript API
- 小程序使用百度地图微信小程序SDK
- 所有API请求需要处理错误情况并显示友好提示
