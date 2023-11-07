<template>
  <div class="navbar" style="z-index: 6;">
    <div class="toplineapp" style="position: relative;">
        <router-link :class="this.$route.path == '/'? 'active':''" :to="{name:'Home'}"><img style="margin: 0px;padding-left: 20px;width: 150px;" class="pagetitle" alt="LC Dog Dante" src="./assets/DanteLogoBanner.png"></router-link>
        &nbsp;
        <b-button size="sm" class="locale-changer" type="submit" style="display:inline;color: #f2f2f2;cursor: pointer;position: absolute;right: 50px;top: 17px;" @click="$i18n.locale = 'en'">English</b-button>
        &nbsp;
        <b-button size="sm" class="locale-changer" type="submit" style="display:inline;color: #f2f2f2;cursor: pointer;position: absolute;right: 10px;top: 15px;" @click="$i18n.locale = 'zh'">中文</b-button>
    </div>

    <div class="topnav">
      <router-link :class="this.$route.path == '/'? 'active':''" :to="{name:'Home'}">{{$t(`Home`)}}</router-link>
      <router-link :class="this.$route.path == '/LCB/About'? 'active':''" :to="{name:'About'}">{{$t(`About`)}}</router-link>
      <router-link :class="this.$route.path == '/LCB/Thread'? 'active':''" :to="{name:'Thread'}">{{$t(`Thread`)}}</router-link>
    </div>
  </div>
  <div class="content" style="z-index: 3;">
    <router-view/>
  </div>
</template>

<script>

// import LimbusCompany from './components/LimbusCompany.vue'

export default {
  name: 'App',
  computed: {
  },
  methods: {
  },
  components: {
  },
  watch:{
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #333;
}

h1,h2{
  margin: 0px;
  padding: 0px;
  border-top-width: 0px;
  border-right-width: 0px;
  border-bottom-width: 0px;
  border-left-width: 0px;
}
.pagetitle {
  padding: 7px;
}
body
{
  margin: 0px;
  padding: 0px;
  border-top-width: 0px;
  border-right-width: 0px;
  border-bottom-width: 0px;
  border-left-width: 0px;
}

/* from https://www.w3schools.com/howto/howto_js_topnav.asp */
.topnav {
  background-color: #333;
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

.toplineapp{
  border-top: 3px solid rgb(211, 55, 16);
  background-size: cover;
  overflow: hidden;
}
.navbar {
  background-image: url("./assets/E041X_2.png");
  position: fixed; /* Set the navbar to fixed position */
  top: 0; /* Position the navbar at the top of the page */
  width: 100%; /* Full width */
  height: 100%;
  background-repeat: no-repeat;
  background-size: cover;
  background-size: 1700px 100px;
  overflow: hidden;
}
.content {
  background-image: url("./assets/maxresdefault.jpg");
  background-size: cover;
  background-repeat: no-repeat;
  overflow: hidden;
}
</style>
