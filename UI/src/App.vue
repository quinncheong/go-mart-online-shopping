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
import { decodeToken, retrieveCookie } from "@/api/cookie"

const url = new URL(window.location.href.replace("#", "?"))
const idToken = url.searchParams.get("id_token")
document.cookie = `idtoken=${idToken}`; // if token doesn't exist, will be "idtoken=null"

// if idtoken is not undefined
if (idToken) {
	const token = decodeToken(idToken)
	window.localStorage.setItem("cognito-user-jwt", JSON.stringify(token)) // for easier testing purposes
	console.log(token)// need to check exp for expiry, email for email
	console.log(retrieveCookie("idToken"))
} 
// else {
// 	const cookie = retrieveCookie("idtoken")
// 	if (!cookie) window.localStorage.removeItem("cognito-user-jwt")
// 	else window.localStorage.setItem("cognito-user-jwt", JSON.stringify(cookie))
// }
</script>
