<template>
  <div class="modal fade" id="signupModal" tabindex="-1" aria-labelledby="signupModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content bg-dark text-light">
        <div class="modal-header border-secondary">
          <h5 class="modal-title" id="signupModalLabel">Sign Up</h5>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <!-- Tabs -->
          <ul class="nav nav-tabs nav-fill mb-4" id="signupTabs">
            <li class="nav-item">
              <a class="nav-link text-light" 
                 :class="{ 'active bg-secondary': userType === 'customer' }"
                 @click="userType = 'customer'" 
                 href="#">Customer</a>
            </li>
            <li class="nav-item">
              <a class="nav-link text-light" 
                 :class="{ 'active bg-secondary': userType === 'professional' }"
                 @click="userType = 'professional'" 
                 href="#">Professional</a>
            </li>
          </ul>

          <!-- Customer Form -->
          <form v-if="userType === 'customer'" @submit.prevent="handleCustomerSignup">
            <div class="mb-3">
              <label for="customerEmail" class="form-label">Email address</label>
              <input type="email" class="form-control bg-dark text-light border-secondary" id="customerEmail" v-model="customerForm.email" required>
            </div>
            <div class="mb-3">
              <label for="customerName" class="form-label">Full Name</label>
              <input type="text" class="form-control bg-dark text-light border-secondary" id="customerName" v-model="customerForm.username" required>
            </div>
            <div class="mb-3">
              <label for="address" class="form-label">Address</label>
              <input type="text" class="form-control bg-dark text-light border-secondary" id="address" v-model="customerForm.address" required>
            </div>
            <div class="mb-3">
              <label for="customerPassword" class="form-label">Password</label>
              <input type="password" class="form-control bg-dark text-light border-secondary" id="customerPassword" v-model="customerForm.password" required>
            </div>
            <div class="text-end">
              <button type="button" class="btn btn-outline-light me-2" data-bs-dismiss="modal">Close</button>
              <button type="submit" class="btn btn-light">Sign Up</button>
            </div>
          </form>

          <!-- Professional Form -->
          <form v-if="userType === 'professional'" @submit.prevent="handleProfessionalSignup">
            <div class="mb-3">
              <label for="profEmail" class="form-label">Email address</label>
              <input type="email" class="form-control bg-dark text-light border-secondary" id="profEmail" v-model="professionalForm.email" required>
            </div>
            <div class="mb-3">
              <label for="profName" class="form-label">Full Name</label>
              <input type="text" class="form-control bg-dark text-light border-secondary" id="profName" v-model="professionalForm.username" required>
            </div>
            <div class="mb-3">
              <label for="about" class="form-label">About</label>
              <textarea class="form-control bg-dark text-light border-secondary" id="about" v-model="professionalForm.about" required></textarea>
            </div>
            <div class="mb-3">
              <label for="profService" class="form-label">Service Type</label>
              <select class="form-select bg-dark text-light border-secondary" id="profService" v-model="professionalForm.service_id" required>
                <option value="">Select a service</option>
                <option v-for="service in servicesStore.sortedServices" :key="service.id" :value="service.id">
                  {{ service.name }}
                </option>
              </select>
            </div>
            <div class="mb-3">
              <label for="profExperience" class="form-label">Years of Experience</label>
              <input type="number" class="form-control bg-dark text-light border-secondary" id="profExperience" v-model="professionalForm.experience_years" required>
            </div>
            <div class="mb-3">
              <label for="profPassword" class="form-label">Password</label>
              <input type="password" class="form-control bg-dark text-light border-secondary" id="profPassword" v-model="professionalForm.password" required>
            </div>
            <div class="text-end">
              <button type="button" class="btn btn-outline-light me-2" data-bs-dismiss="modal">Close</button>
              <button type="submit" class="btn btn-light">Sign Up</button>
            </div>
          </form>
          <div class="mt-3 text-center">
            <p>Already have an account? 
              <a href="#" class="text-light" data-bs-dismiss="modal" data-bs-toggle="modal" data-bs-target="#loginModal">Login</a>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useServicesStore } from '@/stores/servicesStore'
import { useAuthStore } from '@/stores/authStore'

const authStore = useAuthStore()
const servicesStore = useServicesStore()
const userType = ref('customer')

const customerForm = ref({
  username: '',
  email: '',
  address: '',
  password: ''
})

const professionalForm = ref({
  username: '',
  email: '',
  about: '',
  service_id: '',
  experience_years: '',
  password: ''
})

const handleCustomerSignup = async () => {
  const result = await authStore.customerSignup(customerForm.value)

  if (result.success) {
    // Clear form
    customerForm.value = {
      username: '',
      email: '',
      address: '',
      password: ''
    }
    
    // Close modal
    const modalElement = document.getElementById('signupModal')
    const modal = bootstrap.Modal.getInstance(modalElement)
    modal.hide()
  } else {
    alert(result.error)
  }
}

const handleProfessionalSignup = async () => {
  const result = await authStore.professionalSignup(professionalForm.value)

  if (result.success) {
    // Clear form
    professionalForm.value = {
      username: '',
      email: '',
      about: '',
      service_id: '',
      experience_years: '',
      password: ''
    }
    
    // Close modal
    const modalElement = document.getElementById('signupModal')
    const modal = bootstrap.Modal.getInstance(modalElement)
    modal.hide()
  } else {
    alert(result.error)
  }
}
</script>

<style scoped>
.nav-tabs .nav-link {
  color: #fff;
  border: none;
}

.nav-tabs .nav-link:hover {
  border: none;
  color: #e5ddd6;
}

.nav-tabs .nav-link.active {
  background-color: #444;
  color: #fff;
  border: none;
}

.nav-tabs {
  border-bottom: 1px solid #444;
}
</style>
