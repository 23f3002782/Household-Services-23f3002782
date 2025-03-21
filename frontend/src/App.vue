<script setup>
import { onMounted } from "vue";
import Navbar from "./components/Navbar.vue";
import Footer from "./components/Footer.vue";
import { useServicesStore } from "./stores/servicesStore";
import NotificationList from "./components/NotificationList.vue";

const servicesStore = useServicesStore();

onMounted(() => {
  servicesStore.fetchServices();
});
</script>

<template>
  <div id="app">
    <NotificationList />
    <Navbar />
    <div class="router-view"><RouterView /></div>

    <Footer />
  </div>
</template>

<style>
body {
  /* background-color: #f2f2f2; */
  /* background-color: hsla(0, 0%, 100%, 0.1); */
  background-color: #f5f5f7;
}

body::-webkit-scrollbar {
  display: none;
}

* {
  font-family: "Montserrat", sans-serif;
  font-style: normal;
  margin: 0;
  padding: 0px;
  box-sizing: border-box;
}

.material-symbols-outlined {
  font-variation-settings: "FILL" 0, "wght" 400, "GRAD" 0, "opsz" 24;
}

.router-view {
  min-height: calc(100vh - 60px);
}
</style>
