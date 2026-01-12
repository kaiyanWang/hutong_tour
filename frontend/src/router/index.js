import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue')
  },
  {
    path: '/pois',
    name: 'POIList',
    component: () => import('@/views/POIList.vue')
  },
  {
    path: '/pois/:id',
    name: 'POIDetail',
    component: () => import('@/views/POIDetail.vue')
  },
  {
    path: '/routes',
    name: 'RouteList',
    component: () => import('@/views/RouteList.vue')
  },
  {
    path: '/routes/:id',
    name: 'RouteDetail',
    component: () => import('@/views/RouteDetail.vue')
  },
  {
    path: '/favorites',
    name: 'Favorites',
    component: () => import('@/views/Favorites.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard for protected routes
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router
