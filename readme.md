## 项目结构

```
├── backend/          # Django后端
├── frontend/         # Vue3前端
├── miniprogram/      # 微信小程序
└── readme.md
```

## 技术栈

- **后端**: Django + Django REST Framework + SQLite
- **前端**: Vue3 + Vite + Element Plus
- **小程序**: 微信原生小程序

## 快速开始

### 后端启动

```
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata initial_data
python manage.py runserver 8000
```

### 前端启动

```
cd frontend
npm install
npm run dev
```

### 小程序

使用微信开发者工具打开 `miniprogram` 目录