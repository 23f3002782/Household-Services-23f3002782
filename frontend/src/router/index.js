import HeroPage from "@/views/HeroPage.vue";
import AdminDashboard from "@/views/AdminDashboard.vue";
import ServicesPage from "@/views/ServicesPage.vue";
import CustomerDashboard from "@/views/CustomerDashboard.vue";
import ProfessionalDashboard from "@/views/ProfessionalDashboard.vue";
import ProfessionalDetails from "@/views/ProfessionalDetails.vue";

import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/authStore";

const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes: [
		{
			path: "/",
			name: "hero",
			component: HeroPage,
		},
		// Admin routes
		{
			path: "/admin",
			name: "admin",
			component: AdminDashboard,
			meta: { requiresAuth: true, requiresAdmin: true },
			children: [
				{
					path: "dashboard",
					name: "admin-dashboard",
					component: AdminDashboard,
				},
				{
					path: "customers",
					name: "admin-customers",
					component: AdminDashboard,
				},
				{
					path: "professionals",
					name: "admin-professionals",
					component: AdminDashboard,
				},
				{
					path: "services",
					name: "admin-services",
					component: AdminDashboard,
				},
			],
		},
		// Customer routes
		{
			path: "/customer",
			name: "customer",
			component: CustomerDashboard,
			meta: { requiresAuth: true, requiresCustomer: true },
			children: [
				{
					path: "dashboard",
					name: "customer-dashboard",
					component: CustomerDashboard,
				},
				{
					path: "profile",
					name: "customer-profile",
					component: CustomerDashboard,
				},
			],
		},
		// Professional routes
		{
			path: "/professional",
			name: "professional",
			component: ProfessionalDashboard,
			meta: { requiresAuth: true, requiresProfessional: true },
			children: [
				{
					path: "dashboard",
					name: "professional-dashboard",
					component: ProfessionalDashboard,
				},
				{
					path: "profile",
					name: "professional-profile",
					component: ProfessionalDashboard,
				},
				{
					path: "requests",
					name: "professional-requests",
					component: ProfessionalDashboard,
				},
			],
		},
		{
			path: "/services",
			name: "services",
			component: ServicesPage,
		},
		{
			path: "/professionals/:id",
			name: "ProfessionalDetails",
			component: ProfessionalDetails,
			meta: { requiresAuth: true },
		},
	],
	scrollBehavior(to, from, savedPosition) {
		return { top: 0 };
	},
});

// Navigation Guards
router.beforeEach((to, from, next) => {
	const authStore = useAuthStore();
	const isAuthenticated = authStore.isAuthenticated;
	const userRole = authStore.user?.role;

	// Check if route requires authentication
	if (to.matched.some((record) => record.meta.requiresAuth)) {
		if (!isAuthenticated) {
			next("/");
			return;
		}

		// Check role-based access
		if (
			to.matched.some((record) => record.meta.requiresAdmin) &&
			userRole !== "admin"
		) {
			next("/");
			return;
		}

		if (
			to.matched.some((record) => record.meta.requiresCustomer) &&
			userRole !== "customer"
		) {
			next("/");
			return;
		}

		if (
			to.matched.some((record) => record.meta.requiresProfessional) &&
			userRole !== "service_professional"
		) {
			next("/");
			return;
		}
	}

	next();
});

export default router;
