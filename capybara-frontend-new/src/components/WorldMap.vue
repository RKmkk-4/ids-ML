<template>
  <div class="w-full h-96 bg-white rounded-lg shadow-lg">
    <div ref="mapContainer" class="w-full h-full rounded-lg"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const mapContainer = ref<HTMLElement>()
let map: L.Map | null = null

// Fix pour les markers Leaflet
delete (L.Icon.Default.prototype as any)._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
})

onMounted(() => {
  if (mapContainer.value) {
    map = L.map(mapContainer.value).setView([46.603, 1.888], 5) // Centré sur la France
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(map)

    // Exemple de markers pour les alertes
    const alertMarkers = [
      { lat: 48.8566, lng: 2.3522, ip: '192.168.1.100', severity: 'HIGH' }, // Paris
      { lat: 51.5074, lng: -0.1278, ip: '10.0.0.50', severity: 'MEDIUM' }, // London
      { lat: 40.7128, lng: -74.0060, ip: '172.16.0.10', severity: 'CRITICAL' }, // New York
    ]

    alertMarkers.forEach(alert => {
      const color = getColorBySeverity(alert.severity)
      const marker = L.circleMarker([alert.lat, alert.lng], {
        radius: 10,
        fillColor: color,
        color: '#000',
        weight: 1,
        opacity: 1,
        fillOpacity: 0.8
      }).addTo(map!)
      
      marker.bindPopup(`
        <div class="p-2">
          <strong>IP:</strong> ${alert.ip}<br>
          <strong>Sévérité:</strong> <span style="color: ${color}">${alert.severity}</span>
        </div>
      `)
    })
  }
})

onUnmounted(() => {
  if (map) {
    map.remove()
  }
})

function getColorBySeverity(severity: string): string {
  const colors: { [key: string]: string } = {
    'LOW': '#22c55e',
    'MEDIUM': '#eab308',
    'HIGH': '#f97316',
    'CRITICAL': '#ef4444'
  }
  return colors[severity] || '#6b7280'
}
</script>