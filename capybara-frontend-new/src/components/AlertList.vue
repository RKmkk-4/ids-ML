<template>
  <div class="space-y-3">
    <div 
      v-for="alert in alerts" 
      :key="alert.id"
      class="p-4 rounded-lg border transition-all duration-200 hover:shadow-md"
      :class="getAlertClasses(alert.severity)"
    >
      <div class="flex justify-between items-start">
        <div class="flex-1">
          <div class="flex items-center space-x-2 mb-1">
            <span class="font-semibold text-gray-900 dark:text-white">{{ alert.type }}</span>
            <span 
              class="px-2 py-1 text-xs font-medium rounded-full"
              :class="getSeverityBadgeClasses(alert.severity)"
            >
              {{ alert.severity }}
            </span>
          </div>
          <p class="text-sm text-gray-600 dark:text-gray-300 mb-1">{{ alert.description }}</p>
          <div class="flex items-center space-x-4 text-xs text-gray-500 dark:text-gray-400">
            <span>IP: {{ alert.src_ip }}</span>
            <span>{{ formatTimestamp(alert.timestamp) }}</span>
          </div>
        </div>
        <button 
          @click="deleteAlert(alert.id)"
          class="text-gray-400 hover:text-red-600 dark:hover:text-red-400 transition-colors ml-4"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>
    
    <!-- Message si aucune alerte -->
    <div 
      v-if="alerts.length === 0"
      class="text-center py-8 text-gray-500 dark:text-gray-400"
    >
      <div class="text-4xl mb-2">🎉</div>
      <p>Aucune alerte pour le moment</p>
      <p class="text-sm">Tout semble normal</p>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Alert {
  id: string
  type: string
  severity: string
  src_ip: string
  description: string
  timestamp: string
}

interface Props {
  alerts: Alert[]
}

defineProps<Props>()

const emit = defineEmits<{
  delete: [id: string]
}>()

function getAlertClasses(severity: string) {
  const classes = {
    'CRITICAL': 'alert-critical border-red-200',
    'HIGH': 'alert-high border-orange-200', 
    'MEDIUM': 'alert-medium border-yellow-200',
    'LOW': 'alert-low border-green-200'
  }
  return classes[severity as keyof typeof classes] || 'alert-low border-gray-200'
}

function getSeverityBadgeClasses(severity: string) {
  const classes = {
    'CRITICAL': 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
    'HIGH': 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200',
    'MEDIUM': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
    'LOW': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
  }
  return classes[severity as keyof typeof classes] || 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
}

function formatTimestamp(timestamp: string) {
  return new Date(timestamp).toLocaleTimeString('fr-FR', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

function deleteAlert(id: string) {
  emit('delete', id)
}
</script>