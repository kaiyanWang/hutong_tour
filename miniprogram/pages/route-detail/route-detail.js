// pages/route-detail/route-detail.js
const api = require('../../utils/api')

// 百度地图小程序AK
const BAIDU_MAP_AK = 'GJmkGJ3hoOKqsZHhGNukaTkcusjcyoIn'

Page({
  data: {
    route: null,
    loading: true,
    markers: [],
    polyline: [],
    mapCenter: {
      latitude: 39.9375,
      longitude: 116.4030
    },
    mapScale: 15
  },

  onLoad(options) {
    const id = options.id
    if (id) {
      this.loadRouteDetail(id)
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

  async loadRouteDetail(id) {
    try {
      this.setData({ loading: true })
      const route = await api.getRouteDetail(id)
      
      // 生成地图标记和路线
      const markers = this.generateMarkers(route.pois)
      const polyline = this.generatePolyline(route.pois)
      
      // 计算地图中心点
      let mapCenter = this.data.mapCenter
      if (route.pois && route.pois.length > 0) {
        mapCenter = {
          latitude: route.pois[0].latitude,
          longitude: route.pois[0].longitude
        }
      }
      
      this.setData({ 
        route,
        markers,
        polyline,
        mapCenter,
        loading: false 
      })
      
      // 设置导航栏标题
      wx.setNavigationBarTitle({
        title: route.name
      })
    } catch (error) {
      console.error('加载路线详情失败:', error)
      this.setData({ loading: false })
      wx.showToast({
        title: '加载失败',
        icon: 'none'
      })
    }
  },

  // 生成地图标记
  generateMarkers(pois) {
    if (!pois || pois.length === 0) return []
    
    return pois.map((poi, index) => ({
      id: poi.id,
      longitude: poi.longitude,
      latitude: poi.latitude,
      title: poi.name,
      width: 32,
      height: 32,
      label: {
        content: `${index + 1}`,
        color: '#ffffff',
        fontSize: 12,
        bgColor: '#8B4513',
        borderRadius: 16,
        padding: 6,
        anchorX: 0,
        anchorY: -40
      },
      callout: {
        content: poi.name,
        color: '#333333',
        fontSize: 14,
        borderRadius: 8,
        bgColor: '#ffffff',
        padding: 8,
        display: 'BYCLICK'
      }
    }))
  },

  // 生成路线
  generatePolyline(pois) {
    if (!pois || pois.length < 2) return []
    
    const points = pois.map(poi => ({
      longitude: poi.longitude,
      latitude: poi.latitude
    }))
    
    return [{
      points,
      color: '#8B4513',
      width: 4,
      dottedLine: false,
      arrowLine: true
    }]
  },

  // 跳转到POI详情
  navigateToPOI(e) {
    const id = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/poi-detail/poi-detail?id=${id}`
    })
  },

  // 地图标记点击
  onMarkerTap(e) {
    const markerId = e.markerId
    const poi = this.data.route.pois.find(p => p.id === markerId)
    if (poi) {
      wx.showActionSheet({
        itemList: ['查看详情', '导航到此'],
        success: (res) => {
          if (res.tapIndex === 0) {
            wx.navigateTo({
              url: `/pages/poi-detail/poi-detail?id=${poi.id}`
            })
          } else if (res.tapIndex === 1) {
            wx.openLocation({
              latitude: poi.latitude,
              longitude: poi.longitude,
              name: poi.name,
              address: poi.address || '',
              scale: 18
            })
          }
        }
      })
    }
  },

  // 格式化时长
  formatDuration(minutes) {
    if (minutes < 60) {
      return `${minutes}分钟`
    }
    const hours = Math.floor(minutes / 60)
    const mins = minutes % 60
    return mins > 0 ? `${hours}小时${mins}分钟` : `${hours}小时`
  },

  // 分享
  onShareAppMessage() {
    const route = this.data.route
    return {
      title: route ? route.name : '南锣鼓巷推荐路线',
      path: `/pages/route-detail/route-detail?id=${route ? route.id : ''}`
    }
  }
})
