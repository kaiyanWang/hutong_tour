// pages/poi-detail/poi-detail.js
const api = require('../../utils/api')
const app = getApp()

// 百度地图小程序AK
const BAIDU_MAP_AK = 'GJmkGJ3hoOKqsZHhGNukaTkcusjcyoIn'

Page({
  data: {
    poi: null,
    loading: true,
    isFavorite: false,
    currentImageIndex: 0,
    markers: []
  },

  onLoad(options) {
    const id = options.id
    if (id) {
      this.loadPOIDetail(id)
    } else {
      wx.showToast({
        title: '参数错误',
        icon: 'none'
      })
      setTimeout(() => {
        wx.navigateBack()
      }, 1500)
    }
  },

  onShow() {
    // 页面显示时检查收藏状态
    if (this.data.poi && app.checkLogin()) {
      this.checkFavoriteStatus(this.data.poi.id)
    }
  },

  async loadPOIDetail(id) {
    try {
      this.setData({ loading: true })
      const poi = await api.getPOIDetail(id)
      
      // 设置地图标记
      const markers = [{
        id: poi.id,
        longitude: poi.longitude,
        latitude: poi.latitude,
        title: poi.name,
        width: 30,
        height: 30,
        callout: {
          content: poi.name,
          color: '#333333',
          fontSize: 14,
          borderRadius: 8,
          bgColor: '#ffffff',
          padding: 8,
          display: 'ALWAYS'
        }
      }]
      
      this.setData({ 
        poi,
        markers,
        loading: false 
      })
      
      // 设置导航栏标题
      wx.setNavigationBarTitle({
        title: poi.name
      })
      
      // 检查收藏状态
      if (app.checkLogin()) {
        this.checkFavoriteStatus(id)
      }
    } catch (error) {
      console.error('加载POI详情失败:', error)
      this.setData({ loading: false })
      wx.showToast({
        title: '加载失败',
        icon: 'none'
      })
    }
  },

  async checkFavoriteStatus(poiId) {
    try {
      const result = await api.checkFavorite(poiId)
      this.setData({
        isFavorite: result.is_favorite
      })
    } catch (error) {
      console.error('检查收藏状态失败:', error)
    }
  },

  // 切换收藏状态
  async toggleFavorite() {
    if (!app.checkLogin()) {
      wx.showModal({
        title: '提示',
        content: '请先登录后再收藏',
        confirmText: '去登录',
        cancelText: '取消',
        success: (res) => {
          if (res.confirm) {
            wx.navigateTo({
              url: '/pages/login/login'
            })
          }
        }
      })
      return
    }

    const poiId = this.data.poi.id
    try {
      if (this.data.isFavorite) {
        await api.removeFavorite(poiId)
        this.setData({ isFavorite: false })
        wx.showToast({
          title: '已取消收藏',
          icon: 'success'
        })
      } else {
        await api.addFavorite(poiId)
        this.setData({ isFavorite: true })
        wx.showToast({
          title: '收藏成功',
          icon: 'success'
        })
      }
    } catch (error) {
      console.error('收藏操作失败:', error)
    }
  },

  // 图片切换
  onSwiperChange(e) {
    this.setData({
      currentImageIndex: e.detail.current
    })
  },

  // 预览图片
  previewImage(e) {
    const current = e.currentTarget.dataset.src
    wx.previewImage({
      current,
      urls: this.data.poi.images
    })
  },

  // 打开地图导航
  openNavigation() {
    if (!this.data.poi) return
    
    const { latitude, longitude, name, address } = this.data.poi
    wx.openLocation({
      latitude: latitude,
      longitude: longitude,
      name: name,
      address: address,
      scale: 18
    })
  },

  // 分享
  onShareAppMessage() {
    const poi = this.data.poi
    return {
      title: poi ? poi.name : '南锣鼓巷景点',
      path: `/pages/poi-detail/poi-detail?id=${poi ? poi.id : ''}`
    }
  }
})
