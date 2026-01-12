// API请求封装
const app = getApp()

// 获取基础URL
const getBaseUrl = () => {
  return app.globalData.baseUrl
}

// 通用请求方法
const request = (options) => {
  return new Promise((resolve, reject) => {
    const { url, method = 'GET', data = {}, needAuth = false } = options
    
    const header = {
      'Content-Type': 'application/json'
    }
    
    // 如果需要认证，添加Token
    if (needAuth) {
      const token = app.globalData.token || wx.getStorageSync('token')
      if (token) {
        header['Authorization'] = `Token ${token}`
      } else {
        // 未登录，跳转到登录页
        wx.showToast({
          title: '请先登录',
          icon: 'none'
        })
        wx.navigateTo({
          url: '/pages/login/login'
        })
        reject(new Error('未登录'))
        return
      }
    }
    
    wx.request({
      url: `${getBaseUrl()}${url}`,
      method,
      data,
      header,
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data)
        } else if (res.statusCode === 401) {
          // Token失效，清除登录状态
          app.clearLoginState()
          wx.showToast({
            title: '登录已过期，请重新登录',
            icon: 'none'
          })
          wx.navigateTo({
            url: '/pages/login/login'
          })
          reject(new Error('认证失败'))
        } else {
          const errorMsg = res.data.error || res.data.detail || '请求失败'
          wx.showToast({
            title: errorMsg,
            icon: 'none'
          })
          reject(new Error(errorMsg))
        }
      },
      fail: (err) => {
        wx.showToast({
          title: '网络错误，请稍后重试',
          icon: 'none'
        })
        reject(err)
      }
    })
  })
}

// ==================== 用户认证API ====================

// 用户注册
const register = (username, password, confirmPassword) => {
  return request({
    url: '/api/register/',
    method: 'POST',
    data: {
      username,
      password,
      confirm_password: confirmPassword
    }
  })
}

// 用户登录
const login = (username, password) => {
  return request({
    url: '/api/login/',
    method: 'POST',
    data: {
      username,
      password
    }
  })
}

// 用户登出
const logout = () => {
  return request({
    url: '/api/logout/',
    method: 'POST',
    needAuth: true
  })
}

// ==================== 胡同API ====================

// 获取胡同概览
const getHutong = () => {
  return request({
    url: '/api/hutong/'
  })
}

// ==================== POI API ====================

// 获取POI列表
const getPOIList = () => {
  return request({
    url: '/api/pois/'
  })
}

// 获取POI详情
const getPOIDetail = (id) => {
  return request({
    url: `/api/pois/${id}/`
  })
}

// 搜索POI
const searchPOI = (keyword) => {
  return request({
    url: `/api/pois/search/?q=${encodeURIComponent(keyword)}`
  })
}

// 检查POI是否已收藏
const checkFavorite = (poiId) => {
  return request({
    url: `/api/pois/${poiId}/is_favorite/`,
    needAuth: true
  })
}

// ==================== 路线API ====================

// 获取路线列表
const getRouteList = () => {
  return request({
    url: '/api/routes/'
  })
}

// 获取路线详情
const getRouteDetail = (id) => {
  return request({
    url: `/api/routes/${id}/`
  })
}

// ==================== 收藏API ====================

// 获取收藏列表
const getFavorites = () => {
  return request({
    url: '/api/favorites/',
    needAuth: true
  })
}

// 添加收藏
const addFavorite = (poiId) => {
  return request({
    url: '/api/favorites/',
    method: 'POST',
    data: {
      poi_id: poiId
    },
    needAuth: true
  })
}

// 删除收藏
const removeFavorite = (poiId) => {
  return request({
    url: `/api/favorites/${poiId}/`,
    method: 'DELETE',
    needAuth: true
  })
}

module.exports = {
  request,
  // 用户认证
  register,
  login,
  logout,
  // 胡同
  getHutong,
  // POI
  getPOIList,
  getPOIDetail,
  searchPOI,
  checkFavorite,
  // 路线
  getRouteList,
  getRouteDetail,
  // 收藏
  getFavorites,
  addFavorite,
  removeFavorite
}
