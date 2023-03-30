import axios from "axios";

const { ITEM_BASEURL } = process.env;
const ITEM_URL = `${ITEM_BASEURL}/v1/item`;

// Fix CORs issue with axios
axios.defaults.headers.common["origin"] = "https://gomartttt.store";

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

// POST APIS
export const queryItemsByEsk = async ({ esk }) => {
	const response = await axios.post(`${ITEM_URL}/esk`, { esk });
	console.info(response);
	return response.data;
};
