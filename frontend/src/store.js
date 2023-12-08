import { createStore } from 'vuex';
import axios from 'axios';

export default createStore({
  state: {
    token: localStorage.getItem('token') || '',
    admin: localStorage.getItem('status') || false,
  },


  mutations: {
    SET_TOKEN(state, token) {
      state.token = token;
      localStorage.setItem('token', token);
    },
    CLEAR_TOKEN(state) {
      state.token = '';
      state.admin = false;
      localStorage.removeItem('token');
    },
    SET_ADMIN_STATUS(state, status) {
      localStorage.setItem('status', status);
      state.admin = status;
    },
    CLEAR_ADMIN(state) {
      state.admin = false;
      localStorage.removeItem('status');
    }
  },


  actions: {
    login({ commit, dispatch }, { username, password }) {
      const params = new URLSearchParams();
      params.append('grant_type', '');
      params.append('username', username);
      params.append('password', password);
      params.append('scope', '');
      params.append('client_id', '');
      params.append('client_secret', '');

      return axios.post('/auth/login', params, {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    })
        .then(response => {
          commit('SET_TOKEN', response.data.access_token);
          dispatch('checkIsAdmin');
        });
    },
    logout({ commit }) {
      commit('CLEAR_TOKEN');
      commit('CLEAR_ADMIN');
    },
    checkIsAdmin({ commit, state }) {
      axios.get('/auth/check-admin', {
        headers: { Authorization: `Bearer ${state.token}` }
      })
      .then(response => {
        commit('SET_ADMIN_STATUS', response.data.status);
      })
      .catch(error => {
        commit('SET_ADMIN_STATUS', false);
      });
    }
  },


  getters: {
    isAuthenticated(state) {
      return !!state.token;
    },
    getToken(state){
      return state.token;
    },
    isAdmin(state) {
      return state.admin;
    }
  },
});
