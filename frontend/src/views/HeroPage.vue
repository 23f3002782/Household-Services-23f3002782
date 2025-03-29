<template>
	<div class="site-wrapper">
		<section class="row py-2 py-md-5">
			<div class="col-md-7 p-5 text-center text-md-start">
				<h1 class="name display-1 text-uppercase fw-semibold mb-5">
					Havenly
				</h1>
				<div class="description px-0 px-md-2 py-md-4">
					<p class="fs-5">
						Your one-stop solution for seamless household services.
						Connect with trusted professionals, book services
						effortlessly, and enjoy a stress-free home experience.
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
					class="img-fluid rounded rounded-top-5 shadow"
					src="https://images.pexels.com/photos/6197106/pexels-photo-6197106.jpeg?auto=compress&cs=tinysrgb&w=600"
					alt="Sweeping image"
				/>
			</div>
		</section>

		<section class="section asymmetric-section py-2 py-md-5">
			<div class="container py-2 py-md-5">
				<div class="row align-items-center py-2 py-md-5">
					<div
						class="col-md-4 order-md-1 text-center text-md-start animate"
					>
						<h2 class="fw-bold">Our Vision</h2>
						<p class="text-muted">
							At Havenly, we believe in a world where everyday
							household chores transform into seamless
							experiences.
						</p>
					</div>
					<div class="col-md-8 order-md-2 animate delay-1">
						<img
							src="https://images.pexels.com/photos/1866149/pexels-photo-1866149.jpeg?auto=compress&cs=tinysrgb&w=800"
							class="img-fluid rounded shadow"
							alt="Modern home interior"
							loading="lazy"
						/>
					</div>
				</div>
			</div>
		</section>

		<section class="section asymmetric-section py-2 py-md-5 bg-light">
			<div class="container py-2 py-md-5">
				<div class="row align-items-center py-2 py-md-5">
					<div class="col-md-8 order-2 order-md-1 animate">
						<img
							src="https://images.pexels.com/photos/3184325/pexels-photo-3184325.jpeg?auto=compress&cs=tinysrgb&w=800"
							class="img-fluid rounded shadow"
							alt="Professional service"
							loading="lazy"
						/>
					</div>
					<div
						class="col-md-4 order-1 order-md-2 animate delay-1 text-center text-md-start"
					>
						<h2 class="fw-bold">Innovative Solutions</h2>
						<p class="text-muted">
							We integrate technology with top-quality
							professionals to ensure that every service is
							executed with precision.
						</p>
					</div>
				</div>
			</div>
		</section>

		<section class="section asymmetric-section py-2 py-md-5">
			<div class="container py-2 py-md-5">
				<div class="row align-items-center py-2 py-md-5">
					<div
						class="col-md-5 order-md-1 animate text-center text-md-start"
					>
						<h2 class="fw-bold">A Tailored Experience</h2>
						<p class="text-muted">
							Our platform adapts to your needs, offering
							personalized solutions that redefine convenience and
							luxury in home services.
						</p>
					</div>
					<div class="col-md-7 order-md-2 animate delay-1">
						<img
							src="https://images.pexels.com/photos/276528/pexels-photo-276528.jpeg?auto=compress&cs=tinysrgb&w=800"
							class="img-fluid rounded shadow"
							alt="Tailored experience"
							loading="lazy"
						/>
					</div>
				</div>
			</div>
		</section>

		<!-- "Why Choose Havenly" Section -->
		<section class="why-choose bg-light py-2 py-md-5">
			<div class="container py-2 py-md-5">
				<h2 class="text-center fw-bold mb-5 animate">
					Why Choose Havenly ?
				</h2>
				<div class="row g-4 py-2 py-md-5">
					<div
						class="col-md-4"
						v-for="(item, index) in whyChoose"
						:key="index"
					>
						<div class="card border-0 animate delay-{{ index }}">
							<img
								:src="item.img"
								class="card-img-top"
								:alt="item.title"
								loading="lazy"
							/>
							<div class="card-body text-center">
								<h5 class="card-title">{{ item.title }}</h5>
								<p class="card-text text-muted">
									{{ item.description }}
								</p>
							</div>
						</div>
					</div>
				</div>
			</div>
		</section>

		<!-- "Discover Our Services" Section -->
		<section class="discover-services py-5 mb-5">
			<div class="container">
				<div class="row align-items-center g-4">
					<div class="col-md-7 animate text-center text-md-start">
						<h2 class="fw-bold">Discover Our Services</h2>
						<p class="text-muted">
							Explore a wide range of services tailored to bring
							ease and elegance to your daily life.
						</p>
						<button
							type="button"
							class="btn btn-dark btn-lg"
							@click="toServices"
						>
							Explore Services
						</button>
					</div>
					<div class="col-md-5 animate delay-1">
						<img
							src="https://images.pexels.com/photos/4239103/pexels-photo-4239103.jpeg?auto=compress&cs=tinysrgb&w=600"
							class="img-fluid rounded shadow"
							alt="Discover services"
							loading="lazy"
						/>
					</div>
				</div>
			</div>
		</section>
	</div>
</template>

<script setup>
	import { onMounted, ref } from "vue";
	import { useRouter } from "vue-router";

	const router = useRouter();

	const toServices = () => router.push("/services");

	const whyChoose = ref([
		{
			title: "Quality",
			description:
				"Our services are backed by industry-leading standards ensuring excellence.",
			img: "https://images.pexels.com/photos/3184465/pexels-photo-3184465.jpeg?auto=compress&cs=tinysrgb&w=600",
		},
		{
			title: "Reliability",
			description:
				"We value your time, delivering prompt and dependable services every time.",
			img: "https://images.pexels.com/photos/3184321/pexels-photo-3184321.jpeg?auto=compress&cs=tinysrgb&w=600",
		},
		{
			title: "Innovation",
			description:
				"Our cutting-edge technology ensures a seamless and personalized experience.",
			img: "https://images.pexels.com/photos/373543/pexels-photo-373543.jpeg?auto=compress&cs=tinysrgb&w=600",
		},
	]);

	onMounted(() => {
		const animatedElements = document.querySelectorAll(".animate");
		const observer = new IntersectionObserver(
			(entries) => {
				entries.forEach((entry) => {
					if (entry.isIntersecting) {
						entry.target.classList.add("in-view");
					}
				});
			},
			{ threshold: 0.15 }
		);
		animatedElements.forEach((el) => observer.observe(el));
	});
</script>

<style scoped>
	.name {
		font-family: "Poiret One", serif;
		font-size: 13vw;
	}

	/* .site-wrapper {
  overflow-x: hidden;
} */

	html {
		scroll-behavior: smooth;
	}

	.asymmetric-section {
		position: relative;
	}
	.asymmetric-section:nth-of-type(odd) {
		background: #fff;
	}
	.asymmetric-section:nth-of-type(even) {
		background: whitesmoke;
	}

	/* .asymmetric-section img {
  width: 100%;
} */

	/* "Why Choose Havenly" Section */
	.why-choose h2 {
		font-size: 2.5rem;
	}
	.card {
		border: none;
		border-radius: 18px;
		box-shadow: 2px 4px 12px #00000014;
		overflow: hidden;
		transition: transform 0.6s ease-out, opacity 0.6s ease-out;
		opacity: 0;
		transform: translateY(20px);
	}
	.card.in-view {
		opacity: 1;
		transform: translateY(0);
	}
	.card img {
		object-fit: cover;
		height: 200px;
		transition: transform 0.4s ease;
	}
	.card:hover img {
		transform: scale(1.1);
	}

	.discover-services h2 {
		font-size: 2.5rem;
	}
	.discover-services p {
		font-size: 1.1rem;
	}

	.animate {
		opacity: 0;
		transform: translateY(20px);
		transition: all 0.8s ease-out;
	}
	.animate.in-view {
		opacity: 1;
		transform: translateY(0);
	}
	.delay-1 {
		transition-delay: 0.4s;
	}
	.delay-2 {
		transition-delay: 0.8s;
	}
	.delay-3 {
		transition-delay: 1.2s;
	}
</style>
