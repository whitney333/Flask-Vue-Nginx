<script setup>
  import { ref, watch } from 'vue';
  import { useRouter } from 'vue-router';

  const mishkanIcon = "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/sidebar_logo.svg"
  const drawer = ref(true)
  const rail = ref(true)
  const isHovered = ref(false);
  const router = useRouter()
  const opened = ref([])
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
        expand-on-hover
        mobile-breakpoint="xs"
        rail
        permanent
        app
        :color="`#212121`"
        v-model="drawer"
        :mini-variant.sync="mini"
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
