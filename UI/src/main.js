/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Components
import App from "./App.vue";

// Composables
import { createApp } from "vue";

// Plugins
import { registerPlugins } from "@/plugins";

// CSS
import "@/assets/fonts.css";
import "nprogress/nprogress.css"
import store from "./store";

const app = createApp(App);

registerPlugins(app);
app.use(store);
app.mount("#app");
