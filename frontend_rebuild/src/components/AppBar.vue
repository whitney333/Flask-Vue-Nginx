<script setup>
import { useRoute, useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n'
import { ref, computed } from 'vue';
import { useUserStore } from "@/stores/user"
import { useArtistStore } from '@/stores/artist'
import { useDisplay } from 'vuetify'
import LangSwitcher from "@/components/LangSwitcher.vue"
const { mdAndUp } = useDisplay()


const { t } = useI18n({ useScope: 'global' })
const props = defineProps({
    isLoggedIn: Boolean,
    handleSignOut: Function,
    drawer: { type: Boolean, required: true }
})
defineEmits(["toggle-drawer"])

const userStore = useUserStore()
const artistStore = useArtistStore()
const route = useRoute()
const router = useRouter()

const handleRegister = () => {
  router.push('/auth/register')
}

function selectArtist(artistId) {
  if (!artistId) return
  artistStore.setArtistId(artistId)
}

const getArtistId = (artist) => artist?.id || artist?.artist_id || artist?._id || artist?.artist_objId || null
const getArtistImage = (artist) => artist?.image || artist?.imageURL || ""
const getArtistEnglishName = (artist) => artist?.english_name || artist?.artist_name || "Artist"
const getArtistKoreanName = (artist) => artist?.korean_name || ""

const followedArtists = computed(() => userStore.followedArtists || []);
const selectedArtist = computed(() => {
  const currentArtistId = artistStore.artistId
  if (!currentArtistId) return null
  return followedArtists.value?.find((artist) => String(getArtistId(artist)) === String(currentArtistId)) || null
})

</script>

<template>
  <v-app-bar app :elevation="1" style="padding: 0px 20px;">

    <v-app-bar-nav-icon class="d-md-none" @click="$emit('toggle-drawer')" />

    <v-app-bar-title class="text-h6 text-md-h5">
      {{ route.name }}
    </v-app-bar-title>

    <template #append>
      <template v-if="mdAndUp">

        <LangSwitcher icon-only />

        <v-menu>
          <template #activator="{ props }">
            <v-btn v-bind="props" class="text-none" :icon="!selectedArtist">
              <v-avatar v-if="getArtistImage(selectedArtist)" size="28" class="mr-2">
                <v-img :src="getArtistImage(selectedArtist)" :alt="getArtistEnglishName(selectedArtist)" cover />
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
              <v-list-item-title>{{ getArtistEnglishName(artist) }}</v-list-item-title>
              <v-list-item-subtitle>{{ getArtistKoreanName(artist) }}</v-list-item-subtitle>
            </v-list-item>
          </v-list>
          <v-list v-else>
            <v-list-item><v-list-item-title>No followed artists</v-list-item-title></v-list-item>
          </v-list>
        </v-menu>

      </template>

      <v-menu v-if="isLoggedIn">
        <template #activator="{ props }">
          <v-btn v-bind="props" icon="mdi-account" />
        </template>
        <v-list density="compact">
          <router-link to="/profile" style="text-decoration:none;color:inherit;">
            <v-list-item prepend-icon="mdi-account"><v-list-item-title>Profile</v-list-item-title></v-list-item>
          </router-link>
          <v-list-item prepend-icon="mdi-logout" @click="handleSignOut()"><v-list-item-title>Log out</v-list-item-title></v-list-item>
        </v-list>
      </v-menu>

      <v-tooltip v-else>
        <template #activator="{ props }">
          <v-btn v-bind="props" icon="mdi-account-plus" @click="handleRegister" />
        </template>
        <span>Register</span>
      </v-tooltip>
    </template>
  </v-app-bar>
</template>
