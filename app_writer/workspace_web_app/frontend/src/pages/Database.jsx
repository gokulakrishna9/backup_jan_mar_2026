import { useEffect, useState } from 'react';
import { useApiCall } from '../utils/api';
import {
  fetchDatabases,
  createDatabase,
  dropDatabase,
  setupDatabase,
  queryDatabase,
} from '../api/database';

/* ── Confirm Dialog ── */

function ConfirmDialog({ open, title, message, onConfirm, onCancel, loading }) {
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40" onClick={onCancel}>
      <div
        className="bg-white rounded-lg shadow-xl w-full max-w-sm mx-4 p-6"
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
        aria-label={title}
      >
        <h3 className="text-lg font-bold text-gray-900 mb-2">{title}</h3>
        <p className="text-sm text-gray-600 mb-5">{message}</p>
        <div className="flex justify-end gap-3">
          <button
            type="button"
            onClick={onCancel}
            className="px-4 py-2 text-sm text-gray-600 hover:text-gray-800"
          >
            Cancel
          </button>
          <button
            type="button"
            onClick={onConfirm}
            disabled={loading}
            className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700 disabled:opacity-50"
          >
            {loading ? 'Dropping…' : 'Drop'}
          </button>
        </div>
      </div>
    </div>
  );
}

/* ── Create Database Modal ── */

function CreateModal({ open, onClose, onSubmit, loading }) {
  const [name, setName] = useState('');
  const [error, setError] = useState('');

  if (!open) return null;

  const handleSubmit = (e) => {
    e.preventDefault();
    const trimmed = name.trim();
    if (!trimmed) { setError('Database name is required'); return; }
    onSubmit(trimmed);
  };

  const handleClose = () => { setName(''); setError(''); onClose(); };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40" onClick={handleClose}>
      <div
        className="bg-white rounded-lg shadow-xl w-full max-w-sm mx-4 p-6"
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
        aria-label="Create Database"
      >
        <h2 className="text-xl font-bold text-gray-900 mb-4">Create Database</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="db-name" className="block text-sm font-medium text-gray-700 mb-1">
              Database Name <span className="text-red-500">*</span>
            </label>
            <input
              id="db-name"
              type="text"
              value={name}
              onChange={(e) => { setName(e.target.value); setError(''); }}
              placeholder="my_database"
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
              autoFocus
            />
            {error && <p className="text-red-500 text-xs mt-1">{error}</p>}
          </div>
          <div className="flex justify-end gap-3 pt-2">
            <button type="button" onClick={handleClose} className="px-4 py-2 text-sm text-gray-600 hover:text-gray-800">
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 disabled:opacity-50"
            >
              {loading ? 'Creating…' : 'Create'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

/* ── Results Table ── */

function ResultsTable({ results }) {
  if (!results || !results.length) return null;

  const columns = Object.keys(results[0]);

  return (
    <div className="overflow-x-auto border border-gray-200 rounded-lg">
      <table className="min-w-full divide-y divide-gray-200 text-sm">
        <thead className="bg-gray-50">
          <tr>
            {columns.map((col) => (
              <th key={col} className="px-4 py-2 text-left font-medium text-gray-700">
                {col}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {results.map((row, i) => (
            <tr key={i} className={i % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
              {columns.map((col) => (
                <td key={col} className="px-4 py-2 text-gray-600 whitespace-nowrap">
                  {typeof row[col] === 'object' ? JSON.stringify(row[col]) : String(row[col] ?? '')}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

/* ── Query Builder ── */

function QueryBuilder({ databases }) {
  const [selectedDb, setSelectedDb] = useState('');
  const [queryText, setQueryText] = useState('');
  const { data: results, loading, error, execute: runQuery } = useApiCall(queryDatabase);

  const handleExecute = async () => {
    if (!selectedDb) return;
    let parsed = queryText.trim();
    // Try parsing as JSON; if it fails, send as raw string
    try { parsed = JSON.parse(parsed); } catch { /* send as-is */ }
    await runQuery(selectedDb, parsed);
  };

  return (
    <div className="bg-white rounded-lg shadow border border-gray-200 p-5 space-y-4">
      <h2 className="text-lg font-semibold text-gray-900">Query Builder</h2>

      <div className="grid grid-cols-1 sm:grid-cols-4 gap-3 items-end">
        <div className="sm:col-span-1">
          <label htmlFor="query-db" className="block text-sm font-medium text-gray-700 mb-1">Database</label>
          <select
            id="query-db"
            value={selectedDb}
            onChange={(e) => setSelectedDb(e.target.value)}
            className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
          >
            <option value="">Select…</option>
            {(databases || []).map((db) => (
              <option key={typeof db === 'string' ? db : db.name} value={typeof db === 'string' ? db : db.name}>
                {typeof db === 'string' ? db : db.name}
              </option>
            ))}
          </select>
        </div>

        <div className="sm:col-span-2">
          <label htmlFor="query-text" className="block text-sm font-medium text-gray-700 mb-1">Query (JSON or SQL)</label>
          <textarea
            id="query-text"
            value={queryText}
            onChange={(e) => setQueryText(e.target.value)}
            rows={3}
            placeholder='{"sql": "SELECT * FROM users LIMIT 10"}'
            className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-indigo-400"
          />
        </div>

        <div className="sm:col-span-1">
          <button
            onClick={handleExecute}
            disabled={!selectedDb || !queryText.trim() || loading}
            className="w-full px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 disabled:opacity-50"
          >
            {loading ? 'Running…' : 'Execute'}
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 rounded-md p-3 text-sm">
          {error}
        </div>
      )}

      {results && Array.isArray(results) && <ResultsTable results={results} />}
      {results && !Array.isArray(results) && (
        <pre className="bg-gray-50 border border-gray-200 rounded-md p-3 text-sm overflow-x-auto">
          {typeof results === 'string' ? results : JSON.stringify(results, null, 2)}
        </pre>
      )}
    </div>
  );
}

/* ── Database Page ── */

export default function Database() {
  const [createOpen, setCreateOpen] = useState(false);
  const [dropTarget, setDropTarget] = useState(null);

  const { data: databases, loading, error, execute: loadDatabases } = useApiCall(fetchDatabases);
  const { loading: creating, execute: doCreate } = useApiCall(createDatabase);
  const { loading: dropping, execute: doDrop } = useApiCall(dropDatabase);
  const { loading: settingUp, execute: doSetup } = useApiCall(setupDatabase);

  useEffect(() => {
    loadDatabases();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const handleCreate = async (name) => {
    try {
      await doCreate(name);
      setCreateOpen(false);
      loadDatabases();
    } catch { /* captured by useApiCall */ }
  };

  const handleDrop = async () => {
    if (!dropTarget) return;
    try {
      await doDrop(dropTarget);
      setDropTarget(null);
      loadDatabases();
    } catch { /* captured by useApiCall */ }
  };

  const handleSetup = async (name) => {
    try {
      await doSetup(name);
      loadDatabases();
    } catch { /* captured by useApiCall */ }
  };

  const dbName = (db) => (typeof db === 'string' ? db : db.name);

  return (
    <div className="max-w-7xl mx-auto px-4 py-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Databases</h1>
        <button
          onClick={() => setCreateOpen(true)}
          className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-400"
        >
          + New Database
        </button>
      </div>

      {/* Loading */}
      {loading && (
        <div className="flex justify-center py-12">
          <div className="h-8 w-8 border-4 border-indigo-400 border-t-transparent rounded-full animate-spin" />
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 rounded-md p-4">
          Failed to load databases: {error}
        </div>
      )}

      {/* Empty state */}
      {!loading && !error && databases && databases.length === 0 && (
        <div className="text-center py-16 text-gray-500">
          <p className="text-lg mb-2">No databases found</p>
          <p className="text-sm">Click "+ New Database" to create one.</p>
        </div>
      )}

      {/* Database list */}
      {!loading && databases && databases.length > 0 && (
        <div className="bg-white rounded-lg shadow border border-gray-200 overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200 text-sm">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left font-medium text-gray-700">Name</th>
                <th className="px-4 py-3 text-right font-medium text-gray-700">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {databases.map((db) => {
                const name = dbName(db);
                return (
                  <tr key={name} className="hover:bg-gray-50">
                    <td className="px-4 py-3 font-medium text-gray-900">{name}</td>
                    <td className="px-4 py-3 text-right space-x-2">
                      <button
                        onClick={() => handleSetup(name)}
                        disabled={settingUp}
                        className="px-3 py-1 text-xs font-medium text-indigo-700 bg-indigo-50 rounded hover:bg-indigo-100 disabled:opacity-50"
                      >
                        Setup
                      </button>
                      <button
                        onClick={() => setDropTarget(name)}
                        className="px-3 py-1 text-xs font-medium text-red-700 bg-red-50 rounded hover:bg-red-100"
                      >
                        Drop
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      {/* Query Builder */}
      <QueryBuilder databases={databases} />

      {/* Create modal */}
      <CreateModal
        open={createOpen}
        onClose={() => setCreateOpen(false)}
        onSubmit={handleCreate}
        loading={creating}
      />

      {/* Drop confirmation */}
      <ConfirmDialog
        open={!!dropTarget}
        title="Drop Database"
        message={`Are you sure you want to drop "${dropTarget}"? This action cannot be undone.`}
        onConfirm={handleDrop}
        onCancel={() => setDropTarget(null)}
        loading={dropping}
      />
    </div>
  );
}
