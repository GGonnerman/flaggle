<template>
	<h3>Welcome to Flaggle
		<div class="modeContainer" @click="switchMode()">
			<span class="mode daily" v-if="isDaily">Daily</span>
			<span class="mode unlimited" v-else>Unlimited</span>!
		</div>
	</h3>
	<div v-if="!gameOver" class="giveUpContainer">
		<button class="giveUp" @click="giveUp">I Give Up</button>
	</div>
	<form @submit.prevent="submitFlag" v-if="!gameOver">
		<input placeholder="Input country/territory name..." type="search" list="country" v-model="countryEntry" @keyup="countryEntryChange" >
		<datalist id="country">
			<option v-for="countryName in remainingCountries" :value="countryName" :key="countryName" />
		</datalist>
	</form>
	<div v-if="gameOver && !showModal">
		<h5 v-if="userWon">You won in {{ entries.length }} guesses...</h5>
		<button v-if="this.isDaily" @click="startUnlimited">Play unlimited?</button>
		<button v-else @click="restartGame">Try Again?</button>
	</div>
	<div v-if="showModal">
	<ModalView v-if="userWon" @closeModal="closeModal" :correctCountry="correctCountry" :correctFlagCode="countries[correctCountry]" :guesses="entries.length" />
	<ModalView v-else @closeModal="closeModal" :correctCountry="correctCountry" :correctFlagCode="countries[correctCountry]" />
	</div>
	<div class="countryCardContainer">
		<CountryCard v-for="country in entries" :key="countries[country]" :countryName="country" :countryCode="countries[country]" :correctFlagCode="countries[correctCountry]" />
	</div>
	<div>
		Credits go to <a href="https://ducc.pythonanywhere.com/flaggle/" target="_blank">Duc Vu's original site</a> for the idea and the images!
	</div>
</template>

<script>
import countries from "../countries.json";
import CountryCard from "./CountryCard.vue";
import ModalView from "./ModalView.vue";

export default {
	components: {
		CountryCard,
		ModalView,
	},
	data() {
		return {
			countryEntry: "",
			countries: {},
			entries: [],
			correctCountry: "",
			gameOver: false,
			userWon: false,
			showModal: false,
			isDaily: true,
		}
	},
	methods: {
		countryEntryChange() { },
		giveUp() {
			this.gameOver = true;
			this.showModal = true;
			this.userWon = false;
			this.entries.unshift(this.correctCountry);
		},
		switchMode() {
			this.isDaily = !this.isDaily;
			this.restartGame();
		},
		startUnlimited() {
			this.isDaily = false;
			this.restartGame();
		},
		restartGame() {
			this.entries = [];
			this.showModal = false;
			this.userWon = false;
			this.gameOver = false;
			this.correctCountry = this.selectRandomCountry();
		},
		closeModal() {
			this.showModal = false;
		},
		submitFlag() {
			const countryName = this.countryEntry.toLowerCase();
			if (this.remainingCountries.includes(countryName)) {
				this.entries.unshift(countryName);
				this.countryEntry = "";
				if (countryName === this.correctCountry) {
					this.gameOver = true;
					this.showModal = true;
					this.userWon = true;
				}
			}
		},
		selectRandomCountry() {
			const keys = Object.keys(this.countries);
			let randomCountry = "";
			if(this.isDaily) {
				// Get the number of days since start of unix time for seeding
				const start = new Date(1970, 0, 1);
				const now = new Date;
				let daysSince = Math.floor((now - start) / ( 1000 * 60 * 60 * 24));

				// Seed to 0-1
				let seed = Math.sin(daysSince++) * 10000;
				seed = seed - Math.floor(seed);

				randomCountry = keys[ Math.round( keys.length * seed ) ];
			} else {
				randomCountry = keys[ Math.round( keys.length * Math.random() ) ];
			}
			return randomCountry;
		},
	},
	computed: {
		  remainingCountries() {
			  const helpLength = Math.floor(this.entries.length / 5);
			  const correctEnd = this.correctCountry.substr(this.correctCountry.length - helpLength, helpLength);
			  //const correctStart = this.correctCountry.substr(0, Math.floor(this.entries.length / 5));
			  return Object.keys(this.countries).filter(country => !this.entries.includes(country) && country.endsWith(correctEnd));
		  }
	},
	mounted() {
		this.countries = countries;
		this.correctCountry = this.selectRandomCountry();
		this.entries.unshift("spain");
	},
}
</script>

<style>
.giveUpContainer {
	width: 100%;
}
.giveUp {
	background-color: rgb(123, 13, 30);
	font-weight: bold;
	border: none;
	width: auto;
	margin: 0 0 20px auto;
}
.countryCardContainer {
	display: grid;
	grid-template-columns: calc(20vw - 140px) calc(30vw + 40px) calc(30vw + 40px) calc(20vw - 140px);
}
.mode {
	color: var(--background-color);
	border-radius: 5px;
	padding: 3px;
	margin: 2px 3px;
	cursor: pointer;
}
.modeContainer {
	display: inline;
}
.mode.daily {
	background-color: var(--color);
}
.mode.unlimited {
	background-color: var(--ins-color);
}
.mode:hover {
    background-color: var(--h6-color);
} 
</style>
