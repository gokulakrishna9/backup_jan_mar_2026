import { useState } from 'react';
import { useApiCall } from '../utils/api';
import { formatDate } from '../utils/format';
import {
  listRepos,
  repoInfo,
  repoTree,
  readFile as readGitHubFile,
  summarize,
} from '../api/github';

/* ── Repository Card ── */

function RepoCard({ repo, onSelect }) {
  return (
    <button
      type="button"
      onClick={() => onSelect(repo)}
      className="bg-white rounded-lg shadow border border-gray-200 p-4 text-left hover:border-indigo-400 hover:shadow-md transition-all w-full"
    >
      <h3 className="text-sm font-semibold text-indigo-700 truncate">{repo.name}</h3>
      {repo.description && (
        <p className="text-xs text-gray-500 mt-1 line-clamp-2">{repo.description}</p>
      )}
      <div className="flex items-center gap-3 mt-3 text-xs text-gray-400">
        {repo.language && (
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-indigo-400 inline-block" />
            {repo.language}
          </span>
        )}
        <span>⭐ {repo.stars ?? repo.stargazers_count ?? 0}</span>
        {(repo.updated_at || repo.last_updated) && (
          <span className="ml-auto">{formatDate(repo.updated_at || repo.last_updated)}</span>
        )}
      </div>
    </button>
  );
}

/* ── File Tree Node ── */

function TreeNode({ node, depth, onFileClick, expandedPaths, onToggle }) {
  const isDir = node.type === 'tree' || node.type === 'dir';
  const isExpanded = expandedPaths.has(node.path);
  const indent = depth * 16;

  return (
    <>
      <button
        type="button"
        onClick={() => (isDir ? onToggle(node.path) : onFileClick(node.path))}
        className={`w-full text-left px-3 py-1.5 text-sm hover:bg-gray-100 flex items-center gap-2 ${
          !isDir ? 'text-indigo-700' : 'text-gray-700 font-medium'
        }`}
        style={{ paddingLeft: `${12 + indent}px` }}
      >
        {isDir ? (
          <span className="text-gray-400 w-4 text-center">{isExpanded ? '▾' : '▸'}</span>
        ) : (
          <span className="text-gray-300 w-4 text-center">📄</span>
        )}
        <span className="truncate">{node.path.split('/').pop()}</span>
      </button>
      {isDir && isExpanded && node.children && (
        node.children.map((child) => (
          <TreeNode
            key={child.path}
            node={child}
            depth={depth + 1}
            onFileClick={onFileClick}
            expandedPaths={expandedPaths}
            onToggle={onToggle}
          />
        ))
      )}
    </>
  );
}

/* ── File Tree Panel ── */

function FileTreePanel({ tree, onFileClick }) {
  const [expandedPaths, setExpandedPaths] = useState(new Set());

  const togglePath = (path) => {
    setExpandedPaths((prev) => {
      const next = new Set(prev);
      if (next.has(path)) next.delete(path);
      else next.add(path);
      return next;
    });
  };

  // Normalize tree: could be an array or { tree: [...] }
  const nodes = Array.isArray(tree) ? tree : tree?.tree ?? [];

  if (nodes.length === 0) {
    return <p className="text-sm text-gray-500 p-4">No files found.</p>;
  }

  // Build nested structure from flat list if needed
  const nested = buildNestedTree(nodes);

  return (
    <div className="bg-white rounded-lg shadow border border-gray-200 overflow-hidden">
      <div className="px-4 py-3 bg-gray-50 border-b border-gray-200">
        <h3 className="text-sm font-semibold text-gray-700">File Tree</h3>
      </div>
      <div className="max-h-96 overflow-y-auto divide-y divide-gray-50">
        {nested.map((node) => (
          <TreeNode
            key={node.path}
            node={node}
            depth={0}
            onFileClick={onFileClick}
            expandedPaths={expandedPaths}
            onToggle={togglePath}
          />
        ))}
      </div>
    </div>
  );
}

/**
 * Build a nested tree from a flat list of { path, type } entries.
 * If entries already have children, return as-is.
 */
function buildNestedTree(nodes) {
  // If already nested (has children), return directly
  if (nodes.length > 0 && nodes[0].children) return nodes;

  const root = [];
  const map = {};

  // Sort so directories come before files, then alphabetically
  const sorted = [...nodes].sort((a, b) => {
    const aDir = a.type === 'tree' || a.type === 'dir' ? 0 : 1;
    const bDir = b.type === 'tree' || b.type === 'dir' ? 0 : 1;
    if (aDir !== bDir) return aDir - bDir;
    return a.path.localeCompare(b.path);
  });

  for (const node of sorted) {
    const parts = node.path.split('/');
    const entry = { ...node, children: node.type === 'tree' || node.type === 'dir' ? [] : undefined };
    map[node.path] = entry;

    if (parts.length === 1) {
      root.push(entry);
    } else {
      const parentPath = parts.slice(0, -1).join('/');
      if (map[parentPath]) {
        map[parentPath].children = map[parentPath].children || [];
        map[parentPath].children.push(entry);
      } else {
        root.push(entry);
      }
    }
  }

  return root;
}

/* ── File Viewer ── */

function FileViewer({ filePath, content, loading, error }) {
  if (!filePath) return null;

  return (
    <div className="bg-white rounded-lg shadow border border-gray-200 overflow-hidden">
      <div className="px-4 py-3 bg-gray-50 border-b border-gray-200 flex items-center justify-between">
        <h3 className="text-sm font-semibold text-gray-700 truncate">{filePath}</h3>
      </div>
      <div className="p-4 overflow-auto max-h-[32rem]">
        {loading && (
          <div className="flex justify-center py-8">
            <div className="h-6 w-6 border-4 border-indigo-400 border-t-transparent rounded-full animate-spin" />
          </div>
        )}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 rounded-md p-3 text-sm">
            {error}
          </div>
        )}
        {!loading && !error && content != null && (
          <pre className="text-xs leading-relaxed overflow-x-auto">
            <code>{typeof content === 'string' ? content : JSON.stringify(content, null, 2)}</code>
          </pre>
        )}
      </div>
    </div>
  );
}

/* ── Summary Viewer ── */

function SummaryViewer({ summaryData, loading, error }) {
  if (!summaryData && !loading && !error) return null;

  return (
    <div className="bg-white rounded-lg shadow border border-gray-200 overflow-hidden">
      <div className="px-4 py-3 bg-gray-50 border-b border-gray-200">
        <h3 className="text-sm font-semibold text-gray-700">Repository Summary</h3>
      </div>
      <div className="p-4">
        {loading && (
          <div className="flex justify-center py-8">
            <div className="h-6 w-6 border-4 border-indigo-400 border-t-transparent rounded-full animate-spin" />
          </div>
        )}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 rounded-md p-3 text-sm">
            {error}
          </div>
        )}
        {!loading && !error && summaryData && (
          <pre className="text-sm whitespace-pre-wrap text-gray-800 leading-relaxed">
            {typeof summaryData === 'string' ? summaryData : summaryData.summary ?? JSON.stringify(summaryData, null, 2)}
          </pre>
        )}
      </div>
    </div>
  );
}

/* ── GitHub Browser Page ── */

export default function GitHubBrowser() {
  const [username, setUsername] = useState('');
  const [selectedRepo, setSelectedRepo] = useState(null);
  const [viewingFile, setViewingFile] = useState(null);

  const { data: repos, loading: reposLoading, error: reposError, execute: doListRepos } = useApiCall(listRepos);
  const { data: tree, loading: treeLoading, error: treeError, execute: doRepoTree } = useApiCall(repoTree);
  const { data: fileContent, loading: fileLoading, error: fileError, execute: doReadFile, setData: setFileContent } = useApiCall(readGitHubFile);
  const { data: summaryData, loading: summaryLoading, error: summaryError, execute: doSummarize } = useApiCall(summarize);

  const handleSearch = (e) => {
    e.preventDefault();
    const trimmed = username.trim();
    if (!trimmed) return;
    setSelectedRepo(null);
    setViewingFile(null);
    setFileContent(null);
    doListRepos(trimmed);
  };

  const handleSelectRepo = (repo) => {
    const owner = repo.owner?.login || repo.owner || username.trim();
    const repoName = repo.name;
    setSelectedRepo(repo);
    setViewingFile(null);
    setFileContent(null);
    doRepoTree(owner, repoName);
  };

  const handleFileClick = (path) => {
    if (!selectedRepo) return;
    const owner = selectedRepo.owner?.login || selectedRepo.owner || username.trim();
    setViewingFile(path);
    doReadFile(owner, selectedRepo.name, path);
  };

  const handleSummarize = () => {
    const trimmed = username.trim();
    if (!trimmed) return;
    doSummarize(trimmed);
  };

  const handleBack = () => {
    setSelectedRepo(null);
    setViewingFile(null);
    setFileContent(null);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-6 space-y-6">
      {/* Header */}
      <h1 className="text-2xl font-bold text-gray-900">GitHub Browser</h1>

      {/* Search Bar */}
      <form onSubmit={handleSearch} className="flex gap-2">
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="GitHub username or organization…"
          className="flex-1 border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
        />
        <button
          type="submit"
          disabled={!username.trim() || reposLoading}
          className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-md hover:bg-indigo-700 disabled:opacity-50"
        >
          {reposLoading ? 'Searching…' : 'Search'}
        </button>
        {username.trim() && (
          <button
            type="button"
            onClick={handleSummarize}
            disabled={summaryLoading}
            className="px-4 py-2 text-sm font-medium text-white bg-green-600 rounded-md hover:bg-green-700 disabled:opacity-50"
          >
            {summaryLoading ? 'Generating…' : 'Generate Summary'}
          </button>
        )}
      </form>

      {/* Error */}
      {reposError && (
        <div className="bg-red-50 border border-red-200 text-red-700 rounded-md p-4 text-sm">
          Failed to load repositories: {reposError}
        </div>
      )}

      {/* Loading */}
      {reposLoading && (
        <div className="flex justify-center py-12">
          <div className="h-8 w-8 border-4 border-indigo-400 border-t-transparent rounded-full animate-spin" />
        </div>
      )}

      {/* Summary */}
      <SummaryViewer summaryData={summaryData} loading={summaryLoading} error={summaryError} />

      {/* Repository Grid (when no repo selected) */}
      {!reposLoading && repos && !selectedRepo && (
        <div>
          <h2 className="text-lg font-semibold text-gray-800 mb-3">
            Repositories ({(Array.isArray(repos) ? repos : repos.repos ?? []).length})
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {(Array.isArray(repos) ? repos : repos.repos ?? []).map((repo) => (
              <RepoCard key={repo.name || repo.full_name} repo={repo} onSelect={handleSelectRepo} />
            ))}
          </div>
          {(Array.isArray(repos) ? repos : repos.repos ?? []).length === 0 && (
            <p className="text-sm text-gray-500">No public repositories found.</p>
          )}
        </div>
      )}

      {/* Repo Detail View (file tree + file viewer) */}
      {selectedRepo && (
        <div className="space-y-4">
          {/* Breadcrumb / Back */}
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={handleBack}
              className="text-sm text-indigo-600 hover:text-indigo-800 font-medium"
            >
              ← Back to repositories
            </button>
            <span className="text-gray-400">/</span>
            <span className="text-sm font-semibold text-gray-800">{selectedRepo.name}</span>
            {viewingFile && (
              <>
                <span className="text-gray-400">/</span>
                <span className="text-sm text-gray-600 truncate">{viewingFile}</span>
              </>
            )}
          </div>

          {/* Repo metadata */}
          {selectedRepo.description && (
            <p className="text-sm text-gray-600">{selectedRepo.description}</p>
          )}

          {/* Tree + File side by side on large screens */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
            <div className="lg:col-span-1">
              {treeLoading && (
                <div className="flex justify-center py-8">
                  <div className="h-6 w-6 border-4 border-indigo-400 border-t-transparent rounded-full animate-spin" />
                </div>
              )}
              {treeError && (
                <div className="bg-red-50 border border-red-200 text-red-700 rounded-md p-3 text-sm">
                  {treeError}
                </div>
              )}
              {!treeLoading && tree && (
                <FileTreePanel tree={tree} onFileClick={handleFileClick} />
              )}
            </div>
            <div className="lg:col-span-2">
              <FileViewer
                filePath={viewingFile}
                content={fileContent}
                loading={fileLoading}
                error={fileError}
              />
              {!viewingFile && !fileLoading && (
                <div className="bg-white rounded-lg shadow border border-gray-200 p-8 text-center text-sm text-gray-400">
                  Select a file from the tree to view its contents.
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
