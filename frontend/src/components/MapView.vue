<template>
  <div id="map" style="height: 500px;"></div>
</template>

<script setup>
import { onMounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

async function fetchPlaces(group) {
  const response = await fetch(`http://localhost:5000/places?group=${group}`)
  const data = await response.json()
  return data
}

onMounted(async () => {
  const map = L.map('map').setView([-34.6037, -58.3816], 13)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map)

  const groups = {
    'Cervecerías': 'cervecerias',
    'Universidades': 'universidades',
    'Farmacias': 'farmacias',
    'Emergencias': 'emergencias',
    'Supermercados': 'supermercados'
  }
  navigator.geolocation.getCurrentPosition(
    (position) => {
      const userLat = position.coords.latitude
      const userLon = position.coords.longitude
      map.setView([userLat, userLon], 15) // Centrar en el usuario

      L.marker([userLat, userLon])
        .addTo(map)
        .bindPopup('¡Estás aquí!')
        .openPopup()
    },
    (error) => {
      console.error('No se pudo obtener la ubicación:', error)
    }
  )
  const overlays = {}

  for (const [label, groupName] of Object.entries(groups)) {
    const places = await fetchPlaces(groupName)

    const markers = places.map(place => {
      return L.marker([place.lat, place.lon]).bindPopup(place.name)
    })

    overlays[label] = L.layerGroup(markers)
    overlays[label].addTo(map)
  }

  L.control.layers(null, overlays).addTo(map)
})
</script>
