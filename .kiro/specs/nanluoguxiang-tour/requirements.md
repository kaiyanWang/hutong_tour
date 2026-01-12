# Requirements Document

## Introduction

南锣鼓巷胡同智慧导览系统是一个面向游客的数字化旅游服务平台，提供Web端和微信小程序端两种访问方式，共享同一Django后端服务。系统旨在解决胡同旅游信息分散、导览体验单一的问题，为游客提供景点浏览、路线推荐、收藏管理等功能。

## Glossary

- **System**: 南锣鼓巷胡同智慧导览系统
- **User**: 使用系统的游客用户
- **POI**: Point of Interest，兴趣点/景点
- **Route**: 推荐游览路线
- **Favorite**: 用户收藏的景点
- **Backend**: Django后端服务
- **Web_Client**: Vue3 Web前端应用
- **MiniProgram**: 微信原生小程序客户端
- **Baidu_Map_API**: 百度地图开放平台API服务

## Requirements

### Requirement 1: 用户注册与登录

**User Story:** As a User, I want to register and login to the system, so that I can access personalized features like favorites.

#### Acceptance Criteria

1. WHEN a User submits registration form with username, password and confirm password, THE System SHALL create a new user account if username is unique and passwords match
2. WHEN a User submits registration with an existing username, THE System SHALL reject the registration and display an error message
3. WHEN a User submits registration with mismatched passwords, THE System SHALL reject the registration and display an error message
4. WHEN a User submits login form with valid credentials, THE System SHALL authenticate the user and return a token
5. WHEN a User submits login form with invalid credentials, THE System SHALL reject the login and display an error message
6. WHEN a User requests logout, THE System SHALL invalidate the user session
7. THE Backend SHALL provide RESTful API endpoints for registration, login and logout operations

### Requirement 2: 胡同概览展示

**User Story:** As a User, I want to view the overview of Nanluoguxiang Hutong, so that I can understand its history and cultural significance.

#### Acceptance Criteria

1. WHEN a User visits the homepage, THE System SHALL display the hutong overview including name, introduction, history and featured image
2. THE System SHALL display the hutong location on Baidu Map
3. WHEN the Web_Client loads the map, THE System SHALL use the Web AK (TfGPBvIrhd5l1qpC8wluqEB9ZZ2AOcCs) for Baidu Map API
4. WHEN the MiniProgram loads the map, THE System SHALL use the MiniProgram AK (GJmkGJ3hoOKqsZHhGNukaTkcusjcyoIn) for Baidu Map API

### Requirement 3: POI景点列表与详情

**User Story:** As a User, I want to browse and view POI details, so that I can learn about interesting places in the hutong.

#### Acceptance Criteria

1. WHEN a User visits the POI list page, THE System SHALL display all POIs with name, category, thumbnail and brief description
2. WHEN a User clicks on a POI item, THE System SHALL navigate to the POI detail page
3. WHEN a User views POI detail page, THE System SHALL display POI name, category, full description, images, location coordinates and address
4. THE System SHALL display the POI location on Baidu Map in the detail page
5. WHEN a User searches for POI by name, THE System SHALL return matching POIs that contain the search keyword
6. THE Backend SHALL provide at least 8 POIs with complete information

### Requirement 4: 推荐路线展示

**User Story:** As a User, I want to view recommended tour routes, so that I can plan my visit efficiently.

#### Acceptance Criteria

1. WHEN a User visits the route list page, THE System SHALL display available tour routes with name, duration and POI count
2. WHEN a User clicks on a route item, THE System SHALL navigate to the route detail page
3. WHEN a User views route detail page, THE System SHALL display route name, description, estimated duration and ordered list of POIs
4. THE System SHALL display the route path on Baidu Map connecting all POIs in order
5. THE Backend SHALL provide at least 2 complete tour routes

### Requirement 5: 景点收藏功能

**User Story:** As a User, I want to collect my favorite POIs, so that I can easily find them later.

#### Acceptance Criteria

1. WHEN an authenticated User clicks the favorite button on a POI, THE System SHALL add the POI to user's favorites
2. WHEN an authenticated User clicks the unfavorite button on a collected POI, THE System SHALL remove the POI from user's favorites
3. WHEN an unauthenticated User attempts to favorite a POI, THE System SHALL prompt the user to login
4. WHEN an authenticated User visits the favorites page, THE System SHALL display all POIs in user's favorites list
5. THE System SHALL indicate whether a POI is already in user's favorites when displaying POI detail

### Requirement 6: 搜索功能

**User Story:** As a User, I want to search for POIs, so that I can quickly find specific places.

#### Acceptance Criteria

1. WHEN a User enters a search keyword, THE System SHALL search POIs by name
2. WHEN search results are found, THE System SHALL display matching POIs in a list
3. WHEN no search results are found, THE System SHALL display a friendly message indicating no results
4. THE System SHALL support searching in both Web_Client and MiniProgram

### Requirement 7: 响应式界面设计

**User Story:** As a User, I want a clean and beautiful interface, so that I can have a pleasant browsing experience.

#### Acceptance Criteria

1. THE Web_Client SHALL use Element UI components for consistent styling
2. THE Web_Client SHALL implement responsive layout for different screen sizes
3. THE MiniProgram SHALL follow WeChat design guidelines
4. THE System SHALL use a consistent color scheme across all pages
5. THE System SHALL display loading indicators during data fetching operations

### Requirement 8: 后端API服务

**User Story:** As a developer, I want a well-structured backend API, so that both Web and MiniProgram clients can share the same data source.

#### Acceptance Criteria

1. THE Backend SHALL use Django framework with SQLite database
2. THE Backend SHALL provide RESTful API endpoints for all data operations
3. THE Backend SHALL support CORS for cross-origin requests from Web_Client
4. THE Backend SHALL use token-based authentication for protected endpoints
5. THE Backend SHALL have a superuser account with username "admin" and password "admin123"
6. THE Backend SHALL use venv virtual environment for dependency management
