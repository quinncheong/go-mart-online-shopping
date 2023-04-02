// Plugins
import vue from "@vitejs/plugin-vue";
import vuetify, { transformAssetUrls } from "vite-plugin-vuetify";

// Utilities
import { defineConfig } from "vite";
import { fileURLToPath, URL } from "node:url";

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [
		vue({
			template: { transformAssetUrls },
		}),
		// https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vite-plugin
		vuetify({
			autoImport: true,
			styles: {
				configFile: "src/styles/settings.scss",
			},
		}),
	],
	define: {
		"process.env": {
			NODE_END: "prod",
			PROD_BASE_URL: "https://api.gomartttt.store",
			USER_BASEURL: "http://localhost:5001",
			PLACE_ORDER_BASEURL: "http://localhost:5002",
			ITEM_BASEURL: "http://localhost:5003",
			ERROR_BASEURL: "http://localhost:5004",
			STRIPE_WRAPPER_BASEURL: "http://localhost:5006",
			ORDER_BASEURL: "http://localhost:5007",
			EMAIL_BASEURL: "http://localhost:5672",
			STRIPE_PUBLISHABLE:
				"pk_test_51KegmTDlqIwRfGLS8skxZOKRQ86IEqZ2uEeZET5H6gWVP1J92gF5qK5xcAmAH2DlX1IbpnRCk445erHe6yKzrBSz00LHcNYTrM",
		},
	},
	resolve: {
		alias: {
			"@": fileURLToPath(new URL("./src", import.meta.url)),
		},
		extensions: [
			".js",
			".json",
			".jsx",
			".mjs",
			".ts",
			".tsx",
			".vue",
			".jpg",
			".png",
		],
	},
	server: {
		port: 3000,
		proxy: {
			"^/api": {
				// target: "http://13.251.16.251:5003",
				target: "http://localhost:5003",
				changeOrigin: true,
				pathRewrite: {
					"^/api": "",
				},
			},
			"^/po": {
				// target: "http://13.251.105.185:5100",
				target: "http://localhost:5002",
				changeOrigin: true,
				pathRewrite: {
					"^/po": "",
				},
			},
		},
	},
});
