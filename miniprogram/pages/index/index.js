const app = getApp()

Page({
  data: {
    hutong: {},
    poiCount: 0,
    routeCount: 0
  },

  onLoad() {
    this.loadHutongInfo()
    this.loadCounts()
  },

  onPullDownRefresh() {
    this.loadHutongInfo().then(() => {
      wx.stopPullDownRefresh()
    })
  },

  async loadHutongInfo() {
    try {
      const data = await app.request('/hutong/')
      this.setData({ hutong: data })
    } catch (err) {
      console.error('获取胡同信息失败:', err)
      wx.showToast({ title: '加载失败', icon: 'none' })
    }
  },

  async loadCounts() {
    try {
      const [pois, routes] = await Promise.all([
        app.request('/pois/'),
        app.request('/routes/')
      ])
      this.setData({
        poiCount: pois.count || 0,
        routeCount: routes.count || 0
      })
    } catch (err) {
      console.error('获取统计失败:', err)
    }
  },

  goToPois() {
    wx.switchTab({ url: '/pages/pois/pois' })
  },

  goToRoutes() {
    wx.switchTab({ url: '/pages/routes/routes' })
  }
})
