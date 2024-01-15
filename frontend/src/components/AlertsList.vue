<script setup>
import { computed, defineProps } from "vue";
import { useStore } from "vuex";
import { defineEmits } from "vue";

const props = defineProps({
  alerts: {
    type: Array,
    default: () => [],
  },
})

const store = useStore();
const isAuthenticated = computed(() => store.getters.isAuthenticated);
const emit = defineEmits(['refresh', 'loadMore', 'ack']);

function emitRefreshEvent() {
  emit('refresh');
}

function emitLoadMoreEvent() {
  emit('loadMore');
}

function emitAckEvent(alertId) {
  emit('ack', alertId);
}
</script>

<template>
  <section>
    <header>
      <h2>Alerts</h2>
      <button v-if="isAuthenticated" class="refresh" @click="emitRefreshEvent">Refresh</button>
    </header>
    <ul
      class="alerts"
      v-infinite-scroll="loadMore"
      infinite-scroll-distance="200"
    >
      <li v-for="alert in alerts" :key="alert.id" 
          :class="{'alert': true, 'acked': isAuthenticated && alert.is_acked}">

        <header>
          <span :class="'level ' + alert.scoreText.toLowerCase()">
            {{ alert.scoreText.toLowerCase() }}
          </span>
          <div class="info">
            <p class="title">{{ alert.id }}</p>
            <p class="time">{{ alert.created_at }}</p>
          </div>

          <button v-if="isAuthenticated" @click="() => emitAckEvent(alert.id)">
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
    <button v-if="isAuthenticated" class="loadMore" @click="emitLoadMoreEvent">Load more</button>
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
