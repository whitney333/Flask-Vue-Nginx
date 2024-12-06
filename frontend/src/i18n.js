import { createI18n } from 'vue-i18n'
import EN from './language/config/en.json'
import KR from './language/config/kr.json'

const messages = {
  en: {
    ...EN
  },
  kr: {
    ...KR
  }
}

const i18n = createI18n({
  locale: 'en',
  legacy: false,
  globalInjection: true,
  messages: messages,
  useScope: 'global'
})

export default i18n