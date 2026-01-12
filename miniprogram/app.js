// app.js
App({
  onLaunch() {
    // 检查登录状态
    const token = wx.getStorageSync('token')
    if (token) {
      this.globalData.isLoggedIn = true
      this.globalData.token = token
    }
  },

  globalData: {
    isLoggedIn: false,
    token: null,
    userInfo: null,
    // 后端API基础URL - 开发时使用本地地址，发布时需要修改为线上地址
    baseUrl: 'http://39.99.43.230:8002'
  },

  // 设置登录状态
  setLoginState(token, userInfo = null) {
    this.globalData.isLoggedIn = true
    this.globalData.token = token
    this.globalData.userInfo = userInfo
    wx.setStorageSync('token', token)
    if (userInfo) {
      wx.setStorageSync('userInfo', userInfo)
    }
  },

  // 清除登录状态
  clearLoginState() {
    this.globalData.isLoggedIn = false
    this.globalData.token = null
    this.globalData.userInfo = null
    wx.removeStorageSync('token')
    wx.removeStorageSync('userInfo')
  },

  // 检查是否已登录
  checkLogin() {
    return this.globalData.isLoggedIn && this.globalData.token
  }
})
