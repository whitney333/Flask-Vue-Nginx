<script setup>
  import axios from '@/axios';
  import { useCounterStore } from '@/stores/counter';
  import { reactive, ref } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  const artistInfo = ref({})
  const memberInfo = ref({})
  const hotData = ref([])
  const router = useRouter()
  const counterStore = useCounterStore()
  const mid = ref('1297') // to do
  const page = ref(1)
  const q = ref("t024")
  const limit = ref(10)
  const cardLoading = reactive({
    artist: true,
    member: true,
    trending: true,
  })
  const handleIncrement = () => {
    counterStore.increment()
  }
  const handleToAbout = () => {
    router.push({path: '/about'})
  }
  const fetchArtistInfo = async () => {
    try {
      const res = await axios.get(`/api/artist/info?mid=${mid.value}`, {setTimeout: 10000})
      artistInfo.value = res.data["results"]
      console.log("artistInfo : ", artistInfo);
    } catch (e) {
      console.error(e);
    }
  }

  const fetchMemberInfo = async () => {
    try {
      const res = await axios.get(`/api/artist/members`, {setTimeout: 10000})
      memberInfo.value = res.data["results"]
      console.log("memberInfo : ", memberInfo);
    } catch (e) {
      console.error(e);
    }
  }

  const fetchTheQoo = async () => {
    try {
      const res = await axios.get(`/api/theqoo/hot?page=${page.value}&limit=${limit.value}&q=${q.value}`, {setTimeout: 10000})
      hotData.value = res.data["posts"]
      console.log("memberInfo : ", memberInfo);
    } catch (e) {
      console.error(e);
    }
  }


  const fetchAll = async () => {
    await fetchArtistInfo()
    cardLoading.artist = false
    await fetchMemberInfo()
    cardLoading.member = false
    await fetchTheQoo()
    cardLoading.trending = false
    console.log("// fetchAll Done");
  }

  fetchAll()

</script>

<template>
  <v-container
    class="bgcolor"
    fluid >
    <v-row
      class="mb-2"
      no-gutters
      align="stretch"
    >
      <!-- Artist Info -->
      <v-col>
        <v-card 
          class="fill-height"
          variant="text"
          title="Summary"
          :loading="cardLoading.artist"
          >
          <template v-slot:text>
          <v-divider></v-divider>
          <br />
          <v-row>
            <v-col 
            align="center"
            justify="center"
            class="flex-grow-2">
              <v-avatar style="height:150px; width:150px;">
                <v-img
                    :src=artistInfo.image
                    class="img-design"
                ></v-img>
              </v-avatar>
            </v-col>
            <v-col  class="flex-grow-2">
              <v-row>
                <v-col>
                  <v-card  class="pa-2 ma-2" variant="text">
                    Artist:
                    <br />
                    {{ artistInfo.artist ? artistInfo.artist : 'N/A'}}
                  </v-card>
                </v-col>
                <v-col>
                  <v-card class="pa-2 ma-2" variant="text">
                    Debut Year:
                    <br />
                    {{ artistInfo.debut_year ? artistInfo.debut_year : 'N/A' }}
                  </v-card>
                </v-col>
                <v-responsive width="100%"></v-responsive>
                <v-col>
                  <v-card class="pa-2 ma-2" variant="text">
                    Country:
                    <br />
                    <img
                            src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/flags/kr.svg"
                            alt="kr-flag"
                            height="30px"
                        >
                  </v-card>
                </v-col>

                <v-col>
                  <v-card class="pa-2 ma-2" variant="text">
                    Birth:
                    <br />
                    {{  artistInfo.birth ? artistInfo.birth : "N/A" }}
                  </v-card>
                </v-col>
              </v-row>
            </v-col>
          </v-row>
          <v-divider></v-divider>
          <v-row>
            <v-col>
              <v-card class="pa-2 ma-2" variant="text">
                Type:
                <br />
                {{  artistInfo.type ? artistInfo.type : "N/A" }}
              </v-card>
            </v-col>
            <v-col>
              <v-card class="pa-2 ma-2" variant="text">
                Members:
                <br />
                {{  memberInfo ? memberInfo : "N/A" }}
              </v-card>
            </v-col>
          </v-row>
          <v-divider></v-divider>
          <v-row>
            <v-col>
              <v-card class="pa-2 ma-2" variant="text">
                Label:
                <br />
                {{  artistInfo.labels ? artistInfo.labels : "N/A" }}
              </v-card>
            </v-col>
            <v-col>
              <v-card class="pa-2 ma-2" variant="text">
                Fandom:
                <br />
                {{  artistInfo.fandom ? artistInfo.fandom : "N/A" }}
              </v-card>
            </v-col>
            <v-col>
              <v-card class="pa-2 ma-2" variant="text">
                Color:
                <br />
                {{  artistInfo.color ? artistInfo.color : "N/A" }}
              </v-card>
            </v-col>
            <v-col>
              <v-card class="pa-2 ma-2" variant="text">
                Last Release:
                <br />
                {{  artistInfo.last_release ? artistInfo.last_release : "N/A" }}
              </v-card>
            </v-col>

          </v-row>

        </template>

        </v-card>
      </v-col>


      <!-- Trending Info -->
      <v-col>
        <v-card 
          class="fill-height"
          title="Trending"
          :loading="cardLoading.trending"
          >
          <template v-slot:text>

          <v-divider></v-divider>
          <br />
          <v-card variant="text" v-if="hot_data" v-for="item in hot_data">

          </v-card>
          <v-card variant="text" v-else>
            No relevant data in 48 hours
          </v-card>
          
        </template>
        </v-card>
      </v-col>
    </v-row>
    <!-- Statistic-->
    <br />
     <v-divider></v-divider>
     <br />
    <h2> Top Statistics</h2>
    <v-card>

    </v-card>

  </v-container>

</template>

<style>
  .card {
    min-width: 600px;
    min-height: 600px;
  }

  .bgcolor {
    background-color: #F5F5F5;
  }

</style>