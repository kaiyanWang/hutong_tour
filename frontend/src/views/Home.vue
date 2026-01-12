<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-content">
        <h1>南锣鼓巷</h1>
        <p class="hero-subtitle">探索北京最具特色的胡同文化</p>
        <div class="hero-actions">
          <el-button type="primary" size="large" @click="$router.push('/pois')">
            浏览景点
          </el-button>
          <el-button size="large" @click="$router.push('/routes')">
            查看路线
          </el-button>
        </div>
      </div>
    </section>

    <!-- Hutong Overview Section -->
    <section class="overview-section">
      <div class="container">
        <el-skeleton :loading="loading" animated :rows="6">
          <template #default>
            <div class="overview-content" v-if="hutong">
              <div class="overview-text">
                <h2>{{ hutong.name }}</h2>
                <p class="introduction">{{ hutong.introduction }}</p>
                <div class="history">
                  <h3>历史沿革</h3>
                  <p>{{ hutong.history }}</p>
                </div>
              </div>
              <div class="overview-image" v-if="hutong.image">
                <el-image :src="hutong.image" fit="cover" />
              </div>
            </div>
          </template>
        </el-skeleton>
      </div>
    </section>

    <!-- Map Section -->
    <section class="map-section">
      <div class="container">
        <h2>地理位置</h2>
        <div id="baiduMap" class="map-container"></div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { hutongAPI } from '@/api'
import { ElMessage } from 'element-plus'

const loading = ref(true)
const hutong = ref(null)
const BAIDU_MAP_AK = 'TfGPBvIrhd5l1qpC8wluqEB9ZZ2AOcCs'

async function fetchHutongData() {
  try {
    loading.value = true
    const response = await hutongAPI.getOverview()
    hutong.value = response.data
  } catch (error) {
    ElMessage.error('获取胡同信息失败')
  } finally {
    loading.value = false
  }
}

function loadBaiduMapScript() {
  return new Promise((resolve, reject) => {
    if (window.BMapGL) {
      resolve()
      return
    }
    window.initBaiduMap = () => {
      resolve()
    }
    const script = document.createElement('script')
    script.src = `https://api.map.baidu.com/api?v=1.0&type=webgl&ak=${BAIDU_MAP_AK}&callback=initBaiduMap`
    script.onerror = reject
    document.head.appendChild(script)
  })
}

async function initMap() {
  if (!hutong.value) return
  
  try {
    await loadBaiduMapScript()
    const BMapGL = window.BMapGL
    const map = new BMapGL.Map('baiduMap')
    const point = new BMapGL.Point(hutong.value.longitude, hutong.value.latitude)
    map.centerAndZoom(point, 16)
    map.enableScrollWheelZoom(true)
    
    const marker = new BMapGL.Marker(point)
    map.addOverlay(marker)
    
    const label = new BMapGL.Label(hutong.value.name, {
      position: point,
      offset: new BMapGL.Size(10, -20)
    })
    label.setStyle({
      color: '#fff',
      backgroundColor: '#409eff',
      borderRadius: '4px',
      padding: '4px 8px',
      fontSize: '12px',
      border: 'none'
    })
    map.addOverlay(label)
  } catch (error) {
    console.error('地图加载失败:', error)
  }
}

onMounted(async () => {
  await fetchHutongData()
  await initMap()
})
</script>


<style scoped>
.home-page {
  min-height: 100%;
}

.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  padding: 80px 20px;
  text-align: center;
}

.hero-content h1 {
  font-size: 48px;
  margin-bottom: 16px;
  font-weight: bold;
}

.hero-subtitle {
  font-size: 20px;
  opacity: 0.9;
  margin-bottom: 32px;
}

.hero-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.overview-section {
  padding: 60px 0;
  background: #fff;
}

.overview-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  align-items: start;
}

.overview-text h2 {
  font-size: 32px;
  color: #303133;
  margin-bottom: 20px;
}

.introduction {
  font-size: 16px;
  line-height: 1.8;
  color: #606266;
  margin-bottom: 24px;
}

.history h3 {
  font-size: 20px;
  color: #303133;
  margin-bottom: 12px;
}

.history p {
  font-size: 15px;
  line-height: 1.8;
  color: #606266;
}

.overview-image {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.overview-image .el-image {
  width: 100%;
  height: 400px;
}

.map-section {
  padding: 60px 0;
  background: #f5f7fa;
}

.map-section h2 {
  font-size: 28px;
  color: #303133;
  text-align: center;
  margin-bottom: 30px;
}

.map-container {
  width: 100%;
  height: 450px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
  .hero-content h1 {
    font-size: 32px;
  }
  
  .hero-subtitle {
    font-size: 16px;
  }
  
  .hero-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .overview-content {
    grid-template-columns: 1fr;
  }
  
  .overview-image .el-image {
    height: 250px;
  }
  
  .map-container {
    height: 300px;
  }
}
</style>
