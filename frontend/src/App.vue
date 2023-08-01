<template>
  <div id="app">
    <!-- <NavBar   /> -->
    <router-view />
  </div>
</template>

<script>
// import NavBar from "./components/NavBar.vue";

export default {
  name: "App",
  components: {
    // NavBar,
  },
  data() {
    return {
      user: null,
      trackers: [],
      name: {},
    };
  },

  methods: {
    getName() {
      fetch(`${process.env.VUE_APP_server_ip}/api/user`, {
        method: "GET",
        headers: {
          Accept: "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "POST,PATCH,OPTIONS",
        },
      })
        .then((resp) => resp.json())
        .then((data) => {
          console.log(data);
          this.name = data;
          this.user = this.name.username;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },

  created() {
    this.getName();
  },
};
</script>

<style>
</style>
