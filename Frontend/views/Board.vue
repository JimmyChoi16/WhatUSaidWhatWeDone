<template>
  <div>
    <section class="pt-28 pb-16 hero-gradient px-4">
      <div class="max-w-5xl mx-auto text-center">
        <p class="text-[12px] uppercase tracking-[0.2em] text-[#86868b] font-semibold mb-3">View the Board</p>
        <h1 class="text-4xl md:text-6xl font-bold tracking-tight mb-4">All ideas in one place.</h1>
        <p class="text-lg md:text-xl text-[#86868b] font-medium max-w-3xl mx-auto mb-8">
          Dive into every idea shared by the community. Status, owners, and timelines stay clear in this focused view.
        </p>
        <div class="flex justify-center flex-wrap gap-4">
          <RouterLink
            to="/"
            class="bg-[#1d1d1f] text-white px-6 py-3 rounded-full font-semibold hover:bg-black transition-all"
          >
            Back to Home
          </RouterLink>
          <a
            href="#board-cards"
            class="text-[#0066cc] px-6 py-3 font-semibold hover:underline flex items-center group"
          >
            Jump to cards
            <svg
              class="w-4 h-4 ml-1 transform group-hover:translate-x-1 transition-transform"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </a>
        </div>
      </div>
    </section>

    <section id="board-cards" class="py-10 px-4 max-w-6xl mx-auto">
      <div class="flex flex-col sm:flex-row sm:items-end sm:justify-between mb-6 gap-4">
        <div>
          <p class="text-sm uppercase text-[#86868b] tracking-[0.2em] mb-2">Board Overview</p>
          <h2 class="text-3xl font-bold tracking-tight">Every idea, every status.</h2>
        </div>
        <div class="text-sm text-[#86868b]">
          <p>Total ideas: {{ todos.length }}</p>
          <p>Last update: {{ lastUpdated }}</p>
        </div>
      </div>
    </section>

    <TodoBoard allowAdd enable-details />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { RouterLink } from 'vue-router';
import TodoBoard from '../components/TodoBoard.vue';
import { useTodos } from '../composables/useTodos';
import type { Todo } from '../types';

const { todos } = useTodos();
const formatDate = (timestamp: number) => new Date(timestamp).toLocaleDateString();

const lastUpdated = computed(() => {
  const list = Array.isArray(todos.value) ? todos.value : [];
  if (!list.length) return 'N/A';
  const latest = Math.max(...list.map((todo: Todo) => todo.createdAt));
  return formatDate(latest);
});
</script>
