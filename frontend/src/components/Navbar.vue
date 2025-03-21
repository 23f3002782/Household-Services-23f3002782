<template>
  <nav class="navbar navbar-expand-lg px-5">
    <div class="container-fluid">
      <router-link
        class="navbar-brand fw-semibold"
        to="/"
        style="font-family: 'Poiret One', serif"
        >HY</router-link
      >
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNavDropdown"
        aria-controls="navbarNavDropdown"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNavDropdown">
        <ul class="navbar-nav ms-auto">
          <!-- Admin Navigation Items -->
          <template v-if="authStore.user?.role === 'admin'">
            <li class="nav-item">
              <router-link
                to="/admin/dashboard"
                class="nav-link"
                :class="{ active: $route.path === '/admin/dashboard' }"
              >
                Dashboard
              </router-link>
            </li>
            <li class="nav-item">
              <router-link
                to="/admin/services"
                class="nav-link"
                :class="{ active: $route.path === '/admin/services' }"
              >
                Services
              </router-link>
            </li>
            <li class="nav-item">
              <router-link
                to="/admin/professionals"
                class="nav-link"
                :class="{ active: $route.path === '/admin/professionals' }"
              >
                Professionals
              </router-link>
            </li>
            <li class="nav-item">
              <router-link
                to="/admin/customers"
                class="nav-link"
                :class="{ active: $route.path === '/admin/customers' }"
              >
                Customers
              </router-link>
            </li>
          </template>

          <!-- Customer Navigation Items -->
          <template v-if="authStore.user?.role === 'customer'">
            <li class="nav-item">
              <router-link
                to="/customer/dashboard"
                class="nav-link"
                :class="{ active: $route.path === '/customer/dashboard' }"
              >
                Dashboard
              </router-link>
            </li>
            <li class="nav-item">
              <router-link
                to="/services"
                class="nav-link"
                :class="{ active: $route.path === '/services' }"
              >
                Services
              </router-link>
            </li>
            <li class="nav-item">
              <router-link
                to="/customer/profile"
                class="nav-link"
                :class="{ active: $route.path === '/customer/profile' }"
              >
                Profile
              </router-link>
            </li>
          </template>

          <!-- Professional Navigation Items -->
          <template v-if="authStore.user?.role === 'service_professional'">
            <li class="nav-item">
              <router-link
                to="/professional/dashboard"
                class="nav-link"
                :class="{ active: $route.path === '/professional/dashboard' }"
              >
                Dashboard
              </router-link>
            </li>
            <li class="nav-item">
              <router-link
                to="/professional/requests"
                class="nav-link"
                :class="{
                  active: $route.path === '/professional/requests',
                }"
              >
                Requests
              </router-link>
            </li>
            <li class="nav-item">
              <router-link
                to="/professional/profile"
                class="nav-link"
                :class="{ active: $route.path === '/professional/profile' }"
              >
                Profile
              </router-link>
            </li>
          </template>

          <template v-if="!isAuthenticated">
            <li class="nav-item">
              <router-link
                class="nav-link"
                :class="{ active: $route.path === '/services' }"
                to="/services"
                >Services</router-link
              >
            </li>
            <li class="nav-item">
              <a
                class="nav-link"
                href="#"
                data-bs-toggle="modal"
                data-bs-target="#loginModal"
                >Login</a
              >
            </li>
          </template>

          <li v-if="isAuthenticated" class="nav-item">
            <a class="nav-link" href="#" @click="logout">Logout</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <LoginModal />
  <SignupModal />
</template>

<script setup>
import { computed } from "vue";
import LoginModal from "./LoginModal.vue";
import SignupModal from "./SignupModal.vue";
import { useAuthStore } from "@/stores/authStore";

const authStore = useAuthStore();
const isAuthenticated = computed(() => authStore.isAuthenticated);
const logout = () => {
  authStore.logout();
};
</script>

<style scoped></style>
