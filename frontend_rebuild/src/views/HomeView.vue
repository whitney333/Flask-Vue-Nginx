<script setup>
  import axios from '@/axios';
import { useCounterStore } from '@/stores/counter';
  import { ref } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  const artistDetails = ref({})
  const router = useRouter()
  const counterStore = useCounterStore()
  const mid = ref('1297') // to do
  const loading = ref(true)
  const handleIncrement = () => {
    counterStore.increment()
  }
  const handleToAbout = () => {
    router.push({path: '/about'})
  }
  const fetchArtistDetails = async () => {
    try {
      const res = await axios.get(`/api/artist/info?mid=${mid.value}`, {setTimeout: 10000})
      artistDetails = res.data["results"]
    } catch (e) {
      console.error(e);
    }
  }

  const fetchAll = async () => {
    await fetchArtistDetails()
    loading = false
  }

  fetchAll()

</script>

<template>
  <v-container 
    fluid 
    class="bg-surface-variant">
    <v-row
      class="mb-2"
      no-gutters
    >
      <v-col>
        <v-card 
          class="pa-2 ma-2"
          title="Summary"
          >
          <v-divider></v-divider>
          <v-row>
            <v-col>
              <v-avatar style="height:130px; width:130px; margin-right:15px">
                      <v-img
                          :src=artistDetails.image
                          class="img-design"
                      ></v-img>
                    </v-avatar>

            </v-col>
            <v-row>
              <v-col>
                Name: 
              </v-col>
              <v-col>
                Age:
              </v-col>
            </v-row>

          </v-row>

        </v-card>
      </v-col>

      <v-col>
        <v-card 
          class="pa-2 ma-2"
          title="Trending"
          >
          <v-divider></v-divider>
        </v-card>
      </v-col>
    </v-row>
  </v-container>

</template>

<style>
  .card {
    min-width: 600px;
    min-height: 600px;
  }

</style>