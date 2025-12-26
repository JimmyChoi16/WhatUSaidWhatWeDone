<template>
  <section v-if="!props.compact" id="chat" class="py-20 px-4">
    <div class="max-w-5xl mx-auto">
      <div class="flex flex-col md:flex-row md:items-end md:justify-between gap-6 mb-8">
        <div>
          <p class="text-[12px] uppercase tracking-[0.2em] text-[#86868b] font-semibold mb-3">Gemini Live</p>
          <h2 class="text-3xl md:text-4xl font-bold tracking-tight mb-2">Chat with your idea.</h2>
          <p class="text-[#86868b] font-medium max-w-3xl">
            Ask for refinements, summaries, or next steps in the same visual language as your board.
          </p>
        </div>
        <div class="text-xs text-[#86868b] font-semibold uppercase tracking-[0.3em]">
          Powered by Gemini
        </div>
      </div>

      <div class="glass-card rounded-3xl p-6 md:p-8 shadow-2xl">
        <div ref="scrollRef" class="flex flex-col space-y-4 max-h-[420px] overflow-y-auto pr-2">
          <div
            v-if="!messages.length && !isLoading"
            class="text-center text-[#86868b] text-sm py-10 border border-dashed border-gray-200 rounded-2xl bg-white/40"
          >
            Start by sharing your idea or ask for feedback on the roadmap.
          </div>

          <div
            v-for="message in messages"
            :key="message.id"
            class="flex"
            :class="message.role === 'user' ? 'justify-end' : 'justify-start'"
          >
            <div
              class="max-w-[80%] rounded-2xl px-4 py-3 shadow-sm chat-bubble"
              :class="message.role === 'user'
                ? 'bg-[#1d1d1f] text-white chat-bubble--user'
                : 'bg-white text-[#1d1d1f] border border-gray-200 chat-bubble--assistant'"
            >
              <p
                class="text-[10px] uppercase tracking-[0.2em] mb-2"
                :class="message.role === 'user' ? 'text-white/60' : 'text-[#86868b]'"
              >
                {{ message.role === 'user' ? 'You' : 'Gemini' }}
              </p>
              <div class="chat-markdown text-sm leading-relaxed" v-html="renderMarkdown(message.text)"></div>
            </div>
          </div>

          <div v-if="isLoading" class="flex justify-start">
            <div class="max-w-[80%] rounded-2xl px-4 py-3 bg-white/80 border border-gray-200 shadow-sm">
              <div class="flex items-center space-x-2 text-xs text-[#86868b]">
                <span class="w-2 h-2 rounded-full bg-[#0071e3] animate-pulse"></span>
                <span>Gemini is thinking...</span>
              </div>
            </div>
          </div>
        </div>

        <form class="mt-6" @submit.prevent="handleSubmit">
          <div class="flex items-end gap-3">
            <div class="flex-1">
              <textarea
                v-model="input"
                rows="2"
                class="w-full bg-white/60 border border-gray-200 rounded-2xl px-4 py-3 text-sm focus:ring-2 focus:ring-[#0071e3] focus:border-transparent transition-all outline-none resize-none"
                placeholder="Ask Gemini about your idea..."
                @keydown.enter.exact.prevent="handleSubmit"
              />
            </div>
            <button
              type="submit"
              class="bg-[#0071e3] text-white px-5 py-3 rounded-full text-sm font-semibold hover:bg-[#0077ed] transition-all shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed"
              :disabled="isLoading || !input.trim()"
            >
              Send
            </button>
          </div>
          <div class="mt-3 flex flex-wrap items-center justify-end gap-3">
            <label class="text-[11px] uppercase tracking-[0.2em] text-[#86868b] font-semibold">Model</label>
            <div class="relative">
              <select
                v-model="selectedModel"
                class="appearance-none bg-white/60 border border-gray-200 rounded-full px-4 py-2 pr-9 text-xs font-semibold text-[#1d1d1f] focus:ring-2 focus:ring-[#0071e3] focus:border-transparent transition-all outline-none"
              >
                <option value="gemini-3-pro-preview">gemini-3-pro-preview</option>
                <option value="gemini-2.5-flash">gemini-2.5-flash</option>
                <option value="gemini-2.0-flash">gemini-2.0-flash (default)</option>
              </select>
              <svg
                class="w-3 h-3 text-[#86868b] absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path d="M5.5 7.5l4.5 4.5 4.5-4.5" />
              </svg>
            </div>
          </div>
          <div class="flex items-center justify-between text-[11px] text-[#86868b] mt-2">
            <span v-if="error" class="text-red-500">{{ error }}</span>
            <span v-else>Press Enter to send, Shift+Enter for a new line.</span>
            <span class="uppercase tracking-[0.2em]">/api/chat</span>
          </div>
        </form>
      </div>
    </div>
  </section>

  <div v-else class="glass-card rounded-3xl p-6 md:p-8 shadow-2xl flex flex-col h-full overflow-hidden">
    <div ref="scrollRef" class="flex flex-col space-y-4 flex-1 min-h-0 overflow-y-auto pr-2">
      <div
        v-if="!messages.length && !isLoading"
        class="text-center text-[#86868b] text-sm py-10 border border-dashed border-gray-200 rounded-2xl bg-white/40"
      >
        Start by sharing your idea or ask for feedback on the roadmap.
      </div>

      <div
        v-for="message in messages"
        :key="message.id"
        class="flex"
        :class="message.role === 'user' ? 'justify-end' : 'justify-start'"
      >
        <div
          class="max-w-[80%] rounded-2xl px-4 py-3 shadow-sm chat-bubble"
          :class="message.role === 'user'
            ? 'bg-[#1d1d1f] text-white chat-bubble--user'
            : 'bg-white text-[#1d1d1f] border border-gray-200 chat-bubble--assistant'"
        >
          <p
            class="text-[10px] uppercase tracking-[0.2em] mb-2"
            :class="message.role === 'user' ? 'text-white/60' : 'text-[#86868b]'"
          >
            {{ message.role === 'user' ? 'You' : 'Gemini' }}
          </p>
          <div class="chat-markdown text-sm leading-relaxed" v-html="renderMarkdown(message.text)"></div>
        </div>
      </div>

      <div v-if="isLoading" class="flex justify-start">
        <div class="max-w-[80%] rounded-2xl px-4 py-3 bg-white/80 border border-gray-200 shadow-sm">
          <div class="flex items-center space-x-2 text-xs text-[#86868b]">
            <span class="w-2 h-2 rounded-full bg-[#0071e3] animate-pulse"></span>
            <span>Gemini is thinking...</span>
          </div>
        </div>
      </div>
    </div>

    <form class="mt-6" @submit.prevent="handleSubmit">
      <div class="flex items-end gap-3">
        <div class="flex-1">
          <textarea
            v-model="input"
            rows="2"
            class="w-full bg-white/60 border border-gray-200 rounded-2xl px-4 py-3 text-sm focus:ring-2 focus:ring-[#0071e3] focus:border-transparent transition-all outline-none resize-none"
            placeholder="Ask Gemini about your idea..."
            @keydown.enter.exact.prevent="handleSubmit"
          />
        </div>
        <button
          type="submit"
          class="bg-[#0071e3] text-white px-5 py-3 rounded-full text-sm font-semibold hover:bg-[#0077ed] transition-all shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="isLoading || !input.trim()"
        >
          Send
        </button>
      </div>
      <div class="mt-3 flex flex-wrap items-center justify-end gap-3">
        <label class="text-[11px] uppercase tracking-[0.2em] text-[#86868b] font-semibold">Model</label>
        <div class="relative">
          <select
            v-model="selectedModel"
            class="appearance-none bg-white/60 border border-gray-200 rounded-full px-4 py-2 pr-9 text-xs font-semibold text-[#1d1d1f] focus:ring-2 focus:ring-[#0071e3] focus:border-transparent transition-all outline-none"
          >
            <option value="gemini-3-pro-preview">gemini-3-pro-preview</option>
            <option value="gemini-2.5-flash">gemini-2.5-flash</option>
            <option value="gemini-2.0-flash">gemini-2.0-flash (default)</option>
          </select>
          <svg
            class="w-3 h-3 text-[#86868b] absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path d="M5.5 7.5l4.5 4.5 4.5-4.5" />
          </svg>
        </div>
      </div>
      <div class="flex items-center justify-between text-[11px] text-[#86868b] mt-2">
        <span v-if="error" class="text-red-500">{{ error }}</span>
        <span v-else>Press Enter to send, Shift+Enter for a new line.</span>
        <span class="uppercase tracking-[0.2em]">/api/chat</span>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import DOMPurify from 'dompurify';
import { marked } from 'marked';
import { nextTick, ref, watch } from 'vue';

const props = withDefaults(
  defineProps<{
    compact?: boolean;
  }>(),
  {
    compact: false,
  },
);

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  text: string;
}

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:5050';

marked.setOptions({ breaks: true });

const input = ref('');
const messages = ref<ChatMessage[]>([]);
const isLoading = ref(false);
const error = ref<string | null>(null);
const scrollRef = ref<HTMLDivElement | null>(null);
const selectedModel = ref('gemini-2.0-flash');

const renderMarkdown = (text: string) => {
  const html = marked.parse(text) as string;
  // Sanitize Markdown before using v-html.
  return DOMPurify.sanitize(html);
};

const scrollToBottom = async () => {
  await nextTick();
  if (!scrollRef.value) return;
  scrollRef.value.scrollTop = scrollRef.value.scrollHeight;
};

const handleSubmit = async () => {
  if (isLoading.value) return;
  const prompt = input.value.trim();
  if (!prompt) return;

  messages.value.push({
    id: `${Date.now()}-user`,
    role: 'user',
    text: prompt,
  });
  input.value = '';
  error.value = null;
  isLoading.value = true;

  try {
    const res = await fetch(`${API_BASE}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt, model: selectedModel.value }),
    });
    if (!res.ok) {
      let message = `Request failed (${res.status})`;
      try {
        const data = await res.json();
        if (data?.error) {
          message = data.error;
        }
      } catch {
        // ignore json parse errors
      }
      throw new Error(message);
    }
    const data = await res.json();
    const text = String(data?.text || '').trim();
    if (!text) {
      throw new Error('Empty response from Gemini');
    }
    messages.value.push({
      id: `${Date.now()}-assistant`,
      role: 'assistant',
      text,
    });
  } catch (err: any) {
    error.value = err?.message || 'Failed to fetch Gemini response';
  } finally {
    isLoading.value = false;
  }
};

watch(
  () => [messages.value.length, isLoading.value],
  () => {
    scrollToBottom();
  },
);
</script>

<style scoped>
.chat-markdown :deep(p) {
  margin: 0;
}

.chat-markdown :deep(p + p) {
  margin-top: 0.75rem;
}

.chat-markdown :deep(ul),
.chat-markdown :deep(ol) {
  margin: 0.5rem 0 0.5rem 1.25rem;
}

.chat-markdown :deep(li) {
  margin: 0.25rem 0;
}

.chat-markdown :deep(strong) {
  font-weight: 600;
}

.chat-markdown :deep(em) {
  font-style: italic;
}

.chat-markdown :deep(a) {
  color: #0066cc;
  text-decoration: underline;
}

.chat-markdown :deep(code) {
  background: rgba(0, 0, 0, 0.06);
  padding: 0.15rem 0.35rem;
  border-radius: 0.375rem;
  font-size: 0.85em;
}

.chat-markdown :deep(pre) {
  background: rgba(0, 0, 0, 0.06);
  padding: 0.75rem;
  border-radius: 0.75rem;
  overflow-x: auto;
}

.chat-markdown :deep(blockquote) {
  border-left: 3px solid rgba(0, 0, 0, 0.12);
  margin: 0.75rem 0;
  padding-left: 0.75rem;
  color: #5b5b5f;
}

.chat-bubble--user .chat-markdown :deep(a) {
  color: #c7ddff;
}

.chat-bubble--user .chat-markdown :deep(code),
.chat-bubble--user .chat-markdown :deep(pre) {
  background: rgba(255, 255, 255, 0.15);
}

.chat-bubble--user .chat-markdown :deep(blockquote) {
  border-left-color: rgba(255, 255, 255, 0.4);
  color: rgba(255, 255, 255, 0.8);
}
</style>
