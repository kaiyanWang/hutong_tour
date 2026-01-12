// pages/poi-list/poi-list.js
const api = require('../../utils/api')

Page({
  data: {
    pois: [],
    filteredPois: [],
    loading: true,
    searchKeyword: '',
    categories: [
      { key: 'all', name: '全部' },
      { key: 'historic', name: '历史古迹' },
      { key: 'shop', name: '特色店铺' },
      { key: 'food', name: '美食餐饮' },
      { key: 'culture', name: '文化场所' },
      { key: 'scenic', name: '景观' }
    ],
    selectedCategory: 'all'
  },

  onLoad() {
    this.loadPOIList()
  },

  onShow() {
    // 页面显示时刷新
  },

  onPullDownRefresh() {
    this.loadPOIList().then(() => {
      wx.stopPullDownRefresh()
    })
  },

  async loadPOIList() {
    try {
      this.setData({ loading: true })
      const pois = await api.getPOIList()
      this.setData({ 
        pois,
        filteredPois: pois,
        loading: false 
      })
    } catch (error) {
      console.error('加载POI列表失败:', error)
      this.setData({ loading: false })
      wx.showToast({
        title: '加载失败，请重试',
        icon: 'none'
      })
    }
  },

  // 搜索输入
  onSearchInput(e) {
    this.setData({
      searchKeyword: e.detail.value
    })
  },

  // 执行搜索
  async onSearch() {
    const keyword = this.data.searchKeyword.trim()
    if (!keyword) {
      this.loadPOIList()
      return
    }

    try {
      this.setData({ loading: true })
      const pois = await api.searchPOI(keyword)
      this.setData({ 
        pois,
        filteredPois: pois,
        selectedCategory: 'all',
        loading: false 
      })
      
      if (pois.length === 0) {
        wx.showToast({
          title: '未找到相关景点',
          icon: 'none'
        })
      }
    } catch (error) {
      console.error('搜索失败:', error)
      this.setData({ loading: false })
    }
  },

  // 清除搜索
  onClearSearch() {
    this.setData({ searchKeyword: '' })
    this.loadPOIList()
  },

  // 选择分类
  onCategorySelect(e) {
    const category = e.currentTarget.dataset.category
    this.setData({ selectedCategory: category })
    this.filterByCategory(category)
  },

  // 按分类筛选
  filterByCategory(category) {
    if (category === 'all') {
      this.setData({ filteredPois: this.data.pois })
    } else {
      const filtered = this.data.pois.filter(poi => poi.category === category)
      this.setData({ filteredPois: filtered })
    }
  },

  // 跳转到POI详情
  navigateToDetail(e) {
    const id = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/poi-detail/poi-detail?id=${id}`
    })
  },

  // 获取分类显示名称
  getCategoryDisplay(category) {
    const categoryMap = {
      'historic': '历史古迹',
      'shop': '特色店铺',
      'food': '美食餐饮',
      'culture': '文化场所',
      'scenic': '景观'
    }
    return categoryMap[category] || category
  }
})
