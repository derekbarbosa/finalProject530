<template>
  <img alt="Vue logo" src="./assets/TTY.png">
  <HelloWorld msg="Enter Your Destination"/>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
//import SearchBar from './components/SearchBar.vue'
//import BudgetBar from './components/BudgetBar.vue'

export default {
  name: 'App',
  components: {
    HelloWorld
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
