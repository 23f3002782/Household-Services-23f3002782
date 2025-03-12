import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useNotificationStore } from './notificationStore'
import { useAuthStore } from './authStore'
export const useServicesStore = defineStore('services', () => {
  const services = ref([])
  const notificationStore = useNotificationStore()
  const authStore = useAuthStore()

  // Fetch all services
  const fetchServices = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/services')
      
      if (!response.ok) {
        throw new Error('Failed to fetch services')
      }

      const data = await response.json()
      services.value = data
    } catch (err) {
      console.error('Error fetching services:', err)
    }
  }

  const addService = async (name, base_price, time_required, description) => {
    try {
      const response = await fetch('http://localhost:5000/api/services', {
        method: 'POST',
        headers: {
          'Authorization': authStore.token,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, base_price, time_required, description })
      })
      if (!response.ok) {
        throw new Error('Failed to add service')
      }
      notificationStore.addNotification({message: 'Service added successfully', type: 'success'})
      await fetchServices()
    } catch (err) {
      console.error('Error adding service:', err)
      notificationStore.addNotification({message: 'Error adding service', type: 'danger'})
    }
  }

  const deleteService = async (id) => {
    try {
      const response = await fetch(`http://localhost:5000/api/services/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': authStore.token,
        }
      })
      if (!response.ok) {
        throw new Error('Failed to delete service')
      }
      notificationStore.addNotification({message: 'Service deleted successfully', type: 'success'})
      await fetchServices()
    } catch (err) {
      console.error('Error deleting service:', err)
      notificationStore.addNotification({message: 'Error deleting service', type: 'danger'})
    }
  }
  
  const updateService = async (id, name, base_price, time_required, description) => {
    try {
      const response = await fetch(`http://localhost:5000/api/services/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': authStore.token
        },
        body: JSON.stringify({
          name,
          base_price,
          time_required,
          description
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to update service');
      }

      notificationStore.addNotification({message: 'Service updated successfully', type: 'success'})
      // Update the service in the local state
      const updatedService = await response.json();
      const index = services.value.findIndex(s => s.id === id);
      if (index !== -1) {
        services.value[index] = updatedService;
      }

      return { success: true };
    } catch (error) {
      console.error('Error updating service:', error);
      return { success: false, error: error.message };
    }
  };

  // Computed property for sorted services
  const sortedServices = computed(() => {
    return [...services.value].sort((a, b) => a.id - b.id)
  })

  return { 
    services,
    fetchServices,
    sortedServices,
    addService,
    deleteService,
    updateService
  }
})
