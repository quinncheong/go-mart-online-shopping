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
import NavigationBar from "@/components/NavigationBar.vue";
import { getCookie, decodeToken } from "@/api/cookie"

const url = new URL(window.location.href.replace("#", "?"))
const idToken = url.searchParams.get("id_token")

if (idToken) {
	document.cookie = `idtoken=${idToken}`;
	const token = decodeToken(getCookie("idtoken"))
	window.localStorage.setItem("cognito-user-jwt", JSON.stringify(token)) // for easier testing purposes
	console.log(token)// need to check exp for expiry, email for email
}
</script>
