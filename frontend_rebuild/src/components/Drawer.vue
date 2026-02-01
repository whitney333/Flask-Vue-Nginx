<script setup>
  import { ref, watch, defineEmits } from 'vue';
  import { useRouter } from 'vue-router';
  import { useDisplay } from 'vuetify'
  import LangSwitcher from "@/components/LangSwitcher.vue";
  import { useUserStore } from "@/stores/user.js";


  const mishkanIcon = "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/sidebar_logo.svg"

  const props = defineProps({
    modelValue: Boolean
  })
  const emit = defineEmits(['update:modelValue'])
  const drawer = ref(props.modelValue)
  const rail = ref(true)
  const isHovered = ref(false);
  const router = useRouter()
  const opened = ref([])
  const userStore = useUserStore()

  const items = ref(
    [
      {
        title:'Dashboard',
        icon:'mdi-view-dashboard',
        to:'/dashboard',
        hasSublinks: false,
        isOpen: false,
      },
      {
        title: 'SNS',
        icon: 'mdi-account-multiple',
        to: '/sns',
        hasSublinks: true,
        isOpen: false,
        sublinks: [
        {
          title: 'Instagram',
          icon: 'mdi-instagram',
          to: '/sns/instagram',
        },
        {
          title: 'Tiktok',
          icon: 'mdi-music-box',
          to: '/sns/tiktok',
        },
        {
          title: 'Youtube',
          icon: 'mdi-youtube',
          to: '/sns/youtube',
        },
        {
          title: 'Bilibili',
          icon: 'mdi-movie-filter',
          to: '/sns/bilibili',
        },
        ]
      },
      {
        title: 'Works',
        icon: 'mdi-creation',
        to: '/works',
        hasSublinks: true,
        isOpen: false,
        sublinks:[
          {
            title: 'Music',
            icon: 'mdi-music-box',
            to: '/works/music'
          }
        ]
      },
      {
        title:'Campaign',
        icon:'mdi-comment-processing',
        to:'/campaign',
        hasSublinks: true,
        isOpen: false,
        sublinks: [
          {
            title: 'Analytics',
            icon: 'mdi-poll',
            to: '/campaign/analytics',
            active: true
          },
          {
            title: 'Posts',
            icon: 'mdi-post',
            to: '/campaign/posts',
            active: true
          }
        ]
      },
      {
        title:'Trending Artists',
        icon:'mdi-trending-up',
        to:'/trending-artists',
        hasSublinks: false,
        isOpen: false,
      }
    ],
  )


  watch(
      () => userStore.admin,
      (isAdmin) => {
        if (isAdmin === true) {
          const exists = items.value.some(i => i.title === 'Admin Manage')
          if (!exists) {
            items.value.push({
              title: 'Admin Manage',
              icon: 'mdi-shield-account',
              to: '/admin',
              hasSublinks: true,
              isOpen: false,
              sublinks: [
                {
                  title: 'Tenants',
                  icon: 'mdi-domain',
                  to: '/admin/tenants'
                },
                {
                  title: 'User',
                  icon: 'mdi-account-cog',
                  to: '/admin/users'
                },
                {
                  title: 'Artist',
                  icon: 'mdi-star-box',
                  to: '/admin/artists'
                },
                {
                  title: 'Campaigns',
                  icon: 'mdi-file-table-box-outline',
                  to: '/admin/campaigns'
                }
              ]
            });
          }
        }
      },
      {immediate: true}
  )


  watch(() => props.modelValue, (val) => {
    drawer.value = val
  })
  watch(drawer, (val) => {
    emit('update:modelValue', val)
  })

  const display = useDisplay()

  const handleMouseEnter = () => {
    isHovered.value = true;
  };

  const handleMouseLeave = () => {
    isHovered.value = false;
  };

  const handleToHomePage = () => {
    router.push({path: "/dashboard"})
  }

  const onDrawerToggle = (val) => {
    if (!val) {
      items.value.forEach((item) => item.isOpen = false)
      console.log("///onDrawerToggle: Active!");
    }
  }

</script>

 <template>
      <v-navigation-drawer
        fill-height
        mobile-breakpoint="960"
        expand-on-hover
        :rail="display.mdAndUp.value"
        :temporary="display.smAndDown.value"
        app
        :color="`#212121`"
        v-model="drawer"
      >
        <v-list>
          <v-list-item>
            <div @click="handleToHomePage()" class="svg-container">
              <img :src="mishkanIcon" class="clipped-svg" />
            </div>
          </v-list-item>
        </v-list>

        <v-divider></v-divider>
        <v-list
          density="compact"
          nav
          lines="two"
          app
          :opened="opened"
          @update:opened="newOpened => opened = newOpened.slice(-1)"
          >
          <template v-for="(item, index) in items" :key="item.title">
            <!-- Without sublinks -->
            <v-list-item
              v-if="!item.hasSublinks"
              :prepend-icon="item.icon"
              :title="item.title"
              :no-action="item.hasSublinks"
              :to="item.to"
              :value="item.title"
              link
            >

            </v-list-item>

            <!-- With sublinks -->

            <v-list-group
              :group="item.title"
              v-if="item.hasSublinks"
              :prepend-icon="item.icon"
              :title="item.title"
              no-action
              :value="item.title"
              v-model="item.isOpen"
              :item="item"
              >
              <template v-slot:activator="{ props }">
                <v-list-item
                v-bind="props"
                :prepend-icon="item.icon"
                :title="item.title"
                ></v-list-item>
              </template>
              <v-list-item
              v-for="(subitem, subIndex) in item.sublinks"
              :key="subIndex"
              link
              :prepend-icon="subitem.icon"
              :title="subitem.title"
              :value="subitem.title"
              :to="subitem.to"
              ></v-list-item>
            </v-list-group>
          </template>
        </v-list>

        <v-spacer />

        <!-- only display in mobile version -->
        <div v-show="display.smAndDown.value" class="drawer-bottom">
          <LangSwitcher/>
        </div>
      </v-navigation-drawer>
  </template>

<style>
.svg-container {
  width: 200px; /* Set the desired width */
  height: 50px; /* Set the desired height */
  overflow: hidden; /* Hide overflow */
}

.svg-container:hover {
  cursor: pointer;
}

.clipped-svg {
  width: 150px;
  height: 50px;
  object-fit: cover;
  transform:  scale(0.7) translate(-31px, 0px);
}

</style>
