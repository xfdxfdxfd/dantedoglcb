<template>
  <div class="topline">
      <img class="pipe" alt="LC Dog Dante" src="./assets/logo.png">
      &nbsp;
      <h1 class="pipe2" style="display:inline;color: rgb(236, 236, 236)">Limbus Company Tools For</h1>
      <h1 class="pipe2" style="display:inline;color: rgb(249, 87, 47)">DANTE THE DOG</h1>
  </div>

  <div class="topnav">
    <template v-if="this.$route.path == '/LCB/Home'"><router-link class="active" :to="{name:'Home'}">Home</router-link></template>
    <template v-else><router-link :to="{name:'Home'}">Home</router-link></template>
    <template v-if="this.$route.path == '/LCB/About'"><router-link class="active" :to="{name:'About'}">About</router-link></template>
    <template v-else><router-link :to="{name:'About'}">About</router-link></template>
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
  width: 50px;
}
h1{
  margin: 0px;
  padding: 0px;
  border-top-width: 0px;
  border-right-width: 0px;
  border-bottom-width: 0px;
  border-left-width: 0px;
}
.pipe {
  padding: 5px;
}
.pipe2 {
  padding: 5px;
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
