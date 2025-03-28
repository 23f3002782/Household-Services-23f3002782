<template>
	<div class="container py-5">
		<div class="d-flex justify-content-between align-items-center mb-5">
			<h1 class="display-5">Our Services</h1>
			<form class="d-flex" role="search" @submit.prevent>
				<input
					class="form-control me-2"
					type="search"
					placeholder="Search services"
					aria-label="Search"
					v-model="searchQuery"
					@input="performSearch"
				/>
			</form>
		</div>

		<!-- If authenticated -->
		<div v-if="authStore.isAuthenticated">
			<div
				v-if="filteredServices.length > 0"
				class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 g-4 mb-5"
			>
				<div
					v-for="service in filteredServices"
					:key="service.id"
					class="col"
				>
					<div
						class="card h-100 shadow border-0 rounded-3"
						@click="selectService(service.id)"
						data-bs-toggle="modal"
						data-bs-target="#bookServiceModal"
						data-bs-theme="light"
						role="button"
					>
						<div
							class="card-body d-flex flex-column justify-content-between"
						>
							<div>
								<h5 class="card-title">{{ service.name }}</h5>
								<p class="card-text">
									{{ service.description }}
								</p>
							</div>
							<div
								class="d-flex justify-content-between align-items-center mt-3"
							>
								<span class="badge text-bg-light p-2">
									{{ service.time_required }} hrs
								</span>
								<span class="badge text-bg-success p-2">
									Rs. {{ service.base_price }}
								</span>
							</div>
						</div>
					</div>
				</div>
			</div>
			<div v-else class="text-center">
				No services found matching your search.
			</div>
		</div>

		<!-- If not authenticated -->
		<div v-else>
			<div
				v-if="filteredServices.length > 0"
				class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4 g-4 mb-5"
			>
				<div
					v-for="service in filteredServices"
					:key="service.id"
					class="col"
				>
					<div
						class="card h-100 shadow border-0 rounded-3"
						data-bs-toggle="modal"
						data-bs-target="#loginModal"
						data-bs-theme="light"
						role="button"
					>
						<div
							class="card-body d-flex flex-column justify-content-between"
						>
							<div>
								<h5 class="card-title">{{ service.name }}</h5>
								<p class="card-text">
									{{ service.description }}
								</p>
							</div>
							<div
								class="d-flex justify-content-between align-items-center mt-3"
							>
								<span class="badge text-bg-light p-2">
									{{ service.time_required }} hrs
								</span>
								<span class="badge text-bg-success p-2">
									Rs. {{ service.base_price }}
								</span>
							</div>
						</div>
					</div>
				</div>
			</div>
			<div v-else class="text-center">
				No services found matching your search.
			</div>
		</div>

		<!-- Book Service Modal -->
		<div
			class="modal fade"
			id="bookServiceModal"
			tabindex="-1"
			aria-labelledby="bookServiceModalLabel"
			aria-hidden="true"
		>
			<div class="modal-dialog">
				<div class="modal-content">
					<div class="modal-header">
						<h5 class="modal-title" id="bookServiceModalLabel">
							Choose a date
						</h5>
						<button
							type="button"
							class="btn-close"
							data-bs-dismiss="modal"
							aria-label="Close"
						></button>
					</div>
					<div class="modal-body">
						<form @submit.prevent="bookService">
							<div class="mb-3">
								<label for="serviceDate" class="form-label"
									>Service Date</label
								>
								<input
									type="date"
									class="form-control"
									id="serviceDate"
									v-model="serviceDate"
									required
								/>
							</div>
							<div class="text-center mt-4">
								<button
									type="submit"
									class="btn btn-dark"
									data-bs-dismiss="modal"
								>
									Book Now
								</button>
							</div>
						</form>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
	import { ref, onMounted } from "vue";
	import { useServicesStore } from "@/stores/servicesStore";
	import { useAuthStore } from "@/stores/authStore";
	import { useNotificationStore } from "@/stores/notificationStore";

	const servicesStore = useServicesStore();
	const authStore = useAuthStore();
	const notificationStore = useNotificationStore();

	const searchQuery = ref("");
	const filteredServices = ref([]);
	const performSearch = () => {
		if (!searchQuery.value.trim()) {
			filteredServices.value = servicesStore.sortedServices;
			return;
		} else {
			filteredServices.value = servicesStore.sortedServices.filter(
				(service) =>
					service.name
						.toLowerCase()
						.includes(searchQuery.value.toLowerCase())
			);
		}
	};

	const serviceDate = ref("");
	const selectedService = ref(null);

	const selectService = (serviceId) => {
		selectedService.value = serviceId;
	};

	const bookService = async () => {
		try {
			const response = await fetch(
				"http://localhost:5000/api/customer/service-requests",
				{
					method: "POST",
					headers: {
						Authorization: authStore.token,
						"Content-Type": "application/json",
					},
					body: JSON.stringify({
						service_id: selectedService.value,
						date_of_request: serviceDate.value,
					}),
				}
			);
			if (!response.ok) {
				throw new Error("Failed to book service");
			}
			notificationStore.addNotification({
				message: "Service booked successfully",
				type: "success",
			});
		} catch (error) {
			console.error("Booking service error:", error);
			throw error;
		} finally {
			serviceDate.value = "";
			selectedService.value = null;
		}
	};

	onMounted(async () => {
		await servicesStore.fetchServices();
		filteredServices.value = servicesStore.sortedServices;
	});
</script>

<style scoped>
	.card {
		transition: all 0.2s ease-in-out;
	}

	.card:hover {
		box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
		scale: 1.01;
	}
</style>
