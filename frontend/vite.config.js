import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')
    }
  },
  server: {
    port: 9002,
    proxy: {
      '/api': {
        target: 'http://39.99.43.230:8002',
        changeOrigin: true
      }
    }
  }
})
