<template>
  <div>
    <NavBar />
    <main class="form-signin w-100 m-auto">
      <form @submit.prevent="getUserData">
        <h1 class="h3 mb-3 fw-normal">Please sign in</h1>

        <input
          type="text"
          v-model="username"
          class="form-control"
          id="floatingInput"
          placeholder="Username"
          required
        />

        <input
          type="password"
          v-model="password"
          class="form-control"
          id="floatingPassword"
          placeholder="Password"
          required
        />

        <button class="w-100 btn btn-lg btn-primary" type="submit">
          Sign in
        </button>
      </form>
      <small id="passwordHelpBlock" class="form-text text-muted" v-if="error">
        {{ error }}
      </small>
    </main>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      username: "",
      password: "",
      error: "",
    };
  },
  components: {
    NavBar: () => import(`./NavBar.vue`),
  },
  methods: {
    async getUserData() {
      try {
        const response = await axios.post(
          `${process.env.VUE_APP_server_ip}/api/login`,
          {
            username: this.username,
            password: this.password,
          }
        );
        console.log(response.data);
        // localStorage.setItem("token", response.data.access_token);
        // this.$router.push({ name: "home" });

        if (response.data == "Invalid Password") {
          this.error = "Invalid username/ password";
        } else {
          localStorage.setItem("token", response.data.access_token);
          localStorage.setItem("is_logged_in", true);
          this.$router.push({ name: "home" });
        }
        // console.log(response.data);
      } catch (e) {
        this.error = "Invalid username/ password";
      }
    },
  },
};
</script>

<style>
.form-signin {
  max-width: 330px;
  padding: 15px;
}

.form-signin .form-floating:focus-within {
  z-index: 2;
}

.form-signin input[type="email"] {
  margin-bottom: -1px;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
}

.form-signin input[type="password"] {
  margin-bottom: 10px;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}
</style>