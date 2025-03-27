<template>
	<div
		class="modal fade"
		id="loginModal"
		tabindex="-1"
		aria-labelledby="loginModalLabel"
		aria-hidden="true"
	>
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header">
					<h5 class="modal-title" id="loginModalLabel">Login</h5>
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
					></button>
				</div>
				<div class="modal-body px-5 py-4">
					<form @submit.prevent="handleLogin">
						<div class="mb-3">
							<label for="email" class="form-label"
								>Email address</label
							>
							<input
								type="email"
								class="form-control"
								id="email"
								v-model="email"
								required
							/>
						</div>
						<div class="mb-3">
							<label for="password" class="form-label"
								>Password</label
							>
							<input
								type="password"
								class="form-control"
								id="password"
								v-model="password"
								required
							/>
						</div>
						<div class="text-center mt-4">
							<button type="submit" class="btn btn-dark">
								Login
							</button>
						</div>
					</form>
					<div class="mt-3 text-center">
						<p>
							Don't have an account?
							<a
								href="#"
								class="text-dark"
								data-bs-dismiss="modal"
								data-bs-toggle="modal"
								data-bs-target="#signupModal"
								>Sign up</a
							>
						</p>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
	import { ref } from "vue";
	import { useAuthStore } from "@/stores/authStore";

	const authStore = useAuthStore();
	const email = ref("");
	const password = ref("");

	const handleLogin = async () => {
		const result = await authStore.login({
			email: email.value,
			password: password.value,
		});

		if (result.success) {
			email.value = "";
			password.value = "";

			const modalElement = document.getElementById("loginModal");
			const modal = bootstrap.Modal.getInstance(modalElement);
			modal.hide();
		}
	};
</script>
