<template>
  <div>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg py-3">
      <div class="container">
        <a class="navbar-brand" href="#">🎵 Streamify</a>
        <div class="d-flex align-items-center">
          <button class="btn btn-outline-light me-2" @click="navigateTo('login')">Login</button>
          <button class="btn btn-primary" @click="navigateTo('signup')">Sign Up</button>
        </div>
      </div>
    </nav>

    <!-- Landing Section -->
    <section class="landing-section text-center">
      <div class="container">
        <h1>Stream Your Favorite Music Anytime, Anywhere</h1>
        <p>Explore millions of songs, podcasts, and playlists with one click.</p>
        <button class="btn btn-primary btn-lg" @click="navigateTo('signup')">Get Started</button>
      </div>
      <!-- Decorative Shapes -->
      <div class="shapes">
        <div class="circle"></div>
        <div class="triangle"></div>
        <div class="rectangle"></div>
      </div>
    </section>

    <!-- Scroll Section -->
    <section class="scroll-section text-center py-5">
      <h2>Join the Party!</h2>
      <p>Sign up today and elevate your music streaming experience.</p>
      <button class="btn btn-primary btn-lg" @click="navigateTo('signup')">Sign Up</button>
      <button class="btn btn-outline-secondary btn-lg" @click="navigateTo('login')">Login</button>
    </section>
  </div>
</template>

<script>
export default {
  methods: {
    navigateTo(route) {
      alert(`Navigate to ${route}`);
    },
  },
};
</script>

<style scoped>
/* Navbar */
.navbar {
  background: linear-gradient(90deg, #6C63FF, #FF6584);
  color: white;
}

.navbar-brand {
  font-size: 1.5rem;
  font-weight: bold;
}

.btn {
  border-radius: 20px;
}

/* Landing Section */
.landing-section {
  background: linear-gradient(to bottom, #F5F6FA, #6C63FF);
  padding: 100px 20px;
  position: relative;
  overflow: hidden;
  color: #333333;
}

.landing-section h1 {
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 20px;
}

.shapes {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
}

.circle {
  width: 200px;
  height: 200px;
  background: #FF6584;
  border-radius: 50%;
  position: absolute;
  top: 20%;
  left: 10%;
}

.triangle {
  width: 0;
  height: 0;
  border-left: 100px solid transparent;
  border-right: 100px solid transparent;
  border-bottom: 200px solid #FFD166;
  position: absolute;
  top: 50%;
  left: 80%;
}

.rectangle {
  width: 150px;
  height: 50px;
  background: #06D6A0;
  position: absolute;
  bottom: 10%;
  right: 20%;
}

/* Scroll Section */
.scroll-section {
  background-color: #F5F6FA;
  color: #333333;
}

.scroll-section h2 {
  font-size: 2rem;
  margin-bottom: 20px;
}
</style>
