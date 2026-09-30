import { useEffect, useState, useCallback } from 'react';
import { useApiCall } from '../utils/api';
import { getAIConfig, updateAIConfig, testProviderConnection } from '../api/aiSettings';
import { maskApiKey } from '../utils/format';
import { validateTemperature, validateMaxTokens } from '../utils/validation';

/* ── Default parameter values ── */

const DEFAULT_PARAMS = {
  temperature: 0.7,
  max_tokens: 4096,
  top_p: 1.0,
  frequency_penalty: 0.0,
};

/* ── Provider Status Indicator ── */

function StatusIndicator({ status }) {
  const colors = {
    reachable: 'bg-green-500',
    connected: 'bg-green-500',
    configured: 'bg-green-500',
    auth_error: 'bg-red-500',
    error: 'bg-red-500',
    timeout: 'bg-yellow-500',
    unconfigured: 'bg-gray-400',
    not_configured: 'bg-gray-400',
  };
  const cls = colors[(status || '').toLowerCase()] || 'bg-gray-400';
  return (
    <span className={`inline-block w-3 h-3 rounded-full ${cls}`} title={status || 'Unknown'} />
  );
}

/* ── Model Selection Dropdown (grouped by provider) ── */

function ModelSelector({ label, value, onChange, modelRegistry, id }) {
  return (
    <div>
      <label htmlFor={id} className="block text-sm font-medium text-gray-700 mb-1">
        {label}
      </label>
      <select
        id={id}
        value={value || ''}
        onChange={(e) => onChange(e.target.value)}
        className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
      >
        <option value="">Select a model…</option>
        {(modelRegistry || []).map((group) => (
          <optgroup key={group.provider} label={group.provider}>
            {(group.models || []).map((model) => (
              <option key={model.id} value={model.id}>
                {model.display_name || model.id}
              </option>
            ))}
          </optgroup>
        ))}
      </select>
    </div>
  );
}

/* ── Parameter Slider ── */

function ParamSlider({ label, id, value, onChange, min, max, step }) {
  return (
    <div>
      <label htmlFor={id} className="block text-sm font-medium text-gray-700 mb-1">
        {label}: <span className="font-mono text-indigo-600">{value}</span>
      </label>
      <input
        id={id}
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-indigo-600"
      />
      <div className="flex justify-between text-xs text-gray-400 mt-1">
        <span>{min}</span>
        <span>{max}</span>
      </div>
    </div>
  );
}

/* ── Provider Card ── */

function ProviderCard({ provider, onTestConnection, testingProvider }) {
  const isTesting = testingProvider === provider.name;

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-4 shadow-sm">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <StatusIndicator status={provider.status} />
          <h3 className="text-sm font-semibold text-gray-900">{provider.name}</h3>
        </div>
        <span className="text-xs text-gray-500">
          {provider.api_key_configured ? 'Key configured' : 'Not configured'}
        </span>
      </div>

      {/* Masked API key display */}
      {provider.api_key_configured && provider.api_key_hint && (
        <div className="mb-3">
          <p className="text-xs text-gray-500 mb-1">API Key</p>
          <code className="text-xs bg-gray-100 px-2 py-1 rounded font-mono text-gray-600">
            {maskApiKey(provider.api_key_hint)}
          </code>
        </div>
      )}

      {!provider.api_key_configured && (
        <p className="text-xs text-gray-400 mb-3 italic">
          Set via environment variable: {provider.api_key_env || `${provider.name.toUpperCase().replace(/\s+/g, '_')}_API_KEY`}
        </p>
      )}

      {/* Test Connection button */}
      <button
        type="button"
        onClick={() => onTestConnection(provider.name)}
        disabled={isTesting}
        className="w-full px-3 py-1.5 text-xs font-medium text-indigo-700 bg-indigo-50 rounded-md hover:bg-indigo-100 disabled:opacity-50 transition-colors"
      >
        {isTesting ? 'Testing…' : 'Test Connection'}
      </button>
    </div>
  );
}

/* ── AI Settings Page ── */

export default function AISettings() {
  const { data: config, loading, error, execute: loadConfig } = useApiCall(getAIConfig);
  const { loading: saving, execute: saveConfig } = useApiCall(updateAIConfig);

  const [activeModel, setActiveModel] = useState('');
  const [fallbackModel, setFallbackModel] = useState('');
  const [params, setParams] = useState({ ...DEFAULT_PARAMS });
  const [validationErrors, setValidationErrors] = useState({});
  const [testingProvider, setTestingProvider] = useState(null);
  const [testResult, setTestResult] = useState(null);
  const [saveSuccess, setSaveSuccess] = useState(false);

  // Load config on mount
  useEffect(() => {
    loadConfig();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // Populate local state from loaded config
  useEffect(() => {
    if (config) {
      setActiveModel(config.active_model || '');
      setFallbackModel(config.fallback_model || '');
      setParams({
        temperature: config.model_params?.temperature ?? DEFAULT_PARAMS.temperature,
        max_tokens: config.model_params?.max_tokens ?? DEFAULT_PARAMS.max_tokens,
        top_p: config.model_params?.top_p ?? DEFAULT_PARAMS.top_p,
        frequency_penalty: config.model_params?.frequency_penalty ?? DEFAULT_PARAMS.frequency_penalty,
      });
    }
  }, [config]);

  // Parameter change handler with validation
  const handleParamChange = useCallback((key, value) => {
    setParams((prev) => ({ ...prev, [key]: value }));
    setSaveSuccess(false);

    // Validate
    const errors = { ...validationErrors };
    if (key === 'temperature') {
      const err = validateTemperature(value);
      if (err) errors.temperature = err;
      else delete errors.temperature;
    }
    if (key === 'max_tokens') {
      const err = validateMaxTokens(value);
      if (err) errors.max_tokens = err;
      else delete errors.max_tokens;
    }
    setValidationErrors(errors);
  }, [validationErrors]);

  // Test provider connection
  const handleTestConnection = useCallback(async (providerName) => {
    setTestingProvider(providerName);
    setTestResult(null);
    try {
      const result = await testProviderConnection(providerName);
      setTestResult({ provider: providerName, ...result });
    } catch (err) {
      setTestResult({
        provider: providerName,
        status: 'error',
        message: err.response?.data?.detail || err.message || 'Connection test failed',
      });
    } finally {
      setTestingProvider(null);
    }
  }, []);

  // Save settings
  const handleSave = useCallback(async () => {
    // Validate before saving
    const errors = {};
    const tempErr = validateTemperature(params.temperature);
    if (tempErr) errors.temperature = tempErr;
    const tokErr = validateMaxTokens(params.max_tokens);
    if (tokErr) errors.max_tokens = tokErr;

    if (Object.keys(errors).length > 0) {
      setValidationErrors(errors);
      return;
    }

    try {
      await saveConfig({
        active_model: activeModel,
        fallback_model: fallbackModel,
        model_params: params,
        save: true,
      });
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
    } catch {
      // error captured by useApiCall
    }
  }, [activeModel, fallbackModel, params, saveConfig]);

  // Reset to defaults
  const handleReset = useCallback(() => {
    setParams({ ...DEFAULT_PARAMS });
    setValidationErrors({});
    setSaveSuccess(false);
  }, []);

  const modelRegistry = config?.model_registry || [];
  const providers = config?.providers || [];

  return (
    <div className="max-w-7xl mx-auto px-4 py-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900">AI Settings</h1>
        <div className="flex gap-3">
          <button
            type="button"
            onClick={handleReset}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-400"
          >
            Reset to Defaults
          </button>
          <button
            type="button"
            onClick={handleSave}
            disabled={saving || Object.keys(validationErrors).length > 0}
            className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 disabled:opacity-50 focus:outline-none focus:ring-2 focus:ring-indigo-400"
          >
            {saving ? 'Saving…' : 'Save Settings'}
          </button>
        </div>
      </div>

      {/* Save success message */}
      {saveSuccess && (
        <div className="bg-green-50 border border-green-200 text-green-700 rounded-md p-3 mb-4 text-sm">
          Settings saved successfully.
        </div>
      )}

      {/* Loading */}
      {loading && (
        <div className="flex justify-center py-12">
          <div className="h-8 w-8 border-4 border-indigo-400 border-t-transparent rounded-full animate-spin" />
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 rounded-md p-4 mb-4">
          Failed to load AI configuration: {error}
        </div>
      )}

      {/* Main content */}
      {!loading && config && (
        <div className="space-y-8">
          {/* ── Model Selection ── */}
          <section className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Model Selection</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <ModelSelector
                label="Default Model"
                id="default-model"
                value={activeModel}
                onChange={(v) => { setActiveModel(v); setSaveSuccess(false); }}
                modelRegistry={modelRegistry}
              />
              <ModelSelector
                label="Fallback Model"
                id="fallback-model"
                value={fallbackModel}
                onChange={(v) => { setFallbackModel(v); setSaveSuccess(false); }}
                modelRegistry={modelRegistry}
              />
            </div>
          </section>

          {/* ── Model Parameters ── */}
          <section className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Model Parameters</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Temperature */}
              <div>
                <ParamSlider
                  label="Temperature"
                  id="param-temperature"
                  value={params.temperature}
                  onChange={(v) => handleParamChange('temperature', v)}
                  min={0}
                  max={2}
                  step={0.1}
                />
                {validationErrors.temperature && (
                  <p className="text-red-500 text-xs mt-1">{validationErrors.temperature}</p>
                )}
              </div>

              {/* Max Tokens */}
              <div>
                <label htmlFor="param-max-tokens" className="block text-sm font-medium text-gray-700 mb-1">
                  Max Tokens
                </label>
                <input
                  id="param-max-tokens"
                  type="number"
                  min={1}
                  value={params.max_tokens}
                  onChange={(e) => handleParamChange('max_tokens', parseInt(e.target.value, 10) || 0)}
                  className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
                />
                {validationErrors.max_tokens && (
                  <p className="text-red-500 text-xs mt-1">{validationErrors.max_tokens}</p>
                )}
              </div>

              {/* Top-P */}
              <ParamSlider
                label="Top-P"
                id="param-top-p"
                value={params.top_p}
                onChange={(v) => handleParamChange('top_p', v)}
                min={0}
                max={1}
                step={0.05}
              />

              {/* Frequency Penalty */}
              <ParamSlider
                label="Frequency Penalty"
                id="param-frequency-penalty"
                value={params.frequency_penalty}
                onChange={(v) => handleParamChange('frequency_penalty', v)}
                min={-2}
                max={2}
                step={0.1}
              />
            </div>
          </section>

          {/* ── Providers ── */}
          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Providers</h2>

            {/* Test result banner */}
            {testResult && (
              <div
                className={`rounded-md p-3 mb-4 text-sm ${
                  testResult.status === 'reachable' || testResult.status === 'connected'
                    ? 'bg-green-50 border border-green-200 text-green-700'
                    : 'bg-red-50 border border-red-200 text-red-700'
                }`}
              >
                <span className="font-medium">{testResult.provider}:</span>{' '}
                {testResult.message || testResult.status}
              </div>
            )}

            {providers.length === 0 && (
              <p className="text-sm text-gray-500">No providers configured.</p>
            )}

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {providers.map((provider) => (
                <ProviderCard
                  key={provider.name}
                  provider={provider}
                  onTestConnection={handleTestConnection}
                  testingProvider={testingProvider}
                />
              ))}
            </div>
          </section>
        </div>
      )}
    </div>
  );
}
