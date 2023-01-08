<template>
	<div class="header">
		<div v-if="!isDaily" class="toggleDifficultyContainer">
			<button class="toggleDifficulty" @click="cycleDifficulty" :class="{easy: currentDifficulty === Difficulty.EASY, medium: currentDifficulty === Difficulty.MEDIUM, hard: currentDifficulty === Difficulty.HARD}">{{ currentDifficulty }}</button>
		</div>
		<div class="welcomeMessage">
			<h3>Welcome to Flags
				<div class="modeContainer" @click="switchMode()">
					<span class="mode daily" v-if="isDaily">Daily</span>
					<span class="mode unlimited" v-else>Unlimited</span>!
				</div>
			</h3>
		</div>
		<div v-if="!gameOver" class="giveUpContainer">
			<button class="giveUp" @click="giveUp">I Give Up</button>
		</div>
	</div>
	<form @submit.prevent="submitFlag" v-if="!gameOver">
		<input placeholder="Input country/territory name..." type="search" list="country" v-model="countryEntry" @keyup="countryEntryChange" >
		<datalist id="country">
			<option v-for="countryName in remainingCountries" :value="countryName" :key="countryName" />
		</datalist>
	</form>
	<div v-if="gameOver && !showModal">
		<h5 v-if="userWon">You won in {{ entries.length }} guesses...</h5>
		<button v-if="this.isDaily" @click="switchMode">Play unlimited?</button>
		<button v-else @click="restartGame">Try Again?</button>
	</div>
	<div v-if="showModal">
	<ModalView v-if="userWon" @closeModal="closeModal" :correctCountry="correctCountry" :correctFlagCode="countries[correctCountry]['code']" :guesses="entries.length" />
	<ModalView v-else @closeModal="closeModal" :correctCountry="correctCountry" :correctFlagCode="countries[correctCountry]['code']" />
	</div>
	<div class="countryCardContainer">
		<CountryCard v-for="country in entries" :key="countries[country]['code']" :countryName="country" :countryCode="countries[country]['code']" :correctFlagCode="countries[correctCountry]['code']" />
	</div>
	<div>
		Credits go to <a href="https://ducc.pythonanywhere.com/flaggle/" target="_blank">Duc Vu's original site</a> for the idea and <a href="https://github.com/lipis/flag-icons" target="_blank">Lipis' flag-icons</a> the (original) images!
	</div>
</template>

<script>
import all_countries from "../countries.json";
import pairs from "../pairs.json";
import CountryCard from "./CountryCard.vue";
import ModalView from "./ModalView.vue";
import Difficulty from "../enums/Difficulty.js";

export default {
	components: {
		CountryCard,
		ModalView,
	},
	data() {
		return {
			countryEntry: "",
			all_countries: {},
			entries: [],
			correctCountry: "",
			gameOver: false,
			userWon: false,
			showModal: false,
			isDaily: true,
			Difficulty: Difficulty,
			currentDifficulty: Difficulty.EASY,
		}
	},
	methods: {
		confirmChange() {
			if(this.entries.length > 0 && !this.gameOver) {
				return confirm('Changing difficulty will end the current game. Continue?');
			}
			return true;
		},
		cycleDifficulty() {
			if(!this.confirmChange()) return;
			if(this.currentDifficulty === Difficulty.EASY) {
				this.currentDifficulty = Difficulty.MEDIUM;
			} else if(this.currentDifficulty === Difficulty.MEDIUM) {
				this.currentDifficulty = Difficulty.HARD;
			} else if(this.currentDifficulty === Difficulty.HARD) {
				this.currentDifficulty = Difficulty.EASY;
			}
			this.restartGame();
		},
		countryEntryChange() { },
		giveUp() {
			this.gameOver = true;
			this.showModal = true;
			this.userWon = false;
			this.entries.unshift(this.correctCountry);
		},
		switchMode() {
			if(!this.confirmChange()) return;
			this.isDaily = !this.isDaily;
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
				} else {
					for(let i = 0; i < this.pairs.length; i++) {
						if(this.pairs[i].includes(this.countries[this.correctCountry]['code']) && this.pairs[i].includes(this.countries[countryName]['code'])) {
							this.gameOver = true;
							this.showModal = true;
							this.userWon = true;
						}
					}
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
		countries() {
			let required_population = -1 // No limit for population (Hard mode)
			if(this.currentDifficulty === Difficulty.EASY) {
				required_population = 1000000 * 20; // 20 million
			} else if(this.currentDifficulty === Difficulty.MEDIUM) {
				required_population = 1000000 * 5; // 5 million
			}

			if(this.isDaily) {
				return this.all_countries;
			} else {
				return Object.keys(this.all_countries).reduce((filtered, key) => {
					if (this.all_countries[key]['population'] > required_population) filtered[key] = this.all_countries[key];
					return filtered;
				}, {});
			}
		},
		remainingCountries() {
			// Only allow countries that have the correct start/end after x guesses
			//const helpLength = Math.floor(this.entries.length / 5);
			//const correctEnd = this.correctCountry.substr(this.correctCountry.length - helpLength, helpLength);
			//const correctStart = this.correctCountry.substr(0, Math.floor(this.entries.length / 5));
			//return Object.keys(this.countries).filter(country => !this.entries.includes(country) && country.endsWith(correctEnd));

			// Do not allow people to repeat countries
			return Object.keys(this.countries).filter(country => !this.entries.includes(country));
		}
	},
	mounted() {
		this.all_countries = all_countries;
		this.pairs = pairs;
		this.correctCountry = this.selectRandomCountry();
	},
}
</script>

<style>
.header {
	display: grid;
	grid-template-columns: 1fr 2fr 1fr;
	align-items: center;
	padding-bottom: 20px;
}
.header button {
	width: auto;
	font-weight: bold;
	border: none;
}

.header button:hover {
	filter: brightness(1.1);
}

.toggleDifficultyContainer {
	grid-column: 1;
}

.toggleDifficultyContainer button {
	margin: 0 auto 0 0;
}

.toggleDifficulty.easy {
	background-color: rgb(3, 125, 80);
}
.toggleDifficulty.medium {
	background-color: rgb(141, 141, 0);
}
.toggleDifficulty.hard {
	background-color: rgb(123, 13, 30);
}
.welcomeMessage {
	grid-column: 2;
}
.welcomeMessage h3 {
	margin: 0;
}
.giveUpContainer {
	grid-column: 3;
}
.giveUp {
	background-color: rgb(123, 13, 30);
	margin: 0 0 0 auto;
}
.countryCardContainer {
	display: grid;
	grid-template-columns: calc(20vw - 140px) calc(30vw + 40px) calc(30vw + 40px) calc(20vw - 140px);
}
.mode {
	color: var(--background-color);
	border-radius: 5px;
	padding: 2px 6px;
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
	background-color: rgb(3, 125, 80);
}
.mode:hover {
	filter: brightness(1.1);
} 
</style>
