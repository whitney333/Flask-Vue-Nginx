<script setup>
    import { computed, onMounted, onUnmounted, ref, watch } from 'vue';
    import getUnicodeFlagIcon from 'country-flag-icons/unicode'
    import youtubeIcon from '@/assets/icons/youtube.svg';
    import tiktokIcon from '@/assets/icons/tiktok.svg';
    import instagramIcon from '@/assets/icons/instagram.svg';
    import bilibiliIcon from '@/assets/icons/bilibili.svg';
    import xiaohongshuIcon from '@/assets/icons/xiaohongshu.svg';
    import youtubeBlackIcon from '@/assets/icons/youtube-black.svg';
    import tiktokBlackIcon from '@/assets/icons/tiktok-black.svg';
    import instagramBlackIcon from '@/assets/icons/instagram-black.svg';
    import bilibiliBlackIcon from '@/assets/icons/bilibili-black.svg';
    import xiaohongshuBlackIcon from '@/assets/icons/xiaohongshu-black.svg';
    import { regions, indexToCountry } from '@/libs/utils';
    import { Book, Captions, Clipboard, DollarSign, File, FileTextIcon, Globe, Box, Link, RadioTower, Share2 } from 'lucide-vue-next';
    import { useArtistStore } from "@/stores/artist.js";
    import { useUserStore } from "@/stores/user.js";

    const artistStore = useArtistStore()
    const userStore = useUserStore()
    const followedArtists = userStore.followedArtists
    const selectedArtist = ref(null)
    const platform = ref([])
    const post = ref({
      title: '',
      description: '',
      hashtag: [],
      text: '',
      url: '',
      file: null,
    })

    const platforms = [
      { name: "Instagram", icon: instagramIcon, color: "#FF0069", blackIcon: instagramBlackIcon },
      { name: "Tiktok", icon: tiktokIcon, color: "#000000", blackIcon: tiktokBlackIcon },
      { name: "Youtube", icon: youtubeIcon, color: "#FF0000", blackIcon: youtubeBlackIcon },
      { name: "Rednote", icon: xiaohongshuIcon, color: "#FF2442", blackIcon: xiaohongshuBlackIcon},
      { name: "Bilibili", icon: bilibiliIcon, color: "#00A1D6", blackIcon: bilibiliBlackIcon },
    ]

    
    const region = ref([])
    // default expand the artist panel
    const state = ref('artist')
    const budgetRange = ['Less than US$50', 'US$50 - US$500', 'US$500 - US$5,000', 'More than US$5000']
    const budget = ref(budgetRange[0])

    const screenWidth = ref(window.innerWidth);

    const updateScreenWidth = () => {
      screenWidth.value = window.innerWidth;
    };

    onMounted(() => {
      window.addEventListener('resize', updateScreenWidth);
    });
    
    onUnmounted(() => {
      window.removeEventListener('resize', updateScreenWidth);
    });
    const handleBackBtn = () => {
        router.go(-1)
    }

    const isLargeScreen = computed(() => screenWidth.value >= 1024); // Tailwind's lg: breakpoint (1024px)

    const handleVisit = () => {
      let url = post.value.url;
      if (!url.startsWith('http')) {
        url = 'http://' + url;
      }
      window.open(url);
    }
    const changeState = (newState) => {
      state.value = newState;
    }

    // select the first artist by default
    onMounted(() => {
      if (followedArtists.length > 0) {
        selectedArtist.value = followedArtists[0]
      }
    })

    const onSubmitted = () => {
      console.log('Submitted', {
        artist: selectedArtist.value,
        region: region.value.map((r) => indexToCountry[r]),
        platform: platform.value.map((i) => platforms[i].name),
        budget: budget.value,
        // post: post.value,
      });
    }

    const submitCampaign = async () => {
      const res = await axios.post(

      )
    }


</script>

<template>
    <v-container
        fluid
        :class="['fill-height', 'align-start', 'bg-grey-lighten-4', 'py-10']">
        <v-card 
        :class="['bg-grey-lighten-4', 'w-full']"
        flat
        >
        <v-card-title class="my-5">
          <span class="text-h4">
            {{ $t('Create Your Post') }}
          </span>
        </v-card-title>
        <v-card-text>
        <v-expansion-panels  mandatory  v-model="state" >
          <!--  artist panel  -->
          <v-expansion-panel value="artist" class="mb-5">
            <v-expansion-panel-title v-slot="{ expanded }">
              <v-row no-gutters class="items-center">
                <v-col class="d-flex justify-start" cols="12" lg="4">
                  <span class="text-2xl font-medium">
                    {{ $t('Select Artist') }}
                  </span>
                </v-col>
                <v-col
                  class="items-center lg:block hidden"
                  cols="8"
                >
                  <v-fade-transition >
                    <span
                      v-if="!expanded"
                      key="1"
                      class="text-lg font-medium capitalize"
                    >
                      {{ selectedArtist.english_name }} ({{ selectedArtist.korean_name }})
                    </span>
                  </v-fade-transition>
                </v-col>
              </v-row>
            </v-expansion-panel-title>
            <v-expansion-panel-text>
              <v-item-group v-model="selectedArtist">
                <v-container class="max-w-screen-md grid md:grid-cols-4 grid-cols-2 gap-5">
                    <div
                      v-for="(artist, i) in followedArtists"
                      :key="artist.id || i"
                      class="flex justify-center items-center"
                    >
                      <v-item v-slot="{ isSelected, toggle }" :value="artist">
                        <v-card
                          :color="'#FFFFFF'"
                          flat
                          class="flex align-center transition-all rounded-lg border-2"
                          :class="isSelected ? ' border-black' : 'border-neutral-200'"
                          height="110"
                          width="100"
                          @click="toggle"
                        >
                          <v-scroll-y-transition>
                            <div
                              class="flex-grow-1 text-center flex flex-col items-center justify-center"
                            >
                              <v-img
                                :src="artist.image"
                                height="50"
                                width="50"
                                class="rounded-full object-cover"
                              ></v-img>
                              <div class="text-xs font-medium text-center mt-2">
                                {{ artist.english_name }}
                              </div>
                              <div class="text-[11px] text-gray-500 text-center">
                                {{ artist.korean_name }}
                              </div>
                            </div>

                          </v-scroll-y-transition>
                        </v-card>
                      </v-item>
                    </div>
                </v-container>
              </v-item-group>
              <div class="flex justify-center items-center gap-10 my-5">
                <div class="flex justify-center items-center">
                  <v-btn color='black'
                  class="w-32 text-none rounded-pill text-white"
                  @click="() => changeState('region')">
                    <span class="font-medium">
                      {{ $t('Next') }}
                    </span>
                  </v-btn>
                </div>
              </div>
            </v-expansion-panel-text>
          </v-expansion-panel>

          <!--  region panel  -->
          <v-expansion-panel value="region" class="mb-5">
            <!--  selected value  -->
            <v-expansion-panel-title v-slot="{ expanded }">
              <v-row no-gutters class="items-center">
                <v-col class="d-flex justify-start" cols="12" lg="4">
                  <span class="text-2xl font-medium">
                    {{ $t('Select Region') }}
                  </span>
                </v-col>
                <v-col
                  class="items-center lg:block hidden"
                  cols="8"
                >
                  <v-fade-transition >
                    <span
                      v-if="!expanded"
                      key="1"
                      class="text-lg font-medium capitalize"
                    >
                      {{ region == '' ? '' :  region.map((r) => indexToCountry[r]).join(' | ')}}
                    </span>
                  </v-fade-transition>
                </v-col>
              </v-row>
            </v-expansion-panel-title>
            <!-- selected options -->
            <v-expansion-panel-text >
              <v-item-group multiple v-model="region">
                <v-container class="max-w-screen-md">
                  <v-row>
                    <v-row v-for="(reg, i) in Object.keys(regions)" :key="i" class="mb-5">
                      <v-col md="2" cols="12">
                        <span class="text-xl font-medium">
                          {{ $t(reg) }}
                        </span>
                      </v-col>
                      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5">
                          <v-col
                            v-for="(country, j) in regions[reg]"
                            :key="j"
                          >
                            <v-item v-slot="{ isSelected, toggle }">
                              <v-card
                                flat
                                class="d-flex align-center transition-all rounded-lg border-2 "
                                :class="isSelected ? ' border-black' : 'border-neutral-200'"
                                height="50"
                                width="120"
                                @click="toggle"
                              >
                                <v-scroll-y-transition>
                                  <div
                                    class="flex-grow-1 text-center text-md font-medium"
                                  >
                                    {{ $t(country) }}
                                  </div>
                                </v-scroll-y-transition>
                              </v-card>
                            </v-item>
                          </v-col>
                        </div>
                    </v-row>
                  </v-row>
                </v-container>
              </v-item-group>
              <div class="flex justify-center items-center gap-10 my-5">
                <div class="flex justify-center items-center">
                  <v-btn
                      variant="outlined"
                      color='black'
                      class="w-32 text-none rounded-pill"
                      @click="() => changeState('artist')">
                    <span class="font-medium">
                      {{ $t('Previous') }}
                    </span>
                  </v-btn>
                </div>
                <div class="my-5 flex justify-center items-center">
                  <v-btn color='black'
                         class="w-32 text-none rounded-pill text-white"
                         @click="() => changeState('platform')">
                  <span class="font-medium">
                    {{ $t('Next') }}
                  </span>
                  </v-btn>
                </div>
              </div>
            </v-expansion-panel-text>
          </v-expansion-panel>
          <!--  platform panel  -->
          <v-expansion-panel value="platform" class="mb-5" >
            <v-expansion-panel-title v-slot="{ expanded }">
              <v-row no-gutters class="items-center">
                <v-col class="d-flex justify-start" cols="12" lg="4">
                  <span class="text-2xl font-medium">
                    {{ $t('Select Platform') }}
                  </span>
                </v-col>
                <v-col
                  class="items-center lg:block hidden"
                  cols="8"
                >
                  <v-fade-transition >
                    <span
                      v-if="!expanded"
                      key="1"
                      class="text-lg font-medium capitalize"
                    >
                      {{ platform == '' ? '' : platform.map((i) => platforms[i].name).join(' | ') }}
                    </span>
                  </v-fade-transition>
                </v-col>
              </v-row>
            </v-expansion-panel-title>
            <v-expansion-panel-text>
              <v-item-group multiple v-model="platform">
                <v-container class="max-w-screen-md grid md:grid-cols-4 grid-cols-2 gap-5">
                    <div
                      v-for="(p, i) in platforms"
                      :key="i"
                      class="flex justify-center items-center"
                    >
                      <v-item v-slot="{ isSelected, toggle }">
                        <v-card
                          :color="'#FFFFFF'"
                          flat
                          class="flex align-center transition-all rounded-lg border-2 "
                          :class="isSelected ? ' border-black' : 'border-neutral-200'"
                          height="80"
                          width="80"
                          @click="toggle"
                        >
                          <v-scroll-y-transition>
                            <div
                              class="flex-grow-1 text-center"
                            >
                              <v-img
                                :src="p.icon"
                                height="30"
                              ></v-img>
                              <div className="text-xs font-normal mt-2">
                                {{ p.name }}
                              </div>
                            </div>
                            
                          </v-scroll-y-transition>
                        </v-card>
                      </v-item>
                    </div>
                </v-container>
              </v-item-group>
              <div class="flex justify-center items-center gap-10 my-5">
                <div class="flex justify-center items-center">
                  <v-btn
                  variant="outlined"
                  color='black'
                  class="w-32 text-none rounded-pill"
                  @click="() => changeState('region')">
                    <span class="font-medium">
                      {{ $t('Previous') }}
                    </span>
                  </v-btn>
                </div>
                <div class="flex justify-center items-center">
                  <v-btn color='black'
                  class="w-32 text-none rounded-pill text-white"
                  @click="() => changeState('budget')">
                    <span class="font-medium">
                      {{ $t('Next') }}
                    </span>
                  </v-btn>
                </div>
              </div>
            </v-expansion-panel-text>
          </v-expansion-panel>
          <!--  budget panel  -->
          <v-expansion-panel value="budget" class="mb-5" >
            <v-expansion-panel-title v-slot="{ expanded }">
              <v-row no-gutters class="items-center">
                <v-col class="d-flex justify-start" cols="12" lg="4">
                  <span class="text-2xl font-medium">
                    {{ $t('Budget') }}
                  </span>
                </v-col>
                <v-col
                  class="items-center lg:block hidden"
                  cols="8"
                >
                  <v-fade-transition >
                    <span
                      v-if="!expanded"
                      key="1"
                      class="text-lg font-medium capitalize"
                    >
                      {{ budget }}
                    </span>
                  </v-fade-transition>
                </v-col>
              </v-row>

            </v-expansion-panel-title>
            <v-expansion-panel-text>
              <v-container class="max-w-screen-md">
                <div class="text-xl font-medium text-center mb-5">
                  Enter your budget
                </div>
                <v-row>
                  <v-col cols="12">
                    <v-select 
                      class="mx-auto font-sans"
                      bg-color="#FFFFFF"
                      :minWidth="200"
                      :maxWidth="300"
                      label="Budget"
                      :items="budgetRange"
                      variant="outlined"
                      rounded
                      single-line
                      density="compact"
                      v-model="budget"
                      ></v-select>
                  </v-col>
                </v-row>
              </v-container>
              <div class="flex my-5 justify-center items-center gap-10">
                
                  <v-btn
                  variant="outlined"
                  color='black'
                  class="w-32 text-none rounded-pill"
                  @click="() => changeState('platform')">
                    <span class="font-medium">
                      {{ $t('Previous') }}
                    </span>
                  </v-btn>

                  <v-btn color='black'
                  class="w-32 text-none rounded-pill text-white"
                  @click="() => changeState('complete')">
                    <span class="font-medium">
                      {{ $t('Next') }}
                    </span>
                  </v-btn>

              </div>

            </v-expansion-panel-text>
          </v-expansion-panel>
          <!--  post panel  -->
<!--          <v-expansion-panel value="post" class="mb-5" >-->
<!--            <v-expansion-panel-title v-slot="{ expanded }">-->
<!--              <v-row no-gutters class="items-center">-->
<!--                <v-col class="d-flex justify-start" cols="12" lg="4">-->
<!--                  <span class="text-2xl font-medium">-->
<!--                    {{ $t('Post') }}-->
<!--                  </span>-->
<!--                </v-col>-->
<!--              </v-row>-->
<!--            </v-expansion-panel-title>-->
<!--            <v-expansion-panel-text>-->
<!--              <v-container class="max-w-screen-md">-->
<!--                <div class="text-xl font-medium mb-1">-->
<!--                  {{ $t('Title') }}-->
<!--                </div>-->
<!--                <v-text-field-->
<!--                  v-model="post.title"-->
<!--                  variant="outlined"-->
<!--                  rounded="xl"-->
<!--                  dense-->
<!--                  placeholder="Title"-->
<!--                  :rules="[v => !!v || 'Post title is required']"-->
<!--                ></v-text-field>-->
<!--                <div class="text-xl font-medium mb-1">-->
<!--                  {{ $t('Description') }}-->
<!--                </div>-->
<!--                <v-text-field-->
<!--                  v-model="post.description"-->
<!--                  variant="outlined"-->
<!--                  rounded="xl"-->
<!--                  dense-->
<!--                  placeholder="Description"-->
<!--                  :rules="[v => !!v || 'Post description is required']"-->
<!--                ></v-text-field>-->
<!--                <div class="text-xl font-medium mb-1">-->
<!--                  {{ $t('Hashtags') }}-->
<!--                </div>-->
<!--                <v-textarea-->
<!--                    v-model="post.hashtag"-->
<!--                    variant="outlined"-->
<!--                    rounded="xl"-->
<!--                    rows="3"-->
<!--                    dense-->
<!--                    placeholder="Hashtags you want to include in your posts/reels"-->
<!--                    :rules="[v => !!v || 'Post text is required']"-->
<!--                ></v-textarea>-->
<!--                <div class="text-xl font-medium mb-1">-->
<!--                  {{ $t('Content') }}-->
<!--                </div>-->
<!--                <v-textarea-->
<!--                  v-model="post.text"-->
<!--                  variant="outlined"-->
<!--                  rounded="xl"-->
<!--                  rows="3"-->
<!--                  dense-->
<!--                  placeholder="What is on your mind?"-->
<!--                  :rules="[v => !!v || 'Post text is required']"-->
<!--                ></v-textarea>-->
<!--                <div class="text-xl font-medium mb-1">-->
<!--                  {{ $t('URL') }}-->
<!--                </div>-->
<!--                <v-text-field-->
<!--                  v-model="post.url"-->
<!--                  variant="outlined"-->
<!--                  rounded="xl"-->
<!--                  dense-->
<!--                  prepend-inner-icon="mdi-link"-->
<!--                  placeholder="Are there any links you’d like to share with us, for example cloud folders?"-->
<!--                ></v-text-field>-->
<!--                <v-file-input-->
<!--                  v-model="post.file"-->
<!--                  dense-->
<!--                  class="mt-5"-->
<!--                  variant="outlined"-->
<!--                  rounded="xl"-->
<!--                  prepend-inner-icon="mdi-paperclip"-->
<!--                  prepend-icon=""-->
<!--                  placeholder="Upload file"-->
<!--                  label="Attached file"-->
<!--                ></v-file-input>-->
<!--              </v-container>-->
<!--              <div class="my-5 flex justify-center items-center gap-10">-->
<!--                <v-btn-->
<!--                variant="outlined"-->
<!--                color='black'-->
<!--                class="w-32 text-none rounded-pill"-->
<!--                @click="() => changeState('budget')">-->
<!--                  <span class="font-medium">-->
<!--                    {{ $t('Previous') }}-->
<!--                  </span>-->
<!--                </v-btn>-->

<!--                <v-btn color='black'-->
<!--                class="w-32 text-none rounded-pill text-white"-->
<!--                @click="() => changeState('complete')">-->
<!--                  <span class="font-medium">-->
<!--                    {{ $t('Next') }}-->
<!--                  </span>-->
<!--                </v-btn>-->
<!--              </div>-->

<!--            </v-expansion-panel-text>-->
<!--          </v-expansion-panel>-->
          <!--  complete panel  -->
          <v-expansion-panel value="complete" class="mb-5" >
            <v-expansion-panel-title v-slot="{ expanded }">
              <v-row no-gutters class="items-center">
                <v-col class="d-flex justify-start" cols="4">
                  <span class="text-h5">
                    {{ $t('Complete') }}
                  </span>
                </v-col>
              </v-row>
            </v-expansion-panel-title>
            <v-expansion-panel-text>
              <!-- Review all selected data -->
              <v-container class="max-w-screen-md">
                <p class="text-3xl font-medium my-5">
                  {{ $t('Details') }}
                </p>
                <div class="grid lg:grid-cols-4 grid-flow-cols-1 gap-3">
                  <span className="text-lg text-gray-500 col-span-1">
                    <div class="flex items-center gap-2">
                      <Box class="size-4"/>
                      {{ $t('Artist') }}
                    </div>
                  </span>
                  <span class="text-lg col-span-3">
                        {{ selectedArtist.english_name }} ({{ selectedArtist.korean_name }})
                  </span>
                  <span className="text-lg text-gray-500 col-span-1">
                    <div class="flex items-center gap-2">
                      <Globe class="size-4"/>
                      {{ $t('Regions') }}
                    </div>
                  </span>
                  <span class="text-lg col-span-3">
                        {{ region.map((r) => indexToCountry[r]).join(', ') || $t('') }}
                  </span>
                  <span className="text-lg text-gray-500 col-span-1">
                    <div class="flex items-center gap-2">
                      <Share2 class="size-4"/>
                      {{ $t('Platforms') }}
                    </div>
                  </span>
                  <span class="text-lg col-span-3">
                      {{ platform.map((i) => platforms[i].name).join(', ') || $t('') }}
                  </span>
                  <span className="text-lg text-gray-500 col-span-1">
                    <div class="flex items-center gap-2">
                      <DollarSign class="size-4"/>
                      {{ $t('Budget') }}
                    </div>
                  </span>
                  <span class="text-lg col-span-3">
                      {{ budget || $t('') }}
                  </span>
                </div>

<!--                <p class="text-3xl font-medium mb-5 mt-7">-->
<!--                  {{ $t('Post') }}-->
<!--                </p>-->
<!--                <div class="grid lg:grid-cols-4 grid-flow-cols-1 gap-3">-->
<!--                  <span className="text-lg text-gray-500 col-span-1">-->
<!--                    <div class="flex items-center gap-2">-->
<!--                      <Clipboard class="size-4"/>-->
<!--                      {{ $t('Title') }}-->
<!--                    </div>-->
<!--                  </span> -->
<!--                  <span class="text-lg col-span-4">-->
<!--                    {{ post.title || $t('') }}-->
<!--                  </span>-->
<!--                  <span className="text-lg text-gray-500 col-span-1">-->
<!--                    <div class="flex items-center gap-2">-->
<!--                      <Captions class="size-4"/>-->
<!--                      {{ $t('Description') }}-->
<!--                    </div>-->
<!--                  </span> -->
<!--                  <span class="text-lg col-span-4">-->
<!--                    {{ post.description || $t('') }}-->
<!--                  </span>-->
<!--                  <span className="text-lg text-gray-500 col-span-1">-->
<!--                    <div class="flex items-center gap-2">-->
<!--                      <Link class="size-4"/>-->
<!--                      {{ $t('URL') }}-->
<!--                    </div>-->
<!--                  </span>-->
<!--                  <span class="text-lg col-span-4">-->
<!--                    <span v-if="post.url" @click="handleVisit" class="cursor-pointer hover:underline">-->
<!--                      {{ post.url }}-->
<!--                    </span>-->
<!--                    <span class="text-lg" v-else>-->
<!--                      {{ $t('') }}-->
<!--                    </span>-->
<!--                  </span>-->
<!--                  <span className="text-lg text-gray-500 col-span-1">-->
<!--                    <div class="flex items-center gap-2">-->
<!--                      <File class="size-4"/>-->
<!--                      {{ $t('File') }}-->
<!--                    </div>-->
<!--                  </span> -->
<!--                  <span class="text-lg col-span-4">-->
<!--                    {{ post.file ? post.file.name : $t('') }}-->
<!--                  </span>-->
<!--                  <span className="text-lg text-gray-500 mt-2">-->
<!--                    <div class="flex items-center gap-2">-->
<!--                      <FileTextIcon class="size-4"/>-->
<!--                      {{ $t('Content') }}-->
<!--                    </div>-->
<!--                  </span> -->
<!--                  <v-textarea rows="2" rounded="xl" auto-grow variant="outlined" :model-value="post.text || $t('')" class="text-lg col-span-5" readonly>-->
<!--                  </v-textarea>-->

<!--                </div>-->
              </v-container>

              <div class="flex justify-center items-center gap-10">
                
                <div class="my-5 flex
                justify-center items-center gap-10">
                  <v-btn
                  variant="outlined"
                  color='black'
                  class="w-32 text-none rounded-pill "
                  @click="() => changeState('budget')">
                    <span class="font-medium">
                      {{ $t('Previous') }}
                    </span>
                  </v-btn>
                  <v-btn color='black'
                  class="w-32 text-none rounded-pill text-white"
                  @click="onSubmitted">
                    <span class="font-medium">
                      {{ $t('Submit') }}
                    </span>
                  </v-btn>
                </div>
              </div>
            </v-expansion-panel-text>
          </v-expansion-panel>

        </v-expansion-panels>
        </v-card-text>

      </v-card>

    </v-container>
</template>

<style scoped>
  .hover\:force-rounded-xl:hover {
    border-radius: 1.5rem !important;
    /* transform: scale(1.1); */
  }
</style>

