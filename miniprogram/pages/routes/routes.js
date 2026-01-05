const app = getApp()

Page({
  data: {
    routes: [],
    expandedRoute: null,
    routeDetail: null
  },

  onLoad() {
    this.loadRoutes()
  },

  onPullDownRefresh() {
    this.loadRoutes().then(() => {
      wx.stopPullDownRefresh()
    })
  },

  async loadRoutes() {
    try {
      const data = await app.request('/routes/')
      this.setData({ routes: data.results || [] })
    } catch (err) {
      console.error('获取路线列表失败:', err)
      wx.showToast({ title: '加载失败', icon: 'none' })
    }
  },

  async toggleRoute(e) {
    const id = e.currentTarget.dataset.id
    
    if (this.data.expandedRoute === id) {
      this.setData({ expandedRoute: null, routeDetail: null })
      return
    }

    try {
      const data = await app.request(`/routes/${id}/`)
      this.setData({ 
        expandedRoute: id,
        routeDetail: data
      })
    } catch (err) {
      console.error('获取路线详情失败:', err)
      wx.showToast({ title: '加载失败', icon: 'none' })
    }
  },

  goToDetail(e) {
    const id = e.currentTarget.dataset.id
    wx.navigateTo({ url: `/pages/poi-detail/poi-detail?id=${id}` })
  },

  getTagClass(type) {
    const classes = {
      'celebrity': 'tag-celebrity',
      'historic': 'tag-historic',
      'food': 'tag-food',
      'shop': 'tag-shop',
      'culture': 'tag-culture'
    }
    return classes[type] || ''
  }
})
