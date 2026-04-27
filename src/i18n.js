import { createI18n } from 'vue-i18n'
import en from './locales/en.json'
import zhTw from './locales/zh.json'
import zhCn from './locales/zh-CN.json'

function loadLocaleMessages() {
  const locales = [{ en: en }, { 'zh-TW': zhTw }, { 'zh-CN': zhCn }, { zh: zhTw }]
  const messages = {}
  locales.forEach(lang => {
    const key = Object.keys(lang)
    messages[key] = lang[key] 
  })
  return messages
}

export default createI18n({
  locale: 'en',
  fallbackLocale: 'en',
  messages: loadLocaleMessages()
})