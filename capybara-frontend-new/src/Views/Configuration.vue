<template>
  <div class="container mx-auto px-4 py-8">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">Configuration</h1>
      <p class="text-gray-600 dark:text-gray-400">Paramètres du système Capybara IDS</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
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

      <div class="lg:col-span-2">
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
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

          <div v-if="activeTab === 'ml'" class="space-y-4">
            <h3 class="text-lg font-semibold text-gray-800 dark:text-white mb-4">
              🤖 Configuration du Machine Learning
            </h3>
            
            <div class="bg-blue-50 dark:bg-blue-900 p-4 rounded-lg">
              <p class="text-sm text-blue-800 dark:text-blue-200">
                Le système utilise le Machine Learning pour détecter automatiquement les anomalies réseau.
              </p>
            </div>
            
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium mb-2">État du modèle</label>
                <div class="flex items-center gap-2">
                  <span :class="mlStatus.is_ready ? 'text-green-500' : 'text-red-500'">
                    {{ mlStatus.is_ready ? '✅ Actif' : '❌ Inactif' }}
                  </span>
                </div>
              </div>
              
              <div>
                <label class="block text-sm font-medium mb-2">Type de modèle</label>
                <select v-model="mlConfig.model_type" class="w-full p-2 border rounded">
                  <option value="random_forest">Random Forest</option>
                  <option value="isolation_forest">Isolation Forest</option>
                </select>
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-medium mb-2">
                Seuil de détection d'anomalie (0.0 - 1.0)
              </label>
              <input
                v-model.number="mlConfig.anomaly_threshold"
                type="number"
                step="0.1"
                min="0"
                max="1"
                class="w-full p-2 border rounded dark:bg-gray-700"
              />
            </div>
            
            <div class="bg-yellow-50 dark:bg-yellow-900 p-4 rounded-lg">
              <p class="text-sm text-yellow-800 dark:text-yellow-200 mb-2">
                ⚠️ L'entraînement utilise les données de trafic capturées. 
                Assurez-vous d'avoir au moins 100 flows capturés.
              </p>
              <p class="text-sm text-yellow-800 dark:text-yellow-200">
                Durée estimée : 30 secondes à 2 minutes selon la quantité de données.
              </p>
            </div>
            
            <div class="flex gap-4">
              <button
                @click="trainModel"
                :disabled="isTraining"
                class="px-6 py-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg hover:from-purple-600 hover:to-pink-600 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {{ isTraining ? '🔄 Entraînement en cours...' : '🚀 Lancer l\'entraînement' }}
              </button>
              
              <button
                @click="checkMLStatus"
                class="px-6 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600"
              >
                🔍 Vérifier l'état
              </button>
            </div>
            
            <div v-if="trainingResults" class="mt-4 p-4 bg-green-50 dark:bg-green-900 rounded-lg">
              <h4 class="font-semibold text-green-800 dark:text-green-200 mb-2">
                ✅ Entraînement terminé !
              </h4>
              <div class="text-sm text-green-700 dark:text-green-300 space-y-1">
                <p v-if="trainingResults.accuracy">Précision : {{ (trainingResults.accuracy * 100).toFixed(2) }}%</p>
                <p v-if="trainingResults.cv_accuracy">
                  Cross-validation : {{ (trainingResults.cv_accuracy * 100).toFixed(2) }}%
                </p>
                <p v-if="trainingResults.model_path">Modèle sauvegardé : {{ trainingResults.model_path }}</p>
              </div>
            </div>
            
            <div v-if="trainingError" class="mt-4 p-4 bg-red-50 dark:bg-red-900 rounded-lg">
              <h4 class="font-semibold text-red-800 dark:text-red-200 mb-2">
                ❌ Erreur d'entraînement
              </h4>
              <p class="text-sm text-red-700 dark:text-red-300">{{ trainingError }}</p>
            </div>
          </div>

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
import { ref, onMounted } from 'vue'
import axios from 'axios'

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

const isTraining = ref(false)
const trainingResults = ref<any>(null)
const trainingError = ref('')
const mlStatus = ref<{ is_ready: boolean }>({ is_ready: false })
const mlConfig = ref({
  model_type: 'random_forest',
  anomaly_threshold: 0.1
})

async function saveConfig() {
  try {
    const response = await axios.post('http://localhost:8000/api/v1/config/', {
      syn_flood_threshold: config.value.synFloodThreshold,
      port_scan_threshold: config.value.portScanThreshold,
      ml_enabled: config.value.enableML
    })
    
    if (response.data.success) {
      alert('✅ Configuration sauvegardée avec succès !')
    } else {
      alert('❌ Erreur: ' + response.data.message)
    }
  } catch (error) {
    console.error('Erreur sauvegarde config:', error)
    alert('❌ Impossible de sauvegarder la configuration')
  }
}

async function loadConfig() {
  try {
    const response = await axios.get('http://localhost:8000/api/v1/config/')
    config.value = {
      synFloodThreshold: response.data.syn_flood_threshold,
      portScanThreshold: response.data.port_scan_threshold,
      enableML: response.data.ml_enabled
    }
  } catch (error) {
    console.error('Erreur chargement config:', error)
  }
}

async function trainModel() {
  isTraining.value = true
  trainingError.value = ''
  trainingResults.value = null
  
  try {
    const response = await axios.post('http://localhost:8000/api/v1/config/train')
    
    if (response.data.success) {
      trainingResults.value = response.data.metrics
      await checkMLStatus()
    } else {
      trainingError.value = response.data.message
    }
  } catch (error: any) {
    trainingError.value = error.response?.data?.message || error.message
  } finally {
    isTraining.value = false
  }
}

async function checkMLStatus() {
  try {
    const response = await axios.get('http://localhost:8000/api/v1/config/')
    mlStatus.value = { is_ready: response.data.ml_enabled }
  } catch (error) {
    console.error('Erreur vérification ML:', error)
  }
}

onMounted(() => {
  loadConfig()
  checkMLStatus()
})
</script>
