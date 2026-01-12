<template>
  <div class="poi-list-page">
    <div class="container">
      <!-- Page Header -->
      <div class="page-header">
        <h1>景点列表</h1>
        <p class="page-subtitle">探索南锣鼓巷的精彩景点</p>
      </div>

      <!-- Search Bar -->
      <div class="search-section">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索景点名称..."
          size="large"
          clearable
          @keyup.enter="handleSearch"
          @clear="handleClear"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
          <template #append>
            <el-button @click="handleSearch" :loading="searching">
              搜索
            </el-button>
          </template>
        </el-input>
      </div>

      <!-- Category Filter -->
      <div class="filter-section">
        <el-radio-group v-model="selectedCategory" @change="handleCategoryChange">
          <el-radio-button value="">全部</el-radio-button>
          <el-radio-button value="historic">历史古迹</el-radio-button>
          <el-radio-button value="shop">特色店铺</el-radio-button>
          <el-radio-button value="food">美食餐饮</el-radio-button>
          <el-radio-button value="culture">文化场所</el-radio-button>
          <el-radio-button value="scenic">景观</el-radio-button>
        </el-radio-group>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="3" animated />
        <el-skeleton :rows="3" animated style="margin-top: 20px" />
      </div>

      <!-- POI Grid -->
      <div v-else-if="filteredPOIs.length > 0" class="poi-grid">
        <POICard 
          v-for="poi in filteredPOIs" 
          :key="poi.id" 
          :poi="poi" 
        />
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <el-empty :description="emptyDescription">
          <el-button v-if="searchKeyword || selectedCategory" @click="resetFilters">
            清除筛选条件
          </el-button>
        </el-empty>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Search } from '@element-plus/icons-vue'
import { poiAPI } from '@/api'
import { ElMessage } from 'element-plus'
import POICard from '@/components/POICard.vue'

const loading = ref(true)
const searching = ref(false)
const pois = ref([])
const searchKeyword = ref('')
const selectedCategory = ref('')
const isSearchResult = ref(false)

// Computed property for filtered POIs
const filteredPOIs = computed(() => {
  let result = pois.value
  
  // Filter by category if selected
  if (selectedCategory.value) {
    result = result.filter(poi => poi.category === selectedCategory.value)
  }
  
  return result
})

// Empty state description
const emptyDescription = computed(() => {
  if (searchKeyword.value) {
    return `未找到与"${searchKeyword.value}"相关的景点`
  }
  if (selectedCategory.value) {
    return '该分类下暂无景点'
  }
  return '暂无景点数据'
})

// Fetch all POIs
async function fetchPOIs() {
  try {
    loading.value = true
    isSearchResult.value = false
    const response = await poiAPI.getList()
    pois.value = response.data
  } catch (error) {
    ElMessage.error('获取景点列表失败')
    pois.value = []
  } finally {
    loading.value = false
  }
}

// Search POIs
async function handleSearch() {
  if (!searchKeyword.value.trim()) {
    await fetchPOIs()
    return
  }
  
  try {
    searching.value = true
    isSearchResult.value = true
    const response = await poiAPI.search(searchKeyword.value.trim())
    pois.value = response.data
  } catch (error) {
    ElMessage.error('搜索失败')
    pois.value = []
  } finally {
    searching.value = false
  }
}

// Handle clear search
async function handleClear() {
  searchKeyword.value = ''
  await fetchPOIs()
}

// Handle category change
function handleCategoryChange() {
  // Category filtering is done via computed property
  // No need to refetch data
}

// Reset all filters
async function resetFilters() {
  searchKeyword.value = ''
  selectedCategory.value = ''
  await fetchPOIs()
}

onMounted(() => {
  fetchPOIs()
})
</script>


<style scoped>
.poi-list-page {
  min-height: 100%;
  background: #f5f7fa;
  padding: 40px 20px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 30px;
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

.search-section {
  max-width: 600px;
  margin: 0 auto 24px;
}

.search-section :deep(.el-input-group__append) {
  background-color: #409eff;
  color: #fff;
}

.search-section :deep(.el-input-group__append .el-button) {
  color: #fff;
}

.filter-section {
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
  flex-wrap: wrap;
  gap: 10px;
}

.loading-container {
  background: #fff;
  padding: 30px;
  border-radius: 8px;
}

.poi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.empty-state {
  background: #fff;
  padding: 60px 20px;
  border-radius: 8px;
  text-align: center;
}

@media (max-width: 768px) {
  .poi-list-page {
    padding: 20px 15px;
  }
  
  .page-header h1 {
    font-size: 28px;
  }
  
  .filter-section :deep(.el-radio-group) {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .poi-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
}
</style>
