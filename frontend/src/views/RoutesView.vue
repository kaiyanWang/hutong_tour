<template>
  <div class="routes-view">
    <h1 class="page-title">🗺️ 推荐路线</h1>
    
    <div v-if="loading" class="loading">
      <el-skeleton :rows="5" animated />
    </div>
    
    <div v-else-if="routes.length > 0">
      <div v-for="route in routes" :key="route.id" class="route-section">
        <RouteCard :route="route" @view="viewRouteDetail" />
        
        <div v-if="selectedRoute === route.id && routeDetail" class="route-detail">
          <h3>路线景点</h3>
          <el-timeline>
            <el-timeline-item
              v-for="item in routeDetail.pois"
              :key="item.order"
              :timestamp="`第${item.order}站`"
              placement="top"
            >
              <div class="timeline-poi" @click="$router.push(`/poi/${item.poi.id}`)">
                <strong>{{ item.poi.name }}</strong>
                <el-tag size="small" :type="getTagType(item.poi.type)">
                  {{ item.poi.type_display }}
                </el-tag>
                <p>{{ item.poi.brief }}</p>
              </div>
            </el-timeline-item>
          </el-timeline>
        </div>
      </div>
    </div>
    
    <div v-else class="empty">
      <el-empty description="暂无推荐路线" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getRouteList, getRouteDetail } from '../api'
import RouteCard from '../components/RouteCard.vue'

const routes = ref([])
const loading = ref(true)
const selectedRoute = ref(null)
const routeDetail = ref(null)

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

const viewRouteDetail = async (id) => {
  if (selectedRoute.value === id) {
    selectedRoute.value = null
    routeDetail.value = null
    return
  }
  try {
    const { data } = await getRouteDetail(id)
    routeDetail.value = data
    selectedRoute.value = id
  } catch (error) {
    console.error('获取路线详情失败:', error)
  }
}

onMounted(async () => {
  try {
    const { data } = await getRouteList()
    routes.value = data.results
  } catch (error) {
    console.error('获取路线列表失败:', error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.routes-view {
  padding: 20px 0;
}

.page-title {
  text-align: center;
  color: #8B0000;
  margin-bottom: 30px;
}

.route-section {
  margin-bottom: 30px;
}

.route-detail {
  background: #fafafa;
  padding: 20px;
  border-radius: 12px;
  margin-top: 15px;
}

.route-detail h3 {
  color: #8B0000;
  margin-bottom: 20px;
}

.timeline-poi {
  cursor: pointer;
  padding: 10px;
  border-radius: 8px;
  transition: background 0.3s;
}

.timeline-poi:hover {
  background: #fff;
}

.timeline-poi strong {
  display: block;
  margin-bottom: 5px;
  color: #333;
}

.timeline-poi p {
  color: #666;
  font-size: 0.9rem;
  margin-top: 8px;
}

.loading, .empty {
  padding: 50px;
}
</style>
