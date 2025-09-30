<script setup>
import { useI18n } from 'vue-i18n'
import getUnicodeFlagIcon from 'country-flag-icons/unicode'
import {ref, onMounted} from "vue";

const { locale } = useI18n()
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

const lang = ref('en')

const currentFlag = computed(() => {
  const lang = languages.find(l => l.code === locale.value)
  return lang ? lang.flag : '🌐'
})

function setLang(code) {
  locale.value = code
}

onMounted(() => {
  const saved = localStorage.getItem('locale')
  if (saved) locale.value = saved
})

</script>

<template>
  <v-menu>
    <template v-slot:activator="{ props }">
      <v-btn v-bind="props" icon>
        {{ currentFlag }}
      </v-btn>
    </template>

    <v-list>
      <v-list-item
          v-for="lang in languages"
          :key="lang.name"
          @click="setLang(lang.name)"
      >
        <v-list-item-title>{{ lang.show }} {{ lang.flag }}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<style scoped>
</style>
