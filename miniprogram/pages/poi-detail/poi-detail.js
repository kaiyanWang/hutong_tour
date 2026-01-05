const app = getApp()

Page({
  data: {
    poi: null
  },

  onLoad(options) {
    if (options.id) {
      this.loadPOIDetail(options.id)
    }
  },

  async loadPOIDetail(id) {
    try {
      const data = await app.request(`/pois/${id}/`)
      this.setData({ poi: data })
      wx.setNavigationBarTitle({ title: data.name })
    } catch (err) {
      console.error('获取景点详情失败:', err)
      wx.showToast({ title: '加载失败', icon: 'none' })
    }
  },

  previewImage(e) {
    const url = e.currentTarget.dataset.url
    wx.previewImage({
      current: url,
      urls: this.data.poi.images
    })
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
