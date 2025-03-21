<template>
  <div class="container-fluid p-5">
    <!-- Dashboard Overview -->
    <div v-if="$route.path === '/admin/dashboard'">
      <h2 class="mb-5 display-5">Dashboard</h2>

      <div class="row mt-4">
        <div class="col-6 p-4">
          <div class="row row-cols-1 row-cols-md-2 g-4">
            <div class="col">
              <div class="card h-100">
                <div class="card-body">
                  <h5 class="card-title">Users</h5>
                  <h2 class="card-text">{{ customers.length }}</h2>
                </div>
              </div>
            </div>
            <div class="col">
              <div class="card h-100">
                <div class="card-body">
                  <h5 class="card-title">Active Professionals</h5>
                  <h2 class="card-text">{{ activeProfessionals.length }}</h2>
                </div>
              </div>
            </div>
            <div class="col">
              <div class="card h-100">
                <div class="card-body">
                  <h5 class="card-title">Pending Approvals</h5>
                  <h2 class="card-text">{{ pendingApprovals.length }}</h2>
                </div>
              </div>
            </div>
            <div class="col">
              <div class="card h-100">
                <div class="card-body">
                  <h5 class="card-title">Total Services</h5>
                  <h2 class="card-text">{{ services.length }}</h2>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-6">
          <div style="height: 400px; width: 100%">
            <canvas id="myChart"></canvas>
          </div>
        </div>
      </div>
    </div>

    <!-- Users Management -->
    <div v-if="$route.path === '/admin/customers'">
      <h2 class="mb-5 display-5">Customers</h2>
      <div class="table-responsive mt-4">
        <table
          class="table text-center table-borderless rounded-3 overflow-hidden"
        >
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Address</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(customer, index) in customers" :key="index">
              <td>{{ index + 1 }}</td>
              <td>{{ customer.username }}</td>
              <td>{{ customer.email }}</td>
              <td>{{ customer.address }}</td>
              <td v-if="customer.active">
                <button
                  @click="blockUser(customer.id)"
                  class="btn btn-danger btn-sm"
                >
                  Block
                </button>
              </td>
              <td v-else>
                <button
                  @click="unblockUser(customer.id)"
                  class="btn btn-success btn-sm"
                >
                  Unblock
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Service Professionals -->
    <div v-if="$route.path === '/admin/professionals'">
      <div v-if="pendingApprovals.length > 0">
        <h2 class="mb-5 display-5">Pending Approvals</h2>
        <div class="table-responsive mt-4 mb-5">
          <table
            class="table text-center table-borderless rounded-3 overflow-hidden"
          >
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Service</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody class="table-group-divider">
              <tr
                v-for="(professional, index) in pendingApprovals"
                :key="index"
              >
                <td>{{ index + 1 }}</td>
                <td>{{ professional.username }}</td>
                <td>{{ professional.email }}</td>
                <td>
                  {{
                    services.find(
                      (service) => service.id === professional.service_id
                    )?.name
                  }}
                </td>
                <td>
                  <button
                    @click="approveProfessional(professional.id, 'approve')"
                    class="btn btn-success btn-sm me-md-2"
                  >
                    Approve
                  </button>
                  <button
                    @click="approveProfessional(professional.id, 'reject')"
                    class="btn btn-danger btn-sm"
                  >
                    Reject
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <h2 class="mb-5 display-5">Service Professionals</h2>
      <div class="table-responsive mt-4">
        <table
          class="table text-center table-borderless rounded-3 overflow-hidden"
        >
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Service</th>
              <th>Experience</th>
              <th>About</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody class="text-center table-group-divider">
            <tr v-for="(professional, index) in oldProfessionals" :key="index">
              <td>{{ index + 1 }}</td>
              <td>{{ professional.username }}</td>
              <td>
                {{
                  services.find(
                    (service) => service.id === professional.service_id
                  )?.name
                }}
              </td>
              <td>{{ professional.experience_years }}</td>
              <td>{{ professional.about }}</td>
              <td v-if="professional.active">
                <button
                  @click="blockUser(professional.id)"
                  class="btn btn-danger btn-sm"
                >
                  Block
                </button>
              </td>
              <td v-else>
                <button
                  @click="unblockUser(professional.id)"
                  class="btn btn-success btn-sm"
                >
                  Unblock
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Services Management -->
    <div v-if="$route.path === '/admin/services'">
      <div class="d-flex justify-content-between align-items-center">
        <h2 class="mb-5 display-5">Services Management</h2>
        <button
          class="btn btn-dark mb-3"
          data-bs-toggle="modal"
          data-bs-target="#addServiceModal"
        >
          Add New Service
        </button>
      </div>
      <div class="table-responsive">
        <table
          class="table text-center align-middle table-borderless rounded-3 overflow-hidden"
        >
          <thead>
            <tr>
              <th>ID</th>
              <th>Service Name</th>
              <th>Base Price</th>
              <th>Time Required</th>
              <th>Description</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody class="table-group-divider">
            <tr v-for="service in services" :key="service.id">
              <td>{{ service.id }}</td>
              <td>{{ service.name }}</td>
              <td>₹{{ service.base_price }}</td>
              <td>{{ service.time_required }} hrs</td>
              <td>{{ service.description }}</td>
              <td class="py-3">
                <div class="d-grid gap-2 d-md-flex justify-content-md-center">
                  <button
                    class="btn btn-outline-warning btn-sm px-3"
                    @click="startEdit(service)"
                    data-bs-toggle="modal"
                    data-bs-target="#editServiceModal"
                  >
                    Edit
                  </button>
                  <button
                    class="btn btn-outline-danger btn-sm px-3"
                    @click="deleteService(service.id)"
                  >
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <!-- Add Service Modal -->
      <div
        class="modal fade"
        id="addServiceModal"
        tabindex="-1"
        aria-labelledby="addServiceModalLabel"
        aria-modal="true"
        role="dialog"
      >
        <div class="modal-dialog">
          <div class="modal-content bg-dark text-light">
            <div class="modal-header border-secondary">
              <h5 class="modal-title" id="addServiceModalLabel">
                Add New Service
              </h5>
              <button
                type="button"
                class="btn-close btn-close-white"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body px-5 py-4">
              <form @submit.prevent="addservice">
                <div class="mb-3">
                  <label for="service_name" class="form-label"
                    >Service Name</label
                  >
                  <input
                    type="text"
                    class="form-control bg-dark text-light border-secondary"
                    id="service_name"
                    v-model="service_name"
                    required
                  />
                </div>
                <div class="mb-3">
                  <label for="base_price" class="form-label">Base Price</label>
                  <input
                    type="number"
                    class="form-control bg-dark text-light border-secondary"
                    id="base_price"
                    v-model="base_price"
                    required
                  />
                </div>
                <div class="mb-3">
                  <label for="time_required" class="form-label"
                    >Time Required (hrs)</label
                  >
                  <input
                    type="number"
                    class="form-control bg-dark text-light border-secondary"
                    id="time_required"
                    v-model="time_required"
                    required
                  />
                </div>
                <div class="mb-3">
                  <label for="description" class="form-label"
                    >Description</label
                  >
                  <input
                    type="text"
                    class="form-control bg-dark text-light border-secondary"
                    id="description"
                    v-model="description"
                    required
                  />
                </div>
                <div class="text-end mt-4">
                  <button
                    type="button"
                    class="btn btn-outline-light me-2"
                    data-bs-dismiss="modal"
                  >
                    Close
                  </button>
                  <button type="submit" class="btn btn-light">
                    Add Service
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
      <!-- Edit Service Modal -->
      <div
        class="modal fade"
        id="editServiceModal"
        tabindex="-1"
        aria-labelledby="editServiceModalLabel"
        aria-modal="true"
        role="dialog"
      >
        <div class="modal-dialog">
          <div class="modal-content bg-dark text-light">
            <div class="modal-header border-secondary">
              <h5 class="modal-title" id="editServiceModalLabel">
                Edit Service
              </h5>
              <button
                type="button"
                class="btn-close btn-close-white"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body px-5 py-4">
              <form @submit.prevent="updateService">
                <div class="mb-3">
                  <label for="edit_service_name" class="form-label"
                    >Service Name</label
                  >
                  <input
                    type="text"
                    class="form-control bg-dark text-light border-secondary"
                    id="edit_service_name"
                    v-model="edit_service_name"
                    required
                  />
                </div>
                <div class="mb-3">
                  <label for="edit_base_price" class="form-label"
                    >Base Price</label
                  >
                  <input
                    type="number"
                    class="form-control bg-dark text-light border-secondary"
                    id="edit_base_price"
                    v-model="edit_base_price"
                    required
                  />
                </div>
                <div class="mb-3">
                  <label for="edit_time_required" class="form-label"
                    >Time Required (hrs)</label
                  >
                  <input
                    type="number"
                    class="form-control bg-dark text-light border-secondary"
                    id="edit_time_required"
                    v-model="edit_time_required"
                    required
                  />
                </div>
                <div class="mb-3">
                  <label for="edit_description" class="form-label"
                    >Description</label
                  >
                  <input
                    type="text"
                    class="form-control bg-dark text-light border-secondary"
                    id="edit_description"
                    v-model="edit_description"
                    required
                  />
                </div>
                <div class="text-end mt-4">
                  <button
                    type="button"
                    class="btn btn-outline-light me-2"
                    data-bs-dismiss="modal"
                  >
                    Cancel
                  </button>
                  <button type="submit" class="btn btn-light">
                    Update Service
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, onUnmounted, watch, nextTick } from "vue";
import { useAuthStore } from "@/stores/authStore";
import { useServicesStore } from "@/stores/servicesStore";
import { useNotificationStore } from "@/stores/notificationStore";
import { Chart } from "chart.js/auto";
import { useRoute } from "vue-router";

const authStore = useAuthStore();
const servicesStore = useServicesStore();
const notificationStore = useNotificationStore();

const users = ref([]);

const customers = computed(() =>
  users.value.filter((user) => user.role === "customer")
);

const professionals = computed(() =>
  users.value.filter((user) => user.role === "service_professional")
);
const activeProfessionals = computed(() =>
  professionals.value.filter((user) => user.status === "approved")
);
const pendingApprovals = computed(() =>
  professionals.value.filter((user) => user.status === "pending")
);
const oldProfessionals = computed(() =>
  professionals.value.filter((user) => user.status !== "pending")
);

const service_name = ref("");
const base_price = ref("");
const time_required = ref("");
const description = ref("");

const editingService = ref(null);
const edit_service_name = ref("");
const edit_base_price = ref("");
const edit_time_required = ref("");
const edit_description = ref("");

const services = computed(() => servicesStore.sortedServices);
// Service related functions
const resetForm = () => {
  service_name.value = "";
  base_price.value = "";
  time_required.value = "";
  description.value = "";
};

const addservice = async () => {
  try {
    await servicesStore.addService(
      service_name.value,
      base_price.value,
      time_required.value,
      description.value
    );
    // Close modal using Bootstrap's API
    const modal = bootstrap.Modal.getInstance(
      document.getElementById("addServiceModal")
    );
    modal.hide();
    resetForm();
  } catch (error) {
    console.error("Error adding service:", error);
  }
};

const deleteService = async (id) => {
  await servicesStore.deleteService(id);
};

const startEdit = (service) => {
  editingService.value = service;
  edit_service_name.value = service.name;
  edit_base_price.value = service.base_price;
  edit_time_required.value = service.time_required;
  edit_description.value = service.description;
};

const resetEditForm = () => {
  editingService.value = null;
  edit_service_name.value = "";
  edit_base_price.value = "";
  edit_time_required.value = "";
  edit_description.value = "";
};

const updateService = async () => {
  try {
    if (!editingService.value) return;

    await servicesStore.updateService(
      editingService.value.id,
      edit_service_name.value,
      edit_base_price.value,
      edit_time_required.value,
      edit_description.value
    );

    // Close modal using Bootstrap's API
    const modal = bootstrap.Modal.getInstance(
      document.getElementById("editServiceModal")
    );
    modal.hide();
    resetEditForm();
  } catch (error) {
    console.error("Error updating service:", error);
  }
};
// End of service related functions

// Professional approval functions
const approveProfessional = async (userId, action) => {
  try {
    const response = await fetch(
      `http://localhost:5000/api/professionals/${userId}/approval`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: authStore.token,
        },
        body: JSON.stringify({
          action: action,
        }),
      }
    );

    if (!response.ok) {
      throw new Error("Failed to process approval");
    }

    await fetchUsers();
    notificationStore.addNotification({
      message: "Professional approved successfully",
      type: "success",
    });
  } catch (error) {
    console.error("Error:", error);
  }
};

const blockUser = async (userId) => {
  try {
    const response = await fetch(
      `http://localhost:5000/api/users/${userId}/block`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: authStore.token,
        },
      }
    );

    if (!response.ok) {
      throw new Error("Failed to block user");
    }

    await fetchUsers();
    notificationStore.addNotification({
      message: "User blocked",
      type: "info",
    });
  } catch (error) {
    console.error("Error:", error);
  }
};

const unblockUser = async (userId) => {
  try {
    const response = await fetch(
      `http://localhost:5000/api/users/${userId}/unblock`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: authStore.token,
        },
      }
    );

    if (!response.ok) {
      throw new Error("Failed to unblock user");
    }

    await fetchUsers();
    notificationStore.addNotification({
      message: "User Unblocked",
      type: "success",
    });
  } catch (error) {
    console.error("Error:", error);
  }
};
// End of professional approval functions

const fetchUsers = async () => {
  try {
    const response = await fetch("http://localhost:5000/api/users", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: authStore.token,
      },
    });

    if (!response.ok) {
      const text = await response.text();
      console.error("Error response:", text);
      throw new Error(`Server error: ${response.status}`);
    }

    const data = await response.json();
    users.value = data;
  } catch (err) {
    console.error("Error details:", err);
    users.value = [];
  }
};

const route = useRoute();
const chart = ref(null);

// Move chart initialization to a separate function
const initializeChart = () => {
  if (chart.value) {
    chart.value.destroy();
  }

  const ctx = document.getElementById("myChart");
  if (ctx && route.path === "/admin/dashboard") {
    chart.value = new Chart(ctx, {
      type: "bar",
      data: {
        labels: services.value.map((service) => service.name),
        datasets: [
          {
            label: "No of Bookings",
            data: services.value.map((service) => service.no_of_bookings),
            backgroundColor: [
              "rgba(255, 99, 132, 0.2)",
              "rgba(54, 162, 235, 0.2)",
              "rgba(255, 206, 86, 0.2)",
              "rgba(75, 192, 192, 0.2)",
            ],
            borderColor: [
              "rgba(255, 99, 132, 1)",
              "rgba(54, 162, 235, 1)",
              "rgba(255, 206, 86, 1)",
              "rgba(75, 192, 192, 1)",
            ],
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
          },
        },
        plugins: {
          legend: {
            color: "#0000002a",
          },
        },
      },
    });
  }
};

// Watch for route changes
watch(
  () => route.path,
  (newPath) => {
    if (newPath === "/admin/dashboard") {
      // Use nextTick to ensure DOM is updated
      nextTick(() => {
        initializeChart();
      });
    }
  }
);

onMounted(async () => {
  await fetchUsers();
  await servicesStore.fetchServices();
  if (route.path === "/admin/dashboard") {
    initializeChart();
  }
});

// Cleanup on unmount
onUnmounted(() => {
  if (chart.value) {
    chart.value.destroy();
  }
});
</script>

<style scoped>
.card {
  border: none;
  background-color: #fff;
  border-radius: 18px;
  box-shadow: 2px 4px 12px #00000090;
  overflow: hidden;
}

table {
  border: none;
  background-color: #fff;
  border-radius: 18px;
  box-shadow: 2px 4px 12px #00000090;
  overflow: hidden;
}
</style>
