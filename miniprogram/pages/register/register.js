// pages/register/register.js
const api = require('../../utils/api')
const app = getApp()

Page({
  data: {
    username: '',
    password: '',
    confirmPassword: '',
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

  // 输入确认密码
  onConfirmPasswordInput(e) {
    this.setData({
      confirmPassword: e.detail.value
    })
  },

  // 注册
  async onRegister() {
    const { username, password, confirmPassword } = this.data
    
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

    if (password.length < 6) {
      wx.showToast({
        title: '密码至少6位',
        icon: 'none'
      })
      return
    }
    
    if (password !== confirmPassword) {
      wx.showToast({
        title: '两次密码不一致',
        icon: 'none'
      })
      return
    }

    this.setData({ loading: true })

    try {
      await api.register(username, password, confirmPassword)
      
      wx.showToast({
        title: '注册成功',
        icon: 'success'
      })
      
      // 延迟跳转到登录页
      setTimeout(() => {
        wx.redirectTo({
          url: '/pages/login/login'
        })
      }, 1500)
    } catch (error) {
      console.error('注册失败:', error)
    } finally {
      this.setData({ loading: false })
    }
  },

  // 跳转到登录页
  navigateToLogin() {
    wx.navigateTo({
      url: '/pages/login/login'
    })
  }
})
