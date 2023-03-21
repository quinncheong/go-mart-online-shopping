let cart = window.localStorage.getItem("cart");
let numCartItems = window.localStorage.getItem("numCartItems");

const state = {
	cart: cart ? JSON.parse(cart) : [],
	numCartItems: numCartItems ? JSON.parse(numCartItems) : 0,
};

const getters = {
	getCart(state) {
		return state.cart;
	},
	getNumCartItems(state) {
		return state.numCartItems;
	},
};

const actions = {
	addItemToCart(context, item) {
		const cartItem = context.state.cart.find(
			(item) => item.item.item_name === item.item_name
		);

		if (!cartItem) {
			context.commit(ADD_ITEM_TO_CART, item);
		} else {
			context.commit(INCREMENT_ITEM_CART_QUANTITY, cartItem);
		}

		context.commit(DECREMENT_ITEM_STOCK, item);
		context.commit(SAVE_CART);
	},

	decrementItemInCartQuantity(context, item) {
		const cartItem = context.state.cart.find(
			(item) => item.item.item_name === item.item_name
		);

		if (cartItem.quantity > 1) {
			context.commit(DECREMENT_ITEM_CART_QUANTITY, cartItem, item);
		} else {
			context.commit(REMOVE_ITEM_FROM_CART, cartItem);
		}

		context.commit(INCREMENT_ITEM_STOCK, item);
		context.commit(SAVE_CART);
	},

	incrementItemInCartQuantity(context, item) {
		const cartItem = context.state.cart.find(
			(item) => item.item.item_name === item.item_name
		);
		context.commit(INCREMENT_ITEM_CART_QUANTITY, cartItem);
		context.commit(DECREMENT_ITEM_STOCK, item);
		context.commit(SAVE_CART);
	},

	clearCart(context) {
		context.commit(CLEAR_CART);
	},
};

const mutations = {
	[ADD_ITEM_TO_CART](state, cartItem) {
		state.cart.push({
			item: cartItem,
			quantity: 1,
		});
		state.numCartItems += 1;
		console.log(state.numCartItems);
	},

	[INCREMENT_ITEM_CART_QUANTITY](state, cartItem) {
		cartItem.quantity += 1;
	},

	[DECREMENT_ITEM_CART_QUANTITY](state, cartItem) {
		cartItem.quantity -= 1;
	},

	[DECREMENT_ITEM_STOCK](state, item) {
		item.item_stock -= 1;
	},

	[INCREMENT_ITEM_STOCK](state, item) {
		item.item_stock += 1;
	},

	[REMOVE_ITEM_FROM_CART](state, cartItem) {
		const index = state.cart.indexOf(cartItem);
		if (index !== -1) {
			state.cart.splice(index, 1);
		}
		state.numCartItems -= 1;
	},

	[SAVE_CART](state) {
		window.localStorage.setItem("cart", JSON.stringify(state.cart));
		window.localStorage.setItem(
			"numCartItems",
			JSON.stringify(state.numCartItems)
		);
	},

	[CLEAR_CART](state) {
		window.localStorage.clear();
		state.cart = [];
		state.numCartItems = 0;
	},
};

export const ADD_ITEM_TO_CART = "ADD_ITEM_TO_CART";
export const REMOVE_ITEM_FROM_CART = "REMOVE_ITEM_FROM_CART";

export const INCREMENT_ITEM_CART_QUANTITY = "INCREMENT_ITEM_CART_QUANTITY";
export const DECREMENT_ITEM_CART_QUANTITY = "DECREMENT_ITEM_CART_QUANTITY";

export const DECREMENT_ITEM_STOCK = "DECREMENT_ITEM_STOCK";
export const INCREMENT_ITEM_STOCK = "INCREMENT_ITEM_STOCK";

export const SAVE_CART = "SAVE_CART";
export const CLEAR_CART = "CLEAR_CART";

export default {
	state,
	getters,
	actions,
	mutations,
};
