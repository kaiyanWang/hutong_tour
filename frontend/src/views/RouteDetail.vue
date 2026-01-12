<template>
  <div class="route-detail-page">
    <div class="container">
      <!-- Back Button -->
      <div class="back-nav">
        <el-button text @click="goBack">
          <el-icon><ArrowLeft /></el-icon>
          返回路线列表
        </el-button>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="8" animated />
      </div>

      <!-- Route Content -->
      <div v-else-if="route" class="route-content">
        <!-- Header Section -->
        <div class="route-header">
          <div class="header-icon">
            <el-icon><Guide /></el-icon>
          </div>
          <div class="header-info">
            <h1>{{ route.name }}</h1>
            <div class="route-meta">
              <el-tag type="primary" size="large">
                <el-icon><Clock /></el-icon>
                约 {{ route.duration }} 分钟
              </el-tag>
              <el-tag type="success" size="large">
                <el-icon><Location /></el-icon>
                {{ route.poi_count }} 个景点
              </el-tag>
            </div>
          </div>
        </div>

        <!-- Description Section -->
        <div class="description-section">
          <h2>路线介绍</h2>
          <p>{{ route.description }}</p>
        </div>

        <!-- Map Section -->
        <div class="map-section">
          <h2>路线地图</h2>
          <div id="routeMap" class="map-container"></div>
        </div>

        <!-- POI List Section -->
        <div class="poi-list-section">
          <h2>途经景点</h2>
          <div class="poi-timeline">
            <div 
              v-for="(poi, index) in route.pois" 
              :key="poi.id" 
              class="poi-item"
              @click="goToPOI(poi.id)"
            >
              <div class="poi-order">
                <span>{{ index + 1 }}</span>
              </div>
              <div class="poi-connector" v-if="index < route.pois.length - 1"></div>
              <div class="poi-card">
                <div class="poi-info">
                  <h3>{{ poi.name }}</h3>
                  <el-tag :type="getCategoryType(poi.category)" size="small">
                    {{ getCategoryLabel(poi.category) }}
                  </el-tag>
                  <p class="poi-brief">{{ poi.brief }}</p>
                  <div class="poi-address">
                    <el-icon><Location /></el-icon>
                    <span>{{ poi.address }}</span>
                  </div>
                </div>
                <div class="poi-arrow">
                  <el-icon><ArrowRight /></el-icon>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Error State -->
      <div v-else class="error-state">
        <el-empty description="路线不存在或已被删除">
          <el-button type="primary" @click="goBack">返回列表</el-button>
        </el-empty>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, ArrowRight, Guide, Clock, Location } from '@element-plus/icons-vue'
import { routeAPI } from '@/api'
import { ElMessage } from 'element-plus'

const routeInstance = useRoute()
const router = useRouter()

const loading = ref(true)
const route = ref(null)

const BAIDU_MAP_AK = 'TfGPBvIrhd5l1qpC8wluqEB9ZZ2AOcCs'

const categoryMap = {
  historic: { label: '历史古迹', type: 'danger' },
  shop: { label: '特色店铺', type: 'warning' },
  food: { label: '美食餐饮', type: 'success' },
  culture: { label: '文化场所', type: 'primary' },
  scenic: { label: '景观', type: 'info' }
}

function getCategoryLabel(category) {
  return categoryMap[category]?.label || category
}

function getCategoryType(category) {
  return categoryMap[category]?.type || 'info'
}

function goBack() {
  router.push({ name: 'RouteList' })
}

function goToPOI(id) {
  router.push({ name: 'POIDetail', params: { id } })
}

async function fetchRouteDetail() {
  try {
    loading.value = true
    const routeId = routeInstance.params.id
    const response = await routeAPI.getDetail(routeId)
    route.value = response.data
  } catch (error) {
    ElMessage.error('获取路线详情失败')
    route.value = null
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
  if (!route.value || !route.value.pois || route.value.pois.length === 0) return
  
  try {
    await loadBaiduMapScript()
    const BMapGL = window.BMapGL
    const map = new BMapGL.Map('routeMap')
    
    const pois = route.value.pois
    
    // Calculate center point
    let totalLat = 0, totalLng = 0
    pois.forEach(poi => {
      totalLat += poi.latitude
      totalLng += poi.longitude
    })
    const centerLat = totalLat / pois.length
    const centerLng = totalLng / pois.length
    
    const centerPoint = new BMapGL.Point(centerLng, centerLat)
    map.centerAndZoom(centerPoint, 16)
    map.enableScrollWheelZoom(true)
    
    // Add markers and labels for each POI
    const points = []
    pois.forEach((poi, index) => {
      const point = new BMapGL.Point(poi.longitude, poi.latitude)
      points.push(point)
      
      // Create custom marker with number
      const marker = new BMapGL.Marker(point)
      map.addOverlay(marker)
      
      // Add label with POI name and order
      const label = new BMapGL.Label(`${index + 1}. ${poi.name}`, {
        position: point,
        offset: new BMapGL.Size(15, -15)
      })
      label.setStyle({
        color: '#fff',
        backgroundColor: '#409eff',
        borderRadius: '4px',
        padding: '4px 8px',
        fontSize: '12px',
        border: 'none',
        whiteSpace: 'nowrap'
      })
      map.addOverlay(label)
    })
    
    // Draw polyline connecting all POIs
    if (points.length > 1) {
      const polyline = new BMapGL.Polyline(points, {
        strokeColor: '#409eff',
        strokeWeight: 4,
        strokeOpacity: 0.8,
        strokeStyle: 'solid'
      })
      map.addOverlay(polyline)
    }
    
    // Adjust view to show all markers
    if (points.length > 1) {
      map.setViewport(points, { margins: [50, 50, 50, 50] })
    }
  } catch (error) {
    console.error('地图加载失败:', error)
  }
}

// Watch for route data to initialize map
watch(() => route.value, (newVal) => {
  if (newVal) {
    setTimeout(() => {
      initMap()
    }, 100)
  }
})

onMounted(() => {
  fetchRouteDetail()
})
</script>


<style scoped>
.route-detail-page {
  min-height: 100%;
  background: #f5f7fa;
  padding: 20px;
}

.container {
  max-width: 900px;
  margin: 0 auto;
}

.back-nav {
  margin-bottom: 20px;
}

.back-nav .el-button {
  font-size: 16px;
  color: #606266;
}

.back-nav .el-button:hover {
  color: #409eff;
}

.loading-container {
  background: #fff;
  padding: 40px;
  border-radius: 12px;
}

.route-content {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.route-header {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 30px;
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
  color: #fff;
}

.header-icon {
  width: 80px;
  height: 80px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.header-icon .el-icon {
  font-size: 40px;
}

.header-info h1 {
  font-size: 28px;
  margin: 0 0 16px 0;
}

.route-meta {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.route-meta .el-tag {
  display: flex;
  align-items: center;
  gap: 4px;
  background: rgba(255, 255, 255, 0.9);
}

.description-section {
  padding: 30px;
  border-bottom: 1px solid #ebeef5;
}

.description-section h2 {
  font-size: 20px;
  color: #303133;
  margin: 0 0 16px 0;
}

.description-section p {
  font-size: 15px;
  line-height: 1.8;
  color: #606266;
  margin: 0;
  white-space: pre-wrap;
}

.map-section {
  padding: 30px;
  border-bottom: 1px solid #ebeef5;
}

.map-section h2 {
  font-size: 20px;
  color: #303133;
  margin: 0 0 20px 0;
}

.map-container {
  width: 100%;
  height: 400px;
  border-radius: 8px;
  overflow: hidden;
}

.poi-list-section {
  padding: 30px;
}

.poi-list-section h2 {
  font-size: 20px;
  color: #303133;
  margin: 0 0 24px 0;
}

.poi-timeline {
  display: flex;
  flex-direction: column;
}

.poi-item {
  display: flex;
  position: relative;
  cursor: pointer;
}

.poi-order {
  width: 36px;
  height: 36px;
  background: #409eff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  z-index: 1;
}

.poi-order span {
  color: #fff;
  font-weight: 600;
  font-size: 14px;
}

.poi-connector {
  position: absolute;
  left: 17px;
  top: 36px;
  width: 2px;
  height: calc(100% - 36px);
  background: #dcdfe6;
}

.poi-card {
  flex: 1;
  margin-left: 16px;
  margin-bottom: 20px;
  padding: 16px;
  background: #fafafa;
  border-radius: 8px;
  display: flex;
  align-items: center;
  transition: background 0.3s ease, transform 0.3s ease;
}

.poi-card:hover {
  background: #f0f7ff;
  transform: translateX(4px);
}

.poi-info {
  flex: 1;
}

.poi-info h3 {
  font-size: 16px;
  color: #303133;
  margin: 0 0 8px 0;
}

.poi-info .el-tag {
  margin-bottom: 8px;
}

.poi-brief {
  font-size: 13px;
  color: #606266;
  margin: 0 0 8px 0;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.poi-address {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #909399;
}

.poi-arrow {
  flex-shrink: 0;
  color: #c0c4cc;
  font-size: 18px;
  margin-left: 12px;
  transition: color 0.3s ease;
}

.poi-card:hover .poi-arrow {
  color: #409eff;
}

.error-state {
  background: #fff;
  padding: 60px 20px;
  border-radius: 12px;
  text-align: center;
}

@media (max-width: 768px) {
  .route-detail-page {
    padding: 15px;
  }
  
  .route-header {
    flex-direction: column;
    text-align: center;
    padding: 24px;
  }
  
  .header-icon {
    width: 64px;
    height: 64px;
  }
  
  .header-icon .el-icon {
    font-size: 32px;
  }
  
  .header-info h1 {
    font-size: 22px;
  }
  
  .route-meta {
    justify-content: center;
  }
  
  .description-section,
  .map-section,
  .poi-list-section {
    padding: 20px;
  }
  
  .map-container {
    height: 300px;
  }
  
  .poi-order {
    width: 30px;
    height: 30px;
  }
  
  .poi-connector {
    left: 14px;
    top: 30px;
    height: calc(100% - 30px);
  }
  
  .poi-card {
    margin-left: 12px;
    padding: 12px;
  }
}
</style>
