<template>
  <div>
    <section class="pt-28 pb-16 hero-gradient px-4">
      <div class="max-w-6xl mx-auto grid lg:grid-cols-2 gap-10 items-start">
        <div>
          <p class="text-[12px] uppercase tracking-[0.2em] text-[#86868b] font-semibold mb-3">Personal Center</p>
          <h1 class="text-4xl md:text-5xl font-bold tracking-tight mb-4">Your profile.</h1>
          <p class="text-lg text-[#86868b] font-medium max-w-xl">
            Keep your account details and security controls in one place.
          </p>
          <div v-if="showIdeas && currentUser" class="mt-8">
            <p class="text-xs uppercase tracking-[0.2em] text-[#86868b] font-semibold mb-3">Idea stats</p>
            <div class="grid gap-4">
              <div class="glass-card rounded-2xl p-5 border border-white/30">
                <p class="text-sm font-semibold mb-1">Total ideas</p>
                <p class="text-2xl font-bold">{{ totalCount }}</p>
              </div>
              <div class="glass-card rounded-2xl p-5 border border-white/30">
                <p class="text-sm font-semibold mb-1">In progress</p>
                <p class="text-2xl font-bold">{{ inProgressCount }}</p>
              </div>
              <div class="glass-card rounded-2xl p-5 border border-white/30">
                <p class="text-sm font-semibold mb-1">Completed</p>
                <p class="text-2xl font-bold">{{ completedCount }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="glass-card rounded-3xl p-8 shadow-2xl">
          <div v-if="currentUser" class="space-y-4">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-xs uppercase tracking-[0.2em] text-[#86868b]">Signed in</p>
                <p class="text-xl font-semibold">{{ currentUser.nickname }}</p>
                <p class="text-sm text-[#86868b]">{{ currentUser.email }}</p>
              </div>
              <div class="w-12 h-12 rounded-full bg-gradient-to-br from-[#0071e3] to-[#00c6ff] text-white flex items-center justify-center text-lg font-bold">
                {{ userInitial }}
              </div>
            </div>
            <div class="text-xs text-[#86868b] space-y-1">
              <p>Member since: {{ createdAtLabel }}</p>
              <p>Last login: {{ lastLoginLabel }}</p>
            </div>
            <div class="flex flex-wrap gap-3">
              <button
                type="button"
                class="px-4 py-2 rounded-full text-xs font-semibold border border-gray-200 hover:bg-white transition"
                @click="toggleIdeas"
              >
                {{ showIdeas ? 'Hide ideas' : 'Manage ideas' }}
              </button>
              <button
                v-if="showIdeas"
                type="button"
                class="px-4 py-2 rounded-full text-xs font-semibold border border-gray-200 hover:bg-white transition"
                @click="refreshTodos"
                :disabled="isLoading"
              >
                Refresh list
              </button>
              <button
                type="button"
                class="px-4 py-2 rounded-full text-xs font-semibold bg-[#1d1d1f] text-white hover:bg-black transition"
                @click="handleLogout"
              >
                Log out
              </button>
            </div>
            <div class="pt-4 border-t border-gray-200 space-y-3">
              <p class="text-xs uppercase tracking-[0.2em] text-[#86868b]">Security</p>
              <div class="flex flex-wrap gap-3">
                <button
                  type="button"
                  class="px-4 py-2 rounded-full text-xs font-semibold bg-[#0071e3] text-white hover:bg-[#0077ed] transition"
                  @click="openPasswordModal"
                >
                  Change password
                </button>
              </div>
              <p class="text-xs text-[#86868b]">Update your password to keep your account secure.</p>
            </div>
          </div>
          <div v-else class="space-y-4">
            <p class="text-xs uppercase tracking-[0.2em] text-[#86868b]">Not signed in</p>
            <p class="text-xl font-semibold">Sign in to manage your ideas.</p>
            <p class="text-sm text-[#86868b]">Your personal center shows only your own items.</p>
            <RouterLink
              to="/auth"
              class="inline-flex items-center justify-center px-5 py-3 rounded-full bg-[#0071e3] text-white text-sm font-semibold hover:bg-[#0077ed] transition"
            >
              Go to Sign In
            </RouterLink>
          </div>
        </div>
      </div>
    </section>

    <section v-if="showIdeas" class="py-12 px-4 max-w-6xl mx-auto">
      <div class="flex flex-col sm:flex-row sm:items-end sm:justify-between mb-6 gap-4">
        <div>
          <p class="text-sm uppercase text-[#86868b] tracking-[0.2em] mb-2">Your submissions</p>
          <h2 class="text-3xl font-bold tracking-tight">Edit or clean up your backlog.</h2>
        </div>
        <div class="text-sm text-[#86868b]">
          <p v-if="currentUser">Total ideas: {{ totalCount }}</p>
          <p v-else>Sign in to load your list.</p>
        </div>
      </div>

      <div v-if="error" class="mb-6 text-sm text-red-500">{{ error }}</div>

      <div v-if="!currentUser" class="glass-card rounded-2xl p-10 text-center text-[#86868b]">
        <p>Sign in to view and manage your ideas.</p>
      </div>

      <div v-else>
        <div v-if="isLoading" class="glass-card rounded-2xl p-10 text-center text-[#86868b]">
          <p>Loading your ideas...</p>
        </div>

        <div v-else-if="todos.length === 0" class="glass-card rounded-2xl p-10 text-center text-[#86868b]">
          <p>No ideas yet. Create one on the board to get started.</p>
        </div>

        <div v-else class="grid gap-6">
          <div
            v-for="todo in todos"
            :key="todo.id"
            class="glass-card rounded-2xl p-6 shadow-sm"
          >
            <div class="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
              <div class="space-y-3">
                <span
                  :class="['text-[10px] uppercase tracking-widest font-bold px-2 py-1 rounded-md', getStatusColor(todo.status)]"
                >
                  {{ todo.status }}
                </span>
                <h3 class="text-xl font-semibold text-[#1d1d1f]">{{ todo.title }}</h3>
                <p class="text-sm text-[#4a4a4f] whitespace-pre-line">{{ todo.content }}</p>
                <div class="text-xs text-[#86868b] flex flex-wrap gap-4">
                  <span>Created {{ formatDate(todo.createdAt) }}</span>
                  <span v-if="todo.updatedAt">Updated {{ formatDate(todo.updatedAt) }}</span>
                </div>
              </div>
              <div class="flex items-center gap-3">
                <button
                  type="button"
                  class="px-4 py-2 rounded-full text-xs font-semibold border border-gray-200 hover:bg-white transition"
                  @click="startEdit(todo)"
                >
                  Edit
                </button>
                <button
                  type="button"
                  class="px-4 py-2 rounded-full text-xs font-semibold bg-red-500 text-white hover:bg-red-600 transition disabled:opacity-60"
                  @click="handleDelete(todo.id)"
                  :disabled="deletingId === todo.id"
                >
                  Delete
                </button>
              </div>
            </div>

            <div v-if="editingId === todo.id" class="mt-6 pt-6 border-t border-gray-200">
              <form class="space-y-4" @submit.prevent="submitEdit">
                <div>
                  <label class="block text-sm font-semibold mb-2 text-[#1d1d1f]">Title</label>
                  <input
                    v-model="editForm.title"
                    type="text"
                    class="w-full bg-white/60 border border-gray-200 rounded-xl px-4 py-3 focus:ring-2 focus:ring-[#0071e3] focus:border-transparent transition-all outline-none"
                    required
                  />
                </div>
                <div>
                  <label class="block text-sm font-semibold mb-2 text-[#1d1d1f]">Content</label>
                  <textarea
                    v-model="editForm.content"
                    class="w-full bg-white/60 border border-gray-200 rounded-xl p-4 focus:ring-2 focus:ring-[#0071e3] focus:border-transparent transition-all outline-none text-sm min-h-[120px]"
                    required
                  />
                </div>
                <div>
                  <label class="block text-sm font-semibold mb-2 text-[#1d1d1f]">Status</label>
                  <select
                    v-model="editForm.status"
                    class="w-full bg-white/60 border border-gray-200 rounded-xl px-4 py-3 focus:ring-2 focus:ring-[#0071e3] focus:border-transparent transition-all outline-none"
                  >
                    <option v-for="status in statusOptions" :key="status" :value="status">
                      {{ status }}
                    </option>
                  </select>
                </div>
                <div class="flex flex-wrap gap-3">
                  <button
                    type="submit"
                    class="px-5 py-2 rounded-full text-xs font-semibold bg-[#1d1d1f] text-white hover:bg-black transition disabled:opacity-60"
                    :disabled="isSaving"
                  >
                    Save changes
                  </button>
                  <button
                    type="button"
                    class="px-5 py-2 rounded-full text-xs font-semibold border border-gray-200 hover:bg-white transition"
                    @click="cancelEdit"
                  >
                    Cancel
                  </button>
                </div>
                <p v-if="actionError" class="text-sm text-red-500">{{ actionError }}</p>
              </form>
            </div>
          </div>
        </div>
      </div>
    </section>

    <div
      v-if="showPasswordModal"
      class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50 px-4"
      @click.self="closePasswordModal"
    >
      <div class="glass-card max-w-lg w-full rounded-3xl p-8 shadow-2xl">
        <div class="flex items-start justify-between mb-6">
          <div>
            <p class="text-xs uppercase tracking-[0.2em] text-[#86868b]">Security</p>
            <h3 class="text-2xl font-bold tracking-tight">Update password</h3>
          </div>
          <button
            type="button"
            class="w-10 h-10 flex items-center justify-center rounded-full bg-white border border-gray-200 hover:bg-gray-50 transition"
            @click="closePasswordModal"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form class="grid gap-4" @submit.prevent="submitPasswordChange">
          <input
            v-model="passwordForm.currentPassword"
            type="password"
            class="w-full bg-white/60 border border-gray-200 rounded-xl px-4 py-3 focus:ring-2 focus:ring-[#0071e3] focus:border-transparent transition-all outline-none text-sm"
            placeholder="Current password"
            autocomplete="current-password"
            required
          />
          <input
            v-model="passwordForm.newPassword"
            type="password"
            class="w-full bg-white/60 border border-gray-200 rounded-xl px-4 py-3 focus:ring-2 focus:ring-[#0071e3] focus:border-transparent transition-all outline-none text-sm"
            placeholder="New password (min 8 chars)"
            autocomplete="new-password"
            required
          />
          <input
            v-model="passwordForm.confirmPassword"
            type="password"
            class="w-full bg-white/60 border border-gray-200 rounded-xl px-4 py-3 focus:ring-2 focus:ring-[#0071e3] focus:border-transparent transition-all outline-none text-sm"
            placeholder="Confirm new password"
            autocomplete="new-password"
            required
          />
          <div class="flex flex-wrap gap-3">
            <button
              type="submit"
              class="px-4 py-2 rounded-full text-xs font-semibold bg-[#0071e3] text-white hover:bg-[#0077ed] transition disabled:opacity-60"
              :disabled="isChangingPassword"
            >
              Update password
            </button>
            <button
              type="button"
              class="px-4 py-2 rounded-full text-xs font-semibold border border-gray-200 hover:bg-white transition"
              @click="closePasswordModal"
            >
              Cancel
            </button>
          </div>
        </form>

        <div class="mt-4 text-xs">
          <p v-if="passwordError" class="text-red-500">{{ passwordError }}</p>
          <p v-else-if="passwordSuccess" class="text-green-600">{{ passwordSuccess }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref, watch } from 'vue';
import { RouterLink } from 'vue-router';
import { useAuth } from '../composables/useAuth';
import { useMyTodos } from '../composables/useMyTodos';
import { Todo, TodoStatus } from '../types';

const { user, logout, changePassword } = useAuth();
const { todos, isLoading, error, fetchMyTodos, updateTodo, deleteTodo } = useMyTodos();

const currentUser = computed(() => user.value);
const userInitial = computed(() => {
  const label = currentUser.value?.nickname || currentUser.value?.email || '';
  return label ? label[0].toUpperCase() : '';
});
const createdAtLabel = computed(() => formatDateString(currentUser.value?.created_at));
const lastLoginLabel = computed(() => formatDateString(currentUser.value?.last_login_at));

const totalCount = computed(() => todos.value.length);
const completedCount = computed(() => todos.value.filter((todo) => todo.status === TodoStatus.COMPLETED).length);
const inProgressCount = computed(() => todos.value.filter((todo) => todo.status === TodoStatus.IN_PROGRESS).length);

const editingId = ref<string | null>(null);
const deletingId = ref<string | null>(null);
const isSaving = ref(false);
const actionError = ref<string | null>(null);
const showIdeas = ref(false);
const showPasswordModal = ref(false);
const isChangingPassword = ref(false);
const passwordError = ref<string | null>(null);
const passwordSuccess = ref<string | null>(null);
const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: '',
});
const editForm = reactive({
  title: '',
  content: '',
  status: TodoStatus.PENDING,
});

const statusOptions = Object.values(TodoStatus);

const formatDate = (timestamp: number) => new Date(timestamp).toLocaleDateString();
const formatDateString = (value?: string | null) => {
  if (!value) return 'N/A';
  const parsed = Date.parse(value);
  return Number.isNaN(parsed) ? 'N/A' : new Date(parsed).toLocaleDateString();
};

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

const refreshTodos = async () => {
  await fetchMyTodos(true);
};

const toggleIdeas = async () => {
  showIdeas.value = !showIdeas.value;
  if (showIdeas.value && currentUser.value) {
    await fetchMyTodos();
  }
};

const openPasswordModal = () => {
  passwordError.value = null;
  passwordSuccess.value = null;
  showPasswordModal.value = true;
};

const closePasswordModal = () => {
  showPasswordModal.value = false;
  isChangingPassword.value = false;
  passwordError.value = null;
  passwordSuccess.value = null;
  passwordForm.currentPassword = '';
  passwordForm.newPassword = '';
  passwordForm.confirmPassword = '';
};

const submitPasswordChange = async () => {
  if (!currentUser.value) return;
  passwordError.value = null;
  passwordSuccess.value = null;
  const currentPassword = passwordForm.currentPassword.trim();
  const newPassword = passwordForm.newPassword.trim();
  const confirmPassword = passwordForm.confirmPassword.trim();
  if (!currentPassword || !newPassword) {
    passwordError.value = 'Please fill in your current and new password.';
    return;
  }
  if (newPassword.length < 8) {
    passwordError.value = 'New password must be at least 8 characters.';
    return;
  }
  if (newPassword !== confirmPassword) {
    passwordError.value = 'New passwords do not match.';
    return;
  }
  isChangingPassword.value = true;
  try {
    await changePassword(currentPassword, newPassword);
    passwordForm.currentPassword = '';
    passwordForm.newPassword = '';
    passwordForm.confirmPassword = '';
    passwordSuccess.value = 'Password updated successfully.';
  } catch (err: any) {
    passwordError.value = err?.message || 'Failed to update password.';
  } finally {
    isChangingPassword.value = false;
  }
};

const startEdit = (todo: Todo) => {
  editingId.value = todo.id;
  editForm.title = todo.title;
  editForm.content = todo.content;
  editForm.status = todo.status;
  actionError.value = null;
};

const cancelEdit = () => {
  editingId.value = null;
  actionError.value = null;
};

const submitEdit = async () => {
  if (!editingId.value) return;
  isSaving.value = true;
  actionError.value = null;
  const trimmedTitle = editForm.title.trim();
  const trimmedContent = editForm.content.trim();
  if (!trimmedTitle || !trimmedContent) {
    actionError.value = 'Title and content are required.';
    isSaving.value = false;
    return;
  }
  try {
    await updateTodo(editingId.value, {
      title: trimmedTitle,
      content: trimmedContent,
      status: editForm.status,
    });
    editingId.value = null;
  } catch (err: any) {
    actionError.value = err?.message || 'Failed to update item';
  } finally {
    isSaving.value = false;
  }
};

const handleDelete = async (id: string) => {
  if (!window.confirm('Delete this idea? This cannot be undone.')) return;
  deletingId.value = id;
  actionError.value = null;
  try {
    await deleteTodo(id);
  } catch (err: any) {
    actionError.value = err?.message || 'Failed to delete item';
  } finally {
    deletingId.value = null;
  }
};

const handleLogout = async () => {
  await logout();
  editingId.value = null;
  todos.value = [];
  showIdeas.value = false;
  closePasswordModal();
};

watch(
  () => currentUser.value?.id,
  (nextId) => {
    if (!nextId) {
      todos.value = [];
      showIdeas.value = false;
      closePasswordModal();
    }
  },
  { immediate: true },
);
</script>
