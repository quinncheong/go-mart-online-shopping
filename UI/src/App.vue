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
const getIdToken = () => { const modifiedUrl = window.location.href.replace("#", "?")
	const url = new URL(modifiedUrl)
	return url.searchParams.get("id_token")
}
const idToken = getIdToken()
console.log(idToken);
document.cookie="idtoken=" + idToken;

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
