<template>
	<div class="text-center">
		<v-container fluid>
			<v-row class="ma-5">
				<!--  -->
				<v-col
					v-for="(
						{
							id,
							item_image,
							item_name,
							item_platform,
							item_price,
							item_stock,
							recommended,
							recommended_picture,
						},
						i
					) in items"
					:key="i"
					:cols="3"
					class="d-flex flex-column"
				>
					<v-card class="rounded-xl">
						<v-container>
							<v-img
								:src="recommended_picture"
								v-if="recommended"
								class="cursor"
								:width="80"
								aspect-ratio="1"
							></v-img>
						</v-container>
						<v-img
							:src="item_image"
							class="white--text align-end cursor"
							height="200px"
							aspect-ratio="1"
							contain
							@click="showItem(item_name, id)"
						></v-img>
						<v-card-title @click="showItem(item_name, id)" class="cursor">
							<v-spacer />
							<div class="text-center">
								<h3>
									{{ item_name }}
								</h3>
								<p class="medium-15 mb-n2">
									{{ item_platform }}
								</p>
								<p class="medium-15 mb-n5 pt-1 pb-2">
									${{ Number(item_price).toFixed(2) }}
								</p>
							</div>
							<v-spacer />
						</v-card-title>
						<v-card-actions>
							<v-btn
								v-if="availableStock(item_stock)"
								class="mx-auto buttons"
								rounded
							>
								<v-card-subtitle
									class="white-15"
									@click="handleAddToCart(item_name)"
									>Add to Cart</v-card-subtitle
								>
								<v-icon color="white">mdi-plus</v-icon>
							</v-btn>
							<v-card>
								<v-card-subtitle
									v-if="!availableStock(item_stock)"
									rounded
									class="mx-auto"
									>Out of Stock</v-card-subtitle
								>
							</v-card>
						</v-card-actions>
					</v-card>
				</v-col>
			</v-row>
			<!-- <v-row>
        <v-col class="text-left ml-7" v-if="showPagePrev">
          <v-btn class="buttons" rounded @click="handlePagePrev">
            <p class="ma-auto">Prev</p>
            <v-icon class="mr-n2">mdi-chevron-left</v-icon>
          </v-btn>
        </v-col>
        <v-col class="text-right mr-7" v-if="showPageNext">
          <v-btn class="buttons" rounded @click="handlePageNext">
            <p class="ma-auto">Next</p>
            <v-icon class="mr-n2">mdi-chevron-right</v-icon>
          </v-btn>
        </v-col>
      </v-row> -->
			<v-snackbar v-model="snackbar.on">
				{{ snackbar.message }} has been successfully added to cart!
				<template v-slot:action="{ attrs }">
					<v-btn color="white" text v-bind="attrs" @click="snackbar.on = false">
						Close
					</v-btn>
				</template>
			</v-snackbar>
		</v-container>
	</div>
</template>

<script>
import { getNumItems } from "@/api/itemService";
import { getRecommendedItems } from "@/api/placeOrderService";
import placeholder from "@/assets/placeholder.jpg";
import recommended_picture from "@/assets/recommended picture.png";
import { getToken } from "@/api/cookie"

export default {
	name: "Items",
	data() {
		return {
			item_id: 0,
			page: 0,
			items_per_page: 10,
			total_pages: 0,
			esk_list: [{ data: "empty" }],
			items: [],
			snackbar: {
				on: false,
				item_name: "",
			},
			token: null,
		};
	},
	computed: {
		showPagePrev() {
			return this.page > 0 ? true : false;
		},
		showPageNext() {
			return this.page < this.total_pages - 1 ? true : false;
		},
	},
	methods: {
		async getNumPages() {
			let res = await getNumItems();
			if (res) {
				this.total_pages = Math.ceil(res / this.items_per_page);
			} else {
				this.total_pages = 1;
			}
		},
		async getItemsByEsk() {
			let items = await getRecommendedItems();
			console.log(items);
			if (items) {
				this.items = items.map(
					({ id, ProductName, Price, ImageLink, Recommendation }) => ({
						id,
						item_name: ProductName,
						item_price: Price,
						item_desc: "Placeholder description",
						item_image: ImageLink,
						item_platform: "",
						item_stock: 100,
						recommended: Recommendation !== undefined ? Recommendation : false,
						recommended_picture, // TODO: change recommended to get from back-end, and not be hard-coded
					})
				).sort(this.compareItems);
			} else {
				this.items = [
					{
						item_name: "Placeholder name",
						item_price: 1,
						item_desc: "Placeholder Desc",
						item_image: placeholder,
						item_platform: "",
						item_stock: 100,
						recommended: false,
						recommended_picture,
					},
					{
						item_name: "Placeholder name",
						item_price: 1,
						item_desc: "Placeholder Desc",
						item_image: placeholder,
						item_platform: "",
						item_stock: 100,
						recommended: true,
						recommended_picture,
					},
					{
						item_name: "Placeholder name",
						item_price: 1,
						item_desc: "Placeholder Desc",
						item_image: placeholder,
						item_platform: "",
						item_stock: 100,
						recommended: false,
						recommended_picture,
					},
					{
						item_name: "Placeholder name",
						item_price: 1,
						item_desc: "Placeholder Desc",
						item_image: placeholder,
						item_platform: "",
						item_stock: 100,
						recommended: true,
						recommended_picture,
					},
					{
						item_name: "Placeholder name",
						item_price: 1,
						item_desc: "Placeholder Desc",
						item_image: placeholder,
						item_platform: "",
						item_stock: 100,
						recommended: true,
						recommended_picture,
					},
				].sort(this.compareItems);
			}
		},
		showItem(name, id) {
			this.$router.push({
				name: "Item",
				query: { item_name: name, id },
			});
		},
		// handlePageNext() {
		//   this.page += 1;
		//   let esk = { data: "empty" };
		//   if (this.items.length !== undefined && this.items.length !== 1) {
		//     const item_name = this.items[this.items_per_page - 1].item_name;
		//     esk = { esk: { item_name: item_name } };
		//     this.esk_list.push(esk);
		//   }
		//   this.getAllItems(esk);
		// },
		// handlePagePrev() {
		//   this.page -= 1;
		//   let esk = this.esk_list[this.page];
		//   this.getAllItems(esk);
		// },
		handleAddToCart(itemName) {
			if (!this.token) {
				alert("Authentication is required to add items to cart (Log-In / Sign-Up)") // for testing
				return // return early, break out of click
			}
			const item = this.items.find(({ item_name }) => item_name === itemName);
			this.$store.dispatch("addItemToCart", item);
			this.snackbar.message = itemName;
			this.snackbar.on = true;
		},
		availableStock(item_stock) {
			return item_stock > 1 ? true : false;
		},
		compareItems(a, b) {
			// comparison function for custom sort
			if (a.recommended && !b.recommended)
				return -1; // a comes before b
			else if (!a.recommended && b.recommended)
				return 1; // b comes before a
			else
				return 0; // no change in order
		},
	},
	created() {
		this.token = getToken("cognito-user-jwt")
		this.getNumPages();
		// const esk = {}; // { data: "empty" }
		this.getItemsByEsk();
	},
};
</script>

<style scoped>
.cursor {
	cursor: pointer;
}
</style>
