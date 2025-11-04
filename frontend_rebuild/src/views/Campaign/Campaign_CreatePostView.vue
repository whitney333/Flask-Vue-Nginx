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
    import axios from '@/axios';
    import { useRouter } from 'vue-router';

    const router = useRouter()
    const artistStore = useArtistStore()

    const userStore = useUserStore()
    const followedArtists = userStore.followedArtists
    const selectedArtist = ref(null)

    const platform = ref([])
    const post = ref({
      title: '',
      description: '',
      hashtag: [],
      url: '',
    })

    const platforms = [
      { name: "Instagram", icon: instagramIcon, color: "#FF0069", blackIcon: instagramBlackIcon },
      { name: "Tiktok", icon: tiktokIcon, color: "#000000", blackIcon: tiktokBlackIcon },
      { name: "Youtube", icon: youtubeIcon, color: "#FF0000", blackIcon: youtubeBlackIcon },
      { name: "Rednote", icon: xiaohongshuIcon, color: "#FF2442", blackIcon: xiaohongshuBlackIcon},
      { name: "Bilibili", icon: bilibiliIcon, color: "#00A1D6", blackIcon: bilibiliBlackIcon },
    ]

    const addHashtag = (event) => {
      const value = event.target.value.trim()
      if (value && !post.value.hashtag.includes(value)) {
        const formatted = value.startsWith('#') ? value : `#${value}`
        post.value.hashtag.push(formatted)
      }
      event.target.value = ''
    }

    const snackbar = ref({
      show: false,
      text: "",
      color: "green",
    });
    const campaign_init_status = "submitted"
    const loading = ref(false)
    const region = ref([])
    // default expand the artist panel
    const state = ref('artist')
    const budgetRange = ['Less than US$100', 'US$100 - US$1,000', 'US$1,000 - US$5,000', 'US$5,000 - US$10,000', 'More than US$10,000']
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
        firebase_id: userStore.firebase_id,
        email: userStore.email,
        artist: selectedArtist.value,
        region: region.value.map((r) => indexToCountry[r]),
        platform: platform.value.map((i) => platforms[i].name),
        budget: budget.value,
        // post: post.value,
      });
    }

    const submitCampaign = async () => {
      try {
        const data = {
          firebase_id: userStore.firebase_id,
          email: userStore.email,
          artist_id: selectedArtist.value.artist_id,
          artist_en_name: selectedArtist.value.english_name,
          artist_kr_name: selectedArtist.value.korean_name,
          region: region.value.map((r) => indexToCountry[r]),
          platform: platform.value.map((i) => platforms[i].name),
          budget: budget.value,
          info: post.value,
          status: campaign_init_status
        }
        // console.log("cp: ", data)
        const res = await axios.post(
            "/campaign/v1/create",
            data,
            {
              headers: {
                "Authorization": `Bearer ${userStore.firebaseToken}`,
                "Content-Type": "application/json"
              }
            }
        )
        // created success
        snackbar.value.text = "Campaign created successfully!";
        snackbar.value.color = "green";
        snackbar.value.show = true;

        setTimeout(() => {
          router.push("/campaign/posts");
        }, 2000);
      } catch (err) {
        // create failed
        snackbar.value.text = "Failed to create campaign!";
        snackbar.value.color = "red";
        snackbar.value.show = true;
      }
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
            {{ $t('campaign.create_your_post') }}
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
                    {{ $t('campaign.select_artist') }}
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
                      {{ $t('campaign.next') }}
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
                    {{ $t('campaign.select_region') }}
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
                      {{ region == '' ? '' :  region.map((r) => $t(`\country.${indexToCountry[r]}`)).join(' | ')}}
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
                          {{ $t(`country.${reg}`) }}
                        </span>
                      </v-col>
                      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5">
                          <v-col
                            v-for="(_country, j) in regions[reg]"
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
                                    {{ $t(`country.${_country}`) }}
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
                      {{ $t('campaign.previous') }}
                    </span>
                  </v-btn>
                </div>
                <div class="my-5 flex justify-center items-center">
                  <v-btn color='black'
                         class="w-32 text-none rounded-pill text-white"
                         @click="() => changeState('platform')">
                  <span class="font-medium">
                    {{ $t('campaign.next') }}
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
                    {{ $t('campaign.select_platform') }}
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
                      {{ platform == '' ? '' : platform.map((i) => $t(`\sns.${platforms[i].name}`)).join(' | ') }}
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
                      {{ $t('campaign.previous') }}
                    </span>
                  </v-btn>
                </div>
                <div class="flex justify-center items-center">
                  <v-btn color='black'
                  class="w-32 text-none rounded-pill text-white"
                  @click="() => changeState('budget')">
                    <span class="font-medium">
                      {{ $t('campaign.next') }}
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
                    {{ $t('campaign.budget') }}
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
                  {{ $t("campaign.enter_your_budget") }}
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
                      {{ $t('campaign.previous') }}
                    </span>
                  </v-btn>

                  <v-btn color='black'
                  class="w-32 text-none rounded-pill text-white"
                  @click="() => changeState('post')">
                    <span class="font-medium">
                      {{ $t('campaign.next') }}
                    </span>
                  </v-btn>

              </div>

            </v-expansion-panel-text>
          </v-expansion-panel>
          <!--  post panel  -->
          <v-expansion-panel value="post" class="mb-5" >
            <v-expansion-panel-title v-slot="{ expanded }">
              <v-row no-gutters class="items-center">
                <v-col class="d-flex justify-start" cols="12" lg="4">
                  <span class="text-2xl font-medium">
                    {{ $t('campaign.post') }}
                  </span>
                </v-col>
              </v-row>
            </v-expansion-panel-title>
            <v-expansion-panel-text>
              <v-container class="max-w-screen-md">
                <div class="text-xl font-medium mb-1">
                  {{ $t('campaign.title') }}
                </div>
                <v-text-field
                  v-model="post.title"
                  variant="outlined"
                  rounded="xl"
                  dense
                  placeholder="Title"
                  :rules="[v => !!v || 'Post title is required']"
                ></v-text-field>
                <div class="text-xl font-medium mb-1">
                  {{ $t('campaign.description') }}
                </div>
                <v-text-field
                  v-model="post.description"
                  variant="outlined"
                  rounded="xl"
                  dense
                  placeholder="Description"
                  :rules="[v => !!v || 'Post description is required']"
                ></v-text-field>
                <div class="text-xl font-medium mb-1">
                  {{ $t('campaign.hashtags') }}
                </div>
<!--                <v-textarea-->
<!--                    v-model="post.hashtag"-->
<!--                    variant="outlined"-->
<!--                    rounded="xl"-->
<!--                    rows="3"-->
<!--                    dense-->
<!--                    placeholder="Hashtags you want to include in your posts/reels"-->
<!--                    :rules="[v => !!v || 'Hashtags are required']"-->
<!--                ></v-textarea>-->
                <v-combobox
                    v-model="post.hashtag"
                    variant="outlined"
                    rounded="xl"
                    multiple
                    chips
                    deletable-chips
                    clearable
                    placeholder="Press Enter to add hashtag"
                    :rules="[v => v.length > 0 || 'At least one hashtag required']"
                    @keydown.enter.prevent="addHashtag"
                ></v-combobox>
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
                <div class="text-xl font-medium mb-1">
                  {{ $t('campaign.url') }}
                </div>
                <v-text-field
                  v-model="post.url"
                  variant="outlined"
                  rounded="xl"
                  dense
                  prepend-inner-icon="mdi-link"
                  placeholder="Are there any links you’d like to share with us, for example cloud folders?"
                ></v-text-field>
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
              </v-container>
              <div class="my-5 flex justify-center items-center gap-10">
                <v-btn
                variant="outlined"
                color='black'
                class="w-32 text-none rounded-pill"
                @click="() => changeState('budget')">
                  <span class="font-medium">
                    {{ $t('campaign.previous') }}
                  </span>
                </v-btn>

                <v-btn color='black'
                class="w-32 text-none rounded-pill text-white"
                @click="() => changeState('complete')">
                  <span class="font-medium">
                    {{ $t('campaign.next') }}
                  </span>
                </v-btn>
              </div>

            </v-expansion-panel-text>
          </v-expansion-panel>
          <!--  complete panel  -->
          <v-expansion-panel value="complete" class="mb-5" >
            <v-expansion-panel-title v-slot="{ expanded }">
              <v-row no-gutters class="items-center">
                <v-col class="d-flex justify-start" cols="4">
                  <span class="text-h5">
                    {{ $t('campaign.complete') }}
                  </span>
                </v-col>
              </v-row>
            </v-expansion-panel-title>
            <v-expansion-panel-text>
              <!-- Review all selected data -->
              <v-container class="max-w-screen-md">
                <p class="text-3xl font-medium my-5">
                  {{ $t('campaign.details') }}
                </p>
                <div class="grid lg:grid-cols-4 grid-flow-cols-1 gap-3">
                  <span className="text-lg text-gray-500 col-span-1">
                    <div class="flex items-center gap-2">
                      <Box class="size-4"/>
                      {{ $t('campaign.artist') }}
                    </div>
                  </span>
                  <span class="text-lg col-span-3">
                        {{ selectedArtist.english_name }} ({{ selectedArtist.korean_name }})
                  </span>
                  <span className="text-lg text-gray-500 col-span-1">
                    <div class="flex items-center gap-2">
                      <Globe class="size-4"/>
                      {{ $t('campaign.regions') }}
                    </div>
                  </span>
                  <span class="text-lg col-span-3">
                        {{ region.map((r) => $t(indexToCountry[r])).join(', ') || $t('') }}
                  </span>
                  <span className="text-lg text-gray-500 col-span-1">
                    <div class="flex items-center gap-2">
                      <Share2 class="size-4"/>
                      {{ $t('campaign.platforms') }}
                    </div>
                  </span>
                  <span class="text-lg col-span-3">
                      {{ platform.map((i) => $t(platforms[i].name)).join(', ') || $t('') }}
                  </span>
                  <span className="text-lg text-gray-500 col-span-1">
                    <div class="flex items-center gap-2">
                      <DollarSign class="size-4"/>
                      {{ $t('campaign.budget') }}
                    </div>
                  </span>
                  <span class="text-lg col-span-3">
                      {{ budget || $t('') }}
                  </span>
                </div>

                <p class="text-3xl font-medium mb-5 mt-7">
                  {{ $t('campaign.post') }}
                </p>
                <div class="grid lg:grid-cols-4 grid-flow-cols-1 gap-3">
                  <span className="text-lg text-gray-500 col-span-1">
                    <div class="flex items-center gap-2">
                      <Clipboard class="size-4"/>
                      {{ $t('campaign.title') }}
                    </div>
                  </span>
                  <span class="text-lg col-span-4">
                    {{ post.title || $t('') }}
                  </span>
                  <span className="text-lg text-gray-500 col-span-1">
                    <div class="flex items-center gap-2">
                      <Captions class="size-4"/>
                      {{ $t('campaign.description') }}
                    </div>
                  </span>
                  <span class="text-lg col-span-4">
                    {{ post.description || $t('') }}
                  </span>
                  <span className="text-lg text-gray-500 col-span-1">
                    <div class="flex items-center gap-2">
                      <Captions class="size-4"/>
                      {{ $t('campaign.hashtags') }}
                    </div>
                  </span>
                  <span class="text-lg col-span-4">
                    {{ post.hashtag || $t('') }}
                  </span>
                  <span className="text-lg text-gray-500 col-span-1">
                    <div class="flex items-center gap-2">
                      <Link class="size-4"/>
                      {{ $t('campaign.url') }}
                    </div>
                  </span>
                  <span class="text-lg col-span-4">
                    <span v-if="post.url" @click="handleVisit" class="cursor-pointer hover:underline">
                      {{ post.url }}
                    </span>
                    <span class="text-lg" v-else>
                      {{ $t('') }}
                    </span>
                  </span>
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

                </div>
              </v-container>

              <div class="flex justify-center items-center gap-10">
                
                <div class="my-5 flex
                justify-center items-center gap-10">
                  <v-btn
                  variant="outlined"
                  color='black'
                  class="w-32 text-none rounded-pill "
                  @click="() => changeState('post')">
                    <span class="font-medium">
                      {{ $t('campaign.previous') }}
                    </span>
                  </v-btn>
                  <v-btn color='black'
                    class="w-32 text-none rounded-pill text-white"
                    @click="submitCampaign"
                    :loading="loading"
                  >
                    <span v-if="!loading" class="font-medium">
                      {{ $t('campaign.submit') }}
                    </span>
                  </v-btn>
                </div>
              </div>
            </v-expansion-panel-text>
          </v-expansion-panel>

        </v-expansion-panels>
        </v-card-text>

      </v-card>
      <v-snackbar
          v-model="snackbar.show"
          :timeout="5000"
          :color="snackbar.color"
          class="text-white"
          location="top"
      >
        {{ snackbar.text }}
      </v-snackbar>
    </v-container>
</template>

<style scoped>
  .hover\:force-rounded-xl:hover {
    border-radius: 1.5rem !important;
    /* transform: scale(1.1); */
  }
</style>

