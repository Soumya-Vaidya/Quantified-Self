<template>
  <div>
    <NavBar />
    <div class="container mt-5">
      <!-- <h2>Hello, {{ name.username }}!</h2> -->
      <br />
      <h3>Your Details:</h3>
      <br />
      <p>Username: {{ user.username }}</p>
      <p>Email: {{ user.email }}</p>
      <br />
      <br />
      <h3>Reminders:</h3>
      <br />
      <p>Would you like to recieve daily reminders?</p>
      <div class="form-group">
        <input
          class="form-check-input"
          type="radio"
          name="inlineRadioOptions"
          id="inlineRadio1"
          value="Yes"
          :checked="this.user.webhook"
          v-model="reminder"
        />
        <label class="form-check-label" for="inlineRadio1"> Yes please!</label
        ><br />
        <input
          class="form-check-input"
          type="radio"
          name="inlineRadioOptions"
          id="inlineRadio1"
          value="No"
          v-model="reminder"
          :checked="!this.user.webhook"
        />
        <label class="form-check-label" for="inlineRadio1"> Nope!</label>
      </div>
      <br />
      <div v-if="reminder == 'Yes'">
        <div class="form-group">
          <label for="exampleFormControlInput1">Enter webhook: </label>
          <input
            type="text"
            name="webhook"
            placeholder="Paste your Google Chat webhook here!"
            required
            v-model="user.webhook"
            class="form-control"
            id="exampleFormControlInput1"
          />
          <br />
        </div>
      </div>
      <div class="form-group">
        <button class="btn btn-primary" v-on:click="send_message">
          Confirm!
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      message: "This is a QuantifiedSelf reminder!",
      reminder: "",
      user: "",
    };
  },
  components: {
    NavBar: () => import(`./NavBar.vue`),
  },
  methods: {
    send_message() {
      if (this.reminder == "Yes") {
        let data = { text: this.message };

        fetch(this.user.webhook, {
          method: "POST",
          body: JSON.stringify(data),
        })
          .then((r) => r.json())
          .then((d) => {
            console.log(d);
            this.updateWebhook();
            // this.$router.go();
          })
          .catch((e) => console.log("Some error occured: ", e));
      } else {
        this.user.webhook = null;
        this.updateWebhook();
      }
    },

    updateWebhook() {
      fetch(`${process.env.VUE_APP_server_ip}/api/webhook`, {
        method: "PUT",
        headers: {
          Accept: "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "POST,PATCH,OPTIONS",
        },
        body: JSON.stringify(this.user),
      })
        .then((resp) => resp.json())
        .then(() => {
          this.$router.go();
        })
        .catch((error) => {
          console.log(error);
        });
    },

    getUserDetails() {
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
          this.user = data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },

  created() {
    this.getUserDetails();
  },
};
</script>

<style>
</style>