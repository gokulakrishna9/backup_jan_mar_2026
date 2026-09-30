import { useEffect, useState, useCallback } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useApiCall } from '../utils/api';
import {
  fetchEntities,
  addEntity,
  removeEntity,
  addField,
  removeField,
  modifyField,
  addEndpoint,
  removeEndpoint,
  addQuery,
  removeQuery,
  addRelationship,
  removeRelationship,
  fetchAppStatus,
} from '../api/entities';
import EntityEditor from '../components/EntityEditor';
import GenerationPanel from '../components/GenerationPanel';
import useAppStore from '../store/appStore';

/* ── Add Entity Form ── */

function AddEntityForm({ onAdd, loading }) {
  const [name, setName] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!name.trim()) return;
    onAdd({ name: name.trim() });
    setName('');
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 p-3 border-t border-gray-200">
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="New entity name"
        className="flex-1 border border-gray-300 rounded px-2 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
      />
      <button
        type="submit"
        disabled={loading}
        className="px-3 py-1.5 text-sm font-medium text-white bg-indigo-600 rounded hover:bg-indigo-700 disabled:opacity-50"
      >
        Add
      </button>
    </form>
  );
}

/* ── Status Summary Bar ── */

function StatusBar({ status }) {
  if (!status) return null;
  const dirty = status.dirtyFiles ?? 0;
  const clean = status.cleanFiles ?? 0;
  return (
    <div className="flex items-center gap-4 text-sm mb-4 px-1">
      <span className="flex items-center gap-1">
        <span className="w-2 h-2 rounded-full bg-yellow-400 inline-block" />
        {dirty} dirty
      </span>
      <span className="flex items-center gap-1">
        <span className="w-2 h-2 rounded-full bg-green-400 inline-block" />
        {clean} clean
      </span>
      {status.lastGeneration && (
        <span className="text-gray-400 text-xs">Last gen: {new Date(status.lastGeneration).toLocaleString()}</span>
      )}
    </div>
  );
}

/* ── AppDetail Page ── */

export default function AppDetail() {
  const { name: appName } = useParams();
  const setSelectedApp = useAppStore((s) => s.setSelectedApp);

  const [selectedEntity, setSelectedEntity] = useState(null);
  const [actionLoading, setActionLoading] = useState(false);

  const { data: entities, loading, error, execute: loadEntities, setData: setEntities } = useApiCall(fetchEntities);
  const { data: status, execute: loadStatus } = useApiCall(fetchAppStatus);

  // Load entities and status on mount / app change
  useEffect(() => {
    setSelectedApp(appName);
    loadEntities(appName);
    loadStatus(appName);
  }, [appName]); // eslint-disable-line react-hooks/exhaustive-deps

  // Auto-select first entity when entities load
  useEffect(() => {
    if (entities && entities.length > 0 && !selectedEntity) {
      setSelectedEntity(entities[0].name);
    }
  }, [entities]); // eslint-disable-line react-hooks/exhaustive-deps

  const currentEntity = entities?.find((e) => e.name === selectedEntity) || null;

  // Reload helper
  const reload = useCallback(async () => {
    await loadEntities(appName);
    await loadStatus(appName);
  }, [appName, loadEntities, loadStatus]);

  // Wrap an async action with loading state + reload
  const withAction = useCallback((fn) => async (...args) => {
    setActionLoading(true);
    try {
      await fn(...args);
      await reload();
    } catch {
      // error captured by useApiCall
    } finally {
      setActionLoading(false);
    }
  }, [reload]);

  /* ── Action handlers ── */

  const handleAddEntity = withAction((data) => addEntity(appName, data));

  const handleRemoveEntity = withAction(async (entityName) => {
    await removeEntity(appName, entityName);
    if (selectedEntity === entityName) setSelectedEntity(null);
  });

  const handleAddField = withAction((field) => addField(appName, selectedEntity, field));
  const handleRemoveField = withAction((fieldName) => removeField(appName, selectedEntity, fieldName));
  const handleModifyField = withAction((fieldName, updates) => modifyField(appName, selectedEntity, fieldName, updates));

  const handleAddEndpoint = withAction((ep) => addEndpoint(appName, selectedEntity, ep));
  const handleRemoveEndpoint = withAction((name) => removeEndpoint(appName, selectedEntity, name));

  const handleAddQuery = withAction((q) => addQuery(appName, selectedEntity, q));
  const handleRemoveQuery = withAction((name) => removeQuery(appName, selectedEntity, name));

  const handleAddRelationship = withAction((rel) => addRelationship(appName, selectedEntity, rel));
  const handleRemoveRelationship = withAction((name) => removeRelationship(appName, selectedEntity, name));

  return (
    <div className="max-w-7xl mx-auto px-4 py-6">
      {/* Breadcrumb + title */}
      <div className="mb-4">
        <Link to="/" className="text-sm text-indigo-600 hover:text-indigo-800">← Dashboard</Link>
        <h1 className="text-2xl font-bold text-gray-900 mt-1">{appName}</h1>
      </div>

      <StatusBar status={status} />

      {/* Error */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 rounded-md p-4 mb-4">
          Failed to load entities: {error}
        </div>
      )}

      {/* Loading */}
      {loading && (
        <div className="flex justify-center py-12">
          <div className="h-8 w-8 border-4 border-indigo-400 border-t-transparent rounded-full animate-spin" />
        </div>
      )}

      {/* Main layout: sidebar + editor */}
      {!loading && entities && (
        <div className="flex gap-6">
          {/* Sidebar — entity list */}
          <div className="w-64 shrink-0">
            <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
              <div className="px-4 py-3 bg-gray-50 border-b border-gray-200">
                <h3 className="text-sm font-semibold text-gray-700">Entities ({entities.length})</h3>
              </div>
              {entities.length === 0 ? (
                <p className="px-4 py-6 text-sm text-gray-400 text-center italic">No entities yet</p>
              ) : (
                <ul className="divide-y divide-gray-100">
                  {entities.map((ent) => {
                    const isSelected = ent.name === selectedEntity;
                    const isDirty = ent.dirty ?? ent.isDirty ?? false;
                    return (
                      <li key={ent.name} className="flex items-center">
                        <button
                          onClick={() => setSelectedEntity(ent.name)}
                          className={`flex-1 text-left px-4 py-2.5 text-sm transition-colors ${
                            isSelected
                              ? 'bg-indigo-50 text-indigo-700 font-medium'
                              : 'text-gray-700 hover:bg-gray-50'
                          }`}
                        >
                          <span>{ent.name}</span>
                          {isDirty && (
                            <span className="ml-1.5 inline-block w-1.5 h-1.5 rounded-full bg-yellow-400" title="Dirty" />
                          )}
                        </button>
                        <button
                          onClick={() => handleRemoveEntity(ent.name)}
                          className="px-2 py-2 text-red-400 hover:text-red-600 text-xs"
                          title={`Remove ${ent.name}`}
                        >
                          ✕
                        </button>
                      </li>
                    );
                  })}
                </ul>
              )}
              <AddEntityForm onAdd={handleAddEntity} loading={actionLoading} />
            </div>
          </div>

          {/* Main area — entity editor + generation panel */}
          <div className="flex-1 min-w-0">
            <EntityEditor
              entity={currentEntity}
              appName={appName}
              onAddField={handleAddField}
              onRemoveField={handleRemoveField}
              onModifyField={handleModifyField}
              onAddEndpoint={handleAddEndpoint}
              onRemoveEndpoint={handleRemoveEndpoint}
              onAddQuery={handleAddQuery}
              onRemoveQuery={handleRemoveQuery}
              onAddRelationship={handleAddRelationship}
              onRemoveRelationship={handleRemoveRelationship}
              loading={actionLoading}
            />
            <GenerationPanel appName={appName} />
          </div>
        </div>
      )}
    </div>
  );
}
