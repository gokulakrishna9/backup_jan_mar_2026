import { useState } from 'react';

/* ── Inline Status Badge ── */

function DirtyBadge({ dirty }) {
  return dirty ? (
    <span className="ml-2 inline-block px-2 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">Dirty</span>
  ) : (
    <span className="ml-2 inline-block px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">Clean</span>
  );
}

/* ── Add Field Form ── */

function AddFieldForm({ onAdd, loading }) {
  const [name, setName] = useState('');
  const [type, setType] = useState('String');
  const [nullable, setNullable] = useState(false);

  const FIELD_TYPES = ['String', 'Integer', 'Long', 'Double', 'Boolean', 'LocalDate', 'LocalDateTime', 'BigDecimal'];

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!name.trim()) return;
    onAdd({ name: name.trim(), type, nullable });
    setName('');
    setType('String');
    setNullable(false);
  };

  return (
    <form onSubmit={handleSubmit} className="flex items-end gap-2 mt-3">
      <div className="flex-1">
        <label className="block text-xs text-gray-500 mb-1">Field Name</label>
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="fieldName"
          className="w-full border border-gray-300 rounded px-2 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
        />
      </div>
      <div>
        <label className="block text-xs text-gray-500 mb-1">Type</label>
        <select
          value={type}
          onChange={(e) => setType(e.target.value)}
          className="border border-gray-300 rounded px-2 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
        >
          {FIELD_TYPES.map((t) => <option key={t} value={t}>{t}</option>)}
        </select>
      </div>
      <label className="flex items-center gap-1 text-sm">
        <input type="checkbox" checked={nullable} onChange={(e) => setNullable(e.target.checked)} />
        Nullable
      </label>
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

/* ── Modify Field Modal ── */

function ModifyFieldModal({ field, onSave, onClose, loading }) {
  const [type, setType] = useState(field?.type || 'String');
  const [nullable, setNullable] = useState(field?.nullable || false);

  const FIELD_TYPES = ['String', 'Integer', 'Long', 'Double', 'Boolean', 'LocalDate', 'LocalDateTime', 'BigDecimal'];

  if (!field) return null;

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(field.name, { type, nullable });
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40" onClick={onClose}>
      <div className="bg-white rounded-lg shadow-xl w-full max-w-sm mx-4 p-5" onClick={(e) => e.stopPropagation()} role="dialog" aria-modal="true">
        <h3 className="text-lg font-semibold mb-3">Modify Field: {field.name}</h3>
        <form onSubmit={handleSubmit} className="space-y-3">
          <div>
            <label className="block text-sm text-gray-600 mb-1">Type</label>
            <select value={type} onChange={(e) => setType(e.target.value)} className="w-full border border-gray-300 rounded px-2 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400">
              {FIELD_TYPES.map((t) => <option key={t} value={t}>{t}</option>)}
            </select>
          </div>
          <label className="flex items-center gap-2 text-sm">
            <input type="checkbox" checked={nullable} onChange={(e) => setNullable(e.target.checked)} />
            Nullable
          </label>
          <div className="flex justify-end gap-2 pt-2">
            <button type="button" onClick={onClose} className="px-3 py-1.5 text-sm text-gray-600 hover:text-gray-800">Cancel</button>
            <button type="submit" disabled={loading} className="px-3 py-1.5 text-sm font-medium text-white bg-indigo-600 rounded hover:bg-indigo-700 disabled:opacity-50">
              {loading ? 'Saving…' : 'Save'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

/* ── Simple List Section (Relationships / Endpoints / Queries) ── */

function ListSection({ title, items, nameKey, onAdd, onRemove, addLabel, addFields, loading }) {
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({});

  const handleAdd = (e) => {
    e.preventDefault();
    const name = formData[nameKey || 'name']?.trim();
    if (!name) return;
    onAdd(formData);
    setFormData({});
    setShowForm(false);
  };

  return (
    <div className="mt-4">
      <div className="flex items-center justify-between mb-2">
        <h4 className="text-sm font-semibold text-gray-700">{title}</h4>
        <button
          onClick={() => setShowForm(!showForm)}
          className="text-xs text-indigo-600 hover:text-indigo-800"
        >
          {showForm ? 'Cancel' : `+ ${addLabel || 'Add'}`}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleAdd} className="flex flex-wrap items-end gap-2 mb-2 p-2 bg-gray-50 rounded">
          {addFields.map((f) => (
            <div key={f.key} className="flex-1 min-w-[120px]">
              <label className="block text-xs text-gray-500 mb-0.5">{f.label}</label>
              <input
                value={formData[f.key] || ''}
                onChange={(e) => setFormData({ ...formData, [f.key]: e.target.value })}
                placeholder={f.placeholder || f.label}
                className="w-full border border-gray-300 rounded px-2 py-1 text-xs focus:outline-none focus:ring-1 focus:ring-indigo-400"
              />
            </div>
          ))}
          <button type="submit" disabled={loading} className="px-2 py-1 text-xs font-medium text-white bg-indigo-600 rounded hover:bg-indigo-700 disabled:opacity-50">
            Add
          </button>
        </form>
      )}

      {(!items || items.length === 0) ? (
        <p className="text-xs text-gray-400 italic">None</p>
      ) : (
        <ul className="space-y-1">
          {items.map((item, i) => {
            const displayName = typeof item === 'string' ? item : item[nameKey || 'name'] || item.name || JSON.stringify(item);
            return (
              <li key={i} className="flex items-center justify-between text-xs bg-gray-50 rounded px-2 py-1">
                <span className="text-gray-700 truncate">{displayName}</span>
                <button
                  onClick={() => onRemove(typeof item === 'string' ? item : item[nameKey || 'name'] || item.name)}
                  className="text-red-500 hover:text-red-700 ml-2 shrink-0"
                  title="Remove"
                >
                  ✕
                </button>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}

/* ── Main EntityEditor Component ── */

export default function EntityEditor({
  entity,
  appName,
  onAddField,
  onRemoveField,
  onModifyField,
  onAddEndpoint,
  onRemoveEndpoint,
  onAddQuery,
  onRemoveQuery,
  onAddRelationship,
  onRemoveRelationship,
  loading,
}) {
  const [editingField, setEditingField] = useState(null);

  if (!entity) {
    return (
      <div className="flex items-center justify-center h-64 text-gray-400">
        Select an entity from the sidebar to edit its fields.
      </div>
    );
  }

  const fields = entity.fields || [];
  const relationships = entity.relationships || [];
  const endpoints = entity.customEndpoints || entity.endpoints || [];
  const queries = entity.customQueries || entity.queries || [];
  const isDirty = entity.dirty ?? entity.isDirty ?? false;

  const handleModifySave = (fieldName, updates) => {
    onModifyField(fieldName, updates);
    setEditingField(null);
  };

  return (
    <div>
      {/* Entity header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center">
          <h2 className="text-xl font-bold text-gray-900">{entity.name}</h2>
          <DirtyBadge dirty={isDirty} />
        </div>
        <span className="text-sm text-gray-500">{fields.length} field{fields.length !== 1 ? 's' : ''}</span>
      </div>

      {/* Fields table */}
      <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50">
            <tr>
              <th className="text-left px-4 py-2 font-medium text-gray-600">Name</th>
              <th className="text-left px-4 py-2 font-medium text-gray-600">Type</th>
              <th className="text-left px-4 py-2 font-medium text-gray-600">Nullable</th>
              <th className="text-right px-4 py-2 font-medium text-gray-600">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {fields.length === 0 ? (
              <tr><td colSpan={4} className="px-4 py-6 text-center text-gray-400 italic">No fields yet</td></tr>
            ) : (
              fields.map((f) => (
                <tr key={f.name} className="hover:bg-gray-50">
                  <td className="px-4 py-2 font-mono text-gray-800">{f.name}</td>
                  <td className="px-4 py-2 text-gray-600">{f.type}</td>
                  <td className="px-4 py-2 text-gray-600">{f.nullable ? 'Yes' : 'No'}</td>
                  <td className="px-4 py-2 text-right space-x-2">
                    <button
                      onClick={() => setEditingField(f)}
                      className="text-indigo-600 hover:text-indigo-800 text-xs"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => onRemoveField(f.name)}
                      className="text-red-500 hover:text-red-700 text-xs"
                    >
                      Remove
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Add field form */}
      <AddFieldForm onAdd={onAddField} loading={loading} />

      {/* Relationships section */}
      <ListSection
        title="Relationships"
        items={relationships}
        nameKey="name"
        onAdd={onAddRelationship}
        onRemove={onRemoveRelationship}
        addLabel="Relationship"
        addFields={[
          { key: 'name', label: 'Name', placeholder: 'userOrders' },
          { key: 'type', label: 'Type', placeholder: 'OneToMany' },
          { key: 'targetEntity', label: 'Target Entity', placeholder: 'Order' },
        ]}
        loading={loading}
      />

      {/* Custom Endpoints section */}
      <ListSection
        title="Custom Endpoints"
        items={endpoints}
        nameKey="name"
        onAdd={onAddEndpoint}
        onRemove={onRemoveEndpoint}
        addLabel="Endpoint"
        addFields={[
          { key: 'name', label: 'Name', placeholder: 'findActive' },
          { key: 'method', label: 'Method', placeholder: 'GET' },
          { key: 'path', label: 'Path', placeholder: '/active' },
        ]}
        loading={loading}
      />

      {/* Custom Queries section */}
      <ListSection
        title="Custom Queries"
        items={queries}
        nameKey="name"
        onAdd={onAddQuery}
        onRemove={onRemoveQuery}
        addLabel="Query"
        addFields={[
          { key: 'name', label: 'Name', placeholder: 'findByStatus' },
          { key: 'query', label: 'Query', placeholder: 'SELECT * FROM ...' },
        ]}
        loading={loading}
      />

      {/* Modify field modal */}
      <ModifyFieldModal
        field={editingField}
        onSave={handleModifySave}
        onClose={() => setEditingField(null)}
        loading={loading}
      />
    </div>
  );
}
