<script setup>
import { useRoute, useRouter } from 'vue-router';
import LangSwitcher from './LangSwitcher.vue'
import getUnicodeFlagIcon from 'country-flag-icons/unicode'
import { useI18n } from 'vue-i18n'
import { ref, watch } from 'vue';
const { t, locale } = useI18n({ useScope: 'global' })

const route = useRoute()
const countriesFlag = {
    'Hong Kong': 'HK',
    'Japan': 'JP',
    'South Korea': 'KR',
    'United Kingdom': 'GB',
}
const lang = ref('en')

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
watch(lang, () => {
    locale.value = lang.value[0]
})

</script>
<template>
    <v-app-bar :elevation="1" app :style="{ padding: '0px 20px' }">        
        <v-app-bar-title :class="['text-h5']">{{ route.name }}</v-app-bar-title>
        <template v-slot:append>
            <v-menu>
                <template v-slot:activator="{ props }">
                    <v-btn v-bind="props" icon="mdi-web"></v-btn>
                </template>
                <v-list
                v-model:selected="lang"
                >
                    <v-list-item
                    v-for="(language, index) in languages"
                    :key="index"
                    :value="language.value"
                    >
                    <v-list-item-title>{{ language.title }}</v-list-item-title>
                    </v-list-item>
                </v-list>

            </v-menu>

            
            <v-btn icon="mdi-magnify"></v-btn>
            
            <v-btn icon="mdi-dots-vertical"></v-btn>
        </template>
    </v-app-bar>
</template>
