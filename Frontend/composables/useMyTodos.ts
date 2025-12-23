import { reactive, ref, toRef } from 'vue';
import { Todo, TodoStatus, TodoUpdateInput } from '../types';
import { useAuth } from './useAuth';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:5000';

const state = reactive<{ todos: Todo[] }>({
  todos: [],
});

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

const parseError = async (res: Response) => {
  try {
    const data = await res.json();
    if (data?.error) return data.error;
  } catch {
    // ignore parse errors
  }
  return `Request failed (${res.status})`;
};

const fetchMyTodos = async (force = false) => {
  if (isLoading.value) return;
  if (hasLoaded.value && !force) return;
  const { accessToken } = useAuth();
  if (!accessToken.value) {
    error.value = 'Please sign in to view your ideas.';
    return;
  }

  isLoading.value = true;
  error.value = null;
  try {
    const res = await fetch(`${API_BASE}/api/todos/mine`, {
      headers: { Authorization: `Bearer ${accessToken.value}` },
    });
    if (!res.ok) throw new Error(await parseError(res));
    const data = await res.json();
    state.todos = Array.isArray(data) ? data.map(mapTodo) : [];
    hasLoaded.value = true;
  } catch (err: any) {
    error.value = err?.message || 'Failed to load your ideas';
  } finally {
    isLoading.value = false;
  }
};

const updateTodo = async (id: string, payload: TodoUpdateInput) => {
  const { accessToken } = useAuth();
  if (!accessToken.value) {
    throw new Error('Please sign in before updating.');
  }
  const res = await fetch(`${API_BASE}/api/todos/${id}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${accessToken.value}`,
    },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(await parseError(res));
  const data = await res.json();
  const updated = mapTodo(data);
  const idx = state.todos.findIndex((todo) => todo.id === updated.id);
  if (idx >= 0) {
    state.todos[idx] = updated;
  } else {
    state.todos.unshift(updated);
  }
  return updated;
};

const deleteTodo = async (id: string) => {
  const { accessToken } = useAuth();
  if (!accessToken.value) {
    throw new Error('Please sign in before deleting.');
  }
  const res = await fetch(`${API_BASE}/api/todos/${id}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${accessToken.value}` },
  });
  if (!res.ok) throw new Error(await parseError(res));
  state.todos = state.todos.filter((todo) => todo.id !== id);
};

export const useMyTodos = () => ({
  todos: todosRef,
  isLoading,
  error,
  fetchMyTodos,
  updateTodo,
  deleteTodo,
});
