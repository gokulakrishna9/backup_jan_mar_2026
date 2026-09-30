import client from './client';

/**
 * Fetch all applications.
 * GET /api/apps → [{ name, entities, dirtyFiles, cleanFiles, lastGeneration, status }]
 */
export async function fetchApps() {
  const res = await client.get('/apps');
  return res.data;
}

/**
 * Scaffold a new application.
 * POST /api/apps { name, entities }
 */
export async function scaffoldApp({ name, entities }) {
  const res = await client.post('/apps', { name, entities });
  return res.data;
}

/**
 * Fetch status for a single application.
 * GET /api/apps/:name/status → { dirtyFiles, cleanFiles, lastGeneration }
 */
export async function fetchAppStatus(appName) {
  const res = await client.get(`/apps/${appName}/status`);
  return res.data;
}
