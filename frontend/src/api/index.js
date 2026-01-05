import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

// 获取胡同信息
export const getHutongInfo = () => api.get('/hutong/')

// 获取POI列表
export const getPOIList = () => api.get('/pois/')

// 获取POI详情
export const getPOIDetail = (id) => api.get(`/pois/${id}/`)

// 获取路线列表
export const getRouteList = () => api.get('/routes/')

// 获取路线详情
export const getRouteDetail = (id) => api.get(`/routes/${id}/`)

// 搜索POI
export const searchPOIs = (keyword) => api.get('/search/', { params: { q: keyword } })

export default api
