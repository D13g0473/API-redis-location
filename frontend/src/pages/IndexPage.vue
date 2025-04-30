<template>
  <q-page padding>
    <div class="row">
      <div class="col-12 q-gutter-xs">                  
        <q-btn label="Agregar ubicación" color="green" @click="addPlaces"/>
        <q-btn label="Calcular distancia" color="secondary" @click="calculateDistance()"/>
        <q-btn label="Mostrar Cercanos" color="info" @click="showNearly" />
        <q-btn label="Setear Ubicación Manual" color="warning" @click="setManualLocation" />
      </div>
    </div>
    <div class="col-6 q-pt-xs q-gutter-xs">
      
      <q-table
        v-if="showNearlyTable"
        bordered
        title="Lugares cercanos"
        row-key     = "name"
        :wrap-cells = true
        :columns    = "columns"
        :rows       = "row"
      >

      </q-table>
    </div>
    <div class="col-6 q-pt-xl">
      <div id="map" style="height: 500px;"></div>
    </div>
  </q-page>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { Dialog } from 'quasar';
import AddForm from 'src/components/dialogs/AddForm.vue';
import CalculateDistance from 'src/components/dialogs/CalculateDistance.vue';
import SetManualLocation from 'src/components/dialogs/SetManualLocation.vue'

// Variables
const map = ref(null)
const overlays = ref({})
const userLat = ref(null)
const userLon = ref(null)
const apiUrl = "http://localhost:5000/"
const showNearlyTable = ref(false)
const columns     = [
                      { name: 'group', align: 'center',label:'Grupo',field:'group',sortable: true,type:  'text'},  
                      { name: 'name', align: 'center',label:'Nombre',field:'name',sortable: true,type:  'text'},
                      { name: 'distance', align: 'center',label:'Distancia(en Km)',field:'distance',sortable: true,type:  'number'},
                    ]
const row        = ref([])
// Grupos
const groups = {
  'Cervecerías': 'cervecerias',
  'Universidades': 'universidades',
  'Farmacias': 'farmacias',
  'Emergencias': 'emergencias',
  'Supermercados': 'supermercados'
}

// Funciones
async function fetchPlaces(group) {
  const response = await fetch(`${apiUrl}places?group=${group}`)
  const data = await response.json()
  return data
}

async function fetchNearby(group, lon, lat) {
  const response = await fetch(`${apiUrl}nearby?group=${group}&lon=${lon}&lat=${lat}`)
  const data = await response.json()
  return data
}

async function reloadPlaces() {
  // Limpiar todas las capas existentes
  for (const groupLayer of Object.values(overlays.value)) {
    map.value.removeLayer(groupLayer)
  }
  overlays.value = {}

  // Volver a cargar todos los lugares
  for (const [label, groupName] of Object.entries(groups)) {
    const places = await fetchPlaces(groupName)

    const markers = places.map(place => {
      return L.marker([place.lat, place.lon]).bindPopup(place.name)
    })

    overlays.value[label] = L.layerGroup(markers)
    overlays.value[label].addTo(map.value)
  }

  // Agregar control de capas de nuevo
  L.control.layers(null, overlays.value).addTo(map.value)
}

async function addPlaces(){
  Dialog.create(
            {
                component:AddForm,
                componentProps:{
                  apiUrl:apiUrl
                }
            }).onOk(async () => {
                console.log('Nuevo lugar agregado, recargando mapa...')
                await reloadPlaces()
  })
}
async function calculateDistance(){
  Dialog.create(
            {
                component:CalculateDistance,
                componentProps:{
                  apiUrl:apiUrl
                }
            }).onOk(async () => {
                console.log('Nuevo lugar agregado, recargando mapa...')
                // await reloadPlaces()
  })
}
async function showNearly() {
  if (!userLat.value || !userLon.value) {
    alert('Ubicación del usuario no disponible todavía.')
    return
  }

  // Limpiamos el mapa (sacamos las capas anteriores)
  for (const groupLayer of Object.values(overlays.value)) {
    map.value.removeLayer(groupLayer)
  }

  const nearbyMarkers = []

  for (const [label, groupName] of Object.entries(groups)) {
    const places = await fetchNearby(groupName, userLon.value, userLat.value)
    // Set para evitar nombres repetidos
    const existingNames = new Set(row.value.map(r => r.name))

    const filteredPlaces = places.filter(([name]) => !existingNames.has(name))
    filteredPlaces.forEach(([name]) => existingNames.add(name)) // Agregar los nuevos para próximos grupos

    // Luego sí: agregar al row
    const newRecords = filteredPlaces.map(([name, distance]) => ({
      name,
      distance,
      group: label
    }))
    row.value.push(...newRecords)

    // Y crear los markers también con los lugares filtrados
    const markers = filteredPlaces.map(([name, distance, [lon, lat]]) =>
      L.marker([lat, lon], { icon: getIconForGroup(label) })
       .bindPopup(`${name} (${distance.toFixed(2)} km)`)
    )

    if (markers.length) {
      const groupLayer = L.layerGroup(markers)
      groupLayer.addTo(map.value)
      nearbyMarkers.push(groupLayer)
    }
  }
  showNearlyTable.value = true; 
  console.log(row.value);
  
}

function getIconForGroup(groupLabel) {
  const colorMap = {
    'Cervecerías': 'green',
    'Universidades': 'blue',
    'Farmacias': 'red',
    'Emergencias': 'orange',
    'Supermercados': 'purple'
  }

  const iconColor = colorMap[groupLabel] || 'gray'

  return L.divIcon({
    className: 'custom-icon',
    html: `<div style="
              background-color: ${iconColor};
              color: white;
              border-radius: 50%;
              width: 24px;
              height: 24px;
              text-align: center;
              line-height: 24px;
              font-size: 12px;
              font-weight: bold;
            ">${groupLabel[0]}</div>`,
    iconSize: [24, 24],
    iconAnchor: [12, 24],
    popupAnchor: [0, -24]
  })
}
async function setManualLocation() {
  Dialog.create({
    component: SetManualLocation,
    componentProps: {
      currentLat: userLat.value,
      currentLon: userLon.value
    }
  }).onOk(async ({ lat, lon }) => {
    userLat.value = lat
    userLon.value = lon

    // Mover marcador en el mapa
    map.value.setView([lat, lon], 15)
    
    // Opcional: eliminar marcador anterior si existía
    if (map.value.userMarker) {
      map.value.removeLayer(map.value.userMarker)
    }

    // Crear nuevo marcador
    const marker = L.marker([lat, lon]).bindPopup('¡Estás aquí!')
    marker.addTo(map.value).openPopup()
    map.value.userMarker = marker

    // Enviar a Redis
    try {
      await fetch(`${apiUrl}update_location`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: '1',
          lat: lat,
          lon: lon
        })
      })
      console.log('Ubicación manual actualizada exitosamente.')
    } catch (error) {
      console.error('Error al actualizar ubicación manual:', error)
    }
  })
}

onMounted(async () => {
  map.value = L.map('map').setView([-34.6037, -58.3816], 13)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map.value)

  navigator.geolocation.getCurrentPosition(
    async (position) => {
      userLat.value = position.coords.latitude
      userLon.value = position.coords.longitude

      map.value.setView([userLat.value, userLon.value], 15) // Centrar en el usuario

      const marker = L.marker([userLat.value, userLon.value]).bindPopup('¡Estás aquí!')
      marker.addTo(map.value).openPopup()
      map.value.userMarker = marker

      // Cargar todos los lugares inicialmente
      for (const [label, groupName] of Object.entries(groups)) {
        const places = await fetchPlaces(groupName)

        const markers = places.map(place => {
          return L.marker([place.lat, place.lon, {icon: getIconForGroup(label) }]).bindPopup(place.name)
        })

        overlays.value[label] = L.layerGroup(markers)
        overlays.value[label].addTo(map.value)
      }

      L.control.layers(null, overlays.value).addTo(map.value)

      try {
            await fetch(`${apiUrl}update_location`, {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                  user_id: '1',  // pon aquí tu lógica real de ID de usuario
                  lat: userLat.value,
                  lon: userLon.value
                })
              })
              console.log('Ubicación actualizada exitosamente en Redis.')
          } catch (error) { console.error('Error al actualizar ubicación:', error) }

    },
    (error) => {
      console.error('No se pudo obtener la ubicación:', error)
    }
  )
})
</script>
