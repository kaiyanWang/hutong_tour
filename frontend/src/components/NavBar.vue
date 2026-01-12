<template>
  <el-header class="navbar">
    <div class="navbar-content">
      <div class="logo" @click="router.push({ name: 'Home' })">
        <el-icon class="logo-icon"><Location /></el-icon>
        <span class="logo-text">南锣鼓巷导览</span>
      </div>
      
      <el-menu
        mode="horizontal"
        :default-active="activeIndex"
        :ellipsis="false"
        class="nav-menu"
        @select="handleSelect"
      >
        <el-menu-item index="/">
          <el-icon><House /></el-icon>
          <span>首页</span>
        </el-menu-item>
        <el-menu-item index="/pois">
          <el-icon><Place /></el-icon>
          <span>景点</span>
        </el-menu-item>
        <el-menu-item index="/routes">
          <el-icon><Guide /></el-icon>
          <span>路线</span>
        </el-menu-item>
        <el-menu-item v-if="userStore.isLoggedIn" index="/favorites">
          <el-icon><Star /></el-icon>
          <span>收藏</span>
        </el-menu-item>
      </el-menu>
      
      <div class="user-area">
        <template v-if="userStore.isLoggedIn">
          <el-dropdown trigger="click">
            <span class="user-dropdown">
              <el-avatar :size="32" class="user-avatar">
                {{ userStore.username.charAt(0).toUpperCase() }}
              </el-avatar>
              <span class="username">{{ userStore.username }}</span>
              <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="router.push({ name: 'Favorites' })">
                  <el-icon><Star /></el-icon>我的收藏
                </el-dropdown-item>
                <el-dropdown-item divided @click="handleLogout">
                  <el-icon><SwitchButton /></el-icon>退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
        <template v-else>
          <el-button type="primary" size="small" @click="router.push({ name: 'Login' })">
            登录
          </el-button>
          <el-button size="small" @click="router.push({ name: 'Register' })">
            注册
          </el-button>
        </template>
      </div>
    </div>
  </el-header>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { Location, House, Place, Guide, Star, ArrowDown, SwitchButton } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const activeIndex = computed(() => route.path)

function handleSelect(index) {
  router.push(index)
}

function handleLogout() {
  userStore.logout()
}
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  padding: 0;
}

.navbar-content {
  max-width: 1200px;
  margin: 0 auto;
  height: 100%;
  display: flex;
  align-items: center;
  padding: 0 20px;
}

.logo {
  cursor: pointer;
  margin-right: 40px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo-icon {
  font-size: 24px;
  color: #409eff;
}

.logo-text {
  font-size: 20px;
  font-weight: bold;
  color: #409eff;
}

.nav-menu {
  flex: 1;
  border-bottom: none;
}

.nav-menu .el-menu-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.user-area {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-dropdown {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: #606266;
}

.user-dropdown:hover {
  color: #409eff;
}

.user-avatar {
  background-color: #409eff;
  color: #fff;
}

.username {
  max-width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Responsive styles */
@media (max-width: 768px) {
  .navbar-content {
    padding: 0 10px;
  }
  
  .logo {
    margin-right: 20px;
  }
  
  .logo-text {
    font-size: 16px;
  }
  
  .nav-menu .el-menu-item span {
    display: none;
  }
  
  .username {
    display: none;
  }
}
</style>
