<template>
  <div>
    <NavBar />
    <div class="container mt-4">
      <h3>Update Log</h3>
      <h4 style="text-transform: capitalize">{{ trackername.name }}</h4>
      <br />
      <form @submit.prevent="updateLog">
        <div class="form-group">
          <label for="exampleFormControlInput1">Date and Time</label>
          <input
            type="datetime-local"
            v-model="logdetails.timestamp"
            name="timestamp"
            class="form-control"
            id="exampleFormControlInput1"
          />
        </div>
        <br />
        <div class="form-group" v-if="trackername.type == 'numerical'">
          <label for="exampleFormControlInput1">Value</label>
          <input
            input
            type="number"
            v-model="logdetails.value"
            step="any"
            name="value"
            class="form-control"
            id="exampleFormControlInput1"
          />
        </div>
        <div class="form-group" v-else-if="trackername.type == 'bool'">
          <label for="exampleFormControlInput1">Boolean Value</label>
          <input
            type="number"
            v-model="logdetails.value"
            name="value"
            min="0"
            max="1"
            class="form-control"
            id="exampleFormControlInput1"
          />
        </div>
        <div class="form-group" v-else-if="trackername.type == 'td'">
          <label for="exampleFormControlInput1">Time Spent</label>
          <input
            input
            type="time"
            v-model="logdetails.value"
            name="value"
            class="form-control"
            id="exampleFormControlInput1"
          />
        </div>
        <div
          class="form-check form-check-inline"
          v-else-if="trackername.type == 'multiple'"
        >
          <div v-for="s in splitComma(trackername.settings)" :key="s">
            <input
              class="form-check-input"
              type="radio"
              name="inlineRadioOptions"
              id="inlineRadio1"
              :value="s"
              v-model="logdetails.value"
            />
            <label class="form-check-label" for="inlineRadio1">{{ s }}</label>
          </div>
        </div>
        <br />
        <br />
        <div class="form-group">
          <label for="exampleFormControlInput1">Note</label>
          <input
            type="text"
            v-model="logdetails.note"
            name="note"
            placeholder="Anything else you want to note!"
            class="form-control"
            id="exampleFormControlInput1"
          />
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
      error: null,
      trackername: {},
      s: {},
      logdetails: {},
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
    log_id: {
      type: [Number, String],
      required: true,
    },
  },

  methods: {
    splitComma(myString) {
      return myString.split(",");
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

    updateLog() {
      fetch(
        `${process.env.VUE_APP_server_ip}/api/trackers/${this.tracker_id}/logs/${this.log_id}`,
        {
          method: "PUT",
          headers: {
            Accept: "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST,PATCH,OPTIONS",
          },
          body: JSON.stringify(this.logdetails),
        }
      )
        .then((resp) => resp.json())
        .then(() => {
          this.$router.push({
            name: "trackerlogs",
          });
        })
        .catch((error) => {
          console.log(error);
        });
    },

    getLogs() {
      fetch(
        `${process.env.VUE_APP_server_ip}/api/trackers/${this.tracker_id}/logs/${this.log_id}`,
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
          this.logdetails = data;
          console.log(this.logdetails);
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },

  created() {
    this.getTrackerDetails();
  },

  mounted() {
    this.getLogs();
  },
};
</script>

<style>
</style>