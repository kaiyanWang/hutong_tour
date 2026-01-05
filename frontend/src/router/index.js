import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import POIListView from '../views/POIListView.vue'
import POIDetailView from '../views/POIDetailView.vue'
import RoutesView from '../views/RoutesView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/pois', name: 'pois', component: POIListView },
  { path: '/poi/:id', name: 'poi-detail', component: POIDetailView },
  { path: '/routes', name: 'routes', component: RoutesView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
