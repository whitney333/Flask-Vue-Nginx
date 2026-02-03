<script setup>
import { useI18n } from 'vue-i18n'
import getUnicodeFlagIcon from 'country-flag-icons/unicode'
import { computed, onMounted } from 'vue'

const { locale } = useI18n()

const countriesFlag = {
    'United Kingdom': 'GB',
    'South Korea': 'KR'
}

const languages = [
    {
        lang: 'English',
        value: 'en',
        flag: getUnicodeFlagIcon(countriesFlag['United Kingdom']),
        title: `${getUnicodeFlagIcon(countriesFlag['United Kingdom'])} English`
    },
    {
        lang: '한국어',
        value: 'kr',
        flag: getUnicodeFlagIcon(countriesFlag['South Korea']),
        title: `${getUnicodeFlagIcon(countriesFlag['South Korea'])} 한국어`
    }
]

const currentFlag = computed(() => {
    const currentLang = languages.find(l => l.value === locale.value)
    return currentLang ? currentLang.flag : '🌐'
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
          v-for="language in languages"
          :key="language.value"
          @click="setLang(language.value)"
      >
        <v-list-item-title>{{ language.flag }} {{ language.lang }}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<style scoped>
</style>
