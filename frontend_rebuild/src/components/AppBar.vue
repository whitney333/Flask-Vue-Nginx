<script setup>
import { useRoute, useRouter } from 'vue-router';
import LangSwitcher from './LangSwitcher.vue'
import getUnicodeFlagIcon from 'country-flag-icons/unicode'
import { useI18n } from 'vue-i18n'
import {ref, watch, computed, reactive, onMounted} from 'vue';
import { useUserStore } from "@/stores/user"
import { useArtistStore } from '@/stores/artist'
import {getAuth} from "firebase/auth";
import axios from "@/axios.js";


const { t, locale } = useI18n({ useScope: 'global' })
const props = defineProps({
    isLoggedIn: Boolean,
    handleSignOut: Function
})

// init user data & followed_artist ids
const userStore = useUserStore()
const artistStore = useArtistStore()

const route = useRoute()
const router = useRouter()
const countriesFlag = {
    'Hong Kong': 'HK',
    'Japan': 'JP',
    'South Korea': 'KR',
    'United Kingdom': 'GB',
}
const lang = ref('en')

const languages = [
    {
        lang: 'English',
        value: 'en',
        title: `${getUnicodeFlagIcon(countriesFlag['United Kingdom'])} English`
    },
    {
        lang: '한국어',
        value: 'kr',
        title: `${getUnicodeFlagIcon(countriesFlag['South Korea'])} 한국어`,
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
      // update artist id
      artistStore.setMid(artistId)
      // console.log("cur: ", artistId)
    }
    const followedArtists = computed(() => userStore.followedArtists);
    // console.log(userStore.followedArtists)
    watch(() => userStore.followedArtists, (val) => {
      console.log("AppBar followedArtists:", val)
    })


</script>

<template>
    <v-app-bar :elevation="1" app :style="{ padding: '0px 20px' }">        
        <v-app-bar-title class="text-h5">{{ route.name }}</v-app-bar-title>
        <template v-slot:append>
            <v-menu>
                <template v-slot:activator="{ props }">
                    <v-btn v-bind="props" icon="mdi-web"></v-btn>
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
                <v-btn v-bind="props" icon="mdi-heart-circle"></v-btn>
              </template>
              <v-list v-if="followedArtists.length > 0">
                <v-list-item
                    v-for="artist in followedArtists"
                    :key="artist.artist_id"
                    :prepend-avatar="artist.image"
                    @click="selectArtist(artist.artist_id)"
                >
                <v-list-item-title class="text-body-1 font-weight-medium">
                  {{ artist.english_name }}
                </v-list-item-title>
                <v-list-item-subtitle class="text-grey">
                  {{ artist.korean_name }}
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
