import client from './client';

/**
 * Fetch discussion summary (open tasks, in-progress tasks, recent decisions).
 * GET /api/discussions/summary
 */
export async function fetchSummary() {
  const res = await client.get('/discussions/summary');
  return res.data;
}

/**
 * Fetch all discussions.
 * GET /api/discussions
 */
export async function fetchDiscussions() {
  const res = await client.get('/discussions');
  return res.data;
}

/**
 * Search discussions, tasks, and decisions by keyword.
 * GET /api/discussions/search?q=query
 */
export async function searchDiscussions(query) {
  const res = await client.get('/discussions/search', { params: { q: query } });
  return res.data;
}

/**
 * Log a new discussion message.
 * POST /api/discussions/log { message }
 */
export async function logDiscussion(message) {
  const res = await client.post('/discussions/log', { message });
  return res.data;
}

/**
 * Create a new task.
 * POST /api/discussions/task { title, description }
 */
export async function createTask(title, description) {
  const res = await client.post('/discussions/task', { title, description });
  return res.data;
}

/**
 * Record a decision.
 * POST /api/discussions/decision { title, rationale }
 */
export async function recordDecision(title, rationale) {
  const res = await client.post('/discussions/decision', { title, rationale });
  return res.data;
}

/**
 * Mark a task as in-progress.
 * PUT /api/discussions/:id/start
 */
export async function startTask(id) {
  const res = await client.put(`/discussions/${id}/start`);
  return res.data;
}

/**
 * Mark a task as completed.
 * PUT /api/discussions/:id/complete
 */
export async function completeTask(id) {
  const res = await client.put(`/discussions/${id}/complete`);
  return res.data;
}
