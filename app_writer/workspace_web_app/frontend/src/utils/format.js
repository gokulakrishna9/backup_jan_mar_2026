/**
 * Format an ISO date string to a readable locale string.
 */
export function formatDate(isoString) {
  if (!isoString) return '—';
  try {
    return new Date(isoString).toLocaleString();
  } catch {
    return isoString;
  }
}

/**
 * Format a status string into a display-friendly label.
 */
export function formatStatus(status) {
  if (!status) return 'Unknown';
  const map = {
    running: 'Running',
    completed: 'Completed',
    failed: 'Failed',
    cancelled: 'Cancelled',
    pending: 'Pending',
    dirty: 'Dirty',
    clean: 'Clean',
  };
  return map[status.toLowerCase()] || titleCase(status);
}

/**
 * Convert a string to Title Case.
 */
export function titleCase(str) {
  if (!str) return '';
  return str
    .replace(/[_-]/g, ' ')
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

/**
 * Mask an API key, showing only the last 3 characters.
 */
export function maskApiKey(key) {
  if (!key) return '';
  if (key.length <= 3) return '***';
  return '•'.repeat(key.length - 3) + key.slice(-3);
}
