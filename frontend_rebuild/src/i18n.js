import { createI18n } from 'vue-i18n'
import EN from './language/config/en.json'
import KR from './language/config/kr.json'
import CN from './language/config/cn.json'
import HK from './language/config/hk.json'
import TW from './language/config/tw.json'

const messages = {
  en: {
    ...EN
  },
  kr: {
    ...KR
  },
  cn: {
    ...CN
  },
  hk: {
    ...HK
  },
  tw: {
    ...TW
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