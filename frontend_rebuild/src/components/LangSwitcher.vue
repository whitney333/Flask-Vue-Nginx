<script setup>
import { useI18n } from 'vue-i18n'
import { computed, onMounted } from "vue"

const { locale } = useI18n()

const languages = [
    {
        value: 'en',
        title: 'English',
        flagClass: 'fi fi-gb'
    },
    {
        value: 'kr',
        title: '한국어',
        flagClass: 'fi fi-kr'
    }
]

const currentLanguage = computed(() => {
  return languages.find(l => l.value === locale.value) || languages[0]
})

function setLang(value) {
  locale.value = value
  localStorage.setItem('locale', value)
}

onMounted(() => {
  const saved = localStorage.getItem('locale')
  if (saved) {
    locale.value = saved
  }
})
</script>

<template>
  <v-menu location="top center">
    <template v-slot:activator="{ props }">
      <v-btn
        v-bind="props"
        block
        variant="outlined"
        color="grey-lighten-1"
        class="text-none justify-space-between px-4"
        prepend-icon="mdi-translate"
      >
        <span>{{ currentLanguage.title }}</span>
        <span :class="[currentLanguage.flagClass, 'rounded-sm']"></span>
      </v-btn>
    </template>

    <v-list bg-color="#2a2a2a" theme="dark">
      <v-list-item
          v-for="lang in languages"
          :key="lang.value"
          :active="locale === lang.value"
          @click="setLang(lang.value)"
      >
        <template #prepend>
          <span :class="[lang.flagClass, 'mr-3 rounded-sm']"></span>
        </template>
        <v-list-item-title>{{ lang.title }}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<style scoped>
:deep(.v-btn__content) {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.fi {
  width: 20px;
  line-height: 1em;
  background-size: contain;
  background-position: center;
  background-repeat: no-repeat;
}
</style>