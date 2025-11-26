<script setup lang="ts">
defineProps<{
  title: string
  value: string | number
  icon?: string
  color?: string
  trend?: 'up' | 'down' | 'stable'
  trendValue?: string
}>()
</script>

<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 transition-all hover:shadow-xl hover:-translate-y-1">
    <div :class="`border-l-4 border-${color}-500 pl-4`">
      <div class="flex justify-between items-start">
        <div>
          <p class="text-gray-500 dark:text-gray-400 text-sm">{{ title }}</p>
          <p class="text-3xl font-bold mt-2 text-gray-800 dark:text-white">{{ value }}</p>
          
          <div v-if="trend" class="mt-2 flex items-center gap-1">
            <span v-if="trend === 'up'" class="text-green-500">↗️</span>
            <span v-if="trend === 'down'" class="text-red-500">↘️</span>
            <span v-if="trend === 'stable'" class="text-gray-500">→</span>
            <span class="text-xs text-gray-500">{{ trendValue }}</span>
          </div>
        </div>
        
        <div v-if="icon" class="text-4xl">{{ icon }}</div>
      </div>
    </div>
  </div>
</template>
