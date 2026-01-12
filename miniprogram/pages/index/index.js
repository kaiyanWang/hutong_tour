// pages/index/index.js
const api = require('../../utils/api')

// 百度地图小程序AK
const BAIDU_MAP_AK = 'GJmkGJ3hoOKqsZHhGNukaTkcusjcyoIn'

Page({
  data: {
    hutong: null,
    loading: true,
    markers: [],
    mapScale: 16,
    // 默认中心点（南锣鼓巷）
    defaultLatitude: 39.9375,
    defaultLongitude: 116.4030
  },

  onLoad() {
    this.loadHutongData()
  },

  onShow() {
    // 每次显示页面时刷新数据
  },

  onPullDownRefresh() {
    this.loadHutongData().then(() => {
      wx.stopPullDownRefresh()
    })
  },

  async loadHutongData() {
    try {
      this.setData({ loading: true })
      const hutong = await api.getHutong()
      
      // 设置地图标记
      const markers = [{
        id: 1,
        longitude: hutong.longitude,
        latitude: hutong.latitude,
        title: hutong.name,
        width: 30,
        height: 30,
        callout: {
          content: hutong.name,
          color: '#333333',
          fontSize: 14,
          borderRadius: 8,
          bgColor: '#ffffff',
          padding: 8,
          display: 'ALWAYS'
        }
      }]
      
      this.setData({ 
        hutong,
        markers,
        loading: false 
      })
    } catch (error) {
      console.error('加载胡同数据失败:', error)
      this.setData({ loading: false })
      wx.showToast({
        title: '加载失败，请重试',
        icon: 'none'
      })
    }
  },

  // 地图标记点击
  onMarkerTap(e) {
    const markerId = e.markerId
    if (this.data.hutong) {
      wx.showToast({
        title: this.data.hutong.name,
        icon: 'none'
      })
    }
  },

  // 打开地图导航
  openNavigation() {
    if (!this.data.hutong) return
    
    const { latitude, longitude, name } = this.data.hutong
    wx.openLocation({
      latitude: latitude,
      longitude: longitude,
      name: name,
      scale: 18
    })
  },

  // 跳转到POI列表
  navigateToPOIList() {
    wx.switchTab({
      url: '/pages/poi-list/poi-list'
    })
  },

  // 跳转到路线列表
  navigateToRouteList() {
    wx.switchTab({
      url: '/pages/route-list/route-list'
    })
  },

  // 跳转到登录页
  navigateToLogin() {
    wx.navigateTo({
      url: '/pages/login/login'
    })
  }
})
