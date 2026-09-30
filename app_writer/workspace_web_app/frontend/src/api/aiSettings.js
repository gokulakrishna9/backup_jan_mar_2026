import client from './client';

/**
 * Fetch AI configuration: model registry, active model, params, provider status.
 * GET /api/ai/config
 */
export async function getAIConfig() {
  const res = await client.get('/ai/config');
  return res.data;
}

/**
 * Update AI configuration: active model, params, custom endpoints.
 * PUT /api/ai/config
 * @param {object} config - { active_model?, model_params?, custom_endpoint?, save? }
 */
export async function updateAIConfig(config) {
  const res = await client.put('/ai/config', config);
  return res.data;
}

/**
 * Test connectivity to a specific LLM provider.
 * POST /api/ai/health-check/:provider
 * @param {string} provider - Provider display name (e.g., "OpenAI")
 * @returns {Promise<{status: string, message: string}>}
 */
export async function testProviderConnection(provider) {
  const res = await client.post(`/ai/health-check/${encodeURIComponent(provider)}`);
  return res.data;
}
