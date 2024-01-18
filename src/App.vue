<template>
  <div class="navbar" style="z-index: 6;">
    <div class="toplineapp">
      <router-link :class="this.$route.path == '/' ? 'active' : ''" :to="{ name: 'Home' }"><img
          style="padding-left: 15px;" class="pagetitle" alt="LC Dog Dante"
          src="./assets/DanteLogoBanner.webp"></router-link>
      <div
        style="display:inline-block;position:relative;float:right;color: #f2f2f2;cursor: pointer;padding-right:3vw;padding-top:50px">
        <b-button size="sm" type="submit" @click="$i18n.locale = 'en', updatelocate('en')">English</b-button>
        &nbsp;
        <b-button size="sm" type="submit" @click="$i18n.locale = 'zh', updatelocate('zh')">中文</b-button>
      </div>
    </div>

    <div class="topnav">
      <router-link :class="this.$route.path == '/' ? 'active' : ''" :to="{ name: 'Home' }">{{ $t(`Home`) }}</router-link>
      <router-link :class="this.$route.path == '/LCB/Changelog' ? 'active' : ''" :to="{ name: 'Changelog' }">{{
        $t(`Changelog`) }}</router-link>
      <router-link :class="this.$route.path == '/LCB/StatusSetting' ? 'active' : ''" :to="{ name: 'StatusSetting' }">{{
        $t(`StatusSetting`) }}</router-link>
      <router-link :class="this.$route.path == '/LCB/UptieCalculator' ? 'active' : ''"
        :to="{ name: 'UptieCalculator' }">{{ $t(`UptieCalculator`) }}</router-link>
    </div>
  </div>
  <div style="z-index: 5;padding-top:10vh">
    <router-view />
  </div>
</template>

<script>

// import LimbusCompany from './components/LimbusCompany.vue'

export default {
  name: 'App',
  computed: {
  },
  methods: {
    updatelocate(lang) {
      localStorage.setItem('locate', lang);
    },
  },
  components: {
  },
  watch: {
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
@import '../src/components/format.css';
</style>
