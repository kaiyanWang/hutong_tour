<template>
  <div class="poi-card" @click="$router.push(`/poi/${poi.id}`)">
    <div class="poi-image">
      <img :src="poi.thumbnail || '/placeholder.jpg'" :alt="poi.name" />
    </div>
    <div class="poi-info">
      <h3 class="poi-name">{{ poi.name }}</h3>
      <el-tag size="small" :type="getTagType(poi.type)">{{ poi.type_display }}</el-tag>
      <p class="poi-brief">{{ poi.brief }}</p>
      <p class="poi-location">📍 {{ poi.location }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  poi: { type: Object, required: true }
})

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
</script>

<style scoped>
.poi-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.poi-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.poi-image {
  height: 160px;
  overflow: hidden;
  background: #f0f0f0;
}

.poi-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.poi-info {
  padding: 15px;
}

.poi-name {
  font-size: 1.1rem;
  margin-bottom: 8px;
  color: #333;
}

.poi-brief {
  color: #666;
  font-size: 0.9rem;
  margin: 10px 0;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.poi-location {
  color: #999;
  font-size: 0.85rem;
}
</style>
