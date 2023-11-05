<template>
  <div class="topline" style="position: relative;">
      <img class="pagetitle" alt="LC Dog Dante" src="./assets/logo.png">
      &nbsp;
      <h2 class="pagetitle" :style="$i18n.locale == 'zh'? 'font-size:29px;position: absolute;left: 70px;top: 1px;':'font-size:28px;position: absolute;left: 70px;top: 5px;'" style="display:inline;color: rgb(211, 55, 16);">{{$t(`DANTE THE DOG'S`)}}</h2>
      <h2 class="pagetitle" :style="$i18n.locale == 'zh'? 'font-size:29px;position: absolute;left: 100px;top: 37px;':'font-size:28px;position: absolute;left: 100px;top: 40px;'" style="display:inline;color: rgb(243, 218, 148);">{{$t(`Limbus Company Tools`)}}</h2>
      &nbsp;
      <b-button size="sm" class="locale-changer" type="submit" style="display:inline;color: #f2f2f2;cursor: pointer;position: absolute;right: 50px;top: 17px;" @click="$i18n.locale = 'en'">English</b-button>
      &nbsp;
      <b-button size="sm" class="locale-changer" type="submit" style="display:inline;color: #f2f2f2;cursor: pointer;position: absolute;right: 10px;top: 15px;" @click="$i18n.locale = 'zh'">中文</b-button>
  </div>

  <div class="topnav">
    <router-link :class="this.$route.path == '/'? 'active':''" :to="{name:'Home'}">{{$t(`Home`)}}</router-link>
    <router-link :class="this.$route.path == '/LCB/Thread'? 'active':''" :to="{name:'Thread'}">{{$t(`Thread`)}}</router-link>
    <router-link :class="this.$route.path == '/LCB/About'? 'active':''" :to="{name:'About'}">{{$t(`About`)}}</router-link>
  </div>
  <router-view/>
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
  color: #2c3e50;
}
img {
  margin: 0px;
  padding: 0px;
  width: 60px;
}
h2{
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

.topline{
  border-top: 3px solid rgb(211, 55, 16);
  overflow: hidden;
  background-image: url("./assets/K_Corp._Class_3_Excision_Staff_Hong_Lu_Full_Uptied.png");
  background-size: cover;
}
</style>
