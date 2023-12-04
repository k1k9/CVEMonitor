<script setup>
import axios from 'axios';
import { ref, onMounted, computed } from 'vue';
import { useStore } from "vuex";
import Stats from '../components/Stats.vue';
import Filters from '../components/Filters.vue';
import List from '../components/AlertsList.vue';

const store = useStore();
const alertsStats = ref([]);
const isAuthenticated = computed(() => store.getters.isAuthenticated);

onMounted(() => {
  loadAlertsStats();
});

function loadAlertsStats() {
  axios.get('/stats/alerts')
    .then(res => {
      alertsStats.value = Object.entries(res.data).map(([key, value]) => {
        return [key, value];
      });
    })
    .catch(error => {});
}
</script>

<template>
  <section :class="{'content': true, 'center' : !isAuthenticated}">
    <section v-if="isAuthenticated" class="desktop">
      <Stats :stats="alertsStats" />
      <Filters />
    </section>
    <List class="alerts" />
  </section>
</template>


<style scoped lang="scss">

.content{
  width: 100%;
  display: flex;
  justify-content: center;
  margin-top: 3rem;
  gap: 3rem;

  @media (min-width: 1000px){
    justify-content: space-between;

    &.center{
      justify-content: center;
    }
  }

  section.desktop{
    display: none;
    flex-direction: column;
    gap: 3rem;
    
    @media (min-width: 1000px){
      display: flex;
      width: 30%;
    }
  }

  .alerts{
    @media (min-width: 1200px){
      display: block;
      width: 70%;
    }
  }
}
</style>