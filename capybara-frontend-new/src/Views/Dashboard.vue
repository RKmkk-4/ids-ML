<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import StatCard from '../components/StatCard.vue'
import WorldMap from '../components/WorldMap.vue'
import SeverityChart from '../components/SeverityChart.vue'
import AlertList from '../components/AlertList.vue'

const API_URL = 'http://localhost:8000/api/v1'

const stats = ref({
  totalPackets: 0,
  totalAlerts: 0,
  packetsPerSecond: 0,
  isCapturing: false
})

const severityData = ref([
  { severity: 'CRITICAL', count: 0, color: '#ef4444' },
  { severity: 'HIGH', count: 0, color: '#f97316' },
  { severity: 'MEDIUM', count: 0, color: '#eab308' },
  { severity: 'LOW', count: 0, color: '#22c55e' }
])

const recentAlerts = ref([])

let interval: number

async function fetchAlerts() {
  try {
    const response = await axios.get(`${API_URL}/alerts/`)
    recentAlerts.value = response.data.alerts
    
    // Mettre à jour les compteurs de sévérité
    updateSeverityCounts(response.data.alerts)
  } catch (error) {
    console.error('Erreur API alerts:', error)
    // Données simulées en fallback
    recentAlerts.value = [
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
      }
    ]
    updateSeverityCounts(recentAlerts.value)
  }
}

async function fetchStats() {
  try {
    const response = await axios.get(`${API_URL}/stats/real-time`)
    stats.value = response.data
  } catch (error) {
    console.error('Erreur API stats:', error)
    // Stats simulées en fallback
    stats.value = {
      totalPackets: 12542,
      totalAlerts: recentAlerts.value.length,
      packetsPerSecond: Math.floor(Math.random() * 100) + 20,
      isCapturing: false
    }
  }
}

function updateSeverityCounts(alerts: any[]) {
  const counts = {
    CRITICAL: 0,
    HIGH: 0,
    MEDIUM: 0,
    LOW: 0
  }
  
  alerts.forEach(alert => {
    if (counts.hasOwnProperty(alert.severity)) {
      counts[alert.severity]++
    }
  })
  
  severityData.value = [
    { severity: 'CRITICAL', count: counts.CRITICAL, color: '#ef4444' },
    { severity: 'HIGH', count: counts.HIGH, color: '#f97316' },
    { severity: 'MEDIUM', count: counts.MEDIUM, color: '#eab308' },
    { severity: 'LOW', count: counts.LOW, color: '#22c55e' }
  ]
}

onMounted(() => {
  fetchAlerts()
  fetchStats()
  interval = setInterval(() => {
    fetchStats()
    fetchAlerts() // Rafraîchir aussi les alertes
  }, 5000)
})

onUnmounted(() => {
  if (interval) {
    clearInterval(interval)
  }
})

function handleDeleteAlert(alertId: string) {
  // Implémentez la suppression via API si disponible
  recentAlerts.value = recentAlerts.value.filter(alert => alert.id !== alertId)
  stats.value.totalAlerts = recentAlerts.value.length
  updateSeverityCounts(recentAlerts.value)
}
</script>