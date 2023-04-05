<template>
	<div class="text-center">
		<v-container fluid class="mt-5">
			<v-card class="d-flex flex-column rounded-xl">
				<v-row class="ma-5">
					<v-col cols="3" class="d-flex flex-column">
						<v-img :src="item_image" position="left" contain max-height="500px">
						</v-img>
					</v-col>
					<v-col class="d-flex flex-column">
						<v-card-title>
							<h3>{{ item_name }}</h3>
						</v-card-title>
						<v-card-subtitle class="text-left mt-2 mb-n4">
							<span class="medium-15">Platform: {{ item_platform }}</span>
						</v-card-subtitle>

						<v-spacer />

						<v-card-subtitle class="text-left mt-2 mb-n4">
							<span class="ml-n1 medium-15"> ${{ item_price }} </span>
						</v-card-subtitle>

						<v-spacer />

						<v-card-subtitle class="text-left">
							<span class="medium-15">Description:</span>
						</v-card-subtitle>

						<v-spacer />

						<v-card-subtitle class="text-left mt-n5">
							<span class="medium-15">{{ item_desc }}</span>
						</v-card-subtitle>

						<v-spacer />

						<v-card-actions class="ml-auto">
							<v-btn class="bg-black" rounded v-if="availableStock">
								<v-card-subtitle @click="handleAddToCart()">
									<span class="white-15">Add to Cart</span>
								</v-card-subtitle>
								<v-icon color="white">mdi-plus</v-icon>
							</v-btn>
							<v-card>
								<v-card-subtitle v-if="!availableStock" rounded class="mx-auto">
									Out of Stock
								</v-card-subtitle>
							</v-card>
						</v-card-actions>
					</v-col>
				</v-row>
			</v-card>
		</v-container>
	</div>
</template>

<script>
import { getItemById } from "@/api/itemService";
import { getRecommendedItems } from "@/api/placeOrderService";
import placeholder from "@/assets/placeholder.jpg";
import { getToken } from "@/api/cookie"

export default {
	name: "Item",
	data() {
		return {
			id: this.$route.query.id,
			item_name: this.$route.query.item_name,
			item_price: 100,
			item_desc: "",
			item_image: "",
			item_platform: "",
			item_stock: 100,
			token: null,
		};
	},
	methods: {
		async getItem() {
			let item = await getItemById(this.id);
			console.log(item);
			if (item) {
				this.item_price = item.Price;
				this.item_desc = "Placeholder Description";
				this.item_image = item.ImageLink;
				this.item_platform = "";
				this.item_stock = 100;
			} else {
				this.item_price = 10;
				this.item_desc = "Test";
				this.item_image = placeholder;
				this.item_platform = "Test";
				this.item_stock = 100;
			}
		},
		handleAddToCart() {
			if (!this.token) {
				alert("Authentication is required to add item to cart (Log-In / Sign-Up)") // for testing
				return // return early, break out of click
			}
			this.$store.dispatch("addItemToCart", {
				id: this.id,
				item_name: this.item_name,
				item_price: this.item_price,
				item_desc: this.item_desc,
				item_image: this.item_image,
				item_platform: this.item_platform,
				item_stock: this.item_stock,
			});
		},
		async getRecommendedItems() {
			let item = await getRecommendedItems();
			console.log(item);
		},
	},
	computed: {
		availableStock() {
			return this.item_stock >= 1 ? true : false;
		},
	},
	mounted() {
		this.getItem();
		this.token = getToken("cognito-user-jwt")
	},
};
</script>
