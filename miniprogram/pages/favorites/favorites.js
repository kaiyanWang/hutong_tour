// pages/favorites/favorites.js
const api = require('../../utils/api')
const app = getApp()

Page({
  data: {
    favorites: [],
    loading: true,
    isLoggedIn: false
  },

  onLoad() {
    this.checkLoginAndLoad()
  },

  onShow() {
    // 每次显示页面时检查登录状态并刷新
    this.checkLoginAndLoad()
  },

  onPullDownRefresh() {
    if (this.data.isLoggedIn) {
      this.loadFavorites().then(() => {
        wx.stopPullDownRefresh()
      })
    } else {
      wx.stopPullDownRefresh()
    }
  },

  checkLoginAndLoad() {
    const isLoggedIn = app.checkLogin()
    this.setData({ isLoggedIn })
    
    if (isLoggedIn) {
      this.loadFavorites()
    } else {
      this.setData({ 
        loading: false,
        favorites: []
      })
    }
  },

  async loadFavorites() {
    try {
      this.setData({ loading: true })
      const favorites = await api.getFavorites()
      this.setData({ 
        favorites,
        loading: false 
      })
    } catch (error) {
      console.error('加载收藏列表失败:', error)
      this.setData({ loading: false })
      wx.showToast({
        title: '加载失败，请重试',
        icon: 'none'
      })
    }
  },

  // 跳转到POI详情
  navigateToDetail(e) {
    const id = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/poi-detail/poi-detail?id=${id}`
    })
  },

  // 跳转到登录页
  navigateToLogin() {
    wx.navigateTo({
      url: '/pages/login/login'
    })
  },

  // 跳转到景点列表
  navigateToPOIList() {
    wx.switchTab({
      url: '/pages/poi-list/poi-list'
    })
  },

  // 取消收藏
  async removeFavorite(e) {
    const poiId = e.currentTarget.dataset.id
    const poiName = e.currentTarget.dataset.name
    
    wx.showModal({
      title: '确认取消收藏',
      content: `确定要取消收藏"${poiName}"吗？`,
      confirmColor: '#8B4513',
      success: async (res) => {
        if (res.confirm) {
          try {
            await api.removeFavorite(poiId)
            wx.showToast({
              title: '已取消收藏',
              icon: 'success'
            })
            // 刷新列表
            this.loadFavorites()
          } catch (error) {
            console.error('取消收藏失败:', error)
          }
        }
      }
    })
  },

  // 格式化时间
  formatTime(dateStr) {
    if (!dateStr) return ''
    const date = new Date(dateStr)
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    return `${year}-${month}-${day}`
  }
})
