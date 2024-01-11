<template>
  <v-app>
    <v-container>
      <headerNav v-if="!$route.meta.showNav"></headerNav>
      <router-view v-if="!$route.meta.requireAuth"></router-view>
    </v-container>
  </v-app>
</template>

<script>
import Nav from "../src/components/Nav"
export default {
  name: 'App',
  components: {
    headerNav: Nav
  },
  data: () => ({
    //
  }),
};
</script>
