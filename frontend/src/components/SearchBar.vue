<template>
  <div class="search-bar">
    <el-input
      v-model="keyword"
      placeholder="搜索景点..."
      clearable
      @keyup.enter="handleSearch"
      @clear="handleClear"
    >
      <template #append>
        <el-button @click="handleSearch">
          <span>🔍</span>
        </el-button>
      </template>
    </el-input>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['search', 'clear'])
const keyword = ref('')

const handleSearch = () => {
  emit('search', keyword.value.trim())
}

const handleClear = () => {
  keyword.value = ''
  emit('clear')
}
</script>

<style scoped>
.search-bar {
  max-width: 400px;
  margin: 20px auto;
}
</style>
