<template>
	<nav class="navbar navbar-expand-lg">
		<div class="container-fluid" data-bs-theme="dark">
			<router-link class="navbar-brand" to="/">Havenly</router-link>
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
				<ul class="navbar-nav ms-auto me-5">
					<!-- Admin Navigation Items -->
					<template v-if="isAuthenticated && authStore.user.role === 'admin'">
						<li class="nav-item">
							<router-link class="nav-link" to="/admin/dashboard">
								<i class="bi bi-speedometer2 me-1"></i>Dashboard
							</router-link>
						</li>
						<li class="nav-item">
							<router-link class="nav-link" to="/admin/users">
								<i class="bi bi-people me-1"></i>Users
							</router-link>
						</li>
						<li class="nav-item">
							<router-link class="nav-link" to="/admin/professionals">
								<i class="bi bi-person-badge me-1"></i>Professionals
							</router-link>
						</li>
						<li class="nav-item">
							<router-link class="nav-link" to="/admin/services">
								<i class="bi bi-tools me-1"></i>Services
							</router-link>
						</li>
					</template>

					<!-- Regular Navigation Items -->
					<li v-if="!isAuthenticated || authStore.user.role !== 'admin'" class="nav-item">
						<router-link class="nav-link" to="/services">Services</router-link>
					</li>

					<!-- Authentication Items -->
					<li v-if="!isAuthenticated" class="nav-item">
						<a
							class="nav-link"
							href="#"
							data-bs-toggle="modal"
							data-bs-target="#loginModal"
						>Login</a>
					</li>
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

<style scoped>
	nav {
		/* background-color: #e5ddd6; */
		font-size: 1.3rem;
		padding: 0.5rem 1rem;
		/* color: black; */
		background-color: #191919;
	}

	.navbar-brand {
		color: white !important;
		font-size: 1.5rem;
		font-weight: bold;
	}

	.nav-link {
		color: white !important;
		transition: all 0.3s ease;
	}

	.nav-link:hover {
		color: #ffffff86 !important;
	}


	

	
</style>
