<template>
  <nav class="navbar navbar-expand-lg bg-light">
    <div class="container-fluid">
      <router-link to="/dashboard" class="navbar-brand" v-if="is_logged_in"
        >Quantified Self</router-link
      >
      <router-link to="/login" class="navbar-brand" v-if="!is_logged_in"
        >Quantified Self</router-link
      >

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0" v-if="!is_logged_in">
          <li class="nav-item">
            <router-link class="nav-link" to="/register">Register</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/login">Login</router-link>
          </li>
        </ul>
        <ul class="navbar-nav me-auto mb-2 mb-lg-0" v-if="is_logged_in">
          <!-- <li class="nav-item">
            <router-link class="nav-link" to="/profile">Profile</router-link>
          </li> -->
          <li class="nav-item">
            <a class="nav-link" href="javascript:void(0)" @click="handleClick"
              >Logout</a
            >
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  methods: {
    handleClick() {
      localStorage.removeItem("token");
      localStorage.removeItem("is_logged_in");
      this.$router.push({
        name: "login",
      });
    },
  },
  created() {
    this.is_logged_in = localStorage.getItem("is_logged_in");
  },
};
</script>

<style>
</style>