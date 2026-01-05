<template>
  <div class="poi-detail-view">
    <el-button @click="$router.back()" class="back-btn">
      ← 返回列表
    </el-button>
    
    <div v-if="loading" class="loading">
      <el-skeleton :rows="8" animated />
    </div>
    
    <div v-else-if="poi" class="poi-detail">
      <div class="poi-header">
        <h1 class="poi-name">{{ poi.name }}</h1>
        <el-tag size="large" :type="getTagType(poi.type)">{{ poi.type_display }}</el-tag>
      </div>
      
      <div class="poi-images" v-if="poi.images && poi.images.length">
        <el-carousel height="300px" indicator-position="outside">
          <el-carousel-item v-for="(img, index) in poi.images" :key="index">
            <img :src="img" :alt="poi.name" class="carousel-img" />
          </el-carousel-item>
        </el-carousel>
      </div>
      
      <div class="poi-content">
        <div class="info-item">
          <h3>📍 位置</h3>
          <p>{{ poi.location }}</p>
        </div>
        
        <div class="info-item" v-if="poi.opening_hours">
          <h3>⏰ 开放时间</h3>
          <p>{{ poi.opening_hours }}</p>
        </div>
        
        <div class="info-item" v-if="poi.tips">
          <h3>💡 游览提示</h3>
          <p>{{ poi.tips }}</p>
        </div>
        
        <div class="info-item description">
          <h3>📖 详细介绍</h3>
          <p>{{ poi.description }}</p>
        </div>
      </div>
    </div>
    
    <div v-else class="error">
      <el-empty description="景点不存在" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getPOIDetail } from '../api'

const route = useRoute()
const poi = ref(null)
const loading = ref(true)

const getTagType = (type) => {
  const types = {
    'celebrity': 'warning',
    'historic': 'danger',
    'food': 'success',
    'shop': 'info',
    'culture': 'primary'
  }
  return types[type] || ''
}

onMounted(async () => {
  try {
    const { data } = await getPOIDetail(route.params.id)
    poi.value = data
  } catch (error) {
    console.error('获取POI详情失败:', error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.poi-detail-view {
  padding: 20px 0;
}

.back-btn {
  margin-bottom: 20px;
}

.poi-detail {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}

.poi-header {
  padding: 25px;
  background: linear-gradient(135deg, #8B0000 0%, #CD5C5C 100%);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 15px;
}

.poi-name {
  font-size: 1.8rem;
}

.poi-images {
  background: #f0f0f0;
}

.carousel-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.poi-content {
  padding: 25px;
}

.info-item {
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.info-item:last-child {
  border-bottom: none;
}

.info-item h3 {
  color: #8B0000;
  margin-bottom: 10px;
  font-size: 1.1rem;
}

.info-item p {
  color: #666;
  line-height: 1.8;
}

.description p {
  text-indent: 2em;
}

.loading, .error {
  padding: 50px;
}
</style>
