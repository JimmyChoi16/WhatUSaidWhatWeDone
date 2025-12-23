<template>
  <section id="board" class="py-20 px-4 max-w-6xl mx-auto">
    <div class="flex justify-between items-end mb-12">
      <div>
        <h2 class="text-3xl font-bold tracking-tight mb-2">{{ title }}</h2>
        <p class="text-[#86868b] font-medium">{{ subtitle }}</p>
      </div>
      <button
        v-if="allowAdd && currentUser"
        type="button"
        @click="toggleAdding"
        class="bg-[#0071e3] text-white p-3 rounded-full hover:bg-[#0077ed] transition-all shadow-lg hover:shadow-xl transform active:scale-95"
      >
        <template v-if="isAdding">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </template>
        <template v-else>
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
        </template>
      </button>
    </div>

    <div
      v-if="allowAdd && !currentUser"
      class="mb-12 glass-card rounded-3xl p-8 shadow-2xl flex flex-col sm:flex-row sm:items-center sm:justify-between gap-6"
    >
      <div>
        <p class="text-xs uppercase tracking-[0.2em] text-[#86868b] mb-2">Members only</p>
        <h3 class="text-2xl font-bold mb-2">Sign in to post your idea.</h3>
        <p class="text-sm text-[#86868b]">Your submissions are tied to your account and editable in your profile.</p>
      </div>
      <RouterLink
        to="/auth"
        class="inline-flex items-center justify-center px-5 py-3 rounded-full bg-[#1d1d1f] text-white text-sm font-semibold hover:bg-black transition"
      >
        Go to Sign In
      </RouterLink>
    </div>

    <div
      v-if="allowAdd && currentUser && isAdding"
      class="mb-12 glass-card rounded-3xl p-8 shadow-2xl animate-in fade-in slide-in-from-top-4 duration-500"
    >
      <form @submit.prevent="handleAddTodo" class="space-y-6">
        <div class="flex items-center justify-between text-xs text-[#86868b]">
          <span class="uppercase tracking-[0.2em]">Posting as</span>
          <span class="font-semibold text-[#1d1d1f]">{{ authorName }}</span>
        </div>
        <div>
          <label class="block text-sm font-semibold mb-2 text-[#1d1d1f]">Idea title</label>
          <input
            type="text"
            v-model="newTodo.title"
            class="w-full bg-white/50 border border-gray-200 rounded-xl px-4 py-3 focus:ring-2 focus:ring-[#0071e3] focus:border-transparent transition-all outline-none"
            placeholder="A short, clear title"
            required
          />
        </div>
        <div>
          <label class="block text-sm font-semibold mb-2 text-[#1d1d1f]">What's your idea?</label>
          <textarea
            v-model="newTodo.content"
            class="w-full bg-white/50 border border-gray-200 rounded-xl p-4 focus:ring-2 focus:ring-[#0071e3] focus:border-transparent transition-all outline-none text-lg min-h-[120px]"
            placeholder="Describe your vision..."
            required
          />
        </div>
        <button
          type="submit"
          class="w-full bg-[#1d1d1f] text-white py-4 rounded-xl font-bold hover:bg-black transition-all disabled:opacity-60"
          :disabled="isSubmitting"
        >
          Post to Stream
        </button>
        <p v-if="addError" class="text-sm text-red-500">{{ addError }}</p>
      </form>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="todo in displayTodos"
        :key="todo.id"
        class="glass-card rounded-2xl p-6 shadow-sm hover:shadow-md transition-all group flex flex-col justify-between cursor-pointer"
        @click="openDetail(todo)"
      >
        <div>
          <div class="flex justify-between items-start mb-4">
            <span
              :class="['text-[10px] uppercase tracking-widest font-bold px-2 py-1 rounded-md', getStatusColor(todo.status)]"
            >
              {{ todo.status }}
            </span>
            <div class="flex items-center space-x-3">
              <button
                type="button"
                class="text-[11px] flex items-center space-x-1 px-3 py-1 rounded-full border bg-white/60 hover:bg-white transition-all shadow-sm"
                :class="isVoted(todo.id) ? 'border-[#c7ddff] bg-[#e9f2ff] text-[#0b5394]' : 'border-gray-200 text-[#1d1d1f]'"
                @click.stop="handleVote(todo.id)"
              >
                <span>🔥</span>
                <span class="font-semibold">{{ todo.heat }}</span>
              </button>
              <span class="text-[10px] text-[#86868b]">{{ formatDate(todo.createdAt) }}</span>
            </div>
          </div>
          <h3 class="text-[#1d1d1f] text-xl font-semibold leading-relaxed mb-2">
            {{ todo.title }}
          </h3>
          <p v-if="props.showContent" class="text-[#4a4a4f] text-sm leading-relaxed line-clamp-3">
            {{ todo.content }}
          </p>
        </div>
        <div class="flex items-center space-x-3 pt-4 border-t border-gray-100">
          <div class="w-8 h-8 rounded-full bg-gradient-to-br from-[#0071e3] to-[#00c6ff] flex items-center justify-center text-white text-xs font-bold">
            {{ getInitial(todo.author) }}
          </div>
          <div>
            <p class="text-sm font-semibold text-[#1d1d1f]">{{ todo.author }}</p>
            <p class="text-[10px] text-[#86868b]">Contributor</p>
          </div>
        </div>
      </div>
    </div>

    <div v-if="todos.length === 0" class="text-center py-20 opacity-40">
      <p class="text-xl italic">No ideas yet. Be the first to start the stream.</p>
    </div>

    <div
      v-if="selected"
      class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50 px-4"
      @click.self="closeDetail"
    >
      <div class="glass-card max-w-2xl w-full rounded-3xl p-8 shadow-2xl relative">
        <div class="flex items-start justify-between mb-4">
          <div class="space-y-2">
            <span
              :class="['text-[10px] uppercase tracking-widest font-bold px-2 py-1 rounded-md inline-block', getStatusColor(selected.status)]"
            >
              {{ selected.status }}
            </span>
            <p class="text-sm text-[#86868b]">Created {{ formatDate(selected.createdAt) }}</p>
          </div>
          <div class="flex items-center space-x-3">
            <button
              type="button"
              class="text-[12px] flex items-center space-x-1 px-3 py-1 rounded-full border bg-white/70 hover:bg-white transition-all shadow-sm"
              :class="isVoted(selected.id) ? 'border-[#c7ddff] bg-[#e9f2ff] text-[#0b5394]' : 'border-gray-200 text-[#1d1d1f]'"
              @click.stop="handleVote(selected.id)"
            >
              <span>🔥</span>
              <span class="font-semibold">{{ selected.heat }}</span>
            </button>
            <button
              type="button"
              class="w-10 h-10 flex items-center justify-center rounded-full bg-white border border-gray-200 hover:bg-gray-50 transition"
              @click="closeDetail"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
        <h3 class="text-2xl font-bold text-[#1d1d1f] mb-3">{{ selected.title }}</h3>
        <p class="text-[#4a4a4f] leading-relaxed mb-6 whitespace-pre-line">{{ selected.content }}</p>
        <div class="flex items-center space-x-3 pt-4 border-t border-gray-100">
          <div class="w-10 h-10 rounded-full bg-gradient-to-br from-[#0071e3] to-[#00c6ff] flex items-center justify-center text-white text-sm font-bold">
            {{ getInitial(selected.author) }}
          </div>
          <div>
            <p class="text-sm font-semibold text-[#1d1d1f]">{{ selected.author }}</p>
            <p class="text-[11px] text-[#86868b]">Contributor</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue';
import { RouterLink } from 'vue-router';
import { NewTodoInput, TodoStatus, Todo } from '../types';
import { useTodos } from '../composables/useTodos';
import { useAuth } from '../composables/useAuth';

const props = withDefaults(
  defineProps<{
    allowAdd?: boolean;
    limit?: number;
    title?: string;
    subtitle?: string;
    enableDetails?: boolean;
    showContent?: boolean;
  }>(),
  {
    allowAdd: false,
    title: 'Community Board',
    subtitle: 'Capture thoughts, prioritize growth.',
    enableDetails: false,
    showContent: true,
  },
);

const isAdding = ref(false);
const newTodo = ref<NewTodoInput>({ title: '', content: '' });
const selected = ref<Todo | null>(null);
const addError = ref<string | null>(null);
const isSubmitting = ref(false);

const { todos, addTodo, toggleVote, isVoted, fetchTodos } = useTodos();
const { user } = useAuth();
const currentUser = computed(() => user.value);
const authorName = computed(() => currentUser.value?.nickname || currentUser.value?.email || '');

const displayTodos = computed(() => {
  const list = Array.isArray(todos.value) ? todos.value : [];
  const sorted = [...list].sort((a, b) => {
    if (b.heat !== a.heat) return b.heat - a.heat;
    return b.createdAt - a.createdAt;
  });
  if (typeof props.limit === 'number') {
    return sorted.slice(0, props.limit);
  }
  return sorted;
});

const getStatusColor = (status: TodoStatus) => {
  switch (status) {
    case TodoStatus.COMPLETED:
      return 'bg-green-100 text-green-700';
    case TodoStatus.IN_PROGRESS:
      return 'bg-blue-100 text-blue-700';
    case TodoStatus.PENDING:
    default:
      return 'bg-gray-100 text-gray-700';
  }
};

const formatDate = (timestamp: number) => new Date(timestamp).toLocaleDateString();

const getInitial = (author: string) => (author ? author[0].toUpperCase() : '');

const handleAddTodo = async () => {
  addError.value = null;
  if (!newTodo.value.title.trim() || !newTodo.value.content.trim()) return;
  isSubmitting.value = true;
  try {
    await addTodo(newTodo.value);
    newTodo.value = { title: '', content: '' };
    isAdding.value = false;
  } catch (err: any) {
    addError.value = err?.message || 'Failed to create idea';
  } finally {
    isSubmitting.value = false;
  }
};

const handleVote = (id: string) => {
  toggleVote(id);
};

const toggleAdding = () => {
  isAdding.value = !isAdding.value;
};

const openDetail = (todo: Todo) => {
  if (!props.enableDetails) return;
  selected.value = todo;
};

const closeDetail = () => {
  selected.value = null;
};

const { title, subtitle, allowAdd } = props;

onMounted(() => {
  // fetchTodos(true);
  fetchTodos(false);
});
</script>
