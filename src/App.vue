<template>
  <div class="topline">
      <img class="pipe" alt="LC Dog Dante" src="./assets/logo.png">
      &nbsp;
      <h1 class="pipe2" style=display:inline>LIMBUS COMPANY SITE FOR DOG DANTE</h1>
  </div>

  <div class="topnav">
    <router-link class="active" :to="{name:'Home'}">Home</router-link>
    <router-link :to="{name:'About'}">About</router-link>
  </div>
  <router-view/>
</template>

<script>
// import LimbusCompany from './components/LimbusCompany.vue'

export default {
  name: 'App',
  components: {
    // LimbusCompany
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
}
</style>
