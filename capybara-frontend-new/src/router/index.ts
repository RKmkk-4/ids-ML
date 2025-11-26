import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../Views/Dashboard.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/alerts',
    name: 'Alerts',
    component: () => import('../Views/Alerts.vue')
  },
  {
    path: '/flows',
    name: 'Flows',
    component: () => import('../Views/Flows.vue')
  },
  {
    path: '/stats',
    name: 'Statistics',
    component: () => import('../Views/Statistics.vue')
  },
  {
    path: '/config',
    name: 'Configuration',
    component: () => import('../Views/Configuration.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router