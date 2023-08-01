<template>
  <div>
    <NavBar />
    <div class="container mt-4">
      <h3>Add Tracker</h3>
      <br />
      <form @submit.prevent="insertTracker">
        <div class="form-group">
          <label for="exampleFormControlInput1">Name</label>
          <input
            type="text"
            name="name"
            placeholder="This is the name of your tracker"
            required
            v-model="name"
            class="form-control"
            id="exampleFormControlInput1"
          />
        </div>
        <br />
        <div class="form-group">
          <label for="inputState">Type</label>
          <select
            name="type"
            v-model="type"
            id="inputState"
            class="form-control"
          >
            <option value="numerical" selected>Numerical</option>
            <option value="multiple">Multiple Values</option>
            <option value="td">Date and Time</option>
            <option value="bool">Boolean</option>
          </select>
        </div>
        <br />
        <div class="form-group" v-if="type == 'multiple'">
          <label for="exampleFormControlInput1">Settings</label>
          <input
            type="text"
            name="settings"
            placeholder="Choice for multiple input type only"
            v-model="settings"
            class="form-control"
            id="exampleFormControlInput1"
          />
        </div>
        <br />
        <div class="form-group">
          <label for="exampleFormControlTextarea1">Description</label>
          <textarea
            placeholder="Describe it!"
            v-model="desc"
            class="form-control"
            id="exampleFormControlTextarea1"
            rows="3"
          ></textarea>
        </div>
        <br />
        <div class="form-group">
          <button type="submit" class="btn btn-primary">Add!</button>
        </div>
      </form>

      <div v-if="error">
        <small id="passwordHelpBlock" class="form-text text-muted">
          {{ error }}
        </small>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      name: null,
      type: null,
      settings: null,
      desc: null,
      error: null,
    };
  },
  components: {
    NavBar: () => import(`./NavBar.vue`),
  },

  methods: {
    insertTracker() {
      if (!this.name || !this.type) {
        this.error = "Please enter all fields";
      } else {
        fetch(`${process.env.VUE_APP_server_ip}/api/trackers`, {
          method: "POST",
          headers: {
            Accept: "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST,PATCH,OPTIONS",
          },
          body: JSON.stringify({
            tuser_id: this.user_id,
            name: this.name,
            type: this.type,
            desc: this.desc,
            settings: this.settings,
          }),
        })
          .then((resp) => resp.json())
          .then(() => {
            this.$router.push({
              name: "home",
            });
          })
          .catch((error) => {
            console.log(error);
          });
      }
    },
  },
};
</script>

<style>
</style>