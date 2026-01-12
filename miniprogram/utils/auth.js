// 认证工具函数
const app = getApp()

/**
 * 检查用户是否已登录
 * @returns {boolean}
 */
const isLoggedIn = () => {
  return app.checkLogin()
}

/**
 * 获取当前用户Token
 * @returns {string|null}
 */
const getToken = () => {
  return app.globalData.token || wx.getStorageSync('token')
}

/**
 * 获取当前用户信息
 * @returns {object|null}
 */
const getUserInfo = () => {
  return app.globalData.userInfo || wx.getStorageSync('userInfo')
}

/**
 * 需要登录的页面守卫
 * 如果未登录，跳转到登录页
 * @param {string} redirectUrl - 登录后重定向的URL
 * @returns {boolean} - 是否已登录
 */
const requireLogin = (redirectUrl = '') => {
  if (!isLoggedIn()) {
    wx.showToast({
      title: '请先登录',
      icon: 'none'
    })
    
    // 保存重定向URL
    if (redirectUrl) {
      wx.setStorageSync('redirectUrl', redirectUrl)
    }
    
    wx.navigateTo({
      url: '/pages/login/login'
    })
    return false
  }
  return true
}

/**
 * 登录成功后的重定向
 */
const redirectAfterLogin = () => {
  const redirectUrl = wx.getStorageSync('redirectUrl')
  if (redirectUrl) {
    wx.removeStorageSync('redirectUrl')
    wx.redirectTo({
      url: redirectUrl
    })
  } else {
    wx.navigateBack()
  }
}

/**
 * 退出登录
 */
const logout = () => {
  app.clearLoginState()
  wx.showToast({
    title: '已退出登录',
    icon: 'success'
  })
}

module.exports = {
  isLoggedIn,
  getToken,
  getUserInfo,
  requireLogin,
  redirectAfterLogin,
  logout
}
