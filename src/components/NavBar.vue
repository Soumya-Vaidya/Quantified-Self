<template>
  <nav class="navbar navbar-expand-lg bg-light">
    <div class="container-fluid">
      <router-link to="/dashboard" class="navbar-brand" v-if="user"
        >Quantified Self</router-link
      >
      <router-link to="/login" class="navbar-brand" v-if="!user"
        >Quantified Self</router-link
      >
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0" v-if="!user">
          <li class="nav-item">
            <router-link class="nav-link" to="/register">Register</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/login">Login</router-link>
          </li>
        </ul>
        <ul class="navbar-nav me-auto mb-2 mb-lg-0" v-if="user">
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
  props: ["user"],
  methods: {
    handleClick() {
      localStorage.removeItem("token");
      this.$router.push({
        name: "login",
      });
    },
  },
};
</script>

<style>
</style>