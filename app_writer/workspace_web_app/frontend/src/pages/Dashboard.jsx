import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useApiCall } from '../utils/api';
import { fetchApps, scaffoldApp } from '../api/apps';
import { formatDate, formatStatus } from '../utils/format';
import useAppStore from '../store/appStore';

/* ── Status Badge ── */

function StatusBadge({ status }) {
  const colors = {
    clean: 'bg-green-100 text-green-800',
    dirty: 'bg-yellow-100 text-yellow-800',
    running: 'bg-blue-100 text-blue-800',
    failed: 'bg-red-100 text-red-800',
  };
  const cls = colors[(status || '').toLowerCase()] || 'bg-gray-100 text-gray-800';
  return (
    <span className={`inline-block px-2 py-0.5 rounded-full text-xs font-medium ${cls}`}>
      {formatStatus(status)}
    </span>
  );
}

/* ── App Card ── */

function AppCard({ app, onClick }) {
  const entityCount = app.entities?.length ?? app.entityCount ?? 0;
  return (
    <button
      type="button"
      onClick={onClick}
      className="w-full text-left bg-white rounded-lg shadow hover:shadow-md transition-shadow p-5 border border-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-400"
    >
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-lg font-semibold text-gray-900 truncate">{app.name}</h3>
        <StatusBadge status={app.status} />
      </div>
      <div className="text-sm text-gray-600 space-y-1">
        <p>{entityCount} {entityCount === 1 ? 'entity' : 'entities'}</p>
        {app.lastGeneration && (
          <p className="text-xs text-gray-400">Last generated: {formatDate(app.lastGeneration)}</p>
        )}
      </div>
    </button>
  );
}

/* ── Scaffold Modal ── */

function ScaffoldModal({ open, onClose, onSubmit, loading }) {
  const [name, setName] = useState('');
  const [entitiesText, setEntitiesText] = useState('');
  const [error, setError] = useState('');

  if (!open) return null;

  const handleSubmit = (e) => {
    e.preventDefault();
    const trimmed = name.trim();
    if (!trimmed) {
      setError('App name is required');
      return;
    }
    const entities = entitiesText
      .split(',')
      .map((s) => s.trim())
      .filter(Boolean);
    onSubmit({ name: trimmed, entities });
  };

  const handleClose = () => {
    setName('');
    setEntitiesText('');
    setError('');
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40" onClick={handleClose}>
      <div
        className="bg-white rounded-lg shadow-xl w-full max-w-md mx-4 p-6"
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
        aria-label="New Application"
      >
        <h2 className="text-xl font-bold text-gray-900 mb-4">New Application</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="app-name" className="block text-sm font-medium text-gray-700 mb-1">
              App Name <span className="text-red-500">*</span>
            </label>
            <input
              id="app-name"
              type="text"
              value={name}
              onChange={(e) => { setName(e.target.value); setError(''); }}
              placeholder="my_app"
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
              autoFocus
            />
            {error && <p className="text-red-500 text-xs mt-1">{error}</p>}
          </div>
          <div>
            <label htmlFor="app-entities" className="block text-sm font-medium text-gray-700 mb-1">
              Initial Entities <span className="text-gray-400">(optional, comma-separated)</span>
            </label>
            <input
              id="app-entities"
              type="text"
              value={entitiesText}
              onChange={(e) => setEntitiesText(e.target.value)}
              placeholder="User, Product, Order"
              className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
            />
          </div>
          <div className="flex justify-end gap-3 pt-2">
            <button
              type="button"
              onClick={handleClose}
              className="px-4 py-2 text-sm text-gray-600 hover:text-gray-800"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 disabled:opacity-50"
            >
              {loading ? 'Creating…' : 'Create App'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

/* ── Dashboard Page ── */

export default function Dashboard() {
  const navigate = useNavigate();
  const setApps = useAppStore((s) => s.setApps);
  const [modalOpen, setModalOpen] = useState(false);

  const { data: apps, loading, error, execute: loadApps } = useApiCall(fetchApps);
  const { loading: scaffolding, execute: doScaffold } = useApiCall(scaffoldApp);

  useEffect(() => {
    loadApps();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // Sync to global store when apps load
  useEffect(() => {
    if (apps) setApps(apps);
  }, [apps, setApps]);

  const handleScaffold = async (payload) => {
    try {
      await doScaffold(payload);
      setModalOpen(false);
      loadApps();
    } catch {
      // error is captured by useApiCall
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Applications</h1>
        <button
          onClick={() => setModalOpen(true)}
          className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-400"
        >
          + New App
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
        <div className="bg-red-50 border border-red-200 text-red-700 rounded-md p-4 mb-4">
          Failed to load applications: {error}
        </div>
      )}

      {/* Empty state */}
      {!loading && !error && apps && apps.length === 0 && (
        <div className="text-center py-16 text-gray-500">
          <p className="text-lg mb-2">No applications yet</p>
          <p className="text-sm">Click "New App" to scaffold your first application.</p>
        </div>
      )}

      {/* App grid */}
      {!loading && apps && apps.length > 0 && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {apps.map((app) => (
            <AppCard
              key={app.name}
              app={app}
              onClick={() => navigate(`/apps/${app.name}`)}
            />
          ))}
        </div>
      )}

      {/* Scaffold modal */}
      <ScaffoldModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        onSubmit={handleScaffold}
        loading={scaffolding}
      />
    </div>
  );
}
