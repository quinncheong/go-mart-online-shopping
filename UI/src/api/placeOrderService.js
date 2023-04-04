import axios from "axios";
import { getToken } from "@/api/cookie";
import { getRaw } from "@/api/cookie";


const { PLACE_ORDER_BASEURL, NODE_ENV, PROD_BASE_URL } = process.env;

let email = null;
let token = getToken("cognito-user-jwt");
if (token) {
	email = token.email;
	console.log(email);
}

let rawToken = getRaw("cognito-encoded-jwt");

const PLACE_ORDER_URL =
	NODE_ENV !== "development"
		? `${PROD_BASE_URL}/v1/place-order`
		: `${PLACE_ORDER_BASEURL}/v1/place-order`;

export const getRecommendedItems = async () => {
	const response = await axios.get(`${PLACE_ORDER_URL}/displayItems/` + email);
	console.info(response);
	return response.data;
};

export const placeOrderCheckout = async (payload) => {
	if (!payload) {
		return 404;
	}
	console.log(payload);

	console.log(rawToken);

	const response = await axios.post(`${PLACE_ORDER_URL}/checkout`, payload, {
		headers: {
			'Content-Type': 'application/json',
			'Authorization': rawToken
		}
	});

	console.log(response);
	if (response) {
		return response.data;
	}

	return false;
};

// Not yet implemented
export const getAllOrders = async () => {
	const response = await axios.get(`${PLACE_ORDER_URL}/all`, {
		headers: {
			Authorization: token,
		},
	});
	console.info(response);
	return response.data;
};

// POST APIS
export const queryItemsByEsk = async ({ payload }) => {
	const response = await axios.post(
		`${PLACE_ORDER_URL}`,
		{ payload },
		{
			headers: {
				Authorization: rawToken,
			},
		}
	);
	console.info(response);
	return response.data;
};
