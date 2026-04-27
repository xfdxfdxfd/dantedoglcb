const { defineConfig } = require('vite')
const vue = require('@vitejs/plugin-vue')
const VueDevTools = require('vite-plugin-vue-devtools')

module.exports = defineConfig({
  plugins: [vue(), VueDevTools()],
})