<template>
  <div class="dashboard-container">
    <!-- Toggle Button for Mobile -->
    <button 
      class="btn btn-primary position-fixed d-lg-none sidebar-toggle" 
      type="button" 
      data-bs-toggle="offcanvas" 
      data-bs-target="#sidebar" 
      aria-controls="sidebar"
    >
    <span class="material-symbols-outlined">
menu
</span>
    </button>

    <!-- Sidebar -->
    <div 
      class="sidebar offcanvas-lg offcanvas-start" 
      tabindex="-1" 
      id="sidebar" 
      aria-labelledby="sidebarLabel"
    >
      <div class="offcanvas-header d-lg-none">
        <h5 class="offcanvas-title" id="sidebarLabel">Menu</h5>
        <button 
          type="button" 
          class="btn-close" 
          data-bs-dismiss="offcanvas" 
          data-bs-target="#sidebar" 
          aria-label="Close"
        ></button>
      </div>
      
      <div class="offcanvas-body p-0">
        <div class="sidebar-header text-center py-4">
          <div class="user-avatar mb-3">
            <img 
              src="https://via.placeholder.com/80" 
              alt="User Avatar" 
              class="rounded-circle"
              width="80"
              height="80"
            >
          </div>
          <h6 class="mb-0">{{ authStore.user.username }}</h6>
          <small class="text-muted">Customer</small>
        </div>

        <ul class="nav flex-column">
          <li class="nav-item">
            <a 
              class="nav-link" 
              :class="{ active: currentView === 'overview' }"
              @click="currentView = 'overview'"
              href="#"
            >
              <i class="bi bi-house-door me-2"></i>
              Overview
            </a>
          </li>
          <li class="nav-item">
            <a 
              class="nav-link" 
              :class="{ active: currentView === 'bookings' }"
              @click="currentView = 'bookings'"
              href="#"
            >
              <i class="bi bi-calendar-check me-2"></i>
              My Bookings
            </a>
          </li>
          <li class="nav-item">
            <a 
              class="nav-link" 
              :class="{ active: currentView === 'services' }"
              @click="currentView = 'services'"
              href="#"
            >
              <i class="bi bi-tools me-2"></i>
              Services
            </a>
          </li>
          <li class="nav-item">
            <a 
              class="nav-link" 
              :class="{ active: currentView === 'profile' }"
              @click="currentView = 'profile'"
              href="#"
            >
              <i class="bi bi-person me-2"></i>
              Profile
            </a>
          </li>
          <li class="nav-item">
            <a 
              class="nav-link" 
              :class="{ active: currentView === 'settings' }"
              @click="currentView = 'settings'"
              href="#"
            >
              <i class="bi bi-gear me-2"></i>
              Settings
            </a>
          </li>
        </ul>
      </div>
    </div>

    <!-- Main Content -->
    <main class="main-content">
      <div class="container-fluid py-4">
        <!-- Overview Section -->
        <div v-if="currentView === 'overview'">
          <h2 class="mb-4">Dashboard Overview</h2>
          <div class="row g-4">
            <div class="col-md-4">
              <div class="card">
                <div class="card-body">
                  <h5 class="card-title">Active Bookings</h5>
                  <h2 class="card-text">3</h2>
                </div>
              </div>
            </div>
            <div class="col-md-4">
              <div class="card">
                <div class="card-body">
                  <h5 class="card-title">Completed Services</h5>
                  <h2 class="card-text">12</h2>
                </div>
              </div>
            </div>
            <div class="col-md-4">
              <div class="card">
                <div class="card-body">
                  <h5 class="card-title">Total Spent</h5>
                  <h2 class="card-text">$450</h2>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Other views can be added here -->
        <div v-if="currentView !== 'overview'">
          <h2 class="mb-4">{{ currentView.charAt(0).toUpperCase() + currentView.slice(1) }}</h2>
          <p>Content for {{ currentView }} will be displayed here.</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/authStore';

const authStore = useAuthStore();
const currentView = ref('overview');
</script>

<style scoped>
.dashboard-container {
  display: flex;
  min-height: 100vh;
}

.sidebar-toggle {
  top: 1rem;
  left: 1rem;
  z-index: 1045;
  background-color: #2f4858;
  border: none;
}

.sidebar-toggle:hover,
.sidebar-toggle:focus {
  background-color: #ff9a3c;
}

/* Base sidebar styles */
.sidebar {
  width: 280px;
  background-color: #2f4858 !important; /* Force background color */
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  min-height: 100vh;
}

.offcanvas-header {
  background-color: #2f4858;
}

.btn-close {
  filter: invert(1) grayscale(100%) brightness(200%);
}

.sidebar .nav-link {
  color: rgba(255, 255, 255, 0.8);
  padding: 0.75rem 1.5rem;
  transition: all 0.3s;
}

.sidebar .nav-link:hover,
.sidebar .nav-link.active {
  color: #ffffff;
  background-color: #ff9a3c;
}

.sidebar-header {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar h6,
.sidebar .offcanvas-title {
  color: white;
}

.sidebar small.text-muted {
  color: rgba(255, 255, 255, 0.6) !important;
}

.main-content {
  flex: 1;
  background-color: #f9fafb;
  margin-left: 280px;
  min-height: 100vh;
  width: calc(100% - 280px);
}

.card {
  border: none;
  border-radius: 10px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-5px);
}

/* Responsive Styles */
@media (max-width: 991.98px) {
  .main-content {
    margin-left: 0;
    width: 100%;
  }
  
  .sidebar {
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
  }
}
</style>