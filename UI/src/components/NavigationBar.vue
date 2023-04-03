<template>
	<div>
		<v-app-bar color="#5ba4a3" dense height="120" elevation="0">
			<router-link to="/" class="d-flex align-center">
				<img
					src="@/assets/GoMart-Logo.png"
					class="mx-4"
					alt="shop_logo_jpg"
					width="100"
				/>
				<v-toolbar-title>
					<h1 class="navbar-title">Go Mart</h1>
				</v-toolbar-title>
			</router-link>
			<v-spacer></v-spacer>
			<v-btn class="white-15" @click="popup">Log-In / Sign-Up</v-btn>
			<v-btn class="white-15"></v-btn>
			<v-badge overlap class="mx-8" color="#efcfda">
				<template v-slot:badge>
					<span class="bold-15">{{ getNumItems }}</span>
				</template>
				<v-btn icon to="/cart">
					<v-icon large color="#FFFFFF">mdi-cart</v-icon>
				</v-btn>
			</v-badge>
		</v-app-bar>
	</div>
</template>

<script>
import { retrieveCookie } from "@/api/cookie"

export default {
	name: "NavigationBar",
	data() {
		return {};
	},
	computed: {
		getNumItems() {
			return this.$store.getters.getNumCartItems;
		},
	},
	methods: {
		redirect() {
			// refresh redirect to cognito
			window.open(
				"https://gomart-welcome.auth.ap-southeast-1.amazoncognito.com/login?client_id=5gt59njjg9khu9a5o3dgq0uo68&response_type=token&scope=email+openid+phone&redirect_uri=https://gomartttt.store",
				"_self"
			);
		},
	},
	mounted() {
		
	},
};
</script>
