<template>
  <div class="route-card">
    <div class="route-header">
      <h3 class="route-name">{{ route.name }}</h3>
      <div class="route-meta">
        <span>⏱️ {{ route.duration }}</span>
        <span>📏 {{ route.distance }}</span>
        <span>📍 {{ route.poi_count }}个景点</span>
      </div>
    </div>
    <p class="route-desc">{{ route.description }}</p>
    <el-button type="primary" size="small" @click="$emit('view', route.id)">
      查看详情
    </el-button>
  </div>
</template>

<script setup>
defineProps({
  route: { type: Object, required: true }
})
defineEmits(['view'])
</script>

<style scoped>
.route-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.route-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 15px;
}

.route-name {
  font-size: 1.3rem;
  color: #8B0000;
}

.route-meta {
  display: flex;
  gap: 15px;
  color: #666;
  font-size: 0.9rem;
}

.route-desc {
  color: #666;
  line-height: 1.6;
  margin-bottom: 15px;
}
</style>
