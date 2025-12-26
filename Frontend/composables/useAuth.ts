import { reactive, ref, toRef } from 'vue';

interface AuthUser {
  id: number;
  email: string;
  nickname: string;
  created_at?: string | null;
  last_login_at?: string | null;
}

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:5050';
const ACCESS_KEY = 'auth.accessToken';
const REFRESH_KEY = 'auth.refreshToken';

const state = reactive<{ user: AuthUser | null }>({
  user: null,
});

const accessToken = ref<string | null>(localStorage.getItem(ACCESS_KEY));
const refreshToken = ref<string | null>(localStorage.getItem(REFRESH_KEY));
let initPromise: Promise<void> | null = null;

const setTokens = (access: string, refresh: string) => {
  accessToken.value = access;
  refreshToken.value = refresh;
  localStorage.setItem(ACCESS_KEY, access);
  localStorage.setItem(REFRESH_KEY, refresh);
};

const clearTokens = () => {
  accessToken.value = null;
  refreshToken.value = null;
  localStorage.removeItem(ACCESS_KEY);
  localStorage.removeItem(REFRESH_KEY);
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

const fetchMe = async () => {
  if (!accessToken.value) return null;
  const res = await fetch(`${API_BASE}/api/auth/me`, {
    headers: { Authorization: `Bearer ${accessToken.value}` },
  });
  if (!res.ok) return null;
  const data = await res.json();
  state.user = data.user;
  return state.user;
};

const refreshSession = async () => {
  if (!refreshToken.value) return null;
  const res = await fetch(`${API_BASE}/api/auth/refresh`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh_token: refreshToken.value }),
  });
  if (!res.ok) {
    clearTokens();
    state.user = null;
    return null;
  }
  const data = await res.json();
  setTokens(data.access_token, data.refresh_token);
  state.user = data.user;
  return state.user;
};

const changePassword = async (currentPassword: string, newPassword: string) => {
  if (!accessToken.value) {
    throw new Error('Please sign in before changing your password.');
  }
  const res = await fetch(`${API_BASE}/api/auth/password`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${accessToken.value}`,
    },
    body: JSON.stringify({ current_password: currentPassword, new_password: newPassword }),
  });
  if (!res.ok) {
    throw new Error(await parseError(res));
  }
  return true;
};

const initAuth = () => {
  if (initPromise) return initPromise;
  initPromise = (async () => {
    if (!accessToken.value && !refreshToken.value) return;
    const user = await fetchMe();
    if (!user && refreshToken.value) {
      await refreshSession();
    }
  })();
  return initPromise;
};

const login = async (email: string, password: string) => {
  const res = await fetch(`${API_BASE}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) {
    throw new Error(await parseError(res));
  }
  const data = await res.json();
  setTokens(data.access_token, data.refresh_token);
  state.user = data.user;
  return data.user as AuthUser;
};

const register = async (email: string, password: string, nickname: string) => {
  const res = await fetch(`${API_BASE}/api/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, nickname }),
  });
  if (!res.ok) {
    throw new Error(await parseError(res));
  }
  const data = await res.json();
  setTokens(data.access_token, data.refresh_token);
  state.user = data.user;
  return data.user as AuthUser;
};

const logout = async () => {
  if (refreshToken.value) {
    await fetch(`${API_BASE}/api/auth/logout`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh_token: refreshToken.value }),
    });
  }
  clearTokens();
  state.user = null;
};

export const useAuth = () => ({
  user: toRef(state, 'user'),
  accessToken,
  refreshToken,
  initAuth,
  login,
  register,
  refreshSession,
  changePassword,
  logout,
});
