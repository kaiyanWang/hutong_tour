const app = getApp()

Page({
  data: {
    pois: [],
    keyword: '',
    loading: false
  },

  onLoad() {
    this.loadPOIs()
  },

  onPullDownRefresh() {
    this.loadPOIs().then(() => {
      wx.stopPullDownRefresh()
    })
  },

  async loadPOIs() {
    this.setData({ loading: true })
    try {
      const data = await app.request('/pois/')
      this.setData({ pois: data.results || [] })
    } catch (err) {
      console.error('获取景点列表失败:', err)
      wx.showToast({ title: '加载失败', icon: 'none' })
    } finally {
      this.setData({ loading: false })
    }
  },

  onSearchInput(e) {
    this.setData({ keyword: e.detail.value })
  },

  async onSearch() {
    const { keyword } = this.data
    if (!keyword.trim()) {
      this.loadPOIs()
      return
    }
    
    this.setData({ loading: true })
    try {
      const data = await app.request(`/search/?q=${encodeURIComponent(keyword)}`)
      this.setData({ pois: data.results || [] })
    } catch (err) {
      console.error('搜索失败:', err)
      wx.showToast({ title: '搜索失败', icon: 'none' })
    } finally {
      this.setData({ loading: false })
    }
  },

  clearSearch() {
    this.setData({ keyword: '' })
    this.loadPOIs()
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
