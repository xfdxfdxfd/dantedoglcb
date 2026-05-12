const runtimeEnv = typeof import.meta !== 'undefined' ? import.meta.env || {} : {};
const legacyEnv = typeof process !== 'undefined' ? process.env || {} : {};
const API_BASE_URL = runtimeEnv.VITE_API_BASE_URL || runtimeEnv.VUE_APP_API_BASE_URL || legacyEnv.VUE_APP_API_BASE_URL || 'http://127.0.0.1:8000';
const GOOGLE_CLIENT_ID = runtimeEnv.VITE_GOOGLE_CLIENT_ID || runtimeEnv.VUE_APP_GOOGLE_CLIENT_ID || legacyEnv.VUE_APP_GOOGLE_CLIENT_ID || '';

export const PROGRESS_STORAGE_KEY = 'IDdata';
export const ACCOUNT_SESSION_STORAGE_KEY = 'accountSession';
export const PROGRESS_UPDATED_EVENT = 'progress-updated';

export function getGoogleClientId() {
  return GOOGLE_CLIENT_ID;
}

export function hasGoogleClientId() {
  return Boolean(GOOGLE_CLIENT_ID);
}

function parseStoredJson(key) {
  try {
    return JSON.parse(localStorage.getItem(key) || 'null');
  } catch (_error) {
    return null;
  }
}

function dispatchProgressUpdated(progress, source = 'local') {
  if (typeof window === 'undefined') {
    return;
  }

  window.dispatchEvent(new CustomEvent(PROGRESS_UPDATED_EVENT, { detail: { progress, source } }));
}

async function readErrorMessage(response) {
  const rawText = await response.text();

  if (!rawText) {
    return 'Request failed.';
  }

  try {
    const parsed = JSON.parse(rawText);
    return parsed.detail || rawText;
  } catch (_error) {
    return rawText;
  }
}

function getStoredToken() {
  return getStoredAccountSession()?.token || '';
}

async function apiRequest(path, options = {}) {
  const { body, headers = {}, ...rest } = options;
  const finalHeaders = { ...headers };
  const token = getStoredToken();

  if (token) {
    finalHeaders.Authorization = `Bearer ${token}`;
  }

  const requestOptions = {
    ...rest,
    headers: finalHeaders,
  };

  if (typeof body !== 'undefined') {
    requestOptions.body = JSON.stringify(body);
    requestOptions.headers['Content-Type'] = 'application/json';
  }

  const response = await fetch(`${API_BASE_URL}${path}`, requestOptions);

  if (!response.ok) {
    throw new Error(await readErrorMessage(response));
  }

  return response.json();
}

function storeAccountSession(payload) {
  const session = {
    token: payload.token,
    user: payload.user,
    updatedAt: payload.updated_at || '',
  };

  localStorage.setItem(ACCOUNT_SESSION_STORAGE_KEY, JSON.stringify(session));
  return session;
}

export function getStoredAccountSession() {
  return parseStoredJson(ACCOUNT_SESSION_STORAGE_KEY);
}

export function clearAccountSession() {
  localStorage.removeItem(ACCOUNT_SESSION_STORAGE_KEY);
}

export function readLocalProgress() {
  return parseStoredJson(PROGRESS_STORAGE_KEY);
}

export function hasProgressEntries(progress) {
  return Boolean(progress && typeof progress === 'object' && Object.keys(progress).length);
}

export function writeLocalProgress(progress, source = 'local') {
  localStorage.setItem(PROGRESS_STORAGE_KEY, JSON.stringify(progress));
  dispatchProgressUpdated(progress, source);
}

export function clearLocalProgress(source = 'local') {
  localStorage.removeItem(PROGRESS_STORAGE_KEY);
  dispatchProgressUpdated(null, source);
}

export async function signUpWithEmail(email, password) {
  const payload = await apiRequest('/api/auth/signup/', {
    method: 'POST',
    body: { email, password },
  });

  storeAccountSession(payload);
  return payload;
}

export async function logInWithEmail(email, password) {
  const payload = await apiRequest('/api/auth/login/', {
    method: 'POST',
    body: { email, password },
  });

  storeAccountSession(payload);
  return payload;
}

export async function logInWithGoogleCredential(credential) {
  const payload = await apiRequest('/api/auth/google/', {
    method: 'POST',
    body: { credential },
  });

  storeAccountSession(payload);
  return payload;
}

export async function restoreAccountSession() {
  if (!getStoredToken()) {
    return null;
  }

  try {
    const payload = await apiRequest('/api/auth/session/', {
      method: 'GET',
    });

    storeAccountSession(payload);
    return payload;
  } catch (_error) {
    clearAccountSession();
    return null;
  }
}

export async function logOutAccount() {
  try {
    await apiRequest('/api/auth/logout/', {
      method: 'POST',
    });
  } finally {
    clearAccountSession();
  }
}

export async function saveAccountProgress(progress) {
  if (!getStoredToken()) {
    return null;
  }

  return apiRequest('/api/account/progress/', {
    method: 'PUT',
    body: { progress },
  });
}

export async function loadAccountProgress() {
  if (!getStoredToken()) {
    return null;
  }

  return apiRequest('/api/account/progress/', {
    method: 'GET',
  });
}

export function cloneProgress(progress) {
  return JSON.parse(JSON.stringify(progress));
}

export function sanitizeLevel(value) {
  const parsed = Number.parseInt(value, 10);

  if (Number.isNaN(parsed)) {
    return 1;
  }

  return Math.min(Math.max(parsed, 1), 60);
}

export function sanitizeUptie(value) {
  const parsed = Number.parseInt(value, 10);

  if (Number.isNaN(parsed)) {
    return '0';
  }

  return String(Math.min(Math.max(parsed, 0), 4));
}

export function hydrateProgress(defaultProgress, storedProgress = {}) {
  const merged = cloneProgress(defaultProgress);

  Object.entries(merged).forEach(([sinnerKey, sinnerGroup]) => {
    ['IDs', 'EGOs'].forEach((category) => {
      Object.entries(sinnerGroup[category]).forEach(([entryKey, entry]) => {
        const storedEntry = storedProgress?.[sinnerKey]?.[category]?.[entryKey];

        if (!storedEntry) {
          return;
        }

        entry.uptied = sanitizeUptie(storedEntry.uptied);

        if (category === 'IDs') {
          entry.level = sanitizeLevel(storedEntry.level);
        }
      });
    });
  });

  return merged;
}

export function createRosterManifest(progress) {
  const manifest = [];

  Object.entries(progress).forEach(([sinnerKey, sinnerGroup]) => {
    ['IDs', 'EGOs'].forEach((category) => {
      Object.entries(sinnerGroup[category]).forEach(([entryKey, entry]) => {
        manifest.push({
          sinnerKey,
          category,
          entryKey,
          name: entryKey,
          rarity: entry.rarity,
          hasLevel: category === 'IDs',
        });
      });
    });
  });

  return manifest;
}

export function mergeRecognizedUpdates(progress, updates = []) {
  const merged = cloneProgress(progress);

  updates.forEach((update) => {
    const target = merged?.[update.sinnerKey]?.[update.category]?.[update.entryKey];

    if (!target) {
      return;
    }

    target.uptied = sanitizeUptie(update.uptied);

    if (update.category === 'IDs' && typeof update.level !== 'undefined' && update.level !== null) {
      target.level = sanitizeLevel(update.level);
    }
  });

  return merged;
}

export async function syncProgressWithScreenshots(files, progress) {
  const payload = new FormData();

  files.forEach((file) => {
    payload.append('images', file);
  });

  payload.append('roster_manifest', JSON.stringify(createRosterManifest(progress)));
  payload.append('current_progress', JSON.stringify(progress));

  const response = await fetch(`${API_BASE_URL}/api/sync/recognize/`, {
    method: 'POST',
    body: payload,
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || 'Screenshot sync failed.');
  }

  return response.json();
}

export async function submitRecognitionFeedback(feedback = []) {
  if (!Array.isArray(feedback) || !feedback.length) {
    return { saved_feedback: 0 };
  }

  const response = await fetch(`${API_BASE_URL}/api/sync/feedback/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ feedback }),
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || 'Failed to save recognition feedback.');
  }

  return response.json();
}