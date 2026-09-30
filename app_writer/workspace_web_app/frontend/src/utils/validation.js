/**
 * Validate temperature is within [0.0, 2.0].
 * Returns error string or null if valid.
 */
export function validateTemperature(value) {
  const num = parseFloat(value);
  if (isNaN(num)) return 'Temperature must be a number';
  if (num < 0 || num > 2) return 'Temperature must be between 0.0 and 2.0';
  return null;
}

/**
 * Validate max tokens is a positive integer.
 * Returns error string or null if valid.
 */
export function validateMaxTokens(value) {
  const num = parseInt(value, 10);
  if (isNaN(num)) return 'Max tokens must be a number';
  if (num <= 0) return 'Max tokens must be greater than 0';
  return null;
}

/**
 * Validate that a value is non-empty.
 * Returns error string or null if valid.
 */
export function validateRequired(value, fieldName = 'Field') {
  if (value === null || value === undefined || String(value).trim() === '') {
    return `${fieldName} is required`;
  }
  return null;
}
