<template>
  <div class="min-h-screen">
    <Header />
    <main>
      <RouterView />
    </main>
    <footer class="py-20 border-t border-gray-200 bg-[#f5f5f7]">
      <div class="max-w-7xl mx-auto px-4 text-xs text-[#86868b]">
        <div class="pb-8 border-b border-gray-300 mb-8">
          <p class="mb-4">
            1. The IdeaStream community is open to all. Ideas shared here are public domain within the application context.
          </p>
          <p>
            2. Apple UI/UX reference design for educational purposes.
          </p>
        </div>
        <div class="flex flex-col md:flex-row justify-between items-center gap-4">
          <div class="flex space-x-6">
            <p>Copyright © 2025 KJ Inc. All rights reserved.</p>
          </div>
          <div class="flex space-x-6">
            <a href="#" class="hover:underline">Privacy Policy</a>
            <span class="text-gray-400">|</span>
            <a href="#" class="hover:underline">Terms of Use</a>
            <span class="text-gray-400">|</span>
            <a href="#" class="hover:underline">Sales and Refunds</a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router';
import Header from './components/Header.vue';
</script>
