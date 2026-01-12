<template>
  <el-card class="poi-card" shadow="hover" @click="goToDetail">
    <div class="poi-image">
      <el-image 
        :src="poi.images && poi.images.length > 0 ? poi.images[0] : defaultImage" 
        fit="cover"
        :alt="poi.name"
      >
        <template #error>
          <div class="image-placeholder">
            <el-icon><Picture /></el-icon>
          </div>
        </template>
      </el-image>
      <el-tag class="category-tag" :type="getCategoryType(poi.category)" size="small">
        {{ getCategoryLabel(poi.category) }}
      </el-tag>
    </div>
    <div class="poi-info">
      <h3 class="poi-name">{{ poi.name }}</h3>
      <p class="poi-brief">{{ poi.brief }}</p>
      <div class="poi-address" v-if="poi.address">
        <el-icon><Location /></el-icon>
        <span>{{ poi.address }}</span>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { Picture, Location } from '@element-plus/icons-vue'

const props = defineProps({
  poi: {
    type: Object,
    required: true
  }
})

const router = useRouter()
const defaultImage = 'https://via.placeholder.com/300x200?text=No+Image'

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

function goToDetail() {
  router.push({ name: 'POIDetail', params: { id: props.poi.id } })
}
</script>

<style scoped>
.poi-card {
  cursor: pointer;
  transition: transform 0.3s ease;
  height: 100%;
}

.poi-card:hover {
  transform: translateY(-4px);
}

.poi-card :deep(.el-card__body) {
  padding: 0;
}

.poi-image {
  position: relative;
  height: 180px;
  overflow: hidden;
}

.poi-image .el-image {
  width: 100%;
  height: 100%;
}

.image-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  background: #f5f7fa;
  color: #909399;
  font-size: 40px;
}

.category-tag {
  position: absolute;
  top: 10px;
  left: 10px;
}

.poi-info {
  padding: 16px;
}

.poi-name {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 8px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.poi-brief {
  font-size: 14px;
  color: #606266;
  line-height: 1.6;
  margin: 0 0 12px 0;
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

.poi-address .el-icon {
  font-size: 14px;
}

.poi-address span {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
