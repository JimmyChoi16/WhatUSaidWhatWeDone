import { createRouter, createWebHistory } from 'vue-router';
import Home from './views/Home.vue';
import Board from './views/Board.vue';

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
      path: '/:pathMatch(.*)*',
      redirect: '/',
    },
  ],
  scrollBehavior() {
    return { top: 0 };
  },
});

export default router;
