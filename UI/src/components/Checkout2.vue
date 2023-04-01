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
				<v-card-title class="bold-30 mb-n5 ma-5">Order Summary</v-card-title>
				<v-card v-for="({ item, quantity }, i) in cart" :key="i" class="rounded-xl">
					<v-row class="ma-5">
						<v-col cols="2" class="d-flex flex-column">
							<v-img
								:src="item.item_image"
								position="left"
								contain
								max-height="200px"
								class="cursor"
							>
							</v-img>
						</v-col>
						<v-col class="d-flex flex-column">
							<v-card-title class="bold-30 cursor">
								{{ item.item_name }}
							</v-card-title>
							<v-card-subtitle class="text-left medium-20 mt-2 mb-n4">
								Platform: {{ item.item_platform }}
							</v-card-subtitle>
							<v-card-subtitle class="text-left medium-20 mt-2 mb-n4">
								$<span class="ml-n1">{{ Number(item.item_price).toFixed(2) }}</span>
							</v-card-subtitle>
							<v-spacer></v-spacer>
							<v-card-subtitle class="text-left medium-20 mt-2 mb-n4">
								Quantity: <span class="ml-n1">{{ quantity }}</span>
							</v-card-subtitle>
						</v-col>
					</v-row>
				</v-card>
				<v-card class="d-flex flex-column rounded-xl">
					<v-row class="ma-3">
						<div ref="cardElement" class="m-4 p-3 border border-secondary rounded bg-white"><!--Stripe.js injects the Card Element--></div>
					</v-row>
				</v-card>
				<v-card class="d-flex flex-column rounded-xl">
					<v-row>
						<v-col class="text-left mx-3">
							<v-card-subtitle class="medium-20">
								Total: ${{ total_price.toFixed(2) }}
							</v-card-subtitle>
						</v-col>
						<v-col class="text-right mx-3">
							<v-btn ref="placeOrder" class="ml-auto mt-2 buttons" rounded :disabled="stripeError" @click="placeOrder">
								Place Order
							</v-btn>
						</v-col>
					</v-row>
				</v-card>
				<v-card class="d-flex flex-column rounded-xl">
					<v-row>
						<div ref="stripeErrorElement" v-if="stripeError">
							{{ stripeErrorMessage }}
						</div>
					</v-row>
				</v-card>
			</v-col>
		</v-row>
	</div>
	<v-snackbar v-model="snackbar.on">
		{{ snackbar.message }}
		<template v-slot:action="{ attrs }">
			<v-btn color="white" text v-bind="attrs" @click="snackbar.on = false">
				Close
			</v-btn>
		</template>
	</v-snackbar>
</template>



<script setup>
import axios from "axios"
import { ref, onMounted, computed } from "vue"
import { useStore } from "vuex"
import { loadStripe } from "@stripe/stripe-js"
// import { StripeElements, StripeElement } from "vue-stripe-js"

const store = useStore() // to access vuex store
const stripe = ref(null) // stripe instance
const card = ref(null) // card instance
const cardElement = ref(null) // card element reference
const stripeError = ref(false) // have error = true
const stripeErrorMessage = ref("") // error message
const stripeErrorElement = ref(null) // error element

const user = ref(null)
const authState = ref(null)
const unsubscribeAuth = ref(null)
const name = ref("test_name")
const email = ref("test_email")
const addres = ref("test_address")
const number = ref("test_number")
const country = ref("test_country")

const cart = ref([
	{
		item: {
			item_id: "1",
			item_name: "Test",
			item_price: 10,
			item_image: "https://i.imgur.com/9YQ9Z9r.jpg",
			item_platform: "PC",
			item_stock: "10",
		},
		quantity: 1
	}
])
const no_stock = ref(false)
const total_price = ref(0)
const items = ref([])
const to = ref(null)
const snackbar = ref({ on: false, message: "" })

const formFields = ref([
	{
		type: "name",
		label: "Name",
		placeholder: "Enter Name",
		inputProps: { required: true },
	},
	{
		type: "username",
		label: "Username",
		placeholder: "Enter Username",
		inputProps: { required: true },
	},
	{
		type: "email",
		label: "Email",
		placeholder: "Enter Email",
		inputProps: { required: true },
	},
	{
		type: "password",
		label: "Password",
		placeholder: "Enter Password",
		inputProps: { required: true, autocomplete: "new-password" },
	},
	{
		type: "phone_number",
		label: "Phone Number",
		dialCode: "+65",
		placeholder: "Enter Phone Number",
		inputProps: { required: true },
	},
	{
		type: "custom:Country",
		label: "Country of Residence",
		placeholder: "Enter Country of Residence",
		inputProps: { required: true },
	},
	{
		type: "address",
		label: "Address",
		placeholder: "Enter Address",
		inputProps: { required: true },
	},
])


onMounted(async () => {
	stripe.value = await loadStripe(process.env.STRIPE_API_KEY)
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
	cart.value = store.state.cart
	getTotalPrice()
})


function activate() {}

function getTotalPrice() {
	total_price.value = 0
	cart.value.forEach(({ item, quantity }) => {
		total_price.value += item.item_price * quantity
	})
}

function getOrderDetails() {
	items.value = []
	cart.value.forEach(({ item, quantity }) => {
		items.value.push({ [item.item_name]: quantity })
	})
}

async function placeOrder() {
	const { PLACE_ORDER_BASEURL } = process.env
	getOrderDetails()
	const payload = {
		phone_number: number.value,
		user_name: name.value,
		email: email.value,
		items: items.value
	}
	console.log(payload)
	try {
		const { data } = await axios.post(`${PLACE_ORDER_BASEURL}/v1/place-order`, payload)
		console.log(data)
		snackbar.value.on = true
		snackbar.value.message = "Order successfully placed!"
		store.dispatch("clearCart")
	} catch (err) {
		console.error(err)
		snackbar.value.on = false
		snackbar.value.message = "There was an error placing your order, please try again later."
	}
}

// assuming this not needed
async function submitPayment() {
	const { error=null, paymentMethod=null } = await stripe.value.createPaymentMethod({
		type: "card",
		card: card.value,
		billing_details: {
			name: name.value,
			email: email.value,
			phone: number.value,
		},
	})
	if (error) {
		console.log(error)
		stripeError.value = true
		stripeErrorMessage.value = error.message
		return
	}
	console.log(paymentMethod)

	try {
		const res = await fetch()
	} catch (err) {}

}
</script>
