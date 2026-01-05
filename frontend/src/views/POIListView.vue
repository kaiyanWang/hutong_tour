<template>
  <div class="poi-list-view">
    <h1 class="page-title">🏠 景点列表</h1>
    
    <SearchBar @search="handleSearch" @clear="loadPOIs" />
    
    <div v-if="loading" class="loading">
      <el-skeleton :rows="3" animated />
    </div>
    
    <div v-else-if="pois.length > 0" class="poi-grid">
      <POICard v-for="poi in pois" :key="poi.id" :poi="poi" />
    </div>
    
    <div v-else class="empty">
      <el-empty :description="searchMode ? '未找到相关景点' : '暂无景点信息'" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getPOIList, searchPOIs } from '../api'
import POICard from '../components/POICard.vue'
import SearchBar from '../components/SearchBar.vue'

const pois = ref([])
const loading = ref(true)
const searchMode = ref(false)

const loadPOIs = async () => {
  loading.value = true
  searchMode.value = false
  try {
    const { data } = await getPOIList()
    pois.value = data.results
  } catch (error) {
    console.error('获取POI列表失败:', error)
  } finally {
    loading.value = false
  }
}

const handleSearch = async (keyword) => {
  if (!keyword) {
    loadPOIs()
    return
  }
  loading.value = true
  searchMode.value = true
  try {
    const { data } = await searchPOIs(keyword)
    pois.value = data.results
  } catch (error) {
    console.error('搜索失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(loadPOIs)
</script>

<style scoped>
.poi-list-view {
  padding: 20px 0;
}

.page-title {
  text-align: center;
  color: #8B0000;
  margin-bottom: 20px;
}

.poi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.loading, .empty {
  padding: 50px;
}
</style>
