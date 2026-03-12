<script setup>
import { useRoute, useRouter } from 'vue-router';
import getUnicodeFlagIcon from 'country-flag-icons/unicode'
import { useI18n } from 'vue-i18n'
import {ref, watch, defineEmits, computed, reactive, onMounted} from 'vue';
import { useUserStore } from "@/stores/user"
import { useArtistStore } from '@/stores/artist'
import {getAuth} from "firebase/auth";
import axios from "@/axios.js";

const { t, locale } = useI18n({ useScope: 'global' })
const props = defineProps({
    isLoggedIn: Boolean,
    handleSignOut: Function,
    drawer: { type: Boolean, required: true }
})
defineEmits(["toggle-drawer"])


// init user data & followed_artist ids
const userStore = useUserStore()
const artistStore = useArtistStore()

const route = useRoute()
const router = useRouter()
const countriesFlag = {
    'South Korea': 'KR',
    'United Kingdom': 'GB',
}
const lang = ref('en')

const languages = [
    {
        value: 'en',
        title: `${getUnicodeFlagIcon(countriesFlag['United Kingdom'])} English`
    },
    {
        value: 'kr',
        title: `${getUnicodeFlagIcon(countriesFlag['South Korea'])} Korean`,
    }]

    const handleRegister = () => {
        router.push('/auth/register')
    }
    watch(lang, () => {
        locale.value = lang.value[0]
    })

    const fetchUserProfile = () => {
        router.push("/profile")
    }

    function selectArtist(artistId) {
      if (!artistId) return
      // update artist id
      artistStore.setArtistId(artistId)
      console.log("cur: ", artistId)
    }

    const getArtistId = (artist) => {
      if (!artist) return null
      return artist.id || artist.artist_id || artist._id || artist.artist_objId || null
    }
    const getArtistImage = (artist) => artist?.image || artist?.imageURL || ""
    const getArtistEnglishName = (artist) => artist?.english_name || artist?.artist_name || "Artist"
    const getArtistKoreanName = (artist) => artist?.korean_name || ""

    const followedArtists = computed(() =>
        userStore.followedArtists
    );

    const selectedArtist = computed(() => {
      const currentArtistId = artistStore.artistId
      if (!currentArtistId) return null
      return followedArtists.value?.find((artist) =>
          String(getArtistId(artist)) === String(currentArtistId)) || null
    })

    // console.log(userStore.followedArtists)
    watch(() => userStore.followedArtists, (val) => {
      console.log("AppBar followedArtists:", val)
    })


</script>

<template>
    <v-app-bar :elevation="1" app :style="{ padding: '0px 20px' }">
      <!-- display  hamburger menu in mobile version -->
      <v-app-bar-nav-icon
           class="d-md-none"
           @click="$emit('toggle-drawer')"
      />
      <v-app-bar-title class="text-h5">{{ route.name }}</v-app-bar-title>
      <!-- display in desktop version -->
      <template v-slot:append>

            <v-menu>
                <template v-slot:activator="{ props }">
                    <v-btn v-bind="props" icon="mdi-translate"></v-btn>
                </template>
                <v-list
                v-model:selected="lang"
                >
                    <v-list-item
                    v-for="(language, index) in languages"
                    :key="index"
                    :value="language.value"
                    >
                    <v-list-item-title>{{ language.title }}</v-list-item-title>
                    </v-list-item>
                </v-list>
            </v-menu>
            <!--  User followed artists list -->
            <v-menu>
              <template v-slot:activator="{ props }">
                <v-btn v-bind="props" :icon="!selectedArtist" class="text-none">
                  <v-avatar v-if="getArtistImage(selectedArtist)" size="28" class="mr-2">
                    <v-img :src="getArtistImage(selectedArtist)" :alt="getArtistEnglishName(selectedArtist) || 'artist avatar'" cover />
                  </v-avatar>
                  <v-icon v-else>mdi-heart-circle</v-icon>
                  <div v-if="selectedArtist" class="d-flex flex-column align-start justify-center">
                    <span class="text-body-2 font-weight-medium">{{ getArtistEnglishName(selectedArtist) }}</span>
                    <span class="text-caption text-grey">{{ getArtistKoreanName(selectedArtist) }}</span>
                  </div>
                </v-btn>
              </template>
              <v-list v-if="followedArtists.length > 0">
                <v-list-item
                    v-for="artist in followedArtists"
                    :key="getArtistId(artist)"
                    :prepend-avatar="getArtistImage(artist)"
                    @click="selectArtist(getArtistId(artist))"
                >
                <v-list-item-title class="text-body-1 font-weight-medium">
                  {{ getArtistEnglishName(artist) }}
                </v-list-item-title>
                <v-list-item-subtitle class="text-grey">
                  {{ getArtistKoreanName(artist) }}
                </v-list-item-subtitle>
                </v-list-item>
              </v-list>
              <v-list v-else>
                <v-list-item>
                  <v-list-item-title>No followed artists</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
            <v-menu v-if="isLoggedIn">
                <template v-slot:activator="{ props }">
                    <v-btn v-bind="props" icon="mdi-account"></v-btn>
                </template>
                <v-list density="compact" >
                  <router-link to="/profile" style="text-decoration: none; color: inherit;">
                  <v-list-item
                      prepend-icon="mdi-account">
                    <v-list-item-title >Profile</v-list-item-title>
                  </v-list-item>
                  </router-link>
                    <v-list-item
                        @click="handleSignOut()"  
                        prepend-icon="mdi-logout">
                        <v-list-item-title >Log out</v-list-item-title>
                    </v-list-item>
                </v-list>
            </v-menu>
            <v-tooltip v-else="isLoggedIn">
                <template v-slot:activator="{ props }">
                    <v-btn @click="handleRegister" v-bind="props" icon="mdi-account-plus"></v-btn>
                </template>
                <span>Register</span>
            </v-tooltip>
        </template>
    </v-app-bar>
</template>


