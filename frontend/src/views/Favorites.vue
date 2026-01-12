<template>
  <div class="favorites">
    <div class="container">
      <div class="page-header">
        <h2>我的收藏</h2>
        <p class="subtitle">您收藏的景点都在这里</p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="3" animated />
        <el-skeleton :rows="3" animated style="margin-top: 20px" />
      </div>

      <!-- Empty State -->
      <el-empty 
        v-else-if="favorites.length === 0" 
        description="您还没有收藏任何景点"
      >
        <el-button type="primary" @click="goToPOIList">去逛逛</el-button>
      </el-empty>

      <!-- Favorites List -->
      <div v-else class="favorites-grid">
        <div v-for="favorite in favorites" :key="favorite.id" class="favorite-item">
          <POICard :poi="favorite.poi" />
          <el-button 
            class="remove-btn" 
            type="danger" 
            size="small" 
            :icon="Delete"
            circle
            @click.stop="removeFavorite(favorite.poi.id)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Delete } from '@element-plus/icons-vue'
import { favoriteAPI } from '@/api'
import POICard from '@/components/POICard.vue'

const router = useRouter()
const favorites = ref([])
const loading = ref(true)

async function fetchFavorites() {
  loading.value = true
  try {
    const response = await favoriteAPI.getList()
    favorites.value = response.data
  } catch (error) {
    console.error('Failed to fetch favorites:', error)
  } finally {
    loading.value = false
  }
}

async function removeFavorite(poiId) {
  try {
    await ElMessageBox.confirm(
      '确定要取消收藏该景点吗？',
      '取消收藏',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await favoriteAPI.remove(poiId)
    favorites.value = favorites.value.filter(f => f.poi.id !== poiId)
    ElMessage.success('已取消收藏')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Failed to remove favorite:', error)
    }
  }
}

function goToPOIList() {
  router.push({ name: 'POIList' })
}

onMounted(() => {
  fetchFavorites()
})
</script>

<style scoped>
.favorites {
  padding: 20px;
  min-height: calc(100vh - 60px);
  background: #f5f7fa;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 30px;
}

.page-header h2 {
  font-size: 28px;
  color: #303133;
  margin: 0 0 8px 0;
}

.subtitle {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.loading-container {
  max-width: 800px;
  margin: 0 auto;
}

.favorites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.favorite-item {
  position: relative;
}

.remove-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 10;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.favorite-item:hover .remove-btn {
  opacity: 1;
}

@media (max-width: 768px) {
  .favorites {
    padding: 15px;
  }

  .page-header h2 {
    font-size: 24px;
  }

  .favorites-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .remove-btn {
    opacity: 1;
  }
}
</style>
