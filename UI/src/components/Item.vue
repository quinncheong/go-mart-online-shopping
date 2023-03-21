<template>
	<div class="text-center">
		<v-container fluid>
			<v-card class="d-flex flex-column rounded-xl">
				<v-row class="ma-5">
					<v-col cols="3" class="d-flex flex-column">
						<v-img
							:src="item.item_image"
							position="left"
							contain
							max-height="500px"
						>
						</v-img>
					</v-col>
					<v-col class="d-flex flex-column">
						<v-card-title class="bold-30">
							{{ item.item_name }}
						</v-card-title>
						<v-card-subtitle class="text-left medium-20 mt-2 mb-n4">
							Platform:
							<span v-text="item.item_platform"></span>
						</v-card-subtitle>

						<v-card-subtitle class="text-left medium-20 mt-2 mb-n4">
							$
							<span class="ml-n1">
								{{ item.item_price }}
							</span>
						</v-card-subtitle>

						<v-card-subtitle class="text-left medium-20"
							>Description:</v-card-subtitle
						>
						<v-card-subtitle class="text-left medium-15 mt-n5">
							{{ item.item_desc }}
						</v-card-subtitle>
						<v-spacer></v-spacer>
						<v-card-actions class="ml-auto">
							<v-btn color="#353535" rounded v-if="availableStock()">
								<v-card-subtitle class="white-15" @click="handleAddToCart()"
									>Add to Cart</v-card-subtitle
								>
								<v-icon color="white">mdi-plus</v-icon>
							</v-btn>
							<v-card>
								<v-card-subtitle
									v-if="!availableStock()"
									rounded
									class="mx-auto"
									>Out of Stock</v-card-subtitle
								>
							</v-card>
						</v-card-actions>
					</v-col>
				</v-row>
			</v-card>
		</v-container>
	</div>
</template>

<script>
import axios from "axios";
import placeholder from "@/assets/placeholder.jpg";

export default {
	name: "Item",
	data() {
		return {
			item_name: this.$route.query.item_name,
			item: {
				item_name: "",
				item_price: 0,
				item_desc: "",
				item_image: "@/assets/itemPlaceholder.jpg",
				item_platform: "",
				item_stock: 0,
			},
		};
	},
	methods: {
		getItem() {
			const payload = { key: { item_name: this.item_name } };
			const path = `api/get-item`;
			axios
				.post(path, payload)
				.then((res) => {
					this.item = res.data.Item;
				})
				.catch((error) => {
					this.item = {
						item_name: "Test Item",
						item_price: 100,
						item_desc: "Tesitng Desc sdfjsdfhsdjkfhsdhf",
						item_image: placeholder,
						item_platform: "hsdfhjsdksdjlsj",
						item_stock: 10000,
					};
					console.error(error);
				});
		},
		handleAddToCart() {
			this.$store.dispatch("addItemToCart", this.item);
		},
		availableStock() {
			return this.item_stock > 1 ? true : false;
		},
	},
	created() {
		this.getItem();
	},
};
</script>
