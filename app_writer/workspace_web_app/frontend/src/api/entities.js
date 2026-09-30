import client from './client';

/* ── Entity CRUD ── */

export async function fetchEntities(app) {
  const res = await client.get(`/apps/${app}/entities`);
  return res.data;
}

export async function addEntity(app, data) {
  const res = await client.post(`/apps/${app}/entities`, data);
  return res.data;
}

export async function removeEntity(app, name) {
  const res = await client.delete(`/apps/${app}/entities/${name}`);
  return res.data;
}

/* ── Field CRUD ── */

export async function addField(app, entity, field) {
  const res = await client.post(`/apps/${app}/entities/${entity}/fields`, field);
  return res.data;
}

export async function removeField(app, entity, fieldName) {
  const res = await client.delete(`/apps/${app}/entities/${entity}/fields/${fieldName}`);
  return res.data;
}

export async function modifyField(app, entity, fieldName, updates) {
  const res = await client.put(`/apps/${app}/entities/${entity}/fields/${fieldName}`, updates);
  return res.data;
}

/* ── Endpoints ── */

export async function addEndpoint(app, entity, endpoint) {
  const res = await client.post(`/apps/${app}/entities/${entity}/endpoints`, endpoint);
  return res.data;
}

export async function removeEndpoint(app, entity, name) {
  const res = await client.delete(`/apps/${app}/entities/${entity}/endpoints/${name}`);
  return res.data;
}

/* ── Queries ── */

export async function addQuery(app, entity, query) {
  const res = await client.post(`/apps/${app}/entities/${entity}/queries`, query);
  return res.data;
}

export async function removeQuery(app, entity, name) {
  const res = await client.delete(`/apps/${app}/entities/${entity}/queries/${name}`);
  return res.data;
}

/* ── Relationships ── */

export async function addRelationship(app, entity, relationship) {
  const res = await client.post(`/apps/${app}/entities/${entity}/relationships`, relationship);
  return res.data;
}

export async function removeRelationship(app, entity, name) {
  const res = await client.delete(`/apps/${app}/entities/${entity}/relationships/${name}`);
  return res.data;
}

/* ── App Status ── */

export async function fetchAppStatus(app) {
  const res = await client.get(`/apps/${app}/status`);
  return res.data;
}
