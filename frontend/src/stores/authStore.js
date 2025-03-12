import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useNotificationStore } from './notificationStore'

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()
  const notificationStore = useNotificationStore()
  const user = ref(JSON.parse(localStorage.getItem('user')) || null)
  const token = ref(localStorage.getItem('token') || null)

  const isAuthenticated = computed(() => !!user.value && !!token.value)

  const setUserData = (userData, userToken) => {
    user.value = userData
    token.value = userToken
    localStorage.setItem('user', JSON.stringify(userData))
    localStorage.setItem('token', userToken)
  }

  const clearUserData = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('user')
    localStorage.removeItem('token')
  }

  const login = async (credentials) => {
    try {
      const response = await fetch('http://localhost:5000/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials)
      })

      const data = await response.json()

      if (response.ok) {
        setUserData(data.user, data.token)
        notificationStore.addNotification({
          message: 'Successfully logged in!',
          type: 'success'
        })

        if (data.user.role === 'admin') {
          router.push('/admin/dashboard')
        } else if (data.user.role === 'professional') {
          router.push('/professional/dashboard')
        } else {
          router.push('/customer/dashboard')
        }

        return { success: true }
      } else {
        throw new Error(data.message || 'Login failed')
      }
    } catch (err) {
      notificationStore.addNotification({
        message: err.message,
        type: 'error'
      })
      return { success: false, error: err.message }
    }
  }

  const customerSignup = async (customerData) => {
    try {
      const response = await fetch('http://localhost:5000/api/signup/customer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(customerData)
      })

      const data = await response.json()

      if (response.ok) {
        setUserData(data.user, data.token)
        notificationStore.addNotification({
          message: 'Welcome! Your account has been created successfully.',
          type: 'success'
        })
        router.push('/customer/dashboard')
        return { success: true }
      } else {
        throw new Error(data.message || 'Customer signup failed')
      }
    } catch (err) {
      notificationStore.addNotification({
        message: err.message,
        type: 'error'
      })
      return { success: false, error: err.message }
    }
  }

  const professionalSignup = async (professionalData) => {
    try {
      const response = await fetch('http://localhost:5000/api/signup/service_professional', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(professionalData)
      })

      const data = await response.json()

      if (response.ok) {
        notificationStore.addNotification({
          message: 'Your registration is pending approval. We will notify you once your account is approved.',
          type: 'info',
          timeout: 5000
        })
        router.push('/')
        return { success: true }
      } else {
        throw new Error(data.message || 'Professional signup failed')
      }
    } catch (err) {
      notificationStore.addNotification({
        message: err.message,
        type: 'error'
      })
      return { success: false, error: err.message }
    }
  }

  const logout = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/logout', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token.value}`
        }
      })

      if (response.ok) {
        clearUserData()
        notificationStore.addNotification({
          message: 'Successfully logged out',
          type: 'success'
        })
        router.push('/')
      }
    } catch (err) {
      console.error('Logout error:', err)
      clearUserData()
      notificationStore.addNotification({
        message: 'Logged out with errors',
        type: 'warning'
      })
      router.push('/')
    }
  }

  return {
    user,
    token,
    isAuthenticated,
    login,
    customerSignup,
    professionalSignup,
    logout
  }
})
