<template>
	<div class="countryNameContiner">
		<div class="countryName">{{ capitalize(countryName) }}</div>
	</div>
	<div>
		<img class="flagImage" :src="require(`../../assets/flags/${countryCode}.png`)">
	</div>
	<div>
		<img class="flagImage result" :src="imageData" />
	</div>
	<div>
	</div>
</template>

<script>
import resemble from "resemblejs";

export default {
	created() {
		const entry = require(`../../assets/flags/${this.countryCode}.png`)
		const correct = require(`../../assets/flags/${this.correctFlagCode}.png`)
		resemble.outputSettings({
			errorColor: {
				red: 0,
				green: 0,
				blue: 0,
			},
			errorType: "flat",
			transparency: 0,
			largeImageThreshold: 1200,
			useCrossOrigin: false,
			outputDiff: true,
		});

		resemble(entry)
			.compareTo(correct)
			.onComplete(data => {
				this.imageData = data.getImageDataUrl();
		});
	},
	props: [ 'countryName', 'countryCode', 'correctFlagCode'],
	data() {
		return {
			imageData: "",
		}
	},
	methods: {
		capitalize(string) {
			return string.split(" ").map(x => x[0].toUpperCase() + x.substring(1)).join(" ");
		}
	},
}
</script>

<style>
.flagImage {
	height: auto;
	width: 30vw;
	max-width: 500px;
	margin: 20px;
}
.flagImage.result {
	background-color: #B200ED;
}
.countryName {
	display: inline-block;
	width: auto;
}
.countryNameContiner {
	display: flex;
	justify-content: right;
}
.countryName {
	margin: auto 0;
	color: var(--color);
	font-weight: bold;
	font-size: 1.1em;
}
</style>
