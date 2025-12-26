<template>
  <div>
    <section class="pt-28 pb-24 hero-gradient px-4">
      <div class="max-w-6xl mx-auto grid lg:grid-cols-2 gap-12 items-start">
        <div>
          <p class="text-[12px] uppercase tracking-[0.2em] text-[#86868b] font-semibold mb-3">Account</p>
          <h1 class="text-4xl md:text-5xl font-bold tracking-tight mb-4">Secure access to your ideas.</h1>
          <p class="text-lg text-[#86868b] font-medium max-w-xl">
            Sign in to sync your roadmap and keep your submissions under one profile. Built with modern
            JWT sessions and refresh tokens.
          </p>
          <div class="grid gap-4 mt-8">
            <div class="glass-card rounded-2xl p-5 border border-white/30">
              <p class="text-sm font-semibold mb-1">Password protection</p>
              <p class="text-xs text-[#86868b]">Hashed credentials and lockout on repeated failures.</p>
            </div>
            <div class="glass-card rounded-2xl p-5 border border-white/30">
              <p class="text-sm font-semibold mb-1">Token-based sessions</p>
              <p class="text-xs text-[#86868b]">Short-lived access tokens with refresh rotation.</p>
            </div>
            <div class="glass-card rounded-2xl p-5 border border-white/30">
              <p class="text-sm font-semibold mb-1">Ready for social login</p>
              <p class="text-xs text-[#86868b]">Framework prepared for WeChat scan-in when deployed.</p>
            </div>
          </div>
        </div>

        <div class="glass-card rounded-3xl p-8 shadow-2xl">
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
            <div>
              <h2 class="text-2xl font-bold tracking-tight">{{ modeTitle }}</h2>
              <p class="text-sm text-[#86868b]">
                {{ mode === 'login' ? 'Welcome back.' : 'Create a profile in under a minute.' }}
              </p>
            </div>
            <div class="flex items-center bg-white/70 border border-gray-200 rounded-full p-1 text-xs font-semibold">
              <button
                type="button"
                class="px-4 py-2 rounded-full transition-all"
                :class="mode === 'login' ? 'bg-[#1d1d1f] text-white shadow' : 'text-[#1d1d1f]'"
                @click="setMode('login')"
              >
                Sign in
              </button>
              <button
                type="button"
                class="px-4 py-2 rounded-full transition-all"
                :class="mode === 'register' ? 'bg-[#1d1d1f] text-white shadow' : 'text-[#1d1d1f]'"
                @click="setMode('register')"
              >
                Register
              </button>
            </div>
          </div>

          <div
            v-if="currentUser"
            class="mb-6 rounded-2xl border border-gray-200 bg-white/70 px-5 py-4 flex flex-col gap-2"
          >
            <p class="text-xs uppercase tracking-[0.2em] text-[#86868b]">Signed in</p>
            <p class="text-sm font-semibold">{{ currentUser.nickname }}</p>
            <p class="text-xs text-[#86868b]">{{ currentUser.email }}</p>
            <div class="flex flex-wrap gap-3 mt-2">
              <button
                type="button"
                class="px-4 py-2 rounded-full text-xs font-semibold border border-gray-200 hover:bg-white transition"
                @click="handleRefresh"
                :disabled="isLoading || !refreshToken"
              >
                Refresh Token
              </button>
              <button
                type="button"
                class="px-4 py-2 rounded-full text-xs font-semibold bg-[#1d1d1f] text-white hover:bg-black transition"
                @click="handleLogout"
                :disabled="isLoading"
              >
                Log out
              </button>
            </div>
          </div>

          <form v-else class="space-y-5" @submit.prevent="handleSubmit">
            <div>
              <label class="block text-sm font-semibold mb-2 text-[#1d1d1f]">Email</label>
              <input
                v-model="form.email"
                type="email"
                class="w-full bg-white/60 border border-gray-200 rounded-xl px-4 py-3 focus:ring-2 focus:ring-[#0071e3] focus:border-transparent transition-all outline-none"
                placeholder="you@example.com"
                autocomplete="email"
                required
              />
            </div>
            <div v-if="mode === 'register'">
              <label class="block text-sm font-semibold mb-2 text-[#1d1d1f]">Nickname</label>
              <input
                v-model="form.nickname"
                type="text"
                class="w-full bg-white/60 border border-gray-200 rounded-xl px-4 py-3 focus:ring-2 focus:ring-[#0071e3] focus:border-transparent transition-all outline-none"
                placeholder="How should we call you?"
                autocomplete="nickname"
                required
              />
            </div>
            <div>
              <label class="block text-sm font-semibold mb-2 text-[#1d1d1f]">Password</label>
              <input
                v-model="form.password"
                type="password"
                class="w-full bg-white/60 border border-gray-200 rounded-xl px-4 py-3 focus:ring-2 focus:ring-[#0071e3] focus:border-transparent transition-all outline-none"
                placeholder="At least 8 characters"
                autocomplete="current-password"
                required
              />
            </div>
            <button
              type="submit"
              class="w-full bg-[#0071e3] text-white py-4 rounded-xl font-bold hover:bg-[#0077ed] transition-all shadow-lg hover:shadow-xl disabled:opacity-60"
              :disabled="isLoading"
            >
              {{ submitLabel }}
            </button>
          </form>

          <div class="mt-4 text-sm">
            <p v-if="error" class="text-red-500">{{ error }}</p>
            <p v-else-if="success" class="text-green-600">{{ success }}</p>
          </div>

          <p class="text-[11px] text-[#86868b] mt-6">
            By continuing you agree to the platform terms. This is a basic auth flow ready for future WeChat scan-in.
          </p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '../composables/useAuth';

const { user, refreshToken, initAuth, login, register, refreshSession, logout } = useAuth();
const router = useRouter();

const mode = ref<'login' | 'register'>('login');
const isLoading = ref(false);
const error = ref<string | null>(null);
const success = ref<string | null>(null);

const form = reactive({
  email: '',
  password: '',
  nickname: '',
});

const currentUser = computed(() => user.value);
const modeTitle = computed(() => (mode.value === 'login' ? 'Sign in' : 'Create account'));
const submitLabel = computed(() => (mode.value === 'login' ? 'Sign in' : 'Register account'));

const setMode = (next: 'login' | 'register') => {
  mode.value = next;
  error.value = null;
  success.value = null;
};

const handleSubmit = async () => {
  error.value = null;
  success.value = null;
  if (!form.email.trim() || !form.password.trim()) return;
  if (mode.value === 'register' && !form.nickname.trim()) return;

  isLoading.value = true;
  try {
    if (mode.value === 'register') {
      await register(form.email.trim(), form.password, form.nickname.trim());
      success.value = 'Account created.';
    } else {
      await login(form.email.trim(), form.password);
      success.value = 'Signed in successfully.';
    }
    form.password = '';
    await router.push('/');
  } catch (err: any) {
    error.value = err?.message || 'Request failed';
  } finally {
    isLoading.value = false;
  }
};

const handleRefresh = async () => {
  error.value = null;
  success.value = null;
  isLoading.value = true;
  try {
    const refreshed = await refreshSession();
    if (!refreshed) {
      throw new Error('Refresh failed');
    }
    success.value = 'Session refreshed.';
  } catch (err: any) {
    error.value = err?.message || 'Refresh failed';
  } finally {
    isLoading.value = false;
  }
};

const handleLogout = async () => {
  error.value = null;
  success.value = null;
  isLoading.value = true;
  try {
    await logout();
  } catch {
    // ignore logout errors
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  initAuth();
});
</script>
