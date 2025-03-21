<template>
  <div class="container p-5">
    <!-- Dashboard Section -->
    <div v-if="$route.path === '/professional/dashboard'" class="pt-3">
      <h1 class="mb-5 display-5">Dashboard</h1>

      <h3 class="mb-4">On Going Requests</h3>
      <div class="table-responsive">
        <table
          class="table text-center table-borderless align-middle rounded-3 overflow-hidden"
        >
          <thead>
            <tr>
              <th>ID</th>
              <th>Customer</th>
              <th>Date</th>
              <th>Address</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(request, index) in onGoingRequests" :key="index">
              <td>{{ index + 1 }}</td>
              <td>{{ request.customer.username }}</td>
              <td>{{ request.date_of_request.split("00:00:00")[0] }}</td>
              <td>{{ request.customer.address }}</td>
              <td>
                {{
                  request.status === "closed by customer" ? "Closed" : "Ongoing"
                }}
              </td>
              <td>
                <div class="d-grid gap-2 d-md-flex justify-content-md-center">
                  <button
                    @click="closeRequest(request.id)"
                    class="btn btn-outline-dark btn-sm"
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

    <!-- Profile Section -->
    <div v-if="$route.path === '/professional/profile'" class="pt-3">
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
              <p class="text-muted mb-3">Service Professional</p>
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
              <form @submit.prevent="updateProfile" class="row g-3">
                <div class="col-12">
                  <label for="username" class="form-label">Name</label>
                  <input
                    type="text"
                    class="form-control"
                    id="username"
                    v-model="profile.username"
                    :disabled="!isEditing"
                  />
                </div>
                <div class="col-12">
                  <label for="email" class="form-label">Email</label>
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
                  <label for="yearsOfExperience" class="form-label"
                    >Years of Experience</label
                  >
                  <input
                    type="number"
                    class="form-control"
                    id="yearsOfExperience"
                    v-model="profile.yearsOfExperience"
                    :disabled="!isEditing"
                  />
                </div>
                <div class="col-12">
                  <label for="serviceName" class="form-label">Service</label>
                  <input
                    type="text"
                    class="form-control"
                    id="serviceName"
                    v-model="profile.serviceName"
                    disabled
                    readonly
                  />
                </div>
                <div class="col-12">
                  <label for="about" class="form-label">About</label>
                  <textarea
                    class="form-control"
                    id="about"
                    v-model="profile.about"
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
                    @click="updateProfile"
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

    <!-- Service Requests Section -->
    <div v-if="$route.path === '/professional/requests'" class="pt-3">
      <h1 class="mb-5 display-5">Service Requests</h1>
      <div v-if="newRequests.length === 0">
        <h3 class="text-center">No new requests</h3>
      </div>
      <div v-else class="table-responsive">
        <table
          class="table text-center table-borderless align-middle rounded-3 overflow-hidden"
        >
          <thead>
            <tr>
              <th>ID</th>
              <th>Customer</th>
              <th>Date</th>
              <th>Address</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(newRequest, index) in newRequests" :key="index">
              <td>{{ index + 1 }}</td>
              <td>{{ newRequest.customer.username }}</td>
              <td>{{ newRequest.date_of_request.split("00:00:00")[0] }}</td>
              <td>{{ newRequest.customer.address }}</td>
              <td>
                <button
                  class="btn btn-outline-success btn-sm"
                  @click="acceptRequest(newRequest.id)"
                >
                  Accept
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useAuthStore } from "@/stores/authStore";
import { useServicesStore } from "@/stores/servicesStore";
import { useNotificationStore } from "@/stores/notificationStore";

const authStore = useAuthStore();
const servicesStore = useServicesStore();
const notificationStore = useNotificationStore();

const myRequests = ref([]);
const onGoingRequests = computed(() =>
  myRequests.value.filter(
    (req) => req.status === "assigned" || req.status === "closed by customer"
  )
);
const fetchMyRequests = async () => {
  try {
    const response = await fetch(
      "http://localhost:5000/api/professional/service-requests",
      {
        headers: {
          Authorization: authStore.token,
        },
      }
    );
    if (!response.ok) {
      throw new Error("Failed to fetch requests");
    }
    const data = await response.json();
    myRequests.value = data;
  } catch (error) {
    console.error("Error fetching requests:", error);
  }
};

const closeRequest = async (requestId) => {
  try {
    const response = await fetch(
      `http://localhost:5000/api/professional/service-requests/${requestId}`,
      {
        method: "PUT",
        headers: {
          Authorization: authStore.token,
        },
      }
    );
    await fetchMyRequests();
    if (!response.ok) {
      throw new Error("Failed to close request");
    }
    notificationStore.addNotification({
      message: "Request closed successfully",
      type: "success",
    });
  } catch (error) {
    console.error("Error closing request:", error);
    notificationStore.addNotification({
      message: "Failed to close request",
      type: "error",
    });
  }
};
// Profile Section
const isEditing = ref(false);
const profile = ref({
  username: authStore.user.username,
  email: authStore.user.email,
  yearsOfExperience: authStore.user.experience_years,
  about: authStore.user.about,
  serviceName: "",
});

const originalProfile = ref({});

onMounted(async () => {
  await fetchMyRequests();

  await servicesStore.fetchServices();
  const service = servicesStore.services.find(
    (service) => service.id === authStore.user.service_id
  );
  if (service) {
    profile.value.serviceName = service.name;
  }
  originalProfile.value = { ...profile.value };

  fetchNewRequests();
});

// Update profile
const startEditing = () => {
  isEditing.value = true;
};

const cancelEdit = () => {
  isEditing.value = false;
  profile.value = { ...originalProfile.value };
  profile.value.serviceName = servicesStore.services.find(
    (service) => service.id === authStore.user.service_id
  ).name;
};

const updateProfile = async () => {
  try {
    await authStore.updateProfessionalProfile(
      profile.value.username,
      profile.value.yearsOfExperience,
      profile.value.about
    );
    isEditing.value = false;
  } catch (error) {
    console.error("Error updating profile:", error);
    notificationStore.addNotification({
      message: "Failed to update profile",
      type: "error",
    });
    profile.value = { ...originalProfile.value };
    profile.value.serviceName = servicesStore.services.find(
      (service) => service.id === authStore.user.service_id
    ).name;
  }
};
// End of Profile Section

// Service Requests Section
const newRequests = ref([]);
const fetchNewRequests = async () => {
  try {
    const response = await fetch("http://localhost:5000/api/service-requests", {
      headers: {
        Authorization: authStore.token,
      },
    });
    if (!response.ok) {
      throw new Error("Failed to fetch requests");
    }
    const data = await response.json();
    newRequests.value = data.filter(
      (req) =>
        req.status === "requested" &&
        req.service_id === authStore.user.service_id
    );
  } catch (error) {
    console.error("Error fetching requests:", error);
  }
};

const acceptRequest = async (requestId) => {
  try {
    const response = await fetch(
      `http://localhost:5000/api/professional/service-requests/${requestId}`,
      {
        method: "POST",
        headers: {
          Authorization: authStore.token,
        },
      }
    );
    if (!response.ok) {
      throw new Error("Failed to accept request");
    }
    notificationStore.addNotification({
      message: "Request accepted successfully",
      type: "success",
    });
    // Refresh both lists after successful acceptance
    await fetchNewRequests();
    await fetchMyRequests();
  } catch (error) {
    console.error("Error accepting request:", error);
    notificationStore.addNotification({
      message: "Failed to accept request",
      type: "error",
    });
  }
};
// End of Service Requests Section
</script>

<style scoped>
.card {
  border: none;
  background-color: #fff;
  border-radius: 18px;
  box-shadow: 2px 4px 12px #00000014;
}

.table {
  border: none;
  border-radius: 18px;
  box-shadow: 2px 4px 12px #00000014;
  overflow-x: auto;
}

.badge {
  font-size: 0.9rem;
  padding: 0.5rem 1rem;
}
</style>
