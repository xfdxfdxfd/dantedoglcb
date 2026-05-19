<template>
  <div class="min-h-screen bg-ink text-mist">
    <div class="fixed inset-x-0 top-0 z-[70]">
      <div v-if="loading" class="h-1 overflow-hidden bg-black/40">
        <div class="animate-[loading_1.2s_linear_infinite] h-full w-2/5 bg-ember"></div>
      </div>
      <div v-else class="h-1 bg-black/40"></div>
    </div>

    <div class="fixed right-4 top-4 z-[85] max-w-[calc(100vw-5rem)] lg:right-6 lg:top-5">
      <div class="account-dock min-w-[15rem] max-w-[20rem] px-3 py-3">
        <div v-if="accountState.user" class="space-y-2">
          <div class="flex items-center gap-3">
            <span class="account-avatar">{{ accountInitial }}</span>
            <div class="min-w-0 flex-1">
              <p class="truncate text-sm font-semibold text-white">{{ accountState.user.email }}</p>
              <p v-if="accountState.status" class="truncate text-[0.68rem] text-emerald-200">{{ accountState.status }}</p>
              <p v-else class="text-[0.68rem] text-stone-400">Synced</p>
            </div>
          </div>

          <div class="grid grid-cols-3 gap-2">
            <button type="button" class="nav-pill min-h-0 px-2 py-2 text-center text-[0.62rem] tracking-[0.12em]" :disabled="accountState.loading" @click="loadSavedProgress()">Load</button>
            <button type="button" class="nav-pill min-h-0 px-2 py-2 text-center text-[0.62rem] tracking-[0.12em]" :disabled="accountState.loading" @click="saveCurrentProgress()">Save</button>
            <button type="button" class="nav-pill min-h-0 border-red-400/35 px-2 py-2 text-center text-[0.62rem] tracking-[0.12em] text-red-200 hover:border-red-300 hover:bg-red-500/10" :disabled="accountState.loading" @click="handleLogout()">Out</button>
          </div>
          <p v-if="accountState.error" class="text-[0.68rem] leading-4 text-red-300">{{ accountState.error }}</p>
        </div>

        <div v-else class="space-y-2">
          <div class="flex items-center justify-between gap-2">
            <p class="text-base font-bold uppercase tracking-[0.18em] text-gold">{{ $t('Account') }}</p>
            <p v-if="accountState.loading" class="text-sm uppercase tracking-[0.16em] text-stone-400">{{ $t('Working') }}</p>
          </div>
          <div v-if="googleReady" class="google-button-shell min-h-[56px]">
            <div ref="googleButtonHost" class="min-h-[40px]"></div>
          </div>
          <button
            v-else
            type="button"
            class="nav-pill w-full px-3 py-2 text-center text-base font-semibold tracking-[0.16em]"
            :disabled="true"
          >
            {{ $t('GoogleSignInUnavailable') }}
          </button>
          <p v-if="accountState.error" class="text-[0.68rem] leading-4 text-red-300">{{ accountState.error }}</p>
          <p v-else-if="accountState.status" class="text-[0.68rem] leading-4 text-emerald-200">{{ accountState.status }}</p>
        </div>
      </div>
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
      <div class="h-full px-3 py-4 md:px-4 md:py-4">
        <div class="content-card flex h-full flex-col bg-black/35 px-3 py-4 md:px-4">
          <div class="flex items-center gap-3">
            <span class="deco-diamond hidden md:inline-flex" aria-hidden="true">
              <span class="h-2.5 w-2.5 bg-gold"></span>
            </span>
            <router-link :to="{ name: 'Home' }" class="inline-flex items-center" @click="handleNavSelection">
              <img class="h-12 w-auto" alt="LC Dog Dante" src="./assets/DanteLogoBanner.webp">
            </router-link>
          </div>


          <div class="mt-4 grid grid-cols-3 gap-3">
            <button
              v-for="locale in localeOptions"
              :key="locale.code"
              type="button"
              class="nav-pill min-h-0 px-3 py-3 text-center text-base font-semibold leading-tight tracking-[0.14em]"
              :class="localeButtonClass(locale.code)"
              @click="setLocale(locale.code)"
            >
              {{ $t(locale.label) }}
            </button>
          </div>

          <div class="panel-divider mt-4"></div>

          <nav class="mt-4 flex flex-col gap-3">
            <router-link
              v-for="item in navItems"
              :key="item.name"
              :to="{ name: item.name }"
              class="nav-pill flex items-center justify-center px-4 py-3 text-center text-base font-semibold tracking-[0.16em]"
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
import {
  getGoogleClientId,
  hasProgressEntries,
  hasGoogleClientId,
  loadAccountProgress,
  logInWithGoogleCredential,
  logOutAccount,
  readLocalProgress,
  restoreAccountSession,
  saveAccountProgress,
  writeLocalProgress,
} from './utils/progressSync'

export default {
  name: 'App',
  data() {
    return {
      loading: true,
      sidebarOpen: false,
      googleReady: false,
      googleButtonRendered: false,
      localeOptions: [
        { code: 'en', label: 'LanguageEnglish' },
        { code: 'zh-TW', label: 'LanguageTraditionalChinese' },
        { code: 'zh-CN', label: 'LanguageSimplifiedChinese' },
      ],
      accountState: {
        loading: false,
        user: null,
        error: '',
        status: '',
      },
      navItems: [
        { name: 'Home', path: '/', label: 'Home' },
        { name: 'Changelog', path: '/LCB/Changelog', label: 'Changelog' },
        { name: 'StatusSetting', path: '/LCB/StatusSetting', label: 'StatusSetting' },
        { name: 'UptieCalculator', path: '/LCB/UptieCalculator', label: 'UptieCalculator' },
        { name: 'ExpCalculator', path: '/LCB/ExpCalculator', label: 'ExpCalculator' },
      ],
    }
  },
  computed: {
    accountInitial() {
      return (this.accountState.user?.email || '?').charAt(0).toUpperCase();
    },
  },
  methods: {
    setAccountStatus(message = '') {
      this.accountState.status = message;
    },
    setAccountError(message = '') {
      this.accountState.error = message;
    },
    async applyAccountProgress(progress) {
      if (!hasProgressEntries(progress)) {
        return false;
      }

      writeLocalProgress(progress, 'account');
      return true;
    },
    async loadGoogleScript() {
      if (!hasGoogleClientId()) {
        return false;
      }

      if (window.google?.accounts?.id) {
        return true;
      }

      await new Promise((resolve, reject) => {
        const existingScript = document.querySelector('script[data-google-identity="true"]');

        if (existingScript) {
          existingScript.addEventListener('load', resolve, { once: true });
          existingScript.addEventListener('error', reject, { once: true });
          return;
        }

        const script = document.createElement('script');
        script.src = 'https://accounts.google.com/gsi/client';
        script.async = true;
        script.defer = true;
        script.dataset.googleIdentity = 'true';
        script.onload = resolve;
        script.onerror = () => reject(new Error('Failed to load Google sign-in.'));
        document.head.appendChild(script);
      });

      return Boolean(window.google?.accounts?.id);
    },
    async initializeGoogleSignIn() {
      this.googleReady = false;
      this.googleButtonRendered = false;

      if (!hasGoogleClientId()) {
        this.setAccountError('Set VITE_GOOGLE_CLIENT_ID to enable Google sign-in.');
        return;
      }

      try {
        const loaded = await this.loadGoogleScript();

        if (!loaded || !window.google?.accounts?.id) {
          throw new Error('Google sign-in is unavailable.');
        }

        window.google.accounts.id.initialize({
          client_id: getGoogleClientId(),
          callback: this.handleGoogleCredential,
          auto_select: false,
          cancel_on_tap_outside: true,
        });

        this.googleReady = true;
        this.$nextTick(() => this.renderGoogleButton());
      } catch (error) {
        this.googleReady = false;
        this.setAccountError(error.message || 'Google sign-in is unavailable.');
      }
    },
    renderGoogleButton() {
      if (!this.googleReady || this.accountState.user || !this.$refs.googleButtonHost || !window.google?.accounts?.id) {
        return;
      }

      this.$refs.googleButtonHost.innerHTML = '';
      window.google.accounts.id.renderButton(this.$refs.googleButtonHost, {
        theme: 'filled_black',
        size: 'large',
        shape: 'pill',
        text: 'signin_with',
        logo_alignment: 'left',
        width: 236,
      });
      this.googleButtonRendered = true;
    },
    async handleGoogleCredential(response) {
      const credential = String(response?.credential || '').trim();

      if (!credential) {
        this.setAccountError('Google sign-in did not return a credential.');
        return;
      }

      this.accountState.loading = true;
      this.setAccountError('');
      this.setAccountStatus('');

      try {
        const payload = await logInWithGoogleCredential(credential);
        this.accountState.user = payload.user;
        const loadedRemote = await this.applyAccountProgress(payload.progress);
        const localProgress = readLocalProgress();

        if (loadedRemote) {
          this.setAccountStatus('Loaded');
        } else if (hasProgressEntries(localProgress)) {
          await saveAccountProgress(localProgress);
          this.setAccountStatus('Saved');
        } else {
          this.setAccountStatus('Signed in');
        }
      } catch (error) {
        this.setAccountError(error.message || 'Google sign-in failed.');
      } finally {
        this.accountState.loading = false;
      }
    },
    async initializeAccount() {
      this.accountState.loading = true;
      this.setAccountError('');

      try {
        const payload = await restoreAccountSession();

        if (!payload) {
          this.accountState.user = null;
          return;
        }

        this.accountState.user = payload.user;
        const loadedRemote = await this.applyAccountProgress(payload.progress);
        const localProgress = readLocalProgress();

        if (loadedRemote) {
          this.setAccountStatus('Loaded');
        } else if (hasProgressEntries(localProgress)) {
          await saveAccountProgress(localProgress);
          this.setAccountStatus('Saved');
        } else {
          this.setAccountStatus('Signed in');
        }
      } catch (error) {
        this.accountState.user = null;
        this.setAccountError(error.message || 'Failed to restore account session.');
      } finally {
        this.accountState.loading = false;
        this.$nextTick(() => this.renderGoogleButton());
      }
    },
    async loadSavedProgress() {
      this.accountState.loading = true;
      this.setAccountError('');

      try {
        const payload = await loadAccountProgress();

        if (await this.applyAccountProgress(payload?.progress)) {
          this.setAccountStatus('Loaded');
        } else {
          this.setAccountStatus('Empty');
        }
      } catch (error) {
        this.setAccountError(error.message || 'Failed to load saved progress.');
      } finally {
        this.accountState.loading = false;
      }
    },
    async saveCurrentProgress() {
      const localProgress = readLocalProgress();

      if (!hasProgressEntries(localProgress)) {
        this.setAccountError('Set your roster progress first, then save it to the account.');
        return;
      }

      this.accountState.loading = true;
      this.setAccountError('');

      try {
        await saveAccountProgress(localProgress);
        this.setAccountStatus('Saved');
      } catch (error) {
        this.setAccountError(error.message || 'Failed to save progress.');
      } finally {
        this.accountState.loading = false;
      }
    },
    async handleLogout() {
      this.accountState.loading = true;
      this.setAccountError('');

      try {
        await logOutAccount();
        this.accountState.user = null;
        this.setAccountStatus('Signed out');
      } catch (error) {
        this.setAccountError(error.message || 'Failed to log out.');
      } finally {
        this.accountState.loading = false;
        this.$nextTick(() => this.renderGoogleButton());
      }
    },
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

    this.initializeGoogleSignIn();
    this.initializeAccount();
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

.account-dock {
  border: 1px solid rgba(240, 197, 111, 0.22);
  background: rgba(10, 10, 12, 0.8);
  backdrop-filter: blur(14px);
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.28);
}

.account-avatar {
  display: inline-flex;
  height: 2rem;
  width: 2rem;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(240, 197, 111, 0.35);
  color: #f0c56f;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.google-button-shell {
  display: inline-flex;
  width: 100%;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(240, 197, 111, 0.28);
  border-radius: 9999px;
  padding: 0.35rem;
  background: linear-gradient(180deg, rgba(0, 0, 0, 0.35), rgba(0, 0, 0, 0.6));
}
</style>
