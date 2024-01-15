<script setup>
import axios from 'axios';
import { ref, onMounted, computed } from 'vue';
import { useStore } from "vuex";
import { useToast } from "vue-toastification";

import Stats from '../components/Stats.vue';
import Filters from '../components/Filters.vue';
import AlertList from '../components/AlertsList.vue';

onMounted(() => {
  loadAlerts();
});

const toast = useToast();
const store = useStore();
const isAuthenticated = computed(() => store.getters.isAuthenticated);

const offset = ref(0);
const limit = 10;
const alerts = ref([]);
const isLoading = ref(false);
const alertsStats = ref([]);

function loadAlerts() {
  axios
    .get(`/alerts/${offset.value}`)
    .then(response =>{
      let resp = response.data.map(formatAlert);
      if (offset.value === 0) {
        alerts.value = resp;
      } else {
        alerts.value = [...alerts.value, ...resp];
      }
    })

    loadAlertsStats();
}

function loadAlertsStats() {
  axios.get('/stats/alerts')
    .then(res => {
      alertsStats.value = Object.entries(res.data).map(([key, value]) => {
        return [key, value];
      });
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

function handleRefreshEvent(){
  isLoading.value = true;
  axios.get("/refresh")
    .then(() => {
      offset.value = 0;
      loadAlerts();
      toast.success("Alerts refreshed");
    })
    .finally(() => {
      isLoading.value = false;
    });
}

function handleLoadMoreEvent(){
  offset.value += limit;
  loadAlerts();
}

function handleAckEvent(alertId){
  console.log('ack');
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
    });
}
</script>

<template>
  <section :class="{
    'content': true,
    'center': !isAuthenticated,
    'isLoadingC': isLoading
  }">
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

    <section v-if="isAuthenticated" class="desktop">
      <Stats :stats="alertsStats"/>
      <Filters />
    </section>
    <AlertList class="alerts" :alerts="alerts" @refresh="handleRefreshEvent"
            @loadMore="handleLoadMoreEvent" @ack="handleAckEvent"/>
  </section>
</template>


<style scoped lang="scss">
@import "@/assets/scss/include/variables.scss";

.content{
  width: 100%;
  display: flex;
  justify-content: center;
  margin-top: 3rem;
  gap: 3rem;
  position: relative;

  @media (min-width: 900px) and (max-width: 1000px){
    flex-direction: column;
    align-items: center;
  }

  @media (min-width: 1001px){
    justify-content: space-between;

    &.center{
      justify-content: center;
    }
  }

  &.isLoadingC .desktop{
    opacity: 0;
  }
  section.desktop{
    display: none;
    gap: 3rem;
    max-width: 850px;
    opacity: 1;
    transition: 0.5s opacity;

    @media (min-width: 900px) and (max-width: 1000px){
      display: flex;
      width: 100%;

      .filters{ display: none;}
  }
    
    @media (min-width: 1001px){
      display: flex;
      flex-direction: column;
    }
  }

  &.isLoadingC .alerts{
    opacity: 0;
  }
  .alerts{
    opacity: 1;
    transition: 0.5s opacity;
    @media (min-width: 1200px){
      display: block;
      width: 70%;
    }
  }
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
</style>