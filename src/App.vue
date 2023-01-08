<template>
	<GameView/>
</template>

<script>
import GameView from "./components/GameView.vue";

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
  margin-top: 20px;
}
</style>
