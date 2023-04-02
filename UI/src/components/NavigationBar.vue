<template>
	<div>
		<v-app-bar color="#5ba4a3" dense height="120" elevation="0">
			<router-link to="/" class="d-flex align-center">
				<img src="@/assets/shopLogo.jpg" class="mx-4" alt="shop_logo_jpg" width="100">
				<v-toolbar-title>
					<h1 class="navbar-title">Go Mart</h1>
				</v-toolbar-title>
			</router-link>
			<v-spacer></v-spacer>
			<v-btn class="white-15" @click="redirect">Log-In / Sign-Up</v-btn>
			<v-btn></v-btn>
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
		popup() {
			// pop up window -- redirects to cognito
			const popupWidth = 600;
			const popupHeight = 400;
			const left = (window.innerWidth - popupWidth) / 2;
			const top = (window.innerHeight - popupHeight) / 3;
			const loginPopup = window.open(
				'https://gomart-welcome.auth.ap-southeast-1.amazoncognito.com/login?client_id=5gt59njjg9khu9a5o3dgq0uo68&response_type=token&scope=email+openid+phone&redirect_uri=https%3A%2F%2Fgomartttt.store',
				'loginPopup',
				`width=${popupWidth}, height=${popupHeight}, left=${left}, top=${top}, resizable=yes, scrollbars=yes`
			);
			if (window.focus) loginPopup.focus(); // just in case
		},
		redirect() {
			// refresh redirect to cognito
			window.open("https://gomart-welcome.auth.ap-southeast-1.amazoncognito.com/login?client_id=5gt59njjg9khu9a5o3dgq0uo68&response_type=token&scope=email+openid+phone&redirect_uri=http%3A%2F%2Flocalhost:3000", "_self")
		},
	},
};
</script>
