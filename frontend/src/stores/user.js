import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authAPI } from '@/api'
import { ElMessage } from 'element-plus'
import router from '@/router'

export const useUserStore = defineStore('user', () => {
  // State
  const token = ref(localStorage.getItem('token') || '')
  const username = ref(localStorage.getItem('username') || '')

  // Getters
  const isLoggedIn = computed(() => !!token.value)

  // Actions
  async function register(userData) {
    try {
      const response = await authAPI.register(userData)
      ElMessage.success('注册成功，请登录')
      router.push({ name: 'Login' })
      return response.data
    } catch (error) {
      throw error
    }
  }

  async function login(credentials) {
    try {
      const response = await authAPI.login(credentials)
      const { token: newToken, username: newUsername } = response.data
      
      // Save to state
      token.value = newToken
      username.value = newUsername
      
      // Save to localStorage
      localStorage.setItem('token', newToken)
      localStorage.setItem('username', newUsername)
      
      ElMessage.success('登录成功')
      
      // Redirect to previous page or home
      const redirect = router.currentRoute.value.query.redirect
      router.push(redirect || { name: 'Home' })
      
      return response.data
    } catch (error) {
      throw error
    }
  }

  async function logout() {
    try {
      await authAPI.logout()
    } catch (error) {
      // Ignore logout errors
    } finally {
      // Clear state
      token.value = ''
      username.value = ''
      
      // Clear localStorage
      localStorage.removeItem('token')
      localStorage.removeItem('username')
      
      ElMessage.success('已退出登录')
      router.push({ name: 'Home' })
    }
  }

  return {
    token,
    username,
    isLoggedIn,
    register,
    login,
    logout
  }
})
