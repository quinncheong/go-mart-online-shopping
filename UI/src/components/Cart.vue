<template>
	<div class="text-center">
		<v-container fluid class="my-4">
			<v-card v-if="isCartEmpty">
				<v-card-title
					><router-link :to="{ path: `/` }">
						Your cart is empty! Head back to the home page to browse through
						items!
					</router-link>
				</v-card-title>
			</v-card>
			<v-card v-for="(item, i) in cart" :key="i" class="rounded-xl my-3">
				<v-row class="ma-5">
					<v-col cols="2" class="d-flex flex-column">
						<v-img
							:src="item.item.item_image"
							position="left"
							contain
							max-height="200px"
							class="cursor"
							@click="showItem(item.item.item_name)"
						>
						</v-img>
					</v-col>
					<v-col class="d-flex flex-column">
						<v-card-title
							class="bold-30 cursor"
							@click="showItem(item.item.item_name)"
						>
							{{ item.item.item_name }}
						</v-card-title>
						<v-card-subtitle class="text-left mt-2 mb-n4">
							<span class="ml-n1 medium-20">
								Platform: {{ item.item.item_platform }}
							</span>
						</v-card-subtitle>
						<v-spacer></v-spacer>
						<v-card-subtitle class="text-left medium-20 mt-2 mb-n4">
							<span class="ml-n1 medium-15">
								${{ Number(item.item.item_price).toFixed(2) }}
							</span>
						</v-card-subtitle>
						<v-spacer></v-spacer>
						<v-card-actions class="ml-auto">
							<v-btn outlined class="v-btn" icon @click="handleMinus(item.item)"
								><v-icon color="#5ba4a3">mdi-minus</v-icon></v-btn
							>
							<v-card-subtitle>
								<span class="medium-15">{{ item.quantity }}</span>
							</v-card-subtitle>
							<v-btn outlined class="v-btn" icon @click="handlePlus(item.item)"
								><v-icon color="#5ba4a3">mdi-plus</v-icon></v-btn
							>
						</v-card-actions>
					</v-col>
				</v-row>
			</v-card>
			<v-card class="d-flex flex-column rounded-xl" v-if="!isCartEmpty">
				<v-row class="align-center">
					<v-col class="text-left mx-3">
						<v-card-subtitle>
							<span class="medium-20">Total: ${{ total_price.toFixed(2) }}</span>
						</v-card-subtitle>
					</v-col>
					<v-col class="text-right mx-3 my-3">
						<v-btn class="ml-auto buttons" rounded to="/checkout">
							Checkout
						</v-btn>
					</v-col>
				</v-row>
			</v-card>
			<v-snackbar v-model="no_stock">
				No additional stock available for this item!
				<template v-slot:action="{ attrs }">
					<v-btn color="white" text v-bind="attrs" @click="no_stock = false">
						Close
					</v-btn>
				</template>
			</v-snackbar>
		</v-container>
	</div>
</template>

<script>
// import { getToken } from "@/api/cookie"

export default {
	name: "Cart",
	data() {
		return {
			cart: [],
			no_stock: false,
			total_price: 0,
		};
	},
	methods: {
		handleMinus(item) {
			const cartItem = this.cart.find(
				(cartItem) => cartItem.item.item_name === item.item_name
			);
			this.$store.dispatch("decrementItemInCartQuantity", cartItem.item);
			this.getTotalPrice();
		},
		handlePlus(item) {
			const cartItem = this.cart.find(
				(cartItem) => cartItem.item.item_name === item.item_name
			);
			if (item.item_stock > 1) {
				this.$store.dispatch("incrementItemInCartQuantity", cartItem.item);
			} else {
				this.no_stock = true;
			}
			this.getTotalPrice();
		},
		showItem(name) {
			this.$router.push({
				name: "Item",
				query: { item_name: name },
			});
		},
		getTotalPrice() {
			this.total_price = 0;
			this.cart.forEach((item) => {
				this.total_price += item.item.item_price * item.quantity;
			});
			this.total_price = Math.round(this.total_price * 100) / 100;
		},
	},
	computed: {
		isCartEmpty() {
			return this.cart.length > 0 ? false : true;
		},
	},
	mounted() {
		this.cart = this.$store.getters.getItems;
		this.getTotalPrice();
		// const token = getToken("cognito-user-jwt")
		// if (!token) {
		// 	alert("Authentication required to access cart")
		// 	this.$router.push({ name: "Home" })
		// }
	},
};
</script>

<style scoped>
.v-btn {
	min-width: 0;
}
</style>
