<template>
  <v-container>
    <v-app-bar
        app
        color="grey lighten-5"
        elevate-on-scroll
        clipped-left
        class="pl-15"
    >
      <v-toolbar-title
        class="hidden-sm-and-down font-weight-light h3"
        v-text="$route.name"
      />
      <v-spacer/>
        <!-- language translate  -->
        <LangSwitcher/>
        <!-- User Profile   -->
        <AccountProfile/>
    </v-app-bar>
    <!--left nav-->
    <v-navigation-drawer
        color="grey darken-4"
        dark
        permanent
        app
        v-model="drawer"
        expand-on-hover
        mobile-breakpoint="960"
        :mini-variant.sync="mini"
    >
      <v-divider class="mb-2"/>
      <v-list
          dense
          nav
      >
        <v-list-item>
<!--          <v-list-item-avatar-->
<!--              class="ma-n2"-->
<!--          >-->
            <v-img
                src="https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/sidebar_logo.svg"
                max-height="40px"
                max-width="120px"
            />
<!--          </v-list-item-avatar>-->
        </v-list-item>
      </v-list>
      <v-divider class="mb-2 white"/>
        <!-- Dashboard -->
        <v-list nav>
          <div v-for="(link, i) in items" :key="i">
            <v-list-item
                v-if="!link.sublinks"
                :to="link.to"
                avatar
                class="v-list-item"
            >
              <v-list-item-icon>
                <v-icon>{{ link.icon }}</v-icon>
              </v-list-item-icon>
              <v-list-item-title v-text="link.title"/>
            </v-list-item>
            <v-list-group
                v-if="link.sublinks"
                :key="link.title"
                no-action
                :prepend-icon="link.icon"
                :value="false"
                color="grey lighten-1"
            >
              <template v-slot:activator>
                <v-list-item-title>{{ link.title }}</v-list-item-title>
              </template>
              <v-list-item
                  v-for="sublink in link.sublinks"
                  :to="sublink.to"
                  :key="sublink.title"
                  dense
                  color="white"
              >
                <v-list-item-icon>
                  <v-icon>{{ sublink.icon }}</v-icon>
                </v-list-item-icon>
                <v-list-item-title>{{ sublink.title }}</v-list-item-title>
              </v-list-item>
            </v-list-group>
          </div>
        </v-list>
    </v-navigation-drawer>
<!--    <v-main>-->
      <router-view></router-view>
<!--    </v-main>-->
  </v-container>
</template>
<script>
import LangSwitcher from "@/components/LangSwitcher";
import AccountProfile from "@/components/accountProfile";
export default {
  name: "Nav",
  components: {AccountProfile, LangSwitcher},
  data: () => ({
  selectedItem: 1,
  model: 1,
  drawer: null,
  items:[
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
          title: 'Bilibili',
          icon: 'mdi-movie-filter',
          to: '/sns-bilibili',
          active: true
        },
        {
          title: 'Instagram',
          icon: 'mdi-instagram',
          to: '/sns-instagram',
        },
        {
          title: 'Tiktok',
          icon: 'mdi-music-box',
          to: '/sns-tiktok',
        },
        {
          title: 'Youtube',
          icon: 'mdi-youtube',
          to: '/sns-youtube',
        }
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
    // {
    //   title:'News',
    //   icon:'mdi-newspaper-variant-multiple-outline',
    //   to:'/news'
    // },
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
        // {
        //   title: 'Create',
        //   icon: 'mdi-shape-circle-plus',
        //   to: '/create-campaign',
        // }
      ]
    },
  ],
  profile: [
    {'name': 'Profile', 'icon': 'mdi-account'},
    {'name': 'Logout', 'icon': 'mdi-log-out'}
  ]
  }),
}
</script>
<style scoped>
</style>