<template>
  <div class="navbar" style="z-index: 6;">
    <div class="toplineapp" style="position: relative;">
      <router-link :class="this.$route.path == '/' ? 'active' : ''" :to="{ name: 'Home' }"><img
          style="margin: 0px;padding-left: 20px;width: 150px;" class="pagetitle" alt="LC Dog Dante"
          src="./assets/DanteLogoBanner.webp"></router-link>
      <div style="text-align: right">
        <b-button size="sm" class="locale-changer" type="submit" style="display:inline;color: #f2f2f2;cursor: pointer;"
          @click="$i18n.locale = 'en', updatelocate('en')">English</b-button>
        &nbsp;
        <b-button size="sm" class="locale-changer" type="submit"
          style="display:inline;color: #f2f2f2;cursor: pointer;padding-right:10%"
          @click="$i18n.locale = 'zh', updatelocate('zh')">中文</b-button>
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
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #333;
}

h1,
h2 {
  margin: 0px;
  padding: 0px;
  border-top-width: 0px;
  border-right-width: 0px;
  border-bottom-width: 0px;
  border-left-width: 0px;
}

.pagetitle {
  padding-top: 5px;
}

body {
  margin: 0px;
  padding: 0px;
  border-top-width: 0px;
  border-right-width: 0px;
  border-bottom-width: 0px;
  border-left-width: 0px;
}

/* from https://www.w3schools.com/howto/howto_js_topnav.asp */
.topnav {
  background-color: #232222;
  overflow: hidden;
}

/* Style the links inside the navigation bar */
.topnav a {
  float: left;
  color: #f2f2f2;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
  font-size: 17px;
}

/* Change the color of links on hover */
.topnav a:hover {
  background-color: #ddd;
  color: black;
}

/* Add a color to the active/current link */
.topnav a.active {
  background-color: rgb(211, 55, 16);
  color: white;
}

.toplineapp {
  border-top: 3px solid rgb(211, 55, 16);
  background-size: cover;
  overflow: hidden;
}

.navbar {
  background-image: url("./assets/E041X_3.webp");
  position: fixed;
  /* Set the navbar to fixed position */
  top: 0;
  /* Position the navbar at the top of the page */
  min-width: 100vw;
  /* Full width */
  min-height: 138px;
  background-repeat: no-repeat;
  background-size: cover;
  background-attachment: fixed;
  overflow: hidden;
}

.bottombar {
  width: 100%;
  /* Full width */
  height: 100%;
  overflow: hidden;
}

.content {
  background-image: url("./assets/maxresdefault.webp");
  background-size: cover;
  background-attachment: fixed;
  background-repeat: no-repeat;
  overflow: hidden;
}
</style>
