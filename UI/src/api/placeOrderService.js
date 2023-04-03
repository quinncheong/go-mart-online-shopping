import axios from "axios";

const { PLACE_ORDER_BASEURL, NODE_ENV, PROD_BASE_URL } = process.env;

const PLACE_ORDER_URL =
	NODE_ENV !== "development"
		? `${PROD_BASE_URL}/v1/place-order`
		: `${PLACE_ORDER_BASEURL}/v1/place-order`;


var token = localStorage.getItem("cognito-user-jwt");

// Not yet implemented
export const getAllOrders = async () => {
	const response = await axios.get(`${PLACE_ORDER_URL}/all`, {
		headers: {
			'Authorization': token 
		}
	});
	console.info(response);
	return response.data;
};

// POST APIS
export const queryItemsByEsk = async ({ payload }) => {
	const response = await axios.post(`${PLACE_ORDER_URL}`, { payload }, {
		headers: {
			'Authorization': token 
		}
	});
	console.info(response);
	return response.data;
};
