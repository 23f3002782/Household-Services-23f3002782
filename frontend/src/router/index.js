import HeroPage from "@/views/HeroPage.vue";
import { createRouter, createWebHistory } from "vue-router";
import AdminDashboard from "@/views/AdminDashboard.vue";
import ServicesPage from "@/views/ServicesPage.vue";
import CustomerDashboard from "@/views/CustomerDashboard.vue";
import ProfessionalDashboard from "@/views/ProfessionalDashboard.vue";
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
          path: "users",
          name: "admin-users",
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
        }
      ]
    },
    {
      path: "/services",
      name: "services",
      component: ServicesPage,
    },
    {
      path: "/customer/dashboard",
      name: "customer-dashboard",
      component: CustomerDashboard,
      meta: { requiresAuth: true, requiresCustomer: true }
    },
    {
      path: "/professional/dashboard",
      name: "professional-dashboard",
      component: ProfessionalDashboard,
      meta: { requiresAuth: true, requiresProfessional: true }
    },
    {
      path: "/about",
      name: "about",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      // component: () => import("../views/AboutView.vue"),
    },
  ],
});

// Navigation Guards
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const isAuthenticated = authStore.isAuthenticated;
  const userRole = authStore.user?.role;

  // Check if route requires authentication
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next('/');
      return;
    }

    // Check role-based access
    if (to.matched.some(record => record.meta.requiresAdmin) && userRole !== 'admin') {
      next('/');
      return;
    }

    if (to.matched.some(record => record.meta.requiresCustomer) && userRole !== 'customer') {
      next('/');
      return;
    }

    if (to.matched.some(record => record.meta.requiresProfessional) && userRole !== 'professional') {
      next('/');
      return;
    }
  }

  next();
});

export default router;
