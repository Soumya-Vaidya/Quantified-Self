<template>
  <div>
    <NavBar />
    <div class="container mt-4">
      <h3>Update Tracker</h3>
      <br />
      <form @submit.prevent="updateTracker">
        <div class="form-group">
          <label for="exampleFormControlInput1">Name</label>
          <input
            type="text"
            name="name"
            placeholder="This is the name of your tracker"
            required
            v-model="trackername.name"
            class="form-control"
            id="exampleFormControlInput1"
          />
        </div>
        <br />
        <div class="form-group">
          <label for="exampleFormControlTextarea1">Description</label>
          <textarea
            placeholder="Describe it!"
            v-model="trackername.desc"
            class="form-control"
            id="exampleFormControlTextarea1"
            rows="3"
          ></textarea>
        </div>
        <br />
        <div class="form-group">
          <button type="submit" class="btn btn-primary">Update!</button>
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
      desc: null,
      error: null,
      trackername: {},
    };
  },
  components: {
    NavBar: () => import(`./NavBar.vue`),
  },
  props: {
    tracker_id: {
      type: [Number, String],
      required: true,
    },
  },

  methods: {
    updateTracker() {
      fetch(
        `${process.env.VUE_APP_server_ip}/api/trackers/${this.tracker_id}`,
        {
          method: "PUT",
          headers: {
            Accept: "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST,PATCH,OPTIONS",
          },
          body: JSON.stringify(this.trackername),
        }
      )
        .then((resp) => resp.json())
        .then(() => {
          this.$router.push({
            name: "home",
          });
        })
        .catch((error) => {
          console.log(error);
        });
    },

    getTrackerDetails() {
      fetch(
        `${process.env.VUE_APP_server_ip}/api/trackers/${this.tracker_id}`,
        {
          method: "GET",
          headers: {
            Accept: "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST,PATCH,OPTIONS",
          },
        }
      )
        .then((resp) => resp.json())
        .then((data) => {
          this.trackername = data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  mounted() {
    this.getTrackerDetails();
  },
};
</script>

<style>
</style>