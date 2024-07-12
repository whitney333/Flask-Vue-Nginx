<script setup>
  import { ref, watch } from 'vue';
  import { useRouter } from 'vue-router';

  const mishkanIcon = "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/sidebar_logo.svg"
  const drawer = ref(true)
  const rail = ref(true)
  const isHovered = ref(false);
  const router = useRouter()
  const items = ref(
    [
      {
        title:'Dashboard',
        icon:'mdi-view-dashboard',
        to:'/'
      },
      {
        title: 'SNS',
        icon: 'mdi-account-multiple',
        to: '/sns',
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
          sublinks: [
            {
              title: 'Analytics',
              icon: 'mdi-poll',
              to: '/campaign-analytics',
              active: true
            },
          ]
        },
      ],
)

  const handleMouseEnter = () => {
    isHovered.value = true;
  };

  const handleMouseLeave = () => {
    isHovered.value = false;
  };

  const handleToHomePage = () => {
    router.push({path: "/"})
  }


</script>

 <template>
    <v-layout>
      <v-navigation-drawer
        expand-on-hover
        mobile-breakpoint="xs"
        rail
        :color="`#212121`"
        @mouseenter="handleMouseEnter"
        @mouseleave="handleMouseLeave"
      >
        <v-list>
          <v-list-item>
            <div @click="handleToHomePage()" class="svg-container">
              <img :src="mishkanIcon" class="clipped-svg" />
            </div>
          </v-list-item>
        </v-list>

        <v-divider></v-divider>
        
        <v-list density="compact" nav>
          <v-list-item 
            v-for="[index, item] in items.entries()" 
            :prepend-icon="item.icon" 
            :title="item.title" 
            :to="item.to"
            :value="index"
            :key="index" />
        </v-list>
      </v-navigation-drawer>

    </v-layout>
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
