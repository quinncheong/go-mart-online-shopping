// Composables
import { createRouter, createWebHistory } from "vue-router";
import { retrieveCookie } from "@/api/cookie"

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

// eslint-disable-next-line
// router.beforeEach((to, from) => {
// 	const cookie = retrieveCookie("idtoken")
// 	if (to.meta.requiresAuth && !cookie) {
// 		return { name: "Home" }
// 	}
// })

export default router;
