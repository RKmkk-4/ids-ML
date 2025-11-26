<template>
  <div class="container mx-auto px-4 py-8">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">Gestion des Alertes</h1>
      <p class="text-gray-600 dark:text-gray-400">Surveillance et gestion des alertes de sécurité</p>
    </div>

    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
      <div class="flex justify-between items-center mb-6">
        <div class="flex space-x-4">
          <select class="border border-gray-300 dark:border-gray-600 rounded-lg px-3 py-2 bg-white dark:bg-gray-700 text-gray-900 dark:text-white">
            <option>Toutes les sévérités</option>
            <option>CRITICAL</option>
            <option>HIGH</option>
            <option>MEDIUM</option>
            <option>LOW</option>
          </select>
          <input 
            type="text" 
            placeholder="Rechercher une IP..."
            class="border border-gray-300 dark:border-gray-600 rounded-lg px-3 py-2 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          >
        </div>
        <button class="bg-primary-600 hover:bg-primary-700 text-white px-4 py-2 rounded-lg transition-colors">
          Exporter CSV
        </button>
      </div>

      <AlertList :alerts="alerts" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import AlertList from '../components/AlertList.vue'

const alerts = ref([
  {
    id: '1',
    type: 'SYN Flood',
    severity: 'HIGH',
    src_ip: '192.168.1.100',
    description: 'SYN flood détecté: 150 SYN/s',
    timestamp: new Date().toISOString()
  },
  {
    id: '2',
    type: 'Port Scan',
    severity: 'MEDIUM',
    src_ip: '10.0.0.50',
    description: 'Scan de ports détecté: 45 ports différents',
    timestamp: new Date(Date.now() - 300000).toISOString()
  },
  {
    id: '3',
    type: 'ML Anomaly',
    severity: 'CRITICAL',
    src_ip: '172.16.0.10',
    description: 'Anomalie détectée par ML (score: -0.234)',
    timestamp: new Date(Date.now() - 600000).toISOString()
  },
  {
    id: '4',
    type: 'Land Attack',
    severity: 'HIGH',
    src_ip: '192.168.1.1',
    description: 'Land attack détecté: source et destination identiques',
    timestamp: new Date(Date.now() - 900000).toISOString()
  }
])
</script>