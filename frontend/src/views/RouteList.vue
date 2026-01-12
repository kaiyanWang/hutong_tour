<template>
  <div class="route-list-page">
    <div class="container">
      <!-- Page Header -->
      <div class="page-header">
        <h1>推荐路线</h1>
        <p class="page-subtitle">精选游览路线，带您深度体验南锣鼓巷</p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="4" animated />
        <el-skeleton :rows="4" animated style="margin-top: 20px" />
      </div>

      <!-- Route List -->
      <div v-else-if="routes.length > 0" class="route-grid">
        <el-card 
          v-for="route in routes" 
          :key="route.id" 
          class="route-card"
          shadow="hover"
          @click="goToDetail(route.id)"
        >
          <div class="route-icon">
            <el-icon><Guide /></el-icon>
          </div>
          <div class="route-info">
            <h3 class="route-name">{{ route.name }}</h3>
            <div class="route-meta">
              <div class="meta-item">
                <el-icon><Clock /></el-icon>
                <span>约 {{ route.duration }} 分钟</span>
              </div>
              <div class="meta-item">
                <el-icon><Location /></el-icon>
                <span>{{ route.poi_count }} 个景点</span>
              </div>
            </div>
          </div>
          <div class="route-arrow">
            <el-icon><ArrowRight /></el-icon>
          </div>
        </el-card>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <el-empty description="暂无推荐路线" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Guide, Clock, Location, ArrowRight } from '@element-plus/icons-vue'
import { routeAPI } from '@/api'
import { ElMessage } from 'element-plus'

const router = useRouter()
const loading = ref(true)
const routes = ref([])

async function fetchRoutes() {
  try {
    loading.value = true
    const response = await routeAPI.getList()
    routes.value = response.data
  } catch (error) {
    ElMessage.error('获取路线列表失败')
    routes.value = []
  } finally {
    loading.value = false
  }
}

function goToDetail(id) {
  router.push({ name: 'RouteDetail', params: { id } })
}

onMounted(() => {
  fetchRoutes()
})
</script>

<style scoped>
.route-list-page {
  min-height: 100%;
  background: #f5f7fa;
  padding: 40px 20px;
}

.container {
  max-width: 900px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-header h1 {
  font-size: 36px;
  color: #303133;
  margin: 0 0 10px 0;
}

.page-subtitle {
  font-size: 16px;
  color: #909399;
  margin: 0;
}

.loading-container {
  background: #fff;
  padding: 30px;
  border-radius: 12px;
}

.route-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.route-card {
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-radius: 12px;
}

.route-card:hover {
  transform: translateX(8px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
}

.route-card :deep(.el-card__body) {
  display: flex;
  align-items: center;
  padding: 24px;
  gap: 20px;
}

.route-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.route-icon .el-icon {
  font-size: 28px;
  color: #fff;
}

.route-info {
  flex: 1;
}

.route-name {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 10px 0;
}

.route-meta {
  display: flex;
  gap: 24px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #909399;
  font-size: 14px;
}

.meta-item .el-icon {
  font-size: 16px;
  color: #409eff;
}

.route-arrow {
  flex-shrink: 0;
  color: #c0c4cc;
  font-size: 20px;
  transition: color 0.3s ease, transform 0.3s ease;
}

.route-card:hover .route-arrow {
  color: #409eff;
  transform: translateX(4px);
}

.empty-state {
  background: #fff;
  padding: 60px 20px;
  border-radius: 12px;
  text-align: center;
}

@media (max-width: 768px) {
  .route-list-page {
    padding: 20px 15px;
  }
  
  .page-header h1 {
    font-size: 28px;
  }
  
  .route-card :deep(.el-card__body) {
    padding: 16px;
    gap: 12px;
  }
  
  .route-icon {
    width: 48px;
    height: 48px;
  }
  
  .route-icon .el-icon {
    font-size: 22px;
  }
  
  .route-name {
    font-size: 17px;
  }
  
  .route-meta {
    flex-direction: column;
    gap: 8px;
  }
}
</style>
