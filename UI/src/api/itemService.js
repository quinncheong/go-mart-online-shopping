import axios from "axios";

const { ITEM_BASEURL, NODE_ENV, PROD_BASE_URL } = process.env;

const ITEM_URL =
	NODE_ENV !== "development"
		? `${PROD_BASE_URL}/v1/item`
		: `${ITEM_BASEURL}/v1/item`;

let token = localStorage.getItem("cognito-user-jwt");

export const getAllItems = async () => {
	const response = await axios.get(`${ITEM_URL}/all`, {
		headers: {
			Authorization: token,
		},
	});
	console.info(response);
	return response.data;
};

export const getItemById = async (id) => {
	const response = await axios.get(`${ITEM_URL}/${id}`, {
		headers: {
			Authorization: token,
		},
	});
	console.info(response);
	return response.data;
};

export const getNumItems = async () => {
	const response = await axios.get(`${ITEM_URL}/get-num-items`, {
		headers: {
			Authorization: token,
		},
	});
	console.info(response);
	return response.data;
};

// POST APIS
export const queryItemsByEsk = async ({ esk }) => {
	const response = await axios.post(
		`${ITEM_URL}/esk`,
		{ esk },
		{
			headers: {
				Authorization: token,
			},
		}
	);
	console.info(response);
	return response.data;
};
