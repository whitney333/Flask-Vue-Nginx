<template>
  <div class="account-profile">
    <v-row justify="space-around">
      <v-menu
          close-on-content-click
          rounded="xl"
          offset-y
      >
        <template v-slot:activator="{ on, attrs }">
          <v-btn
              small
              elevation="0"
              v-bind="attrs"
              v-on="on"
              icon
              class="mr-5"
          >
            <v-icon>mdi-account</v-icon>
          </v-btn>
        </template>
        <v-list flat>
          <v-list-item-group color="deep-purple darken-1">
            <v-list-item>
              <v-list-item-icon>
                <v-icon>mdi-logout</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>
                  Logout
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </v-menu>
    </v-row>
  </div>
</template>
<script>
export default {
  name: "accountProfile",
  data() {
    return {
      model: 1,
      profile: [
        {'name': 'Profile', 'icon': 'mdi-account'},
        {'name': 'Logout', 'icon': 'mdi-logout'}
      ]
    }
  }
}
</script>
<style scoped>
</style>