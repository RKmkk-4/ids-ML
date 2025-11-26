<template>
  <div class="container mx-auto px-4 py-8">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">Statistiques</h1>
      <p class="text-gray-600 dark:text-gray-400">Analyse et métriques du trafic réseau</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Graphique temporel -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
        <h2 class="text-xl font-semibold mb-4 text-gray-900 dark:text-white">Trafic par Heure</h2>
        <div class="h-64 flex items-center justify-center text-gray-500 dark:text-gray-400">
          <div class="text-center">
            <div class="text-4xl mb-2">📈</div>
            <p>Graphique temporel</p>
          </div>
        </div>
      </div>

      <!-- Top protocoles -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
        <h2 class="text-xl font-semibold mb-4 text-gray-900 dark:text-white">Répartition des Protocoles</h2>
        <div class="space-y-3">
          <div v-for="proto in protocols" :key="proto.name" class="flex items-center justify-between">
            <span class="text-gray-700 dark:text-gray-300">{{ proto.name }}</span>
            <div class="flex items-center space-x-3">
              <div class="w-32 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div 
                  class="h-2 rounded-full" 
                  :class="proto.color"
                  :style="{ width: proto.percentage + '%' }"
                ></div>
              </div>
              <span class="text-sm text-gray-600 dark:text-gray-400 w-8">{{ proto.percentage }}%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Top IPs sources -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
        <h2 class="text-xl font-semibold mb-4 text-gray-900 dark:text-white">Top IPs Sources</h2>
        <div class="space-y-3">
          <div v-for="ip in topIPs" :key="ip.address" class="flex justify-between items-center p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <span class="font-mono text-sm text-gray-900 dark:text-white">{{ ip.address }}</span>
            <span class="text-sm text-gray-600 dark:text-gray-400">{{ ip.count }} paquets</span>
          </div>
        </div>
      </div>

      <!-- Métriques générales -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
        <h2 class="text-xl font-semibold mb-4 text-gray-900 dark:text-white">Métriques Réseau</h2>
        <div class="grid grid-cols-2 gap-4">
          <div class="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <div class="text-2xl font-bold text-primary-600 dark:text-primary-400">{{ metrics.avgPacketSize }} bytes</div>
            <div class="text-sm text-gray-600 dark:text-gray-400">Taille moyenne</div>
          </div>
          <div class="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <div class="text-2xl font-bold text-primary-600 dark:text-primary-400">{{ metrics.uniqueIPs }}</div>
            <div class="text-sm text-gray-600 dark:text-gray-400">IPs uniques</div>
          </div>
          <div class="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <div class="text-2xl font-bold text-primary-600 dark:text-primary-400">{{ metrics.totalConnections }}</div>
            <div class="text-sm text-gray-600 dark:text-gray-400">Connexions</div>
          </div>
          <div class="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <div class="text-2xl font-bold text-primary-600 dark:text-primary-400">{{ metrics.uptime }}</div>
            <div class="text-sm text-gray-600 dark:text-gray-400">Uptime</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const protocols = ref([
  { name: 'TCP', percentage: 65, color: 'bg-blue-500' },
  { name: 'UDP', percentage: 25, color: 'bg-green-500' },
  { name: 'ICMP', percentage: 8, color: 'bg-purple-500' },
  { name: 'Autres', percentage: 2, color: 'bg-gray-500' }
])

const topIPs = ref([
  { address: '192.168.1.100', count: 1245 },
  { address: '10.0.0.50', count: 892 },
  { address: '172.16.0.10', count: 567 },
  { address: '192.168.1.1', count: 234 },
  { address: '8.8.8.8', count: 198 }
])

const metrics = ref({
  avgPacketSize: 842,
  uniqueIPs: 156,
  totalConnections: 2894,
  uptime: '12h 34m'
})
</script>