import client from './client';

/* ── Generation triggers ── */

export async function generateFull(app) {
  const res = await client.post(`/generate/${app}/full`);
  return res.data;
}

export async function generateIncremental(app) {
  const res = await client.post(`/generate/${app}/incremental`);
  return res.data;
}

export async function generateSQLOnly(app) {
  const res = await client.post(`/generate/${app}/sql-only`);
  return res.data;
}

export async function generateReact(app) {
  const res = await client.post(`/generate/${app}/react`);
  return res.data;
}

/* ── Job management ── */

export async function getJobStatus(app, jobId) {
  const res = await client.get(`/generate/${app}/jobs/${jobId}`);
  return res.data;
}

export async function cancelJob(app, jobId) {
  const res = await client.delete(`/generate/${app}/jobs/${jobId}`);
  return res.data;
}
