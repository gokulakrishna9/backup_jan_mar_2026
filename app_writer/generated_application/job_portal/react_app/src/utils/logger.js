/**
 * Client-side logger utility.
 * Controlled by VITE_ENABLE_LOGGING env variable.
 * Logs API errors, network errors, data validation errors, and unhandled exceptions.
 */
const LOGGING_ENABLED = import.meta.env.VITE_ENABLE_LOGGING === 'true';

const formatTimestamp = () => new Date().toISOString();

const logger = {
  /** Log API/HTTP errors (non-2xx responses) */
  apiError: (method, url, status, data) => {
    if (!LOGGING_ENABLED) return;
    console.error(
      `[API ERROR] ${formatTimestamp()} ${method} ${url} → ${status}`,
      data || ''
    );
  },

  /** Log network errors (no response received) */
  networkError: (method, url, error) => {
    if (!LOGGING_ENABLED) return;
    console.error(
      `[NETWORK ERROR] ${formatTimestamp()} ${method} ${url}`,
      error?.message || error
    );
  },

  /** Log data/validation errors (bad payloads, missing fields, parse failures) */
  dataError: (context, message, detail) => {
    if (!LOGGING_ENABLED) return;
    console.warn(
      `[DATA ERROR] ${formatTimestamp()} [${context}]`,
      message,
      detail || ''
    );
  },

  /** Log Redux action errors */
  storeError: (action, error) => {
    if (!LOGGING_ENABLED) return;
    console.error(
      `[STORE ERROR] ${formatTimestamp()} ${action}`,
      error?.message || error
    );
  },

  /** Log auth errors (token expired, permission denied) */
  authError: (message, detail) => {
    if (!LOGGING_ENABLED) return;
    console.warn(
      `[AUTH ERROR] ${formatTimestamp()}`,
      message,
      detail || ''
    );
  },

  /** Log render/component errors */
  renderError: (component, error) => {
    if (!LOGGING_ENABLED) return;
    console.error(
      `[RENDER ERROR] ${formatTimestamp()} <${component}>`,
      error?.message || error,
      error?.stack || ''
    );
  },

  /** General info log (only in dev) */
  info: (context, message) => {
    if (!LOGGING_ENABLED) return;
    console.info(`[INFO] ${formatTimestamp()} [${context}]`, message);
  },
};

export default logger;