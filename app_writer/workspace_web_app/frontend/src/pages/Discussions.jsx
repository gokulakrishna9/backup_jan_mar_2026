import { useEffect, useState } from 'react';
import { useApiCall } from '../utils/api';
import { formatDate } from '../utils/format';
import {
  fetchSummary,
  fetchDiscussions,
  searchDiscussions,
  logDiscussion,
  createTask,
  recordDecision,
  startTask,
  completeTask,
} from '../api/discussions';

/* ── Status Badge ── */

function TaskStatusBadge({ status }) {
  const colors = {
    open: 'bg-yellow-100 text-yellow-800',
    in_progress: 'bg-blue-100 text-blue-800',
    completed: 'bg-green-100 text-green-800',
    deferred: 'bg-gray-100 text-gray-800',
  };
  const labels = {
    open: 'Open',
    in_progress: 'In Progress',
    completed: 'Completed',
    deferred: 'Deferred',
  };
  const cls = colors[(status || '').toLowerCase()] || 'bg-gray-100 text-gray-800';
  return (
    <span className={`inline-block px-2 py-0.5 rounded-full text-xs font-medium ${cls}`}>
      {labels[(status || '').toLowerCase()] || status || 'Unknown'}
    </span>
  );
}

/* ── Summary Cards ── */

function SummaryCards({ summary }) {
  if (!summary) return null;

  const openTasks = summary.open_tasks ?? summary.openTasks ?? [];
  const inProgressTasks = summary.in_progress_tasks ?? summary.inProgressTasks ?? [];
  const recentDecisions = summary.recent_decisions ?? summary.recentDecisions ?? [];
  const earmarked = summary.earmarked ?? [];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div className="bg-white rounded-lg shadow border border-gray-200 p-4">
        <h3 className="text-sm font-medium text-gray-500 mb-1">Open Tasks</h3>
        <p className="text-2xl font-bold text-yellow-600">{openTasks.length}</p>
      </div>
      <div className="bg-white rounded-lg shadow border border-gray-200 p-4">
        <h3 className="text-sm font-medium text-gray-500 mb-1">In Progress</h3>
        <p className="text-2xl font-bold text-blue-600">{inProgressTasks.length}</p>
      </div>
      <div className="bg-white rounded-lg shadow border border-gray-200 p-4">
        <h3 className="text-sm font-medium text-gray-500 mb-1">Recent Decisions</h3>
        <p className="text-2xl font-bold text-green-600">{recentDecisions.length}</p>
      </div>
      <div className="bg-white rounded-lg shadow border border-gray-200 p-4">
        <h3 className="text-sm font-medium text-gray-500 mb-1">Earmarked</h3>
        <p className="text-2xl font-bold text-purple-600">{earmarked.length}</p>
      </div>
    </div>
  );
}

/* ── Task List ── */

function TaskList({ tasks, title, onStart, onComplete, startingId, completingId }) {
  if (!tasks || tasks.length === 0) return null;

  return (
    <div className="bg-white rounded-lg shadow border border-gray-200 overflow-hidden">
      <div className="px-4 py-3 bg-gray-50 border-b border-gray-200">
        <h3 className="text-sm font-semibold text-gray-700">{title}</h3>
      </div>
      <ul className="divide-y divide-gray-100">
        {tasks.map((task) => (
          <li key={task.id} className="px-4 py-3 flex items-center justify-between gap-3">
            <div className="min-w-0 flex-1">
              <p className="text-sm font-medium text-gray-900 truncate">{task.title}</p>
              {task.description && (
                <p className="text-xs text-gray-500 truncate mt-0.5">{task.description}</p>
              )}
              {task.timestamp && (
                <p className="text-xs text-gray-400 mt-0.5">{formatDate(task.timestamp)}</p>
              )}
            </div>
            <div className="flex items-center gap-2 shrink-0">
              <TaskStatusBadge status={task.status} />
              {task.status === 'open' && onStart && (
                <button
                  onClick={() => onStart(task.id)}
                  disabled={startingId === task.id}
                  className="px-2 py-1 text-xs font-medium text-blue-700 bg-blue-50 rounded hover:bg-blue-100 disabled:opacity-50"
                >
                  {startingId === task.id ? 'Starting…' : 'Start'}
                </button>
              )}
              {(task.status === 'open' || task.status === 'in_progress') && onComplete && (
                <button
                  onClick={() => onComplete(task.id)}
                  disabled={completingId === task.id}
                  className="px-2 py-1 text-xs font-medium text-green-700 bg-green-50 rounded hover:bg-green-100 disabled:opacity-50"
                >
                  {completingId === task.id ? 'Completing…' : 'Complete'}
                </button>
              )}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

/* ── Log Discussion Form ── */

function LogDiscussionForm({ onSubmit, loading }) {
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    const trimmed = message.trim();
    if (!trimmed) return;
    onSubmit(trimmed);
    setMessage('');
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Log a discussion note…"
        className="flex-1 border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
      />
      <button
        type="submit"
        disabled={!message.trim() || loading}
        className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 disabled:opacity-50"
      >
        {loading ? 'Logging…' : 'Log'}
      </button>
    </form>
  );
}

/* ── Create Task Form ── */

function CreateTaskForm({ onSubmit, loading }) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    const trimmedTitle = title.trim();
    if (!trimmedTitle) return;
    onSubmit(trimmedTitle, description.trim());
    setTitle('');
    setDescription('');
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-2">
      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Task title"
        className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
      />
      <textarea
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="Description (optional)"
        rows={2}
        className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
      />
      <button
        type="submit"
        disabled={!title.trim() || loading}
        className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 disabled:opacity-50"
      >
        {loading ? 'Creating…' : 'Create Task'}
      </button>
    </form>
  );
}

/* ── Record Decision Form ── */

function RecordDecisionForm({ onSubmit, loading }) {
  const [title, setTitle] = useState('');
  const [rationale, setRationale] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    const trimmedTitle = title.trim();
    if (!trimmedTitle) return;
    onSubmit(trimmedTitle, rationale.trim());
    setTitle('');
    setRationale('');
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-2">
      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Decision title"
        className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
      />
      <textarea
        value={rationale}
        onChange={(e) => setRationale(e.target.value)}
        placeholder="Rationale (optional)"
        rows={2}
        className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
      />
      <button
        type="submit"
        disabled={!title.trim() || loading}
        className="px-4 py-2 text-sm font-medium text-white bg-green-600 rounded-md hover:bg-green-700 disabled:opacity-50"
      >
        {loading ? 'Recording…' : 'Record Decision'}
      </button>
    </form>
  );
}

/* ── Search Bar ── */

function SearchBar({ onSearch, loading }) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    const trimmed = query.trim();
    if (!trimmed) return;
    onSearch(trimmed);
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search discussions, tasks, decisions…"
        className="flex-1 border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
      />
      <button
        type="submit"
        disabled={!query.trim() || loading}
        className="px-4 py-2 text-sm font-medium text-white bg-gray-700 rounded-md hover:bg-gray-800 disabled:opacity-50"
      >
        {loading ? 'Searching…' : 'Search'}
      </button>
    </form>
  );
}

/* ── Search Results ── */

function SearchResults({ results }) {
  if (!results) return null;
  const items = Array.isArray(results) ? results : results.results ?? [];
  if (items.length === 0) {
    return <p className="text-sm text-gray-500 py-2">No results found.</p>;
  }

  return (
    <div className="bg-white rounded-lg shadow border border-gray-200 overflow-hidden">
      <ul className="divide-y divide-gray-100">
        {items.map((item, i) => (
          <li key={item.id ?? i} className="px-4 py-3">
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs font-medium px-2 py-0.5 rounded bg-gray-100 text-gray-600">
                {item.type || 'item'}
              </span>
              {item.status && <TaskStatusBadge status={item.status} />}
            </div>
            <p className="text-sm font-medium text-gray-900">{item.title || item.message || item.text}</p>
            {item.description && (
              <p className="text-xs text-gray-500 mt-0.5">{item.description}</p>
            )}
            {item.rationale && (
              <p className="text-xs text-gray-500 mt-0.5">{item.rationale}</p>
            )}
            {item.timestamp && (
              <p className="text-xs text-gray-400 mt-0.5">{formatDate(item.timestamp)}</p>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

/* ── Discussions Page ── */

export default function Discussions() {
  const [activeTab, setActiveTab] = useState('summary');
  const [startingId, setStartingId] = useState(null);
  const [completingId, setCompletingId] = useState(null);

  const { data: summary, loading: summaryLoading, error: summaryError, execute: loadSummary } = useApiCall(fetchSummary);
  const { data: discussions, loading: listLoading, execute: loadDiscussions } = useApiCall(fetchDiscussions);
  const { data: searchResults, loading: searchLoading, execute: doSearch } = useApiCall(searchDiscussions);
  const { loading: logging, execute: doLog } = useApiCall(logDiscussion);
  const { loading: creatingTask, execute: doCreateTask } = useApiCall(createTask);
  const { loading: recording, execute: doRecordDecision } = useApiCall(recordDecision);
  const { execute: doStart } = useApiCall(startTask);
  const { execute: doComplete } = useApiCall(completeTask);

  useEffect(() => {
    loadSummary();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const refresh = () => {
    loadSummary();
    if (activeTab === 'all') loadDiscussions();
  };

  const handleLog = async (message) => {
    try {
      await doLog(message);
      refresh();
    } catch { /* captured by useApiCall */ }
  };

  const handleCreateTask = async (title, description) => {
    try {
      await doCreateTask(title, description);
      refresh();
    } catch { /* captured by useApiCall */ }
  };

  const handleRecordDecision = async (title, rationale) => {
    try {
      await doRecordDecision(title, rationale);
      refresh();
    } catch { /* captured by useApiCall */ }
  };

  const handleStart = async (id) => {
    setStartingId(id);
    try {
      await doStart(id);
      refresh();
    } catch { /* captured by useApiCall */ }
    setStartingId(null);
  };

  const handleComplete = async (id) => {
    setCompletingId(id);
    try {
      await doComplete(id);
      refresh();
    } catch { /* captured by useApiCall */ }
    setCompletingId(null);
  };

  const handleSearch = async (query) => {
    try {
      await doSearch(query);
    } catch { /* captured by useApiCall */ }
  };

  const handleTabChange = (tab) => {
    setActiveTab(tab);
    if (tab === 'all' && !discussions) loadDiscussions();
  };

  const openTasks = summary?.open_tasks ?? summary?.openTasks ?? [];
  const inProgressTasks = summary?.in_progress_tasks ?? summary?.inProgressTasks ?? [];

  const tabs = [
    { key: 'summary', label: 'Summary' },
    { key: 'log', label: 'Log Discussion' },
    { key: 'task', label: 'New Task' },
    { key: 'decision', label: 'Record Decision' },
    { key: 'search', label: 'Search' },
    { key: 'all', label: 'All Items' },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 py-6 space-y-6">
      {/* Header */}
      <h1 className="text-2xl font-bold text-gray-900">Discussions</h1>

      {/* Tabs */}
      <div className="flex flex-wrap gap-1 border-b border-gray-200 pb-px">
        {tabs.map(({ key, label }) => (
          <button
            key={key}
            onClick={() => handleTabChange(key)}
            className={`px-4 py-2 text-sm font-medium rounded-t transition-colors ${
              activeTab === key
                ? 'bg-white border border-b-white border-gray-200 text-indigo-600 -mb-px'
                : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            {label}
          </button>
        ))}
      </div>

      {/* Summary Tab */}
      {activeTab === 'summary' && (
        <div className="space-y-6">
          {summaryLoading && (
            <div className="flex justify-center py-12">
              <div className="h-8 w-8 border-4 border-indigo-400 border-t-transparent rounded-full animate-spin" />
            </div>
          )}

          {summaryError && (
            <div className="bg-red-50 border border-red-200 text-red-700 rounded-md p-4">
              Failed to load summary: {summaryError}
            </div>
          )}

          {!summaryLoading && summary && (
            <>
              <SummaryCards summary={summary} />

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <TaskList
                  tasks={openTasks}
                  title="Open Tasks"
                  onStart={handleStart}
                  onComplete={handleComplete}
                  startingId={startingId}
                  completingId={completingId}
                />
                <TaskList
                  tasks={inProgressTasks}
                  title="In Progress"
                  onStart={handleStart}
                  onComplete={handleComplete}
                  startingId={startingId}
                  completingId={completingId}
                />
              </div>
            </>
          )}
        </div>
      )}

      {/* Log Discussion Tab */}
      {activeTab === 'log' && (
        <div className="bg-white rounded-lg shadow border border-gray-200 p-5 space-y-4">
          <h2 className="text-lg font-semibold text-gray-900">Log Discussion</h2>
          <LogDiscussionForm onSubmit={handleLog} loading={logging} />
        </div>
      )}

      {/* New Task Tab */}
      {activeTab === 'task' && (
        <div className="bg-white rounded-lg shadow border border-gray-200 p-5 space-y-4">
          <h2 className="text-lg font-semibold text-gray-900">Create Task</h2>
          <CreateTaskForm onSubmit={handleCreateTask} loading={creatingTask} />
        </div>
      )}

      {/* Record Decision Tab */}
      {activeTab === 'decision' && (
        <div className="bg-white rounded-lg shadow border border-gray-200 p-5 space-y-4">
          <h2 className="text-lg font-semibold text-gray-900">Record Decision</h2>
          <RecordDecisionForm onSubmit={handleRecordDecision} loading={recording} />
        </div>
      )}

      {/* Search Tab */}
      {activeTab === 'search' && (
        <div className="space-y-4">
          <div className="bg-white rounded-lg shadow border border-gray-200 p-5 space-y-4">
            <h2 className="text-lg font-semibold text-gray-900">Search</h2>
            <SearchBar onSearch={handleSearch} loading={searchLoading} />
          </div>
          <SearchResults results={searchResults} />
        </div>
      )}

      {/* All Items Tab */}
      {activeTab === 'all' && (
        <div className="space-y-4">
          {listLoading && (
            <div className="flex justify-center py-12">
              <div className="h-8 w-8 border-4 border-indigo-400 border-t-transparent rounded-full animate-spin" />
            </div>
          )}
          {discussions && <SearchResults results={discussions} />}
        </div>
      )}
    </div>
  );
}
