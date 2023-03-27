<template>
	<v-app style="background: #faf8f7">
		<NavigationBar />
		<div class="container pa-5 mt-5">
			<v-content>
				<router-view />
			</v-content>
		</div>
	</v-app>
</template>

<script setup>
import HelloWorld from "@/components/HelloWorld.vue";
import NavigationBar from "@/components/NavigationBar.vue";
import Items from "@/components/Items.vue";
import Checkout from "@/components/Checkout.vue";
</script>

<script>
export default {
	name: "App",
	components: {
		NavigationBar,
		HelloWorld,
		Items,
		Checkout,
	},
};
</script>
