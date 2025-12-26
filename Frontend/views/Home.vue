<template>
  <div>
    <Hero />
    <TodoBoard
      :limit="3"
      title="Top ideas"
      subtitle="Highest heat picks from the community."
      :enable-details="false"
      :show-content="false"
    />
    <GeminiChat />
  </div>
</template>

<script setup lang="ts">
import Hero from '../components/Hero.vue';
import GeminiChat from '../components/GeminiChat.vue';
import TodoBoard from '../components/TodoBoard.vue';
</script>
