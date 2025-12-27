import { createRouter, createWebHistory } from 'vue-router';
import Auth from './views/Auth.vue';
import Board from './views/Board.vue';
import Graph from './views/Graph.vue';
import GraphCreate from './views/GraphCreate.vue';
import Home from './views/Home.vue';
import Profile from './views/Profile.vue';

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
      path: '/profile',
      name: 'profile',
      component: Profile,
    },
    {
      path: '/graph',
      name: 'graph',
      component: Graph,
    },
    {
      path: '/graph/create',
      name: 'graph-create',
      component: GraphCreate,
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
