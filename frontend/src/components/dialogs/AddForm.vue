<template>
    <!-- notice dialogRef here -->
    <q-dialog  ref="dialogRef" @hide="onDialogHide" maximized >
      <q-card class="q-dialog-plugin custom-card" style="width: auto; background-color: transparent;">
        <center>
          <div class="container row justify-center pc-sa q-mt-xl">
              <div elevated class="q-ma-sm q-card--bordered col-12">
                <q-card>
                    <q-card-section  >
                        <div class="text-h6">
                          <center>
                            {{ "Agregar Ubicación" }}
                          </center>
                        </div>
                    </q-card-section >
                    <q-card-section  >
                       <q-form @submit="onSubmit" >
                        <div class="row q-pb-sm">
                            <div class="col-6" style="height: 50px;">
                                      <q-item>
                                        <q-input
                                            v-model= "name"
                                            type='text'
                                            label='Nombre del lugar'
                                            required
                                            filled
                                            dense
                                        />
                                      </q-item>
                            </div>
                            <div class="col-6" style="height: 50px;">
                                      <q-item>
                                        <q-select
                                          style          = "min-width: 13.3vw; height: 56px;"
                                          v-model        = "selectedGroup"
                                          :options       = "groups"
                                          :label         = "'Seleccione grupo'"
                                          option-label   = "name"
                                          option-value   = "value" 
                                          required
                                          filled
                                          dense
                                        />  
                                      </q-item>
                            </div>
                            <div class="col-6 q-pt-sm" style="height: 50px;">
                                      <q-item>
                                        <q-input
                                            v-model= "lat"
                                            type='decimal'
                                            label='Latitud'
                                            required
                                            filled
                                            dense
                                        />
                                      </q-item>
                            </div>
                            <div class="col-6 q-pt-sm" style="height: 50px;">
                                      <q-item>
                                        <q-input
                                            v-model="lon"
                                            type='decimal'
                                            label='Longitud'
                                            required
                                            filled
                                            dense
                                        />
                                      </q-item>
                            </div>
                        </div>
                        <div class="q-pt-xl col-12 q-gutter-xl space-between" >
                            <q-btn
                              :label="'Cancelar'" 
                              @click="onCancelClick" 
                              color="grey"
                            />
                             <q-btn  
                               :label="'Guardar'" 
                               type="submit"
                               color="green" 
                             />
                        </div>
                       </q-form>
                    </q-card-section >
                </q-card>
            </div>
          </div>
        </center>
      </q-card>
    </q-dialog>
  </template>
  
  <script>
//   import { onMounted } from "vue";
  import { useDialogPluginComponent }         from 'quasar';
  import { ref } from 'vue'




  export default {
    props: {
      apiUrl: {
        type: String,
        required: true,
      },
    },
  
    emits: [
      ...useDialogPluginComponent.emits
    ],
    // components: {
    //     FormScheme          : defineAsyncComponent(() => import('components/assets/FormScheme.vue'))
    // }, 
    setup (props) 
    {
      const { dialogRef, onDialogHide, onDialogOK, onDialogCancel } = useDialogPluginComponent()
      // REQUIRED; must be called inside of setup()
      // dialogRef      - Vue ref to be applied to QDialog
      // onDialogHide   - Function to be used as handler for @hide on QDialog
      // onDialogOK     - Function to call to settle dialog with "ok" outcome
      //                    example: onDialogOK() - no payload
      //                    example: onDialogOK({ /*.../* }) - with payload
      // onDialogCancel - Function to call to settle dialog with "cancel" outcome
      const lat     = ref(0);
      const lon     = ref(0);
      const name    = ref('');

      const groups = [
                    {name:'Cervecerías'   , value: 'cervecerias'},
                    {name:'Universidades' , value: 'universidades'},
                    {name:'Farmacias'     , value: 'farmacias'},
                    {name:'Emergencias'   , value: 'emergencias'},
                    {name:'Supermercados' , value: 'supermercados'}
                ];
      const selectedGroup            = ref(null);  
      const onSubmit = async () => {
          try {
            const response = await fetch(`${props.apiUrl}add`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({
                group: selectedGroup.value.value,   
                name: name.value,         
                lon: lon.value,
                lat: lat.value
              })
            })
        
            if (!response.ok) {
              throw new Error('Error al agregar ubicación')
            }
        
            const data = await response.json()
            console.log(data)
        
            // Cerramos el diálogo con éxito
            onDialogOK() 
          } catch (error) {
            console.error(error)
            alert('Hubo un problema agregando la ubicación.')
          }
        }


      return {
        name          , 
        selectedGroup ,
        lat           ,
        lon           ,
        groups        ,
        dialogRef     ,
        onDialogHide  ,
        onOKClick () 
        {
          onDialogOK()
        },
        onSubmit,
        onCancelClick: onDialogCancel

      }
    }
  }
  </script>

  <style>

.custom-card{
  box-shadow:none

}
</style>