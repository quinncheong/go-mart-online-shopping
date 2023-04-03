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
import { setToken, decodeToken, getToken } from "@/api/cookie"

const url = new URL(window.location.href.replace("#", "?"))
const idToken = url.searchParams.get("id_token")
document.cookie = `idtoken=${idToken}`; // if token doesn't exist, will be "idtoken=null"

console.log(idToken)

if (idToken) {
	const token = decodeToken(idToken) // decode the URI
	setToken("cognito-user-jwt", token) // might be null, or an actual token, idk, we'll do checks later lmao
	console.log("cognito-user-jwt", token)
} else {
	const token = getToken("cognito-user-jwt")
	if (!token) {
		setToken("cognito-user-jwt", null)
	}
	// no need to change token :D
}


</script>
