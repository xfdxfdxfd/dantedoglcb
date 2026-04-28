<template>
  <div class="min-h-screen bg-ink text-mist">
    <div class="fixed inset-x-0 top-0 z-[70]">
      <div v-if="loading" class="h-1 overflow-hidden bg-black/40">
        <div class="animate-[loading_1.2s_linear_infinite] h-full w-2/5 bg-ember"></div>
      </div>
      <div v-else class="h-1 bg-black/40"></div>
    </div>

    <button
      type="button"
      class="fixed left-4 top-4 z-[80] inline-flex h-11 w-11 items-center justify-center border border-gold/40 bg-black/65 text-gold shadow-glow backdrop-blur transition hover:border-gold hover:bg-black/80 lg:hidden"
      :aria-expanded="sidebarOpen.toString()"
      :aria-label="$t(sidebarOpen ? 'CloseMenu' : 'OpenMenu')"
      @click="toggleSidebar"
    >
      <svg class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <path v-if="!sidebarOpen" d="M4 7h16M4 12h16M4 17h16" />
        <path v-else d="M6 6l12 12M18 6L6 18" />
      </svg>
      <span class="sr-only">{{ $t(sidebarOpen ? 'CloseMenu' : 'OpenMenu') }}</span>
    </button>

    <div
      v-if="sidebarOpen"
      class="fixed inset-0 z-[55] bg-black/70 backdrop-blur-sm lg:hidden"
      @click="closeSidebar"
    ></div>

    <aside
      class="app-header-bg fixed inset-y-0 left-0 z-[60] w-72 border-r border-gold/20 bg-cover bg-center shadow-2xl transition-transform duration-300 ease-out lg:translate-x-0"
      :class="sidebarOpen ? 'translate-x-0' : '-translate-x-full'"
    >
      <div class="h-full overflow-y-auto px-4 py-6 md:px-6">
        <div class="content-card min-h-full bg-black/35 px-4 py-5 md:px-5">
          <div class="flex items-center gap-4">
            <span class="deco-diamond hidden md:inline-flex" aria-hidden="true">
              <span class="h-2.5 w-2.5 bg-gold"></span>
            </span>
            <router-link :to="{ name: 'Home' }" class="inline-flex items-center" @click="handleNavSelection">
              <img class="h-14 w-auto" alt="LC Dog Dante" src="./assets/DanteLogoBanner.webp">
            </router-link>
          </div>

          <div class="mt-6 grid gap-2">
            <button
              v-for="locale in localeOptions"
              :key="locale.code"
              type="button"
              class="nav-pill w-full text-left"
              :class="localeButtonClass(locale.code)"
              @click="setLocale(locale.code)"
            >
              {{ $t(locale.label) }}
            </button>
          </div>

          <div class="deco-divider mt-6 whitespace-nowrap text-[0.78rem] font-accent uppercase tracking-[0.2em]">{{ $t('Navigation') }}</div>

          <nav class="mt-5 flex flex-col gap-2 border-t border-gold/10 pt-4">
            <router-link
              v-for="item in navItems"
              :key="item.name"
              :to="{ name: item.name }"
              class="nav-pill"
              :class="navLinkClass(item.path)"
              @click="handleNavSelection"
            >
              {{ $t(item.label) }}
            </router-link>
          </nav>
        </div>
      </div>
    </aside>

    <div class="min-h-screen lg:pl-72">
      <main class="pt-16 lg:pt-0">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      loading: true,
      sidebarOpen: false,
      localeOptions: [
        { code: 'en', label: 'LanguageEnglish' },
        { code: 'zh-TW', label: 'LanguageTraditionalChinese' },
        { code: 'zh-CN', label: 'LanguageSimplifiedChinese' },
      ],
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
    normalizeLocale(lang) {
      return lang === 'zh' ? 'zh-TW' : lang;
    },
    updatelocate(lang) {
      localStorage.setItem('locate', this.normalizeLocale(lang));
    },
    setLocale(lang) {
      const locale = this.normalizeLocale(lang);
      this.$i18n.locale = locale;
      this.updatelocate(locale);
      this.closeSidebar();
    },
    toggleSidebar() {
      this.sidebarOpen = !this.sidebarOpen;
    },
    closeSidebar() {
      this.sidebarOpen = false;
    },
    handleNavSelection() {
      this.closeSidebar();
    },
    navLinkClass(path) {
      return this.$route.path === path
        ? 'border-gold bg-gold text-stone-950 shadow-glow'
        : 'border-gold/30 bg-black/20 text-mist hover:border-gold hover:bg-black/35';
    },
    localeButtonClass(locale) {
      return this.normalizeLocale(this.$i18n.locale) === locale
        ? 'border-gold bg-gold text-stone-950'
        : 'border-gold/25 bg-black/20 text-mist hover:border-gold hover:bg-black/35';
    },
  },
  watch: {
    $route() {
      this.closeSidebar();
    },
  },
  created() {
    setTimeout(() => this.loading = false, 1000)
  },
  mounted() {
    const language = this.normalizeLocale(localStorage.getItem('locate'));
    if (language) {
      this.$i18n.locale = language;
      this.updatelocate(language);
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
