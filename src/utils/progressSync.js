const runtimeEnv = typeof import.meta !== 'undefined' ? import.meta.env || {} : {};
const legacyEnv = typeof process !== 'undefined' ? process.env || {} : {};
const API_BASE_URL = runtimeEnv.VITE_API_BASE_URL || runtimeEnv.VUE_APP_API_BASE_URL || legacyEnv.VUE_APP_API_BASE_URL || 'http://127.0.0.1:8000';

export const PROGRESS_STORAGE_KEY = 'IDdata';

export function cloneProgress(progress) {
  return JSON.parse(JSON.stringify(progress));
}

export function sanitizeLevel(value) {
  const parsed = Number.parseInt(value, 10);

  if (Number.isNaN(parsed)) {
    return 1;
  }

  return Math.min(Math.max(parsed, 1), 50);
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