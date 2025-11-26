<template>
  <div class="container mx-auto px-4 py-8">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">Configuration</h1>
      <p class="text-gray-600 dark:text-gray-400">Paramètres du système Capybara IDS</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Menu latéral -->
      <div class="lg:col-span-1">
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <nav class="space-y-2">
            <button 
              v-for="tab in tabs"
              :key="tab.id"
              @click="activeTab = tab.id"
              class="w-full text-left px-4 py-2 rounded-lg transition-colors"
              :class="activeTab === tab.id 
                ? 'bg-primary-100 text-primary-700 dark:bg-primary-900 dark:text-primary-300' 
                : 'text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700'"
            >
              {{ tab.name }}
            </button>
          </nav>
        </div>
      </div>

      <!-- Contenu -->
      <div class="lg:col-span-2">
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <!-- Capture Réseau -->
          <div v-if="activeTab === 'network'" class="space-y-6">
            <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Configuration Réseau</h2>
            
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Interface Réseau
                </label>
                <select class="w-full border border-gray-300 dark:border-gray-600 rounded-lg px-3 py-2 bg-white dark:bg-gray-700 text-gray-900 dark:text-white">
                  <option>eth0</option>
                  <option>wlan0</option>
                  <option>en0</option>
                  <option>tous</option>
                </select>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Filtre BPF (Optionnel)
                </label>
                <input 
                  type="text" 
                  placeholder="ex: tcp port 80"
                  class="w-full border border-gray-300 dark:border-gray-600 rounded-lg px-3 py-2 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                >
              </div>

              <div class="flex items-center space-x-2">
                <input type="checkbox" id="promiscuous" class="rounded border-gray-300 text-primary-600 focus:ring-primary-500">
                <label for="promiscuous" class="text-sm text-gray-700 dark:text-gray-300">Mode promiscuous</label>
              </div>
            </div>
          </div>

          <!-- Détection -->
          <div v-if="activeTab === 'detection'" class="space-y-6">
            <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Règles de Détection</h2>
            
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Seuil SYN Flood (SYN/s)
                </label>
                <input 
                  type="number" 
                  v-model="config.synFloodThreshold"
                  class="w-full border border-gray-300 dark:border-gray-600 rounded-lg px-3 py-2 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                >
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Seuil Port Scan (ports/min)
                </label>
                <input 
                  type="number" 
                  v-model="config.portScanThreshold"
                  class="w-full border border-gray-300 dark:border-gray-600 rounded-lg px-3 py-2 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                >
              </div>

              <div class="flex items-center space-x-2">
                <input type="checkbox" v-model="config.enableML" class="rounded border-gray-300 text-primary-600 focus:ring-primary-500">
                <label class="text-sm text-gray-700 dark:text-gray-300">Activer la détection ML</label>
              </div>
            </div>
          </div>

          <!-- Sauvegarde -->
          <div class="flex justify-end space-x-4 mt-8 pt-6 border-t border-gray-200 dark:border-gray-700">
            <button class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
              Réinitialiser
            </button>
            <button 
              @click="saveConfig"
              class="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg transition-colors"
            >
              Sauvegarder
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const activeTab = ref('network')

const tabs = [
  { id: 'network', name: '📡 Capture Réseau' },
  { id: 'detection', name: '🔍 Règles de Détection' },
  { id: 'alerts', name: '🚨 Configuration Alertes' },
  { id: 'ml', name: '🤖 Modèles ML' },
  { id: 'system', name: '⚙️ Système' }
]

const config = ref({
  synFloodThreshold: 100,
  portScanThreshold: 50,
  enableML: true
})

function saveConfig() {
  console.log('Configuration sauvegardée:', config.value)
}
</script>