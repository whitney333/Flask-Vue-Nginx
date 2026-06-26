<script setup>
import {ref, watch, computed} from 'vue'
import {useRouter} from 'vue-router'
import {useDisplay} from 'vuetify'
import LangSwitcher from "@/components/LangSwitcher.vue"
import {useUserStore} from "@/stores/user.js"
import {useArtistStore} from "@/stores/artist.js"

const mishkanIcon = "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/sidebar_logo.svg"

const props = defineProps({
  modelValue: Boolean
})

const emit = defineEmits(['update:modelValue'])

const drawer = ref(props.modelValue)
const opened = ref([])

const router = useRouter()
const userStore = useUserStore()
const artistStore = useArtistStore()
const display = useDisplay()

const items = ref([
  {
    key: 'dashboard',      // add only key
    title: 'menu.dashboard',
    icon: 'mdi-view-dashboard',
    to: '/dashboard',
    hasSublinks: false,
  },
  {
    key: 'sns',            // add only key
    title: 'menu.sns',
    icon: 'mdi-account-multiple',
    to: '/sns',
    hasSublinks: true,
    sublinks: [
      {key: 'instagram', title: 'sns.instagram', icon: 'mdi-instagram', to: '/sns/instagram'},
      {key: 'tiktok', title: 'sns.tiktok', icon: 'mdi-music-box', to: '/sns/tiktok'},
      {key: 'youtube', title: 'sns.youtube', icon: 'mdi-youtube', to: '/sns/youtube'},
      {key: 'bilibili', title: 'sns.bilibili', icon: 'mdi-movie-filter', to: '/sns/bilibili'}
    ]
  },
  {
    key: 'works',
    title: 'menu.works',
    icon: 'mdi-creation',
    to: '/works',
    hasSublinks: true,
    sublinks: [
      {key: 'music', title: 'menu.music', icon: 'mdi-music-box', to: '/works/music'}
    ]
  },
  {
    key: 'campaign',
    title: 'menu.campaign',
    icon: 'mdi-comment-processing',
    to: '/campaign',
    hasSublinks: true,
    sublinks: [
      {key: 'analytics', title: 'menu.analytics', icon: 'mdi-poll', to: '/campaign/analytics'},
      {key: 'posts', title: 'menu.posts', icon: 'mdi-post', to: '/campaign/posts'}
    ]
  },
  {
    key: 'trending-artists',
    title: 'menu.trending_artist',
    icon: 'mdi-trending-up',
    to: '/trending-artists',
    hasSublinks: false,
  }
])


// add key attributes to each item
watch(
    () => userStore.admin,
    (isAdmin) => {
      // find items using key
      if (isAdmin && !items.value.find(i => i.key === 'admin-manage')) {
        items.value.push({
          key: 'admin-manage',
          title: 'menu.admin_manage',
          icon: 'mdi-shield-account',
          to: '/admin',
          hasSublinks: true,
          sublinks: [
            {key: 'tenants', title: 'menu.tenants', icon: 'mdi-domain', to: '/admin/tenants'},
            {key: 'users', title: 'menu.users', icon: 'mdi-account-cog', to: '/admin/users'},
            {key: 'artists', title: 'menu.artists', icon: 'mdi-star-box', to: '/admin/artists'},
            {key: 'campaigns', title: 'menu.campaigns', icon: 'mdi-file-table-box-outline', to: '/admin/campaigns'},
            {key: 'dramas', title: 'menu.dramas', icon: 'mdi-movie-open-outline', to: '/admin/dramas'}
          ]
        })
      }
    },
    {immediate: true}
)


// sync v-model
watch(() => props.modelValue, (val) => {
  drawer.value = val
})

watch(drawer, (val) => {
  emit('update:modelValue', val)
})


// ===== Artists =====
const followedArtists = computed(() => userStore.followedArtists || [])

const getArtistId = (a) =>
    a?.id || a?.artist_id || a?._id || a?.artist_objId

const getArtistImage = (a) =>
    a?.image || a?.imageURL || ''

const getArtistName = (a) =>
    a?.english_name || a?.artist_name || 'Artist'

const selectArtist = (id) => {
  if (!id) return
  artistStore.setArtistId(id)

  // close drawer on mobile
  if (display.smAndDown.value) {
    drawer.value = false
  }
}

const handleToHomePage = () => {
  router.push('/dashboard')
}
</script>

 <template>
  <v-navigation-drawer
    v-model="drawer"
    app
    class="app-drawer"
    :rail="display.mdAndUp.value"
    :temporary="display.smAndDown.value"
    mobile-breakpoint="960"
    expand-on-hover
    color="#212121"
  >
    <div class="d-flex flex-column h-100">

      <v-list class="flex-shrink-0">
        <v-list-item>
          <div @click="handleToHomePage" class="svg-container">
            <img :src="mishkanIcon" class="clipped-svg" />
          </div>
        </v-list-item>
      </v-list>

      <v-divider />

      <div class="drawer-content flex-grow-1">
        <v-list
            density="compact"
            nav
            :opened="opened"
            @update:opened="val => opened = val.slice(-1)"
        >
          <template v-for="item in items" :key="item.key">

            <v-list-item
                v-if="!item.hasSublinks"
                :prepend-icon="item.icon"
                :title="$t(item.title)"
                :to="item.to"
                link
            />

            <v-list-group
                v-else
                :value="item.key"
            >
              <template #activator="{ props }">
                <v-list-item
                    v-bind="props"
                    :prepend-icon="item.icon"
                    :title="$t(item.title)"
                />
              </template>

              <v-list-item
                  v-for="sub in item.sublinks"
                  :key="sub.key"
                  :prepend-icon="sub.icon"
                  :title="$t(sub.title)"
                  :to="sub.to"
                  link
              />
            </v-list-group>

          </template>
        </v-list>
      </div>

      <div v-if="display.smAndDown.value" class="drawer-bottom flex-shrink-0">
        <v-divider class="my-2"/>

        <div class="px-4 pb-2 text-caption text-grey">
          Followed Artists
        </div>

        <v-list density="compact" nav max-height="200" style="overflow-y: auto;">
          <v-list-item
              v-for="artist in followedArtists"
              :key="getArtistId(artist)"
              @click="selectArtist(getArtistId(artist))"
          >
            <template #prepend>
              <v-avatar size="28">
                <v-img :src="getArtistImage(artist)" cover/>
              </v-avatar>
            </template>
            <v-list-item-title>{{ getArtistName(artist) }}</v-list-item-title>
          </v-list-item>
        </v-list>

        <v-divider class="my-2"/>

        <div class="px-4 py-3">
          <LangSwitcher/>
        </div>
      </div>

    </div>
  </v-navigation-drawer>
</template>

<style scoped>
.app-drawer :deep(.v-navigation-drawer__content) {
  height: 100% !important;
  display: flex !important;
  flex-direction: column !important;
}

.drawer-content {
  overflow-y: auto;
}

.drawer-bottom {
  background-color: #212121;
  padding-bottom: calc(env(safe-area-inset-bottom) + 16px) !important; /* 防止 iOS 底部白條遮擋 */
}

.svg-container {
  width: 200px;
  height: 50px;
  overflow: hidden;
  cursor: pointer;
}

.clipped-svg {
  width: 150px;
  height: 50px;
  object-fit: cover;
  transform: scale(0.7) translate(-31px, 0px);
}
</style>
