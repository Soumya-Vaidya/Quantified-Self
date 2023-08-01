<template>
  <div>
    <NavBar />
    <main class="form-signin w-100 m-auto">
      <form @submit.prevent="handleSubmit">
        <h1 class="h3 mb-3 fw-normal">Please register</h1>

        <input
          type="text"
          v-model="username"
          class="form-control"
          placeholder="Username"
          required
        />

        <input
          type="email"
          v-model="email"
          class="form-control"
          placeholder="Email"
          required
        />

        <input
          type="password"
          v-model="password"
          class="form-control"
          placeholder="Password"
          required
        />

        <button class="w-100 btn btn-lg btn-primary" type="submit">
          Submit
        </button>
      </form>
      <small id="passwordHelpBlock" class="form-text text-muted" v-if="error">
        {{ error }}
      </small>
    </main>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      email: "",
      password: "",
      error: null,
    };
  },
  components: {
    NavBar: () => import(`./NavBar.vue`),
  },

  methods: {
    handleSubmit() {
      fetch(`${process.env.VUE_APP_server_ip}/api/register`, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "POST,PATCH,OPTIONS",
        },
        body: JSON.stringify({
          username: this.username,
          email: this.email,
          password: this.password,
        }),
      })
        .then((response) => {
          response.json();
          console.log(response);
        })
        .then(() => {
          this.$router.push({
            name: "login",
          });
        })
        .catch((error) => {
          console.log(error);
          this.error = "Username/ Email already registered";
        });
    },
  },
};
</script>

<style>
</style>