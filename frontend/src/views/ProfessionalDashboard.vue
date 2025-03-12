<template>
    <div>
      <h1>Professional Dashboard</h1>
      <p>Welcome, {{ authStore.user.username }}</p>
    </div>
  
  </template>
  
  <script setup>
  import { useAuthStore } from '@/stores/authStore';
  
  const authStore = useAuthStore();
  </script>
  
  <style>
  
  </style>