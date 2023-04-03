import axios from "axios";
var email="";
if (localStorage) {
	// local storage is available, set the value
	email = JSON.parse(localStorage.getItem("cognito-user-jwt"));
	email = email["email"];
  } else {
	// local storage is not available, set the value to false
	email = "False";
  }

<<<<<<< Updated upstream
const { ITEM_BASEURL, NODE_ENV, PROD_BASE_URL } = process.env;

const ITEM_URL =
	NODE_ENV !== "development"
		? `${PROD_BASE_URL}/v1/item`
		: `${ITEM_BASEURL}/v1/item`;
=======
const { ITEM_BASEURL } = process.env;
const { PLACE_ORDER_BASEURL } = process.env
const ITEM_URL = `${ITEM_BASEURL}/v1/item`;
const PLACE_ORDER_URL = `${PLACE_ORDER_BASEURL}/v1/`;
>>>>>>> Stashed changes

export const getAllItems = async () => {
	const response = await axios.get(`${ITEM_URL}/all`);
	console.info(response);
	return response.data;
};

export const getItemById = async (id) => {
	const response = await axios.get(`${ITEM_URL}/${id}`);
	console.info(response);
	return response.data;
};

export const getNumItems = async () => {
	const response = await axios.get(`${ITEM_URL}/get-num-items`);
	console.info(response);
	return response.data;
};

export const getRecommendedItems= async () => {
	const response = await axios.get(`${PLACE_ORDER_URL}/displayItems/`+email);
	console.info(response);
	return response.data;
};
// POST APIS
export const queryItemsByEsk = async ({ esk }) => {
	const response = await axios.post(`${ITEM_URL}/esk`, { esk });
	console.info(response);
	return response.data;
};
