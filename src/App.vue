<template>
  <div class="min-h-screen bg-ink text-mist">
    <header class="app-header-bg sticky top-0 z-50 border-b border-white/10 bg-cover bg-center shadow-2xl backdrop-blur-sm">
      <div v-if="loading" class="h-1 overflow-hidden rounded-full bg-black/40">
        <div class="animate-[loading_1.2s_linear_infinite] h-full w-2/5 bg-ember"></div>
      </div>
      <div v-else class="h-1 bg-black/40"></div>

      <div class="mx-auto flex max-w-7xl flex-col gap-4 px-4 py-4 md:px-6 lg:px-8">
        <div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <router-link :to="{ name: 'Home' }" class="inline-flex items-center">
            <img class="h-14 w-auto md:h-16" alt="LC Dog Dante" src="./assets/DanteLogoBanner.webp">
          </router-link>

          <div class="flex gap-2 self-start md:self-auto">
            <button
              type="button"
              class="rounded-full border px-4 py-2 text-sm font-semibold transition"
              :class="localeButtonClass('en')"
              @click="setLocale('en')"
            >
              English
            </button>
            <button
              type="button"
              class="rounded-full border px-4 py-2 text-sm font-semibold transition"
              :class="localeButtonClass('zh')"
              @click="setLocale('zh')"
            >
              中文
            </button>
          </div>
        </div>

        <nav class="flex flex-wrap gap-2 pb-2">
          <router-link
            v-for="item in navItems"
            :key="item.name"
            :to="{ name: item.name }"
            class="rounded-full border px-4 py-2 text-sm font-semibold tracking-wide transition"
            :class="navLinkClass(item.path)"
          >
            {{ $t(item.label) }}
          </router-link>
        </nav>
      </div>
    </header>

    <main>
      <router-view />
    </main>
  </div>
</template>

<script>

export default {
  name: 'App',
  data() {
    return {
      loading: true,
      navItems: [
        { name: 'Home', path: '/', label: 'Home' },
        { name: 'Changelog', path: '/LCB/Changelog', label: 'Changelog' },
        { name: 'StatusSetting', path: '/LCB/StatusSetting', label: 'StatusSetting' },
        { name: 'UptieCalculator', path: '/LCB/UptieCalculator', label: 'UptieCalculator' },
        { name: 'ExpCalculator', path: '/LCB/ExpCalculator', label: 'ExpCalculator' },
      ],
    }
  },
  methods: {
    updatelocate(lang) {
      localStorage.setItem('locate', lang);
    },
    setLocale(lang) {
      this.$i18n.locale = lang;
      this.updatelocate(lang);
    },
    navLinkClass(path) {
      return this.$route.path === path
        ? 'border-ember bg-ember text-white shadow-lg shadow-ember/30'
        : 'border-white/15 bg-black/20 text-stone-100 hover:border-gold/60 hover:bg-white/10';
    },
    localeButtonClass(locale) {
      return this.$i18n.locale === locale
        ? 'border-gold bg-gold text-stone-950'
        : 'border-white/20 bg-black/25 text-white hover:border-gold/60 hover:bg-white/10';
    },
  },
  created() {
    setTimeout(() => this.loading = false, 1000)
  },
  mounted() {

    //no reset the language after reload
    var language = localStorage.getItem('locate');
    if (language) {
      this.$i18n.locale = localStorage.getItem('locate');
    } else {
      localStorage.setItem('locate', 'en');
      this.$i18n.locale = localStorage.getItem('locate');
    }
  },
}
</script>

<style>
@keyframes loading {
  0% {
    transform: translateX(-140%);
  }

  50% {
    transform: translateX(70%);
  }

  100% {
    transform: translateX(240%);
  }
}
</style>
