<script setup>
import axios from "axios";
import { ref, onMounted, computed } from "vue";
import { useStore } from "vuex";

const store = useStore();
const alerts = ref([]);
const offset = ref(0);
const limit = 10;
const isLoading = ref(false);
const isAuthenticated = computed(() => store.getters.isAuthenticated);

function refresh() {
  isLoading.value = true;
  offset.value = 0;
  
  axios
    .get("/refresh")
    .then(() => {
      loadAlerts();
    });
}


function loadAlerts() {
  axios
    .get(`/alerts/${offset.value}`)
    .then((response) => {
      const newAlerts = response.data.map(formatAlert);
      if (offset.value === 0) {
        alerts.value = newAlerts;
      } else {
        alerts.value = [...alerts.value, ...newAlerts];
      }
      offset.value += limit;
    })
    .catch((error) => {
      console.error("Error loading alerts:", error);
    })
    .finally(() => {
      isLoading.value = false;
    });
}

function formatAlert(alert) {
  const inputDate = new Date(alert.created_at);
  const day = inputDate.getDate().toString().padStart(2, "0");
  const month = (inputDate.getMonth() + 1).toString().padStart(2, "0");
  const year = inputDate.getFullYear().toString().slice(-2);
  const hours = inputDate.getHours().toString().padStart(2, "0");
  const minutes = inputDate.getMinutes().toString().padStart(2, "0");
  const formattedDate = `${day}.${month}.${year} ${hours}:${minutes}`;
  return { ...alert, created_at: formattedDate };
}

function loadMore() {
  loadAlerts();
}

function ackAlert(alertId) {
  axios
    .get(`/alert/${alertId}/ack`, {
      headers: { Authorization: `Bearer ${store.getters.getToken}` },
    })
    .then(() => {
      const alertIndex = alerts.value.findIndex(
        (alert) => alert.id === alertId
      );
      if (alertIndex !== -1) {
        alerts.value[alertIndex].is_acked = !alerts.value[alertIndex].is_acked;
      }
    })
    .catch((error) => {});
}

onMounted(() => {
  loadAlerts();
});
</script>

<template>
  <section>
    <div class="isLoading" v-if="isLoading">
      <div class="lds-roller">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
      </div>
    </div>
    <header>
      <h2>Alerts</h2>
      <button v-if="isAuthenticated" class="refresh" @click="refresh">Refresh</button>
    </header>
    <ul
      class="alerts"
      v-infinite-scroll="loadMore"
      infinite-scroll-distance="200"
    >
      <li v-if="!isLoading" v-for="alert in alerts" :key="alert.id" 
          :class="{'alert': true, 'acked': isAuthenticated && alert.is_acked}">

        <header>
          <span :class="'level ' + alert.scoreText.toLowerCase()">
            {{ alert.scoreText.toLowerCase() }}
          </span>
          <div class="info">
            <p class="title">{{ alert.id }}</p>
            <p class="time">{{ alert.created_at }}</p>
          </div>

          <button v-if="isAuthenticated" @click="() => ackAlert(alert.id)">
            <span v-if="!alert.is_acked">ACK</span>
            <span v-if="alert.is_acked">UNACK</span>
          </button>
        </header>

        <main>
          <p>{{ alert.description }}</p>
        </main>

        <footer>
          <ul>
            <li>Status: {{ alert.status }}</li>
            <li>Score: {{ alert.score }}</li>
            <li>
              <a :href="alert.url" target="_blank" rel="noopener noreferrer"
                >Read more</a
              >
            </li>
          </ul>
        </footer>
      </li>
    </ul>
    <button v-if="isAuthenticated" class="loadMore" @click="loadMore">Load more</button>
  </section>
</template>

<style scoped lang="scss">
@import "@/assets/scss/include/variables.scss";

section {
  width: 100%;
  max-width: 850px;
  min-height: 80vh;
  box-sizing: border-box;
  overflow: hidden;
  padding-bottom: 2rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  position: relative;

  @media (min-width: 768px) {
    height: 100%;
    min-height: 70vh;
  }

  .isLoading {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    min-height: 100vh;
    border-radius: 5px;
    background: $background;
    border: 1px solid $lighter-background;
    display: flex;
    justify-content: center;
    padding-top: 10rem;
    box-sizing: border-box;
    z-index: 9;

    .lds-roller {
      display: inline-block;
      position: relative;
      width: 80px;
      height: 80px;
    }
    .lds-roller div {
      animation: lds-roller 1.2s cubic-bezier(0.5, 0, 0.5, 1) infinite;
      transform-origin: 40px 40px;
    }
    .lds-roller div:after {
      content: " ";
      display: block;
      position: absolute;
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: $darker-foreground;
      margin: -4px 0 0 -4px;
    }
    .lds-roller div:nth-child(1) {
      animation-delay: -0.036s;
    }
    .lds-roller div:nth-child(1):after {
      top: 63px;
      left: 63px;
    }
    .lds-roller div:nth-child(2) {
      animation-delay: -0.072s;
    }
    .lds-roller div:nth-child(2):after {
      top: 68px;
      left: 56px;
    }
    .lds-roller div:nth-child(3) {
      animation-delay: -0.108s;
    }
    .lds-roller div:nth-child(3):after {
      top: 71px;
      left: 48px;
    }
    .lds-roller div:nth-child(4) {
      animation-delay: -0.144s;
    }
    .lds-roller div:nth-child(4):after {
      top: 72px;
      left: 40px;
    }
    .lds-roller div:nth-child(5) {
      animation-delay: -0.18s;
    }
    .lds-roller div:nth-child(5):after {
      top: 71px;
      left: 32px;
    }
    .lds-roller div:nth-child(6) {
      animation-delay: -0.216s;
    }
    .lds-roller div:nth-child(6):after {
      top: 68px;
      left: 24px;
    }
    .lds-roller div:nth-child(7) {
      animation-delay: -0.252s;
    }
    .lds-roller div:nth-child(7):after {
      top: 63px;
      left: 17px;
    }
    .lds-roller div:nth-child(8) {
      animation-delay: -0.288s;
    }
    .lds-roller div:nth-child(8):after {
      top: 56px;
      left: 12px;
    }
    @keyframes lds-roller {
      0% {
        transform: rotate(0deg);
      }
      100% {
        transform: rotate(360deg);
      }
    }
  }

  header {
    display: flex;
    width: 100%;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 3rem;

    h2 {
      padding: 0;
      font-size: 0.85rem;

      @media (min-width: 768px) {
        font-size: 1.3rem;
      }
    }

    button.refresh {
      background: $lighter-background;
      color: $darker-foreground;
    }
  }

  button.loadMore {
    margin: 0 auto;
    background: transparent;
    width: 100%;
    text-align: center;
    padding-top: 3rem;
  }

  ul.alerts {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 3rem;

    li.alert {
      display: flex;
      flex-direction: column;
      background: $lighter-background;
      padding: 1rem;
      box-sizing: border-box;
      border-radius: 5px;

      &.acked {
        opacity: 0.3;
      }

      header {
        width: 100%;
        display: grid;
        grid-template-columns: 0.75fr 1.5fr 0.75fr;
        align-items: center;
        gap: 1rem;
        color: $foreground;
        padding-bottom: 0rem;

        @media (min-width: 768px) {
          grid-template-columns: 0.3fr 2.4fr 0.3fr;
        }

        .level {
          box-sizing: border-box;
          font-weight: 700;
          font-size: 0.8rem;
          padding: 0.5rem;
          background-color: $alert-undefined;
          border-radius: 5px;
          text-align: center;
          color: white;

          @media (min-width: 768px) {
            font-size: 0.9rem;
          }

          &.critical {
            background-color: $alert-critical;
          }
          &.high {
            background-color: $alert-high;
          }
          &.medium {
            background-color: $alert-medium;
          }
          &.low {
            background-color: $alert-low;
          }
        }

        .info {
          @media (min-width: 768px) {
            display: flex;
            gap: 0.5rem;
          }
          .title {
            font-size: 1.3rem;
            margin: 0;
            padding: 0;
          }

          .time {
            font-size: 0.9rem;
            color: $darker-foreground;
            margin: 0;
            padding: 0;
          }
        }
      }

      main {
        color: $darker-foreground;
        p {
          word-wrap: break-word;
        }
      }

      footer {
        width: 100%;
        ul {
          display: flex;
          flex-direction: row;
          justify-content: space-between;
          width: 100%;
          list-style: none;
          margin: 0;
          padding: 0;
          font-size: 0.9rem;

          @media (min-width: 768px) {
            justify-content: flex-start;
            gap: 1rem;
          }

          li {
            a {
              color: inherit;
              text-decoration: none;
              &:hover {
                cursor: pointer;
                opacity: 0.5;
              }
            }
          }
        }
      }
    }
  }
}
</style>
