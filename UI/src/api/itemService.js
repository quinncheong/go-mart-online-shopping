import axios from "axios";

var email="";
var token = localStorage.getItem("cognito-user-jwt");
if (token) {
	// local storage is available, set the value
	email = JSON.parse(token);
	if (email["Email"]) {
		email = email["email"];
	
	}
	else {
		email= "False"
	}
		
  } else {
	// local storage is not available, set the value to false
	email = "False";
  }

const { ITEM_BASEURL, NODE_ENV, PROD_BASE_URL, PLACE_ORDER_BASEURL } = process.env;
const PLACE_ORDER_URL = `${PLACE_ORDER_BASEURL}/v1`;

const ITEM_URL =
	NODE_ENV !== "development"
		? `${PROD_BASE_URL}/v1/item`
		: `${ITEM_BASEURL}/v1/item`;

export const getAllItems = async () => {
	const response = await axios.get(`${ITEM_URL}/all`, {
		headers: {
			'Authorization': token 
		}
	});
	console.info(response);
	return response.data;
};

export const getItemById = async (id) => {
	const response = await axios.get(`${ITEM_URL}/${id}`, {
		headers: {
			'Authorization': token 
		}
	});
	console.info(response);
	return response.data;
};

export const getNumItems = async () => {
	const response = await axios.get(`${ITEM_URL}/get-num-items`, {
		headers: {
			'Authorization': token 
		}
	});
	console.info(response);
	return response.data;
};

export const getRecommendedItems= async () => {
	const response = await axios.get(`${PLACE_ORDER_URL}/displayItems/`+email, {
		headers: {
			'Authorization': token 
		}
	});
	console.info(response);
	return response.data;
};
// POST APIS
export const queryItemsByEsk = async ({ esk }) => {
	const response = await axios.post(`${ITEM_URL}/esk`, { esk }, {
		headers: {
			'Authorization': token 
		}
	});
	console.info(response);
	return response.data;
};
