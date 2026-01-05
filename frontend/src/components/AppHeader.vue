<template>
  <header class="app-header">
    <div class="header-content">
      <div class="logo" @click="$router.push('/')">
        <span class="logo-icon">🏮</span>
        <span class="logo-text">南锣鼓巷导览</span>
      </div>
      <nav class="nav-menu">
        <router-link to="/" class="nav-item">首页</router-link>
        <router-link to="/pois" class="nav-item">景点</router-link>
        <router-link to="/routes" class="nav-item">路线</router-link>
      </nav>
    </div>
  </header>
</template>

<script setup>
</script>

<style scoped>
.app-header {
  background: linear-gradient(135deg, #8B0000 0%, #CD5C5C 100%);
  color: white;
  padding: 15px 20px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  cursor: pointer;
  font-size: 1.5rem;
  font-weight: bold;
}

.logo-icon {
  font-size: 2rem;
  margin-right: 10px;
}

.nav-menu {
  display: flex;
  gap: 30px;
}

.nav-item {
  color: white;
  text-decoration: none;
  font-size: 1rem;
  padding: 8px 16px;
  border-radius: 20px;
  transition: background 0.3s;
}

.nav-item:hover,
.nav-item.router-link-active {
  background: rgba(255,255,255,0.2);
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 15px;
  }
  .nav-menu {
    gap: 15px;
  }
}
</style>
