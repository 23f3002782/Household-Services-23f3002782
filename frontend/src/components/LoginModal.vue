<template>
  <!-- Login Modal -->
  <div class="modal fade" id="loginModal" tabindex="-1" aria-labelledby="loginModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content bg-dark text-light">
        <div class="modal-header border-secondary">
          <h5 class="modal-title" id="loginModalLabel">Login</h5>
          <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="handleLogin">
            <div class="mb-3">
              <label for="email" class="form-label">Email address</label>
              <input type="email" class="form-control bg-dark text-light border-secondary" id="email" v-model="email" required>
            </div>
            <div class="mb-3">
              <label for="password" class="form-label">Password</label>
              <input type="password" class="form-control bg-dark text-light border-secondary" id="password" v-model="password" required>
            </div>
            <div class="text-end">
              <button type="button" class="btn btn-outline-light me-2" data-bs-dismiss="modal">Close</button>
              <button type="submit" class="btn btn-light" data-bs-dismiss="modal">Login</button>
            </div>
          </form>
          <div class="mt-3 text-center">
            <p>Don't have an account? 
              <a href="#" class="text-light" data-bs-dismiss="modal" data-bs-toggle="modal" data-bs-target="#signupModal">Sign up</a>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/authStore'

const authStore = useAuthStore()
const email = ref('')
const password = ref('')

const handleLogin = async () => {
  const result = await authStore.login({
    email: email.value,
    password: password.value
  })

  if (result.success) {
    email.value = ''
    password.value = ''
    
    const modalElement = document.getElementById('loginModal')
    const modal = bootstrap.Modal.getInstance(modalElement)
    modal.hide()
  } 
}
</script>
