<template>
  <div class="poi-detail-page">
    <div class="container">
      <!-- Back Button -->
      <div class="back-nav">
        <el-button text @click="goBack">
          <el-icon><ArrowLeft /></el-icon>
          返回列表
        </el-button>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="8" animated />
      </div>

      <!-- POI Content -->
      <div v-else-if="poi" class="poi-content">
        <!-- Header Section -->
        <div class="poi-header">
          <div class="header-info">
            <el-tag :type="getCategoryType(poi.category)" size="large">
              {{ getCategoryLabel(poi.category) }}
            </el-tag>
            <h1>{{ poi.name }}</h1>
            <div class="address-info">
              <el-icon><Location /></el-icon>
              <span>{{ poi.address }}</span>
            </div>
          </div>
          <div class="header-actions">
            <el-button 
              :type="isFavorite ? 'danger' : 'default'"
              :icon="isFavorite ? StarFilled : Star"
              size="large"
              @click="toggleFavorite"
              :loading="favoriteLoading"
            >
              {{ isFavorite ? '已收藏' : '收藏' }}
            </el-button>
          </div>
        </div>

        <!-- Image Gallery -->
        <div class="image-gallery" v-if="poi.images && poi.images.length > 0">
          <el-carousel 
            :interval="5000" 
            type="card" 
            height="300px"
            v-if="poi.images.length > 1"
          >
            <el-carousel-item v-for="(image, index) in poi.images" :key="index">
              <el-image :src="image" fit="cover" class="gallery-image">
                <template #error>
                  <div class="image-error">
                    <el-icon><Picture /></el-icon>
                  </div>
                </template>
              </el-image>
            </el-carousel-item>
          </el-carousel>
          <div v-else class="single-image">
            <el-image :src="poi.images[0]" fit="cover">
              <template #error>
                <div class="image-error">
                  <el-icon><Picture /></el-icon>
                </div>
              </template>
            </el-image>
          </div>
        </div>

        <!-- Description Section -->
        <div class="description-section">
          <h2>景点介绍</h2>
          <p>{{ poi.description }}</p>
        </div>

        <!-- Map Section -->
        <div class="map-section">
          <h2>地理位置</h2>
          <div id="poiMap" class="map-container"></div>
        </div>
      </div>

      <!-- Error State -->
      <div v-else class="error-state">
        <el-empty description="景点不存在或已被删除">
          <el-button type="primary" @click="goBack">返回列表</el-button>
        </el-empty>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, Location, Star, StarFilled, Picture } from '@element-plus/icons-vue'
import { poiAPI, favoriteAPI } from '@/api'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const loading = ref(true)
const poi = ref(null)
const isFavorite = ref(false)
const favoriteLoading = ref(false)

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
  router.push({ name: 'POIList' })
}

async function fetchPOIDetail() {
  try {
    loading.value = true
    const poiId = route.params.id
    const response = await poiAPI.getDetail(poiId)
    poi.value = response.data
    
    // Check favorite status if logged in
    if (userStore.isLoggedIn) {
      await checkFavoriteStatus()
    }
  } catch (error) {
    ElMessage.error('获取景点详情失败')
    poi.value = null
  } finally {
    loading.value = false
  }
}

async function checkFavoriteStatus() {
  try {
    const poiId = route.params.id
    const response = await poiAPI.checkFavorite(poiId)
    isFavorite.value = response.data.is_favorite
  } catch (error) {
    // Ignore errors for favorite check
    isFavorite.value = false
  }
}

async function toggleFavorite() {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录后再收藏')
    router.push({ name: 'Login', query: { redirect: route.fullPath } })
    return
  }

  try {
    favoriteLoading.value = true
    const poiId = route.params.id
    
    if (isFavorite.value) {
      await favoriteAPI.remove(poiId)
      isFavorite.value = false
      ElMessage.success('已取消收藏')
    } else {
      await favoriteAPI.add(poiId)
      isFavorite.value = true
      ElMessage.success('收藏成功')
    }
  } catch (error) {
    ElMessage.error(isFavorite.value ? '取消收藏失败' : '收藏失败')
  } finally {
    favoriteLoading.value = false
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
  if (!poi.value) return
  
  try {
    await loadBaiduMapScript()
    const BMapGL = window.BMapGL
    const map = new BMapGL.Map('poiMap')
    const point = new BMapGL.Point(poi.value.longitude, poi.value.latitude)
    map.centerAndZoom(point, 17)
    map.enableScrollWheelZoom(true)
    
    const marker = new BMapGL.Marker(point)
    map.addOverlay(marker)
    
    const label = new BMapGL.Label(poi.value.name, {
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

// Watch for POI data to initialize map
watch(() => poi.value, (newVal) => {
  if (newVal) {
    // Use nextTick to ensure DOM is ready
    setTimeout(() => {
      initMap()
    }, 100)
  }
})

onMounted(() => {
  fetchPOIDetail()
})
</script>


<style scoped>
.poi-detail-page {
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

.poi-content {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.poi-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 30px;
  border-bottom: 1px solid #ebeef5;
}

.header-info h1 {
  font-size: 28px;
  color: #303133;
  margin: 12px 0;
}

.address-info {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #909399;
  font-size: 14px;
}

.header-actions {
  flex-shrink: 0;
}

.image-gallery {
  padding: 30px;
  background: #fafafa;
}

.gallery-image {
  width: 100%;
  height: 100%;
  border-radius: 8px;
}

.single-image {
  max-width: 600px;
  margin: 0 auto;
}

.single-image .el-image {
  width: 100%;
  height: 350px;
  border-radius: 8px;
}

.image-error {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  background: #f5f7fa;
  color: #909399;
  font-size: 48px;
}

.description-section {
  padding: 30px;
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
  border-top: 1px solid #ebeef5;
}

.map-section h2 {
  font-size: 20px;
  color: #303133;
  margin: 0 0 20px 0;
}

.map-container {
  width: 100%;
  height: 350px;
  border-radius: 8px;
  overflow: hidden;
}

.error-state {
  background: #fff;
  padding: 60px 20px;
  border-radius: 12px;
  text-align: center;
}

@media (max-width: 768px) {
  .poi-detail-page {
    padding: 15px;
  }
  
  .poi-header {
    flex-direction: column;
    gap: 20px;
    padding: 20px;
  }
  
  .header-info h1 {
    font-size: 22px;
  }
  
  .header-actions {
    width: 100%;
  }
  
  .header-actions .el-button {
    width: 100%;
  }
  
  .image-gallery,
  .description-section,
  .map-section {
    padding: 20px;
  }
  
  .single-image .el-image {
    height: 250px;
  }
  
  .map-container {
    height: 280px;
  }
}
</style>
