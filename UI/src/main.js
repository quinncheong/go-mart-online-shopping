/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Components
import App from "./App.vue";
// import NProgress from "nprogress"

// Composables
import { createApp } from "vue";

// Plugins
import { registerPlugins } from "@/plugins";

// CSS
import "nprogress/nprogress.css"
import "@/assets/fonts.css";
import store from "./store";

const app = createApp(App);

registerPlugins(app);
app.use(store);
// app.use(NProgress)
app.mount("#app");
