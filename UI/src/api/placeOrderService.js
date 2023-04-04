import axios from "axios";
import { getToken } from "@/api/cookie"

const { PLACE_ORDER_BASEURL, NODE_ENV, PROD_BASE_URL } = process.env;

let email = null;
let token = getToken("cognito-user-jwt");
if (token) {
	email = token.email;
	console.log(email)
}

const PLACE_ORDER_URL =
	NODE_ENV !== "development"
		? `${PROD_BASE_URL}/v1/place-order`
		: `${PLACE_ORDER_BASEURL}/v1/place-order`;

export const getRecommendedItems = async () => {
	const response = await axios.get(`${PLACE_ORDER_URL}/displayItems/` + email);
	console.info(response);
	return response.data;
};

export const placeOrderCheckout = async (payload={}) => {
	try {
		const { data } = await axios.post(PLACE_ORDER_URL, payload)
		// const data = await fetch(PLACE_ORDER_URL, {
		// 	method: "POST",
		// 	body: JSON.stringify(payload)
		// })
		return data
	} catch (err) {
		throw new Error(err)
	}
}

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
				Authorization: token,
			},
		}
	);
	console.info(response);
	return response.data;
};
