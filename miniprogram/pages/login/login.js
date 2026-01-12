// pages/login/login.js
const api = require('../../utils/api')
const app = getApp()

Page({
  data: {
    username: '',
    password: '',
    loading: false
  },

  onLoad() {
    // 如果已登录，返回上一页
    if (app.checkLogin()) {
      wx.navigateBack()
    }
  },

  // 输入用户名
  onUsernameInput(e) {
    this.setData({
      username: e.detail.value
    })
  },

  // 输入密码
  onPasswordInput(e) {
    this.setData({
      password: e.detail.value
    })
  },

  // 登录
  async onLogin() {
    const { username, password } = this.data
    
    // 验证输入
    if (!username.trim()) {
      wx.showToast({
        title: '请输入用户名',
        icon: 'none'
      })
      return
    }
    
    if (!password) {
      wx.showToast({
        title: '请输入密码',
        icon: 'none'
      })
      return
    }

    this.setData({ loading: true })

    try {
      const result = await api.login(username, password)
      
      // 保存登录状态
      app.setLoginState(result.token, { username })
      
      wx.showToast({
        title: '登录成功',
        icon: 'success'
      })
      
      // 延迟返回上一页
      setTimeout(() => {
        wx.navigateBack()
      }, 1500)
    } catch (error) {
      console.error('登录失败:', error)
    } finally {
      this.setData({ loading: false })
    }
  },

  // 跳转到注册页
  navigateToRegister() {
    wx.navigateTo({
      url: '/pages/register/register'
    })
  }
})
