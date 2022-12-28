<template>
	<GameView/>
</template>

<script>
import GameView from "./components/GameView.vue";

// <img src="../assets/flags/svg/au.svg"/>
// <img :src="require(`@/assets/${footerItem.icon}`)">

export default {
  name: 'App',
  components: {
	  GameView,
  },
}
</script>

<style>
html, body {
	padding: 0 50px;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
