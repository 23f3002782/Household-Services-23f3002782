<template>
	<div class="container py-5">
		<!-- Dashboard Overview -->
		<div v-if="$route.path === '/customer/dashboard'" class="pt-3">
			<h1 class="mb-5 display-5">Dashboard</h1>

			<div
				v-if="
					requestedBookings.length === 0 &&
					assignedBookings.length === 0
				"
			>
				<h3 class="text-center">No bookings yet...</h3>
				<p class="text-center">Request a service now.</p>
				<div class="d-grid gap-2 d-md-flex justify-content-md-center">
					<button
						class="btn btn-outline-dark btn-sm"
						@click="$router.push('/services')"
					>
						Click here
					</button>
				</div>
			</div>

			<div v-else>
				<div v-if="requestedBookings.length > 0">
					<h3>Requested Bookings</h3>
					<div class="table-responsive mt-4 mb-5">
						<table
							class="table text-center rounded-3 table-borderless overflow-hidden align-middle"
						>
							<thead>
								<tr>
									<th>ID</th>
									<th>Service</th>
									<th>Date of Request</th>
									<th>Actions</th>
								</tr>
							</thead>
							<tbody>
								<tr
									v-for="(
										booking, index
									) in requestedBookings"
									:key="index"
								>
									<td>{{ index + 1 }}</td>
									<td>{{ booking.service.name }}</td>
									<td>
										{{
											booking.date_of_request.split(
												"00:00:00"
											)[0]
										}}
									</td>
									<td>
										<div
											class="d-grid gap-2 d-md-flex justify-content-md-center"
										>
											<button
												class="btn btn-outline-warning btn-sm"
												data-bs-toggle="modal"
												data-bs-target="#editBookingModal"
												@click="
													startEditingBooking(
														booking.id
													)
												"
											>
												Edit
											</button>
											<button
												class="btn btn-outline-danger btn-sm"
												@click="
													deleteBooking(booking.id)
												"
											>
												Delete
											</button>
										</div>
									</td>
								</tr>
							</tbody>
						</table>
					</div>
				</div>

				<div v-if="assignedBookings.length > 0">
					<h3>Ongoing Bookings</h3>
					<div class="table-responsive mt-4 mb-5">
						<table
							class="table text-center rounded-3 table-borderless overflow-hidden align-middle"
						>
							<thead>
								<tr>
									<th>ID</th>
									<th>Service</th>
									<th>Date of Service</th>
									<th>Professional</th>
									<th>Status</th>
									<th>Actions</th>
								</tr>
							</thead>
							<tbody>
								<tr
									v-for="(booking, index) in assignedBookings"
									:key="index"
								>
									<td>{{ index + 1 }}</td>
									<td>{{ booking.service.name }}</td>
									<td>
										{{
											booking.date_of_request.split(
												"00:00:00"
											)[0]
										}}
									</td>
									<td>
										<div
											class="d-grid gap-2 d-md-flex justify-content-md-center"
										>
											{{ booking.professional.username }}
											<button
												@click="
													$router.push(
														`/professionals/${booking.professional.id}`
													)
												"
												class="btn btn-outline-dark btn-sm"
											>
												View
											</button>
										</div>
									</td>
									<td>
										{{
											booking.status ===
											"closed by professional"
												? "Closed"
												: "Ongoing"
										}}
									</td>
									<td>
										<div
											class="d-grid gap-2 d-md-flex justify-content-md-center"
										>
											<!-- <button
                        v-if="booking.status !== 'closed_by_professional'"
                        class="btn btn-outline-warning btn-sm"
                        data-bs-toggle="modal"
                        data-bs-target="#editBookingModal"
                        @click="startEditingBooking(booking.id)"
                      >
                        Edit
                      </button> -->
											<button
												class="btn btn-outline-success btn-sm"
												data-bs-toggle="modal"
												data-bs-target="#reviewModal"
												@click="
													startEditingBooking(
														booking.id
													)
												"
											>
												Close
											</button>
										</div>
									</td>
								</tr>
							</tbody>
						</table>
					</div>
				</div>
			</div>
		</div>

		<!-- Edit Booking Modal -->
		<div
			class="modal fade text-light"
			id="editBookingModal"
			tabindex="-1"
			aria-labelledby="editBookingModalLabel"
			aria-hidden="true"
			data-bs-theme="dark"
		>
			<div class="modal-dialog">
				<div class="modal-content">
					<div class="modal-header">
						<h5 class="modal-title" id="editBookingModalLabel">
							Edit Booking
						</h5>
						<button
							type="button"
							class="btn-close"
							data-bs-dismiss="modal"
							aria-label="Close"
						></button>
					</div>
					<div class="modal-body">
						<form @submit.prevent="editBooking">
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
							<button
								type="submit"
								class="btn btn-outline-light"
								data-bs-dismiss="modal"
							>
								Save Changes
							</button>
						</form>
					</div>
				</div>
			</div>
		</div>

		<!-- Profile Section -->
		<div v-if="$route.path === '/customer/profile'" class="pt-3">
			<h1 class="mb-5 display-5">Profile</h1>
			<div class="row g-4">
				<!-- Profile Card -->
				<div class="col-md-4">
					<div class="card text-center h-100">
						<div
							class="card-body d-flex flex-column justify-content-center align-items-center"
						>
							<div class="mb-4">
								<img
									src="https://api.dicebear.com/9.x/avataaars/svg?seed=Christopher&eyebrows=default&eyes=default&facialHair[]&facialHairColor[]&mouth=default&skinColor=edb98a&top=dreads01,dreads02,frida,frizzle,froBand,hat,miaWallace,shaggy,shaggyMullet,shavedSides,shortCurly,sides,straight02,straightAndStrand"
									alt="Profile Avatar"
									class="rounded-circle mb-3 border border-2 border-dark"
									width="120"
									height="120"
								/>
							</div>
							<h4 class="mb-1">{{ authStore.user.username }}</h4>
							<p class="text-muted mb-3">Customer</p>
						</div>
					</div>
				</div>

				<!-- Profile Form -->
				<div class="col-md-8">
					<div class="card h-100">
						<div
							class="card-header d-flex justify-content-between align-items-center"
						>
							<h5>Profile Information</h5>
							<button
								v-if="!isEditing"
								@click="startEditing"
								class="btn btn-outline-dark btn-sm"
							>
								Edit Profile
							</button>
						</div>
						<div class="card-body">
							<form
								@submit.prevent="updateProfile"
								class="row g-3"
							>
								<div class="col-12">
									<label for="username" class="form-label"
										>Name</label
									>
									<input
										type="text"
										class="form-control"
										id="username"
										v-model="profile.username"
										:disabled="!isEditing"
									/>
								</div>
								<div class="col-12">
									<label for="email" class="form-label"
										>Email</label
									>
									<input
										type="email"
										class="form-control"
										id="email"
										v-model="profile.email"
										disabled
										readonly
									/>
								</div>
								<div class="col-12">
									<label for="address" class="form-label"
										>Address</label
									>
									<textarea
										class="form-control"
										id="address"
										rows="3"
										v-model="profile.address"
										:disabled="!isEditing"
									></textarea>
								</div>
								<div v-if="isEditing" class="col-12 text-end">
									<button
										type="button"
										@click="cancelEdit"
										class="btn btn-outline-dark me-2"
									>
										Cancel
									</button>
									<button
										type="submit"
										class="btn btn-dark px-4"
									>
										Save Changes
									</button>
								</div>
							</form>
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- Review Modal -->
		<div
			class="modal fade"
			id="reviewModal"
			tabindex="-1"
			aria-labelledby="reviewModalLabel"
			aria-hidden="true"
		>
			<div class="modal-dialog modal-dialog-centered">
				<div class="modal-content">
					<div class="modal-header">
						<h5 class="modal-title" id="reviewModalLabel">
							Give a review
						</h5>
						<button
							type="button"
							class="btn-close"
							data-bs-dismiss="modal"
							aria-label="Close"
						></button>
					</div>
					<div class="modal-body">
						<form @submit.prevent="closeBooking">
							<div class="mb-3">
								<label for="review" class="form-label" hidden
									>Review</label
								>
								<textarea
									class="form-control"
									id="review"
									v-model="review"
									placeholder="Write your review here..."
									required
								/>
							</div>
							<div class="text-center">
								<button
									type="submit"
									class="btn btn-dark"
									data-bs-dismiss="modal"
								>
									Close Booking
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
	import { ref, computed, onMounted } from "vue";
	import { useAuthStore } from "@/stores/authStore";
	import { useNotificationStore } from "@/stores/notificationStore";

	const authStore = useAuthStore();
	const notificationStore = useNotificationStore();

	const isEditing = ref(false);
	const profile = ref({
		username: authStore.user?.username || "",
		email: authStore.user?.email || "",
		address: authStore.user?.address || "",
	});

	const originalProfile = ref({});

	const startEditing = () => {
		originalProfile.value = { ...profile.value };
		isEditing.value = true;
	};

	const cancelEdit = () => {
		profile.value = { ...originalProfile.value };
		isEditing.value = false;
	};

	const updateProfile = async () => {
		try {
			await authStore.updateCustomerProfile(
				profile.value.username,
				profile.value.address
			);
			isEditing.value = false;
		} catch (error) {
			console.error("Error updating profile:", error);
			notificationStore.addNotification({
				message: "Failed to update profile",
				type: "error",
			});
			profile.value = { ...originalProfile.value };
		}
	};

	// Booking related functions
	const bookings = ref([]);
	const requestedBookings = computed(() => {
		return bookings.value.filter(
			(booking) => booking.status === "requested"
		);
	});
	const assignedBookings = computed(() => {
		return bookings.value.filter(
			(booking) =>
				booking.status === "assigned" ||
				booking.status === "closed by professional"
		);
	});

	const fetchBookings = async () => {
		try {
			const response = await fetch(
				"http://localhost:5000/api/customer/service-requests",
				{
					method: "GET",
					headers: {
						Authorization: authStore.token,
					},
				}
			);
			if (!response.ok) {
				throw new Error("Failed to fetch service requests");
			}
			const data = await response.json();
			bookings.value = data;
		} catch (error) {
			console.error("Error fetching service requests:", error);
		}
	};

	const serviceDate = ref("");
	const editingBookingId = ref(null);
	const review = ref("");

	const startEditingBooking = (bookingId) => {
		editingBookingId.value = bookingId;
	};
	const editBooking = async () => {
		try {
			const response = await fetch(
				`http://localhost:5000/api/customer/service-requests/${editingBookingId.value}`,
				{
					method: "PUT",
					headers: {
						Authorization: authStore.token,
					},
					body: JSON.stringify({
						date_of_request: serviceDate.value,
					}),
				}
			);
			if (!response.ok) {
				throw new Error("Failed to edit booking");
			}
			editingBookingId.value = null;
			await fetchBookings();
		} catch (error) {
			console.error("Error editing booking:", error);
		}
	};

	const deleteBooking = async (bookingId) => {
		try {
			const response = await fetch(
				`http://localhost:5000/api/customer/service-requests/${bookingId}`,
				{
					method: "DELETE",
					headers: {
						Authorization: authStore.token,
					},
				}
			);
			if (!response.ok) {
				throw new Error("Failed to delete booking");
			}
			await fetchBookings();
			notificationStore.addNotification({
				message: "Booking deleted",
				type: "success",
			});
		} catch (error) {
			console.error("Error deleting booking:", error);
			notificationStore.addNotification({
				message: "Failed to delete booking",
				type: "error",
			});
		}
	};

	const closeBooking = async () => {
		try {
			const response = await fetch(
				`http://localhost:5000/api/customer/service-requests/${editingBookingId.value}`,
				{
					method: "PUT",
					headers: {
						"Content-Type": "application/json",
						Authorization: authStore.token,
					},
					body: JSON.stringify({
						review: review.value,
					}),
				}
			);
			if (!response.ok) {
				throw new Error("Failed to complete booking");
			}
			await fetchBookings();
			notificationStore.addNotification({
				message: "Booking completed",
				type: "success",
			});
		} catch (error) {
			console.error("Error completing booking:", error);
			notificationStore.addNotification({
				message: "Failed to complete booking",
				type: "error",
			});
		}
	};

	onMounted(async () => {
		await fetchBookings();
	});
</script>

<style scoped>
	.card {
		border: none;
		background-color: #fff;
		border-radius: 18px;
		box-shadow: 2px 4px 12px #00000014;
		overflow: hidden;
	}

	.badge {
		font-size: 0.9rem;
		padding: 0.5rem 1rem;
	}
</style>
