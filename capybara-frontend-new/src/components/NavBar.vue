<template>
  <nav class="bg-white dark:bg-gray-800 shadow-lg border-b border-gray-200 dark:border-gray-700">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex items-center">
          <div class="flex-shrink-0 flex items-center">
            <span class="text-2xl font-bold text-primary-600 dark:text-primary-400">🦫 Capybara IDS</span>
          </div>
          <div class="hidden md:ml-6 md:flex md:space-x-8">
            <router-link 
              v-for="item in navigation"
              :key="item.name"
              :to="item.to"
              class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
              :class="[
                $route.path === item.to 
                  ? 'border-primary-500 text-gray-900 dark:text-white' 
                  : 'border-transparent text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'
              ]"
            >
              {{ item.name }}
            </router-link>
          </div>
        </div>
        
        <div class="flex items-center space-x-4">
          <button 
            @click="toggleDarkMode"
            class="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
          >
            {{ darkMode ? '☀️' : '🌙' }}
          </button>
          <div class="text-sm text-gray-500 dark:text-gray-400">
            Status: <span class="font-medium text-green-600">En ligne</span>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const darkMode = ref(false)

const navigation = [
  { name: 'Dashboard', to: '/' },
  { name: 'Alertes', to: '/alerts' },
  { name: 'Flux Réseau', to: '/flows' },
  { name: 'Statistiques', to: '/stats' },
  { name: 'Configuration', to: '/config' },
]

const toggleDarkMode = () => {
  darkMode.value = !darkMode.value
  if (darkMode.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
  localStorage.setItem('darkMode', darkMode.value.toString())
}

onMounted(() => {
  const saved = localStorage.getItem('darkMode')
  darkMode.value = saved === 'true'
  if (darkMode.value) {
    document.documentElement.classList.add('dark')
  }
})
</script>