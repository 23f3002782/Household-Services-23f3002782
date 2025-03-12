import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useNotificationStore = defineStore('notification', () => {
  const notifications = ref([])

  const addNotification = ({ message, type = 'info', timeout = 3000 }) => {
    const id = Date.now()
    notifications.value.push({
      id,
      message,
      type,
      timeout
    })

    // Automatically remove notification after timeout
    setTimeout(() => {
      removeNotification(id)
    }, timeout)
  }

  const removeNotification = (id) => {
    notifications.value = notifications.value.filter(notification => notification.id !== id)
  }

  const clearNotifications = () => {
    notifications.value = []
  }

  return {
    notifications,
    addNotification,
    removeNotification,
    clearNotifications
  }
}) 