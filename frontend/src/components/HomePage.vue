<template>
  <div>
    <NavBar />
    <div class="container mt-5" v-if="!check">
      <h2>Hello, {{ name.username }}!</h2>
      <br />
      <router-link
        class="btn btn-success mx-2 mt-2"
        :to="{ name: 'createtracker' }"
        >ADD Tracker
      </router-link>
      <br />
      <br />
      <div class="table-responsive">
        <table class="table" style="text-transform: capitalize">
          <thead>
            <tr>
              <th scope="col">Name</th>
              <th scope="col">Last Update</th>
              <th scope="col">Recent Value</th>
              <th scope="col"></th>
              <th scope="col"></th>
              <th scope="col"></th>
              <th scope="col"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="tracker in trackers" :key="tracker.tracker_id">
              <td>
                <router-link
                  :to="{
                    name: 'trackerlogs',
                    params: { tracker_id: tracker.tracker_id },
                  }"
                >
                  {{ tracker.name }}
                </router-link>
              </td>
              <td>{{ tracker.last_modified }}</td>
              <td>{{ tracker.last_modified_value }}</td>
              <td>
                <router-link
                  class="btn btn-success mx-2 mt-2"
                  :to="{
                    name: 'createlog',
                    params: {
                      user_id: name.user_id,
                      tracker_id: tracker.tracker_id,
                    },
                  }"
                  >+</router-link
                >
              </td>
              <td>
                <router-link
                  class="btn btn-warning mx-2 mt-2"
                  :to="{
                    name: 'updatetracker',
                    params: {
                      user_id: name.user_id,
                      tracker_id: tracker.tracker_id,
                    },
                  }"
                  >Update</router-link
                >
              </td>
              <td>
                <button
                  class="btn btn-danger mx-2 mt-2"
                  @click="deleteTracker(tracker.tracker_id)"
                >
                  Delete
                </button>
              </td>
              <td>
                <button
                  type="button"
                  class="btn btn-light mx-2 mt-2"
                  @click="downloadLog(tracker.tracker_id)"
                >
                  Download
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      check: null,
      user: null,
      trackers: [],
      name: {},
      last_time: "",
      last_value: "",
    };
  },
  components: {
    NavBar: () => import(`./NavBar.vue`),
  },

  methods: {
    getTrackers() {
      fetch(`${process.env.VUE_APP_server_ip}/api/trackers`, {
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
          this.trackers.push(...data);
        })
        .catch((error) => {
          this.check = 1;
          console.log(error);
          this.$router.push({
            name: "login",
          });
        });
    },

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

    deleteTracker(tracker_id) {
      fetch(`${process.env.VUE_APP_server_ip}/api/trackers/${tracker_id}`, {
        method: "DELETE",
        headers: {
          Accept: "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "POST,PATCH,OPTIONS",
        },
      })
        .then(() => {
          // this.$router.go();
        })
        .catch((error) => {
          console.log(error);
        });
      let index = this.trackers.indexOf(tracker_id);
      this.trackers.splice(index, 1);
    },

    downloadLog(tracker_id) {
      fetch(
        `${process.env.VUE_APP_server_ip}/api/trackers/${tracker_id}/download`,
        {
          method: "POST",
          headers: {
            Accept: "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST,PATCH,OPTIONS",
          },
        }
      )
        .then((response) => response.blob())
        .then((blob) => {
          var url = window.URL.createObjectURL(blob);
          var a = document.createElement("a");
          a.href = url;
          a.download = `./export/${tracker_id}_logs.csv`;
          document.body.appendChild(a);
          a.click();
          a.remove();
          //   this.$router.go();
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },

  created() {
    this.getTrackers(), this.getName();
  },
};
</script>

<style>
</style>