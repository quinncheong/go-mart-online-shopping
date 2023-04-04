// Composables
import { createRouter, createWebHistory } from "vue-router";
import NProgress from "nprogress"
import { getToken } from "@/api/cookie"

const routes = [
	{
		path: "/",
		component: () => import("@/layouts/default/Default.vue"),
		children: [
			{
				path: "/item",
				name: "Item",
				component: () => import("@/views/ItemPage.vue"),
			},
			{
				path: "/checkout",
				name: "Checkout",
				component: () => import("@/views/CheckoutPage.vue"),
				meta: {
					requiresAuth: true,
				},
			},
			{
				path: "/cart",
				name: "Cart",
				component: () => import("@/views/CartPage.vue"),
				meta: {
					requiresAuth: true,
				},
			},
			{
				path: "/about",
				name: "About",
				component: () => import("@/views/About.vue"),
			},
			{
				path: "/hello",
				name: "Hello",
				component: () => import("@/views/Hello.vue"),
			},
			{
				path: "",
				name: "Home",
				// route level code-splitting
				// this generates a separate chunk (about.[hash].js) for this route
				// which is lazy-loaded when the route is visited.
				component: () =>
					import(/* webpackChunkName: "home" */ "@/views/Home.vue"),
			},
		],
	},
];

const router = createRouter({
	history: createWebHistory(process.env.BASE_URL),
	routes,
	scrollBehavior(to, from, savedPosition) { // eslint-disable-line
		return { top: 0 };
	},
});

NProgress.configure({
	minimum: 0.1,
  easing: 'ease',
  speed: 800,
	showSpinner: false,
})

// eslint-disable-next-line
router.beforeEach((to, from) => {
	NProgress.start()
	const token = getToken("cognito-user-jwt")
	if (to.meta.requiresAuth && !token) {
		alert("Authentication is required to enter cart & proceed to checkout")
		return { name: "Home" }
	}
})

// eslint-disable-next-line
router.afterEach((to, from) => {
	NProgress.done()
})

export default router;
