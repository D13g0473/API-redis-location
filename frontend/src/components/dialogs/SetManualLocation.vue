<template>
        <q-dialog  ref="dialogRef" @hide="onDialogHide" maximized >
      <q-card class="q-dialog-plugin custom-card" style="width: auto; background-color: transparent;">
        <center>
          <div class="container row justify-center pc-sa q-mt-xl">
              <div elevated class="q-ma-sm q-card--bordered col-12">
                <q-card style="min-width: 300px">
                  <q-card-section class="text-h6">Cambiar Ubicación Manualmente</q-card-section>

                  <q-card-section>
                    <q-input v-model.number="lat" label="Latitud" type="number" />
                    <q-input v-model.number="lon" label="Longitud" type="number" />
                  </q-card-section>
              
                  <q-card-actions align="right">
                    <q-btn flat label="Cancelar" color="primary" v-close-popup />
                    <q-btn flat label="Guardar" color="positive" @click="save" />
                  </q-card-actions>
                </q-card>
            </div>
          </div>
        </center>
      </q-card>
    </q-dialog>
  </template>
  
  <script setup>
  import { ref }                      from 'vue'
  import { useDialogPluginComponent } from 'quasar';
    const { dialogRef, onDialogHide } = useDialogPluginComponent()
  const props = defineProps(['currentLat', 'currentLon'])
  const emit = defineEmits(['ok'])
  
  const lat = ref(props.currentLat)
  const lon = ref(props.currentLon)
  
  function save() {
    emit('ok', { lat: lat.value, lon: lon.value })
  }
  </script>
  