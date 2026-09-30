import client from './client';

/**
 * Send a chat message to the agent. Returns a fetch Response with SSE body.
 * Uses fetch (not axios) because the response is an SSE stream.
 *
 * @param {string} appName - Target application name (empty string for global context)
 * @param {string} message - User message
 * @param {string} sessionId - Browser session ID
 * @returns {Promise<Response>} fetch Response with SSE body
 */
export async function sendChatMessage(appName, message, sessionId = '') {
  const response = await fetch('/api/agent/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message,
      app_name: appName || '',
      session_id: sessionId,
    }),
  });

  if (!response.ok) {
    const text = await response.text().catch(() => 'Request failed');
    throw new Error(text);
  }

  return response;
}

/**
 * Fetch conversation history for a specific application.
 * @param {string} appName - Application name (use '_global' for global context)
 * @returns {Promise<object>} Conversation history
 */
export async function getHistory(appName) {
  const key = appName || '_global';
  const res = await client.get(`/agent/history/${encodeURIComponent(key)}`);
  return res.data;
}

/**
 * Clear conversation history for a specific application.
 * @param {string} appName - Application name (use '_global' for global context)
 * @returns {Promise<object>} Confirmation
 */
export async function clearHistory(appName) {
  const key = appName || '_global';
  const res = await client.delete(`/agent/history/${encodeURIComponent(key)}`);
  return res.data;
}
