import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/alerts',
    name: 'Alerts',
    component: () => import('../views/Alerts.vue')
  },
  {
    path: '/flows',
    name: 'Flows',
    component: () => import('../views/Flows.vue')
  },
  {
    path: '/stats',
    name: 'Statistics',
    component: () => import('../views/Statistics.vue')
  },
  {
    path: '/config',
    name: 'Configuration',
    component: () => import('../views/Configuration.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router