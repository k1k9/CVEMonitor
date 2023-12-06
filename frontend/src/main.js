import axios from 'axios'
import { createApp } from 'vue'
import infiniteScroll from 'vue-infinite-scroll';

import App from './App.vue'
import store from './store'
import router from './router'
import './assets/scss/main.scss'

import Toast from "vue-toastification";
import './assets/scss/toast.scss';

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

app.use(router)
app.use(store)
app.use(infiniteScroll)


app.use(Toast, {
  transition: "Vue-Toastification__bounce",
  maxToasts: 5,
  newestOnTop: true,
  filterToasts: toasts => {
    // Keep track of existing types
    const types = {};
    return toasts.reduce((aggToasts, toast) => {
      // Check if type was not seen before
      if (!types[toast.type]) {
        aggToasts.push(toast);
        types[toast.type] = true;
      }
      return aggToasts;
    }, []);
  }
});

app.mount('#app')
