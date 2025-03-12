<template>
  <footer class="footer">
    <div class="container">
      <div class="row text-center">
        <div class="col-md-4">
          <h5>About Us</h5>
          <p>
            We provide seamless household services. Connect with trusted
            professionals and enjoy a stress-free home experience.
          </p>
        </div>
        <div class="col-md-4">
          <h5>Quick Links</h5>
          <ul class="list-unstyled">
            <li><router-link to="/">Home</router-link></li>
            <li><router-link to="/">About</router-link></li>
            <li><router-link to="/">Contact</router-link></li>
          </ul>
        </div>
        <div class="col-md-4">
          <h5>Contact Us</h5>
          <p>Email: support@havenly.com</p>
          <p>Phone: +123 456 7890</p>
        </div>
      </div>
      <div class="text-center mt-3">
        <p>&copy; 2023 Havenly. All rights reserved.</p>
      </div>
    </div>
  </footer>
</template>

<script setup></script>

<style scoped>
* {
  background-color: #333;
  color: white;
}
.footer {
  background-color: #333;
  color: white;
  padding: 2rem 0;
}

.footer h5 {
  margin-bottom: 1rem;
}

.footer p,
.footer a {
  color: white;
  text-decoration: none;
  transition: all 0.5 ease;
}

.footer a:hover {
  text-decoration: underline;
}
</style>
