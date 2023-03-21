<template>
	<div>
		<v-app-bar color="#5ba4a3" dense height="120" elevation="0">
			<v-btn to="/" :ripple="false" plain>
				<v-img
					class="mx-8"
					src="@/assets/shopLogo.jpg"
					max-height="100"
					max-width="100"
				></v-img>
				<v-toolbar-title>
					<h1 class="navbar-title">Go Mart</h1>
				</v-toolbar-title>
			</v-btn>
			<v-spacer></v-spacer>
			<v-badge overlap class="mx-5" color="#efcfda">
				<span slot="badge" class="bold-15">{{ getNumItems }}</span>
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
			// return this.$store.getters.getNumItemsInCart;
			return 30;
		},
	},
};
</script>
