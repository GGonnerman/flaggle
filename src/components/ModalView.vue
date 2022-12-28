<template>
	<div class="backdrop" @click.self="dontcloseModal">
		<div class="modal">
			<h3 v-if="guesses">You Win!</h3>
			<h3 v-else>Nice Try!</h3>
			<p>The correct country was {{ correctCountry }}</p>
			<p v-if="guesses">It took you {{ guesses }} guesses!</p>
			<img class="flagImage" :src="require(`../../assets/flags/${correctFlagCode}.png`)">
			<button ref="closeButton" @click="closeModal" class="closeButton">Close</button>
		</div>
	</div>
</template>

<script>
export default {
	props: [ "correctCountry", "correctFlagCode", "guesses" ],
	methods: {
		closeModal() {
			this.$emit("closeModal");
		}
	},
	mounted() {
		this.$refs.closeButton.focus()
	},
}
</script>

<style>
.backdrop {
	top: 0;
	left: 0;
	position: fixed;
	background: rgba(0, 0, 0, 0.5);
	width: 100%;
	height: 100%;
	display: flex;
	justify-content: center;
	align-items: center;
}
.modal {
	width: 500px;
	margin: 100px auto;
	padding: 20px 0;
	background: var(--color);
	border-radius: 10px;
}
.modal img {
	width: 90%;
	margin: 20px;
}
.modal * {
	color: var(--background-color);
}
.closeButton {
	width: 90%;
	color: black;
	font-weight: bold;
	margin: 0 auto;
}
</style>
