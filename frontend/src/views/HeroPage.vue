<template>
  <div class="container-fluid mt-3">
    <div class="row">
      <div class="col-md-7 p-5 text-center text-md-start">
        <h1 class="name display-1 text-uppercase fw-semibold mb-5">Havenly</h1>
        <div class="description px-0 px-md-2 py-md-4">
          <p class="fs-5">
            Your one-stop solution for seamless household services. Connect with
            trusted professionals, book services effortlessly, and enjoy a
            stress-free home experience.
          </p>
        </div>
        <button
          type="button"
          class="btn btn-outline-dark btn-lg"
          data-bs-toggle="modal"
          data-bs-target="#signupModal"
        >
          Sign Up Now
        </button>
      </div>
      <div class="col-md-5 text-center text-md-start p-4 p-md-0">
        <img
          class="img-fluid"
          src="https://images.pexels.com/photos/6197106/pexels-photo-6197106.jpeg?auto=compress&cs=tinysrgb&w=600"
          alt="Sweeping image"
        />
      </div>
    </div>

    <div class="container mt-5 g-5">
      <div class="row text-center text-md-start mt-5 mb-5 row-animate">
        <div class="col-md-4 py-5 img-col order-2 order-md-1">
          <img
            class="img-fluid"
            src="https://media.istockphoto.com/id/1276530099/photo/woman-cleaning-couch-with-vacuum-cleaner-at-home-cleaning-service-concept.jpg?s=612x612&w=0&k=20&c=5qj7mEVu85Fs1XDtB1_PTbiyhq_aKDFIlkdb5ZU9FFo="
            alt=""
          />
        </div>
        <div
          class="col-md-6 p-5 d-flex flex-column justify-content-center order-1 order-md-2"
        >
          <p class="fs-5">
            Lorem ipsum, dolor sit amet consectetur adipisicing elit. Eveniet
            ullam vero nobis eos dolorem. Repellendus veniam, nostrum beatae
            quisquam delectus harum natus numquam nesciunt officiis consequuntur
            quam aperiam voluptates aliquam.
          </p>
        </div>
      </div>
      <div class="row text-center text-md-start mt-5 mb-5 row-animate">
        <div class="col-md-2"></div>
        <div class="col-md-6 p-5 d-flex flex-column justify-content-center">
          <p class="fs-5 text-center text-md-end">
            Lorem ipsum dolor, sit amet consectetur adipisicing elit. Sunt
            laudantium libero optio rem nulla molestias obcaecati laborum
            doloremque enim veritatis?
          </p>
        </div>
        <div class="col-md-4 py-5 img-col">
          <img
            class="img-fluid"
            src="https://media.istockphoto.com/id/1067496776/photo/top-view-of-drill-tool-and-another-equipment-on-wood-table-furniture-assembly-improvement-or.jpg?s=612x612&w=0&k=20&c=pW5vu2TK9yaOvqLG8jktB59DRIvVdr6eAVnI72RwPPI="
            alt=""
          />
        </div>
      </div>
      <div class="row text-center text-md-start mt-5 mb-5 row-animate">
        <div class="col-md-4 py-5 img-col order-2 order-md-1">
          <img
            class="img-fluid"
            src="https://media.istockphoto.com/id/1361116682/photo/plumber-fixing-a-leaking-bathroom-faucet.jpg?s=612x612&w=0&k=20&c=THa1uoYgW4gGz0C8YMqenM58UFY-uD1X79dP3obYLLI="
            alt=""
          />
        </div>
        <div
          class="col-md-6 p-5 d-flex flex-column justify-content-center order-1 order-md-2"
        >
          <p class="fs-5">
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Laboriosam
            minus perspiciatis veritatis velit ducimus amet vel voluptatum
            repellat sunt? Similique nulla beatae dicta quo fuga
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup></script>

<style scoped>
.name {
  font-family: "Poiret One", serif;
  font-size: 11vw;
}

.img-fluid {
  border-radius: 50px;
  transition: 0.4s ease;
}
.row-animate:hover img {
  transform: scale(1.05);
}
</style>
