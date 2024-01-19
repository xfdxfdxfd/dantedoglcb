<template>
  <div class="wholenavbar" style="z-index:6">
    <div class="navbar">
      <div class="loader-line" v-if="loading"></div>
      <div v-else
        style="width: 100vw;height: 3px;overflow: hidden;background-color: #232222;-webkit-border-radius: 20px;-moz-border-radius: 20px;border-radius: 20px;">
      </div>
      <div class="toplineapp">
        <router-link :class="this.$route.path == '/' ? 'active' : ''" :to="{ name: 'Home' }">
          <img style="padding-left: 15px;" class="pagetitle" alt="LC Dog Dante"
            src="./assets/DanteLogoBanner.webp"></router-link>
        <div class="locateselector">
          <b-button size="sm" type="submit" @click="$i18n.locale = 'en', updatelocate('en')">English</b-button>
          &nbsp;
          <b-button size="sm" type="submit" @click="$i18n.locale = 'zh', updatelocate('zh')">中文</b-button>
        </div>
      </div>
    </div>
    <div class="navbar2" id="navbar2">
      <div class="topnav">
        <router-link :class="this.$route.path == '/' ? 'active' : ''" :to="{ name: 'Home' }">{{ $t(`Home`)
        }}</router-link>
        <router-link :class="this.$route.path == '/LCB/Changelog' ? 'active' : ''" :to="{ name: 'Changelog' }">{{
          $t(`Changelog`) }}</router-link>
        <router-link :class="this.$route.path == '/LCB/StatusSetting' ? 'active' : ''" :to="{ name: 'StatusSetting' }">{{
          $t(`StatusSetting`) }}</router-link>
        <router-link :class="this.$route.path == '/LCB/UptieCalculator' ? 'active' : ''"
          :to="{ name: 'UptieCalculator' }">{{ $t(`UptieCalculator`) }}</router-link>
      </div>
    </div>
  </div>
  <div style="z-index:5;" id="appContent">
    <router-view />
  </div>
</template>

<script>

export default {
  name: 'App',
  data() {
    return {
      loading: true,
    }
  },
  computed: {
  },
  methods: {
    updatelocate(lang) {
      localStorage.setItem('locate', lang);
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

    //calc the reposition of the content
    document.getElementById("appContent").style.paddingTop = document.getElementById("navbar2").offsetHeight - 20 + "px";
    window.onresize = () => {
      let height = document.getElementById("navbar2").offsetHeight;
      console.log(height);
      document.getElementById("appContent").style.paddingTop = height - 20 + "px";
    };
  },
}
</script>

<style>
@import '../src/components/format.css';
</style>
