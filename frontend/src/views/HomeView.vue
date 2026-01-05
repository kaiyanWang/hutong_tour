<template>
  <div class="home-view">
    <div v-if="loading" class="loading">
      <el-skeleton :rows="5" animated />
    </div>
    <div v-else-if="hutong" class="hutong-info">
      <div class="hero-section">
        <h1 class="hutong-name">{{ hutong.name }}</h1>
        <div class="hutong-tags">
          <el-tag v-for="tag in hutong.features" :key="tag" type="danger" effect="plain">
            {{ tag }}
          </el-tag>
        </div>
      </div>
      
      <div class="info-section">
        <div class="info-card">
          <h2>📍 地理位置</h2>
          <p>{{ hutong.location }}</p>
        </div>
        
        <div class="info-card">
          <h2>📖 简介</h2>
          <p>{{ hutong.description }}</p>
        </div>
        
        <div class="info-card">
          <h2>🏛️ 历史沿革</h2>
          <p>{{ hutong.history }}</p>
        </div>
      </div>
      
      <div class="action-buttons">
        <el-button type="primary" size="large" @click="$router.push('/pois')">
          🏠 浏览景点
        </el-button>
        <el-button type="success" size="large" @click="$router.push('/routes')">
          🗺️ 推荐路线
        </el-button>
      </div>
    </div>
    <div v-else class="error">
      <el-empty description="暂无胡同信息" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getHutongInfo } from '../api'

const hutong = ref(null)
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await getHutongInfo()
    hutong.value = data
  } catch (error) {
    console.error('获取胡同信息失败:', error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.home-view {
  padding: 20px 0;
}

.hero-section {
  text-align: center;
  padding: 40px 20px;
  background: linear-gradient(135deg, #8B0000 0%, #CD5C5C 100%);
  border-radius: 16px;
  color: white;
  margin-bottom: 30px;
}

.hutong-name {
  font-size: 2.5rem;
  margin-bottom: 20px;
}

.hutong-tags {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 10px;
}

.info-section {
  display: grid;
  gap: 20px;
}

.info-card {
  background: white;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}

.info-card h2 {
  color: #8B0000;
  margin-bottom: 15px;
  font-size: 1.3rem;
}

.info-card p {
  color: #666;
  line-height: 1.8;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 30px;
}

.loading, .error {
  padding: 50px;
}

@media (max-width: 768px) {
  .hutong-name {
    font-size: 1.8rem;
  }
  .action-buttons {
    flex-direction: column;
  }
}
</style>
