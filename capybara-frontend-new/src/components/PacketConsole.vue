<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

interface PacketLog {
  id: string
  timestamp: string
  type: 'packet' | 'alert' | 'info'
  message: string
  details?: any
}

const logs = ref<PacketLog[]>([])
const maxLogs = 100
const isPaused = ref(false)

let ws: WebSocket | null = null

onMounted(() => {
  connectWebSocket()
})

onUnmounted(() => {
  if (ws) {
    ws.close()
  }
})

function connectWebSocket() {
  ws = new WebSocket('ws://localhost:8000/ws')
  
  ws.onopen = () => {
    addLog('info', 'WebSocket connecté - En écoute du trafic réseau...')
  }
  
  ws.onmessage = (event) => {
    if (isPaused.value) return
    
    try {
      const data = JSON.parse(event.data)
      
      if (data.type === 'new_alert') {
        addLog('alert', `🚨 ALERTE: ${data.data.type} depuis ${data.data.src_ip}`, data.data)
      } else if (data.type === 'packet') {
        addLog('packet', `📦 Paquet: ${data.data.src_ip} → ${data.data.dst_ip} [${data.data.protocol}]`, data.data)
      }
    } catch (e) {
      console.error('Erreur parsing WebSocket:', e)
    }
  }
  
  ws.onerror = () => {
    addLog('alert', '❌ Erreur WebSocket - Reconnexion...')
  }
  
  ws.onclose = () => {
    addLog('info', '🔌 WebSocket déconnecté')
    setTimeout(() => {
      if (!ws || ws.readyState === WebSocket.CLOSED) {
        connectWebSocket()
      }
    }, 5000)
  }
}

function addLog(type: PacketLog['type'], message: string, details?: any) {
  const log: PacketLog = {
    id: `${Date.now()}-${Math.random()}`,
    timestamp: new Date().toLocaleTimeString(),
    type,
    message,
    details
  }
  
  logs.value.unshift(log)
  
  if (logs.value.length > maxLogs) {
    logs.value = logs.value.slice(0, maxLogs)
  }
}

function clearLogs() {
  logs.value = []
}

function togglePause() {
  isPaused.value = !isPaused.value
}

function getLogClass(type: string) {
  switch (type) {
    case 'alert': return 'text-red-400 bg-red-950'
    case 'packet': return 'text-green-400 bg-gray-900'
    case 'info': return 'text-blue-400 bg-blue-950'
    default: return 'text-gray-400'
  }
}
</script>

<template>
  <div class="bg-black rounded-lg border border-gray-700 overflow-hidden font-mono text-sm">
    <div class="bg-gray-800 px-4 py-2 flex justify-between items-center border-b border-gray-700">
      <div class="flex items-center gap-2">
        <span class="text-green-400">●</span>
        <span class="text-gray-300 font-semibold">Console de Capture Réseau</span>
      </div>
      <div class="flex gap-2">
        <button 
          @click="togglePause" 
          class="px-3 py-1 bg-gray-700 hover:bg-gray-600 text-white rounded"
        >
          {{ isPaused ? '▶️ Reprendre' : '⏸️ Pause' }}
        </button>
        <button 
          @click="clearLogs" 
          class="px-3 py-1 bg-gray-700 hover:bg-gray-600 text-white rounded"
        >
          🗑️ Effacer
        </button>
      </div>
    </div>
    
    <div class="h-96 overflow-y-auto p-4 space-y-1">
      <div 
        v-for="log in logs" 
        :key="log.id" 
        :class="getLogClass(log.type)"
        class="px-2 py-1 rounded text-xs"
      >
        <span class="text-gray-500">[{{ log.timestamp }}]</span>
        {{ log.message }}
      </div>
      
      <div v-if="logs.length === 0" class="text-gray-600 text-center py-8">
        Aucun événement capturé pour le moment...
      </div>
    </div>
  </div>
</template>
