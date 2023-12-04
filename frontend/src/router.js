import { useStore } from 'vuex';
import { computed } from 'vue';
import HomeView from './views/HomeView.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('./views/LoginView.vue')
    },
    {
      path: '/filters',
      name: 'filters',
      component: () => import('./views/FiltersView.vue')
    },
    {
      path: '/users',
      name: 'users',
      component: () => import('./views/UsersView.vue')
    },
    {
      path: '/:catchAll(.*)*',
      component: () => import('./views/ErrorNotFound.vue')
    }
  ]
})


router.beforeEach((to, from, next) => {
  const store = useStore();
  const isAuthenticated = computed(() => store.getters.isAuthenticated).value;
  const isAdmin = computed(() => store.getters.isAdmin).value;


  // Allow not authenticated users to access only this sites
  const notLoggedPages = ['/', '/login']
  const notLoggedRequired = !notLoggedPages.includes(to.path)

  if (notLoggedRequired && !isAuthenticated) {
    return next('/login')
  }


  // Disallow authenticated users to access this sites
  const loggedPages = ['/login', '/register']
  const loggedRequired = loggedPages.includes(to.path)
  if (loggedRequired && isAuthenticated) {
    return next('/')
  }

  // Admin only
  const adminPages = ['/users']
  const adminRequired = adminPages.includes(to.path)
  if (adminRequired && !isAdmin) {
    return next('/')
  }

  next()
})

export default router
