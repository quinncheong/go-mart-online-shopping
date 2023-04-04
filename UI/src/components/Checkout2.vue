<template>
	<div class="mt-10">
		<v-row>
			<v-col cols="4">
				<v-card-title class="bold-30 mb-n5 ma-5">
					Shipping Information
				</v-card-title>
				<v-card class="rounded-xl ma-5">
					<v-card-title>Name: {{ name }}</v-card-title>
					<v-card-title>Email: {{ email }}</v-card-title>
					<v-card-title>Number: {{ number }}</v-card-title>
					<v-card-title>Address: {{ address }}</v-card-title>
				</v-card>
			</v-col>
			<v-col cols="7">
				<v-card-title class="bold-30 my-3">Order Summary</v-card-title>
				<v-card v-for="({ item, quantity }) in store.getters.getItems" :key="item.id" class="rounded-xl mb-3">
					<v-row class="ma-5">
						<v-col cols="2" class="d-flex flex-column">
							<v-img
								:src="item.item_image"
								position="left"
								contain
								max-height="200px"
								class="cursor"
							></v-img>
						</v-col>
						<v-col class="d-flex flex-column">
							<v-card-title class="bold-30 cursor">{{ item.item_name }}</v-card-title>
							<v-card-subtitle class="text-left mt-1">
								<span class="medium-20 mt-2">Platform: {{ item.item_platform }}</span>
							</v-card-subtitle>
							<v-spacer></v-spacer>
							<v-card-subtitle class="text-left mt-1">
								<span class="medium-20 mt-2">${{ Number(item.item_price).toFixed(2) }}</span>
							</v-card-subtitle>
							<v-spacer></v-spacer>
							<v-card-subtitle class="text-left mt-1">
								<span class="medium-20 mt-2">Quantity: {{ quantity }}</span>
							</v-card-subtitle>
						</v-col>
					</v-row>
				</v-card>
				<v-card class="d-flex flex-column rounded-xl my-3">
					<v-row class="align-center">
						<v-col class="mx-3 my-3">
							<div ref="cardElement" class="m-4 p-3 border border-secondary rounded bg-white"><!--Stripe mounts Card Element--></div>
						</v-col>
					</v-row>
				</v-card>
				<v-card class="d-flex flex-column rounded-xl my-3">
					<v-row class="align-center">
						<v-col class="text-left mx-3 my-3">
							<v-card-subtitle>
								<span class="medium-20">Total: ${{ total_price.toFixed(2) }}</span>
							</v-card-subtitle>
						</v-col>
						<v-col class="text-right mx-3 my-3">
							<v-btn :loading="loading" class="ml-auto buttons" rounded @click="placeOrder">Place Order</v-btn>
						</v-col>
					</v-row>
				</v-card>
				<v-card class="d-flex flex-column rounded-xl">
					<v-row v-if="stripeError.err">
						<v-col>
							<v-card-subtitle>{{ stripeError.message }}</v-card-subtitle>
						</v-col>
					</v-row>
				</v-card>
			</v-col>
		</v-row>
	</div>
	<v-snackbar v-model="snackbar.on">{{ snackbar.message }}
		<template v-slot:action="{ attrs }">
			<v-btn color="white" text v-bind="attrs" @click="snackbar.on = false">Close</v-btn>
		</template>
	</v-snackbar>
</template>



<script setup>
import { ref, onMounted, computed } from "vue"
import { useStore } from "vuex"
import { useRouter } from "vue-router"
import { loadStripe } from "@stripe/stripe-js"
import { getToken } from "@/api/cookie"
import { placeOrderCheckout } from "@/api/placeOrderService"

const token = getToken("cognito-user-jwt")

const store = useStore() // to access vuex store
const router = useRouter() // to access vue-router
const stripe = ref(null) // stripe instance
const card = ref(null) // card instance
const cardElement = ref(null) // card element reference
const stripeError = ref({	err: false, message: "no error" }) // have error = true

const name = ref("test_name")
const email = ref(token.email ?? "test_name@gmail.com")
const address = ref("00 Test Avenue")
const number = ref("00000000")

const cart = computed(() => store.getters.getItems)
const total_price = computed(() => {
	let total = 0
	cart.value.forEach(({ item, quantity }) => {
		total += item.item_price * quantity
	})
	return total
})
console.log(cart.value)
// const no_stock = ref(false)
const items = computed(() => cart.value.map(({ item, quantity }) => ({ [item.id]: quantity })))
// const to = ref(null)
const snackbar = ref({ on: false, message: "" })
const loading = ref(false)



async function placeOrder() {
	console.log("card:", card.value)
	loading.value = true

	// creating the card to send to the api (not sure if this is still wanted or not)
	const { error=null, paymentMethod=null } = await stripe.value.createPaymentMethod({
		type: "card",
		card: card.value,
	})

	if (error) {
		console.log(error)
		stripeError.value.err = true
		stripeError.value.message = error.message
		loading.value = false
		return
	}
	console.log(paymentMethod)
	stripeError.value.err = false
	stripeError.value.message = "no error"

	try {
		const payload = {
			order_data: {
				product_ids: items.value, // [{ id: quantity }, { id: quantity }]
				email: email.value, // ""
			},
			payment_data: {
				payment_method_id: paymentMethod.id,
				amount: total_price.value * 100, // in cents
			},
		}

		console.log(payload)

		const data = await placeOrderCheckout(payload)
		console.log(data)
		snackbar.value.on = true
		snackbar.value.message = "Order successfully placed!"
		card.value.unmount()
		store.dispatch("clearCart")
		setTimeout(() => {
			router.push({ name: "Home" })
		}, 1000)
	} catch (err) {
		console.log(err)
		snackbar.value.on = true
		snackbar.value.message = "There was an error placing your order, please try again later."
	}
	setTimeout(() => {
		snackbar.value.on = false
	}, 2000)
	loading.value = false
}

onMounted(async () => {
	console.log(cart.value)
	stripe.value = await loadStripe(process.env.STRIPE_PUBLISHABLE)
	const elements = stripe.value.elements()
	card.value = elements.create("card", {
		hidePostalCode: true,
		value: '4242424242424242', // attempt to add defaults (not working)
		style: {
			base: {
				iconColor: "#202020",
				color: "#202020",
				fontWeight: "500",
				fontFamily: "Roboto, Open Sans, Segoe UI, sans-serif",
				fontSize: "16px",
				fontSmoothing: "antialiased",
				":-webkit-autofill": {
					color: "#202020",
				},
				"::placeholder": {
					color: "#202020",
				},
			},
			invalid: {
				iconColor: "#B22222",
				color: "#B22222",
			},
		},
	})
	card.value.mount(cardElement.value)
})
</script>
