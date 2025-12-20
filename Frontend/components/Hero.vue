<template>
  <section class="pt-32 pb-20 hero-gradient px-4">
    <div class="max-w-4xl mx-auto text-center">
      <h1 class="text-5xl md:text-7xl font-bold tracking-tight mb-6">
        The Hub of Great Ideas.
      </h1>
      <p class="text-xl md:text-2xl text-[#86868b] font-medium max-w-2xl mx-auto mb-10">
        A minimalist space to capture, collaborate, and evolve. Built for those who see things differently.
      </p>
      <div class="flex flex-wrap justify-center gap-4">
        <RouterLink
          to="/board"
          class="bg-[#1d1d1f] text-white px-8 py-3 rounded-full font-semibold hover:bg-[#000] transition-all transform hover:scale-105"
        >
          View the Board
        </RouterLink>
        <a href="#" class="text-[#0066cc] px-8 py-3 font-semibold hover:underline flex items-center group">
          Learn how it works
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
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router';
</script>
