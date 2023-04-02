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
						<v-card-title class="bold-30">
							{{ item_name }}
						</v-card-title>
						<v-card-subtitle class="text-left medium-20 mt-2 mb-n4">
							Platform: {{ item_platform }}
						</v-card-subtitle>

						<v-spacer></v-spacer>

						<v-card-subtitle class="text-left medium-20 mt-2 mb-n4">
							<span class="ml-n1"> ${{ item_price }} </span>
						</v-card-subtitle>

						<v-spacer></v-spacer>

						<v-card-subtitle class="text-left medium-20">
							Description:
						</v-card-subtitle>

						<v-spacer></v-spacer>

						<v-card-subtitle class="text-left medium-15 mt-n5">
							{{ item_desc }}
						</v-card-subtitle>

						<v-spacer></v-spacer>

						<v-card-actions class="ml-auto">
							<v-btn class="bg-black" rounded v-if="availableStock">
								<v-card-subtitle class="white-15" @click="handleAddToCart()">
									Add to Cart
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
import placeholder from "@/assets/placeholder.jpg";

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
		};
	},
	methods: {
		async getItem() {
			let item = await getItemById(this.id);
			console.log(item)
			if (item) {
				this.item_price = item.Price;
				this.item_desc = "Placeholder Description";
				this.item_image = item.ImageLink;
				this.item_platform = "Placeholder Platform";
				this.item_stock = 100;
			} else {
				this.item_name = "Test Item";
				this.item_price = 100;
				this.item_desc = "Tesitng Desc sdfjsdfhsdjkfhsdhf";
				this.item_image = placeholder;
				this.item_platform = "hsdfhjsdksdjlsj";
				this.item_stock = 10000;
			}
		},
		handleAddToCart() {
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
	},
	computed: {
		availableStock() {
			return this.item_stock >= 1 ? true : false;
		},
	},
	created() {
		this.getItem();
	},
};
</script>
