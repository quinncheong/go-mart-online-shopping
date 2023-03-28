import Vuex from "vuex";
import cart from "./modules/cart";
import api from "./modules/api_BaseURL"

export default new Vuex.Store({
	modules: {
		cart,
		api,
	},
});
