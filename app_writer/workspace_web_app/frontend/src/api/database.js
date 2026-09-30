import client from './client';

/**
 * Fetch all databases.
 * GET /api/databases → [{ name, ... }]
 */
export async function fetchDatabases() {
  const res = await client.get('/databases');
  return res.data;
}

/**
 * Create a new database.
 * POST /api/databases { name }
 */
export async function createDatabase(name) {
  const res = await client.post('/databases', { name });
  return res.data;
}

/**
 * Drop a database (requires confirm: true).
 * DELETE /api/databases/:name
 */
export async function dropDatabase(name) {
  const res = await client.delete(`/databases/${name}`, { data: { confirm: true } });
  return res.data;
}

/**
 * Run setup workflow for a database.
 * POST /api/databases/:name/setup
 */
export async function setupDatabase(name) {
  const res = await client.post(`/databases/${name}/setup`);
  return res.data;
}

/**
 * Execute a query against a database.
 * POST /api/databases/:name/query { query }
 */
export async function queryDatabase(name, query) {
  const res = await client.post(`/databases/${name}/query`, { query });
  return res.data;
}
