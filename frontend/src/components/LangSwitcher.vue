<template>
  <div class="locale-changer">
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
              class="mr-10"
          >
            <v-icon>mdi-translate</v-icon>
          </v-btn>
        </template>
        <v-list flat>
          <v-list-item-group
              v-model="$i18n.locale"
              color="deep-purple darken-1"
              mandatory
          >
            <v-list-item
                v-for="(lang, i) in langs"
                :key="`Lang${i}`"
                :value="lang.name"
            >
              <v-list-item-icon>
                <v-img :src="lang.flag"
                  width="15px" height="15px"
                ></v-img>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>{{ lang.show }}</v-list-item-title>
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
  name: "LangSwitcher",
  data() {
    return {
      langs: [
        {'name': 'kr',
         'show': '한국어',
         'flag': 'https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/flags/kr.svg'
        },
        {'name': 'en',
         'show': 'English',
         'flag': 'https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/flags/us.svg'}
      ]
    }
  }
}
</script>
<style scoped>
</style>