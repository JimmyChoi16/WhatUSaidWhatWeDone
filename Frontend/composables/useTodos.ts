import { reactive, ref, toRef } from 'vue';
import { INITIAL_TODOS } from '../data/todos';
import { NewTodoInput, Todo, TodoStatus } from '../types';
import { useAuth } from './useAuth';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:5050';

const state = reactive<{ todos: Todo[] }>({
  todos: [],
});

const votes = reactive<Record<string, boolean>>({});
const isLoading = ref(false);
const hasLoaded = ref(false);
const error = ref<string | null>(null);
const todosRef = toRef(state, 'todos');

const mapTodo = (data: any): Todo => ({
  id: String(data.id ?? data._id ?? Math.random().toString(36).slice(2)),
  title: data.title ?? '',
  content: data.content ?? '',
  status: (data.status as TodoStatus) || TodoStatus.PENDING,
  author: data.author ?? '',
  heat: Number.isFinite(Number(data.heat)) ? Number(data.heat) : 0,
  createdAt: data.created_at ? new Date(data.created_at).getTime() : Date.now(),
  updatedAt: data.updated_at ? new Date(data.updated_at).getTime() : undefined,
  userId: Number.isFinite(Number(data.user_id)) ? Number(data.user_id) : undefined,
});

const upsertTodo = (todo: Todo) => {
  const idx = state.todos.findIndex((t) => t.id === todo.id);
  if (idx >= 0) {
    state.todos[idx] = todo;
  } else {
    state.todos.unshift(todo);
  }
};

const fetchTodos = async (force = false) => {
  if (isLoading.value) return;
  if (hasLoaded.value && !force) return;
  isLoading.value = true;
  error.value = null;
  try {
    const res = await fetch(`${API_BASE}/api/todos`);
    if (!res.ok) throw new Error(`Failed to fetch todos: ${res.status}`);
    const data = await res.json();
    const mapped = Array.isArray(data) ? data.map(mapTodo) : [];
    state.todos = mapped.length > 0 ? mapped : [...INITIAL_TODOS];
    hasLoaded.value = true;
  } catch (err: any) {
    error.value = err?.message || 'Failed to load todos';
    // fallback to mock if fetch fails
    if (!state.todos.length) {
      state.todos = [...INITIAL_TODOS];
    }
  } finally {
    isLoading.value = false;
  }
};

const parseError = async (res: Response) => {
  try {
    const data = await res.json();
    if (data?.error) return data.error;
  } catch {
    // ignore parse errors
  }
  return `Request failed (${res.status})`;
};

const addTodo = async (input: NewTodoInput) => {
  const { accessToken } = useAuth();
  if (!accessToken.value) {
    throw new Error('Please sign in before posting.');
  }
  try {
    const res = await fetch(`${API_BASE}/api/todos`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${accessToken.value}`,
      },
      body: JSON.stringify({
        title: input.title,
        content: input.content,
        status: TodoStatus.PENDING,
      }),
    });
    if (!res.ok) throw new Error(await parseError(res));
    const data = await res.json();
    upsertTodo(mapTodo(data));
  } catch (err) {
    throw err;
  }
};

const isVoted = (id: string) => !!votes[id];

const toggleVote = async (id: string) => {
  const match = state.todos.find((item) => item.id === id);
  if (!match) return;

  const delta = votes[id] ? -1 : 1;
  try {
    const res = await fetch(`${API_BASE}/api/todos/${id}/vote`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ delta }),
    });
    if (!res.ok) throw new Error('Failed to vote');
    const data = await res.json();
    const mapped = mapTodo(data);
    upsertTodo(mapped);
    if (delta === 1) {
      votes[id] = true;
    } else {
      delete votes[id];
    }
  } catch {
    // on failure, do not change vote state
  }
};

export const useTodos = () => ({
  todos: todosRef,
  isLoading,
  error,
  fetchTodos,
  addTodo,
  toggleVote,
  isVoted,
});
