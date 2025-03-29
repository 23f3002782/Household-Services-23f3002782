<template>
	<div class="container py-5">
		<div class="row g-4">
			<!-- Professional Card -->
			<div class="col-md-4">
				<div class="card text-center h-100 shadow border-0 rounded-3">
					<div
						class="card-body d-flex flex-column justify-content-center align-items-center"
					>
						<div class="mb-4">
							<img
								:src="`https://api.dicebear.com/7.x/avataaars/svg?seed=${professional?.id}&accessories[]&accessoriesColor[]&clothing=blazerAndShirt,blazerAndSweater,collarAndSweater,overall,shirtCrewNeck,shirtScoopNeck,hoodie,graphicShirt,shirtVNeck&eyebrows=default&eyes=default&facialHairColor=2c1b18,4a312c,a55728&hairColor=2c1b18,724133,a55728,b58143,d6b370,ecdcbf&hatColor[]&mouth=default&skinColor=d08b5b,ffdbb4,fd9841,edb98a&top=bigHair,bob,bun,curly,dreads,fro,longButNotTooLong,miaWallace,straight02,straight01,straightAndStrand`"
								alt="Profile Avatar"
								class="rounded-circle mb-3 border border-2 border-dark"
								width="120"
								height="120"
							/>
						</div>
						<h4 class="mb-1">{{ professional?.username }}</h4>
						<p class="text-muted mb-2">Service Professional</p>
						<div class="badge bg-success mb-3">
							{{
								professional?.status === "approved"
									? "Approved"
									: "Blocked"
							}}
						</div>
					</div>
				</div>
			</div>

			<!-- Professional Details -->
			<div class="col-md-8">
				<div class="card h-100 shadow border-0 rounded-3">
					<div class="card-header">
						<h5 class="mb-0">Professional Information</h5>
					</div>
					<div class="card-body">
						<div class="row g-3">
							<div class="col-12">
								<label class="form-label fw-bold"
									>Service</label
								>
								<p>{{ serviceName }}</p>
							</div>
							<div class="col-12">
								<label class="form-label fw-bold"
									>Years of Experience</label
								>
								<p>
									{{ professional?.experience_years }} years
								</p>
							</div>
							<div class="col-12">
								<label class="form-label fw-bold">About</label>
								<p>{{ professional?.about }}</p>
							</div>
						</div>
					</div>
				</div>
			</div>

			<!-- Reviews Section -->
			<div class="col-12">
				<div class="card shadow border-0 rounded-3">
					<div class="card-header">
						<h5 class="mb-0">Reviews</h5>
					</div>
					<div class="card-body">
						<div
							v-if="reviews.length === 0"
							class="text-center py-4"
						>
							<p class="mb-0">No reviews yet</p>
						</div>
						<div v-else class="row g-4">
							<div
								v-for="(review, index) in reviews"
								:key="index"
								class="col-12"
							>
								<div
									class="d-flex align-items-start border-bottom pb-3"
								>
									<img
										:src="`https://api.dicebear.com/7.x/avataaars/svg?seed=${review.customer.id}&accessories[]&accessoriesColor[]&clothing=blazerAndShirt,blazerAndSweater,collarAndSweater,overall,shirtCrewNeck,shirtScoopNeck,hoodie,graphicShirt,shirtVNeck&eyebrows=default&eyes=default&facialHairColor=2c1b18,4a312c,a55728&hairColor=2c1b18,724133,a55728,b58143,d6b370,ecdcbf&hatColor[]&mouth=default&skinColor=d08b5b,ffdbb4,fd9841,edb98a&top=bigHair,bob,bun,curly,dreads,fro,longButNotTooLong,miaWallace,straight02,straight01,straightAndStrand`"
										alt="Customer Avatar"
										class="rounded-circle me-3"
										width="48"
										height="48"
									/>
									<div class="flex-grow-1">
										<div
											class="d-flex justify-content-between align-items-center mb-2"
										>
											<h6 class="mb-0">
												{{ review.customer.username }}
											</h6>
											<small class="text-muted">{{
												formatDate(review.date)
											}}</small>
										</div>
										<p class="mb-0">{{ review.content }}</p>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
	import { ref, onMounted, computed } from "vue";
	import { useRoute } from "vue-router";
	import { useAuthStore } from "@/stores/authStore";
	import { useServicesStore } from "@/stores/servicesStore";
	import { useNotificationStore } from "@/stores/notificationStore";

	const route = useRoute();
	const authStore = useAuthStore();
	const servicesStore = useServicesStore();
	const notificationStore = useNotificationStore();

	const professional = ref(null);
	const reviews = ref([]);

	const serviceName = computed(() => {
		if (!professional.value || !servicesStore.services.length) return "";
		const service = servicesStore.services.find(
			(s) => s.id === professional.value.service_id
		);
		return service ? service.name : "";
	});

	const fetchProfessionalDetails = async () => {
		try {
			const response = await fetch(
				`http://localhost:5000/api/users/${route.params.id}`,
				{
					headers: {
						Authorization: authStore.token,
					},
				}
			);
			if (!response.ok)
				throw new Error("Failed to fetch professional details");
			professional.value = await response.json();
		} catch (error) {
			console.error("Error fetching professional details:", error);
			notificationStore.addNotification({
				message: "Failed to load professional details",
				type: "error",
			});
		}
	};

	const fetchReviews = async () => {
		try {
			const response = await fetch(
				`http://localhost:5000/api/service-requests`,
				{
					headers: {
						Authorization: authStore.token,
					},
				}
			);
			if (!response.ok) throw new Error("Failed to fetch reviews");
			const requests = await response.json();
			const myRequests = requests.filter(
				(request) => request.professional_id == route.params.id
			);
			const closedRequests = myRequests.filter(
				(request) => request.status == "closed"
			);
			closedRequests.forEach((request) => {
				console.log(request);
				reviews.value.push({
					customer: request.customer,
					date: request.date_of_completion,
					content: request.review,
				});
			});
		} catch (error) {
			console.error("Error fetching reviews:", error);
		}
	};

	const formatDate = (dateString) => {
		let arr = dateString.split(" ");
		let day = arr[1];
		let month = arr[2];
		let year = arr[3];
		return `${day} ${month} ${year}`;
	};

	onMounted(async () => {
		await Promise.all([fetchProfessionalDetails(), fetchReviews()]);
	});
</script>
