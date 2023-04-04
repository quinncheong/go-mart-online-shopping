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

			<!-- if else authenticated | currently just shows user_email -->
			<v-btn v-if="isAuthenticated" class="white-15">
				{{ user_email }}
				<v-menu activator="parent">
					<v-list>
						<v-list-item>
							<v-list-item-title @click="logout">Sign-out</v-list-item-title>
						</v-list-item>
					</v-list>
				</v-menu>
			</v-btn>

			<v-btn v-else class="white-15" v-bind="props" @click="redirect"
				>Log-In / Sign-Up</v-btn
			>

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
import { getToken, setToken } from "@/api/cookie";

export default {
	name: "NavigationBar",
	data() {
		return {
			isAuthenticated: false,
			user_email: "",
		};
	},
	computed: {
		getNumItems() {
			return this.$store.getters.getNumCartItems;
		},
	},
	methods: {
		redirect() {
			// refresh redirect to cognito
			// const redirect_url = "https://gomartttt.store"
			const redirect_url = "http://localhost:3000";
			window.open(
				`https://gomart-welcome.auth.ap-southeast-1.amazoncognito.com/login?client_id=5gt59njjg9khu9a5o3dgq0uo68&response_type=token&scope=email+openid+phone&redirect_uri=${redirect_url}`,
				"_self"
			);
		},
		logout() {
			setToken("cognito-user-jwt", null);
			this.isAuthenticated = false;
			this.$router.push({ name: "Home" });
		},
	},
	mounted() {
		const token = getToken("cognito-user-jwt");
		if (!token) {
			// handle token expired or not there
			this.isAuthenticated = false;
		} else {
			// handle token authenticated
			this.isAuthenticated = true;
			this.user_email = token.email;
		}
	},
};
</script>
