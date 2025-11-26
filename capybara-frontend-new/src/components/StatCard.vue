<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border-l-4" :class="borderColorClass">
    <div class="flex items-center">
      <div class="flex-shrink-0 text-2xl">
        {{ icon }}
      </div>
      <div class="ml-4">
        <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400">{{ title }}</h3>
        <p class="text-2xl font-semibold text-gray-900 dark:text-white">{{ value }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  title: string
  value: string | number
  icon: string
  color: 'blue' | 'red' | 'green' | 'yellow' | 'gray'
}

defineProps<Props>()

const borderColorClass = {
  blue: 'border-blue-500',
  red: 'border-red-500',
  green: 'border-green-500',
  yellow: 'border-yellow-500',
  gray: 'border-gray-500'
}
</script>