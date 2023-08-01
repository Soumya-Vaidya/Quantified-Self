<template>
  <div>
    <NavBar :user="true" />
    <div class="container mt-5">
      <div>
        <h2 style="text-transform: capitalize">{{ trackername.name }}</h2>
        <p style="text-transform: capitalize">{{ trackername.desc }}</p>
        <br />
        <div class="container-sm" v-if="logs.length">
          <button
            type="button"
            class="btn btn-light"
            @click="downloadLog(trackername.tracker_id)"
          >
            Download
          </button>
          <br />
          <br />
          <h3>Graph</h3>
          <div
            class="container-sm"
            style="max-width: 600px"
            v-if="trackername.type == 'multiple' || trackername.type == 'bool'"
          >
            <canvas id="myChart"></canvas>
          </div>
          <div class="container-sm" v-else>
            <canvas id="myChart" width="400" height="125"></canvas>
          </div>
          <br />
        </div>
        <br />
        <h3>Logs</h3>
        <p v-if="!logs.length">No Logs Yet!</p>
        <div class="table-responsive">
          <table
            class="table"
            style="text-transform: capitalize"
            v-if="logs.length"
          >
            <thead>
              <tr>
                <th scope="col">On</th>
                <th scope="col">Value</th>
                <th scope="col">Note</th>
                <th scope="col"></th>
                <th scope="col"></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="log in logs" :key="log.log_id">
                <td>{{ log.timestamp }}</td>
                <td>{{ log.value }}</td>
                <td>{{ log.note }}</td>
                <td>
                  <router-link
                    class="btn btn-warning mx-2 mt-2"
                    :to="{
                      name: 'updatelog',
                      params: {
                        tracker_id: trackername.tracker_id,
                        log_id: log.log_id,
                      },
                    }"
                    >Update</router-link
                  >
                </td>
                <td>
                  <button
                    class="btn btn-danger mx-2 mt-2"
                    @click="deleteLog(log.ltracker_id, log.log_id)"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Chart from "chart.js/auto";
export default {
  data() {
    return {
      logs: {},
      trackername: {},
      graph: [],
      check: null,
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
    getLogs() {
      fetch(
        `${process.env.VUE_APP_server_ip}/api/trackers/${this.tracker_id}/logs`,
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
          this.logs = data;
          //   if (this.logs) {
          //     this.check = 1;
          //   }
        })
        .catch((error) => {
          console.log(error);
        });
    },

    getTrackerName() {
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
          this.createChart(this.trackername.type);
        })
        .catch((error) => {
          console.log(error);
        });
    },

    deleteLog(tracker_id, log_id) {
      fetch(
        `${process.env.VUE_APP_server_ip}/api/trackers/${tracker_id}/logs/${log_id}`,
        {
          method: "DELETE",
          headers: {
            Accept: "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST,PATCH,OPTIONS",
          },
        }
      )
        .then(() => {
          // this.$router.push({
          //     name:'home'
          // })
          // this.$router.go();
        })
        .catch((error) => {
          console.log(error);
        });
      let index = this.logs.indexOf(log_id);
      this.logs.splice(index, 1);
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

    createChart(type) {
      fetch(`${process.env.VUE_APP_server_ip}/api/chart/${this.tracker_id}`, {
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
          this.graph = data;
          console.log(this.graph);
          if (type == "multiple" || type == "bool") {
            const ctx = document.getElementById("myChart");
            const myChart = new Chart(ctx, {
              type: "doughnut",
              //   type: "bar",
              data: {
                labels: this.graph.options,
                datasets: [
                  {
                    label: this.graph.options,
                    data: this.graph.count,
                    backgroundColor: [
                      "rgb(255, 99, 132)",
                      "rgb(54, 162, 235)",
                      "rgb(255, 205, 86)",
                      "rgb(255, 159, 64)",
                      "rgb(75, 192, 192)",
                      "rgb(153, 102, 255)",
                      "rgb(201, 203, 207)",
                    ],
                    hoverOffset: 4,
                  },
                ],
                options: {
                  scales: {
                    y: {
                      beginAtZero: true,
                    },
                  },
                  //   responsive: false,
                  //   maintainAspectRatio: false,
                  //   aspectRatio: 1,
                },
              },
            });
            myChart;
          } else if (type == "td" || type == "numerical") {
            console.log(this.graph.value);
            const ctx = document.getElementById("myChart");
            const myChart = new Chart(ctx, {
              type: "line",
              data: {
                labels: this.graph.timestamp,
                datasets: [
                  {
                    label: "Values",
                    data: this.graph.value,
                    fill: false,
                    borderColor: "rgb(75, 192, 192)",
                    tension: 0.1,
                  },
                ],
              },
              options: {
                // maintainAspectRatio: false,
                scales: {
                  y: {
                    beginAtZero: true,
                  },
                },
              },
            });
            myChart;
          }
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },

  created() {
    this.getLogs(), this.getTrackerName();
  },

  mounted() {},
};
</script>

<style>
/* #container-sm {
  min-width: 512px;
} */
/* #myChart {
  height: 512px !important;
  width: 512px !important;
} */
</style>