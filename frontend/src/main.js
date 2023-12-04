import axios from 'axios'
import { createApp } from 'vue'
import infiniteScroll from 'vue-infinite-scroll';

import App from './App.vue'
import store from './store'
import router from './router'
import './assets/scss/main.scss'

const app = createApp(App)

axios.defaults.baseURL = import.meta.env.VITE_BACKEND_URL;

axios.interceptors.request.use(
    (config) => {
      if (store.state.token) {
        config.headers.Authorization = `Bearer ${store.state.token}`;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

app.use(store)
app.use(infiniteScroll)
app.use(router)

app.mount('#app')
