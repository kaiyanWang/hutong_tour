// pages/route-list/route-list.js
const api = require('../../utils/api')

Page({
  data: {
    routes: [],
    loading: true
  },

  onLoad() {
    this.loadRouteList()
  },

  onShow() {
    // 页面显示时刷新
  },

  onPullDownRefresh() {
    this.loadRouteList().then(() => {
      wx.stopPullDownRefresh()
    })
  },

  async loadRouteList() {
    try {
      this.setData({ loading: true })
      const routes = await api.getRouteList()
      this.setData({ 
        routes,
        loading: false 
      })
    } catch (error) {
      console.error('加载路线列表失败:', error)
      this.setData({ loading: false })
      wx.showToast({
        title: '加载失败，请重试',
        icon: 'none'
      })
    }
  },

  // 跳转到路线详情
  navigateToDetail(e) {
    const id = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/route-detail/route-detail?id=${id}`
    })
  },

  // 格式化时长
  formatDuration(minutes) {
    if (minutes < 60) {
      return `${minutes}分钟`
    }
    const hours = Math.floor(minutes / 60)
    const mins = minutes % 60
    return mins > 0 ? `${hours}小时${mins}分钟` : `${hours}小时`
  }
})
