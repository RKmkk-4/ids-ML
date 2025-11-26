<template>
  <div class="container mx-auto px-4 py-8">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">Flux Réseau</h1>
      <p class="text-gray-600 dark:text-gray-400">Visualisation des flux réseau en temps réel</p>
    </div>

    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="border-b border-gray-200 dark:border-gray-700">
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-500 dark:text-gray-400">Timestamp</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-500 dark:text-gray-400">Source IP</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-500 dark:text-gray-400">Destination IP</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-500 dark:text-gray-400">Protocole</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-500 dark:text-gray-400">Taille</th>
            </tr>
          </thead>
          <tbody>
            <tr 
              v-for="flow in flows" 
              :key="flow.id"
              class="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
            >
              <td class="py-3 px-4 text-sm text-gray-600 dark:text-gray-300">{{ formatTime(flow.timestamp) }}</td>
              <td class="py-3 px-4 text-sm font-mono text-gray-900 dark:text-white">{{ flow.src_ip }}</td>
              <td class="py-3 px-4 text-sm font-mono text-gray-900 dark:text-white">{{ flow.dst_ip }}</td>
              <td class="py-3 px-4 text-sm">
                <span class="px-2 py-1 rounded-full text-xs" :class="getProtocolClass(flow.protocol)">
                  {{ getProtocolName(flow.protocol) }}
                </span>
              </td>
              <td class="py-3 px-4 text-sm text-gray-600 dark:text-gray-300">{{ flow.length }} bytes</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const flows = ref([
  {
    id: '1',
    timestamp: new Date().toISOString(),
    src_ip: '192.168.1.100',
    dst_ip: '8.8.8.8',
    protocol: 6,
    length: 1500
  },
  {
    id: '2',
    timestamp: new Date(Date.now() - 1000).toISOString(),
    src_ip: '10.0.0.50',
    dst_ip: '1.1.1.1',
    protocol: 17,
    length: 512
  },
  {
    id: '3',
    timestamp: new Date(Date.now() - 2000).toISOString(),
    src_ip: '172.16.0.10',
    dst_ip: '192.168.1.1',
    protocol: 1,
    length: 84
  }
])

function formatTime(timestamp: string) {
  return new Date(timestamp).toLocaleTimeString('fr-FR')
}

function getProtocolName(protocol: number) {
  const protocols: { [key: number]: string } = {
    1: 'ICMP',
    6: 'TCP',
    17: 'UDP'
  }
  return protocols[protocol] || `Proto ${protocol}`
}

function getProtocolClass(protocol: number) {
  const classes: { [key: number]: string } = {
    1: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
    6: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
    17: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
  }
  return classes[protocol] || 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
}
</script>