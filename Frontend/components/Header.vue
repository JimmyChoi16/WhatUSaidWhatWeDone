<template>
  <header class="fixed top-0 left-0 right-0 z-50 apple-blur border-b border-gray-200 h-12 flex items-center px-4 md:px-8">
    <nav class="max-w-7xl mx-auto w-full flex justify-between items-center text-xs font-normal tracking-tight">
      <div class="flex items-center space-x-8">
        <a href="#" class="opacity-80 hover:opacity-100 transition-opacity">
          <svg class="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
          </svg>
        </a>
        <div class="hidden md:flex space-x-8">
          <a href="#" class="opacity-60 hover:opacity-100 transition-opacity">Explore</a>
          <a href="#" class="opacity-60 hover:opacity-100 transition-opacity">Ideas</a>
          <a href="#" class="opacity-60 hover:opacity-100 transition-opacity">Roadmap</a>
          <a href="#" class="opacity-60 hover:opacity-100 transition-opacity">Community</a>
        </div>
      </div>
      <div class="flex items-center space-x-6">
        <button class="bg-[#0071e3] text-white px-3 py-1 rounded-full text-[10px] font-semibold hover:bg-[#0077ed] transition-colors">
          Share Idea
        </button>
      </div>
    </nav>
  </header>
</template>

<script setup lang="ts">
</script>
