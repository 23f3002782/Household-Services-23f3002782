<template>
  <div>
    <h1>Services</h1>
    <div v-if="servicesStore.loading">
      <p>Loading...</p>
    </div>
    <div v-else-if="servicesStore.error">
      <p>Error: {{ servicesStore.error }}</p>
    </div>
    <div v-else>
      <div v-for="service in servicesStore.sortedServices" :key="service.id">
        <h2>{{ service.name }}</h2>
        <p>{{ service.description }}</p>
      </div>
    </div>
  </div>

</template>

<script setup>
import { useServicesStore } from "@/stores/servicesStore";

const servicesStore = useServicesStore();
</script>

<style>

</style>