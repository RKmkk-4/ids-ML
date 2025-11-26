<template>
  <div class="h-64 flex items-center justify-center">
    <div class="text-center text-gray-500 dark:text-gray-400">
      <div class="text-4xl mb-2">📊</div>
      <p>Graphique des sévérités</p>
      <p class="text-sm mt-2">(Chart.js sera intégré ici)</p>
      
      <!-- Visualisation simple en attendant Chart.js -->
      <div class="mt-6 space-y-2 max-w-xs mx-auto">
        <div 
          v-for="item in data" 
          :key="item.severity"
          class="flex items-center justify-between p-2 rounded-lg text-white text-sm"
          :style="{ backgroundColor: item.color, width: (item.count * 10) + 'px' }"
        >
          <span>{{ item.severity }}</span>
          <span>{{ item.count }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface SeverityData {
  severity: string
  count: number
  color: string
}

defineProps<{
  data: SeverityData[]
}>()
</script>