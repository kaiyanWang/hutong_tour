import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

// Create axios instance
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor - add token to headers
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Token ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor - handle errors
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response) {
      const { status, data } = error.response
      
      switch (status) {
        case 401:
          // Unauthorized - clear token and redirect to login
          localStorage.removeItem('token')
          localStorage.removeItem('username')
          ElMessage.error('请先登录')
          router.push({ name: 'Login' })
          break
        case 404:
          ElMessage.error('资源不存在')
          break
        case 409:
          ElMessage.error(data.error || '操作冲突')
          break
        case 500:
          ElMessage.error('服务器错误，请稍后重试')
          break
        default:
          ElMessage.error(data.error || '请求失败')
      }
    } else if (error.request) {
      ElMessage.error('网络错误，请检查网络连接')
    } else {
      ElMessage.error('请求配置错误')
    }
    return Promise.reject(error)
  }
)

// Auth API
export const authAPI = {
  register(data) {
    return api.post('/register/', data)
  },
  login(data) {
    return api.post('/login/', data)
  },
  logout() {
    return api.post('/logout/')
  }
}

// Hutong API
export const hutongAPI = {
  getOverview() {
    return api.get('/hutong/')
  }
}

// POI API
export const poiAPI = {
  getList() {
    return api.get('/pois/')
  },
  getDetail(id) {
    return api.get(`/pois/${id}/`)
  },
  search(keyword) {
    return api.get('/pois/search/', { params: { q: keyword } })
  },
  checkFavorite(id) {
    return api.get(`/pois/${id}/is_favorite/`)
  }
}

// Route API
export const routeAPI = {
  getList() {
    return api.get('/routes/')
  },
  getDetail(id) {
    return api.get(`/routes/${id}/`)
  }
}

// Favorite API
export const favoriteAPI = {
  getList() {
    return api.get('/favorites/')
  },
  add(poiId) {
    return api.post('/favorites/add/', { poi_id: poiId })
  },
  remove(poiId) {
    return api.delete(`/favorites/${poiId}/`)
  }
}

export default api
