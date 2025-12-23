import { createRouter, createWebHistory } from 'vue-router';
import Home from './views/Home.vue';
import Board from './views/Board.vue';
import Auth from './views/Auth.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/board',
      name: 'board',
      component: Board,
    },
    {
      path: '/auth',
      name: 'auth',
      component: Auth,
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/',
    },
  ],
  scrollBehavior() {
    return { top: 0 };
  },
});

export default router;
