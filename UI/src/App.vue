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

const url = new URL(window.location.href.replace("#", "?"))
const idToken = url.searchParams.get("id_token")

if (idToken) {
	// console.log(idToken);
	document.cookie="idtoken=" + idToken;
	// const base64Url = document.cookie.split('.')[1];
	// const base64 = base64Url.replace('-', '+').replace('_', '/');
	// const parsedJWT = JSON.parse(atob(base64));
	// console.log(parsedJWT) // cookie key thing
	// window.localStorage.setItem("cognito-user-jwt", JSON.stringify(parsedJWT)) // for easier testing purposes
}
</script>
