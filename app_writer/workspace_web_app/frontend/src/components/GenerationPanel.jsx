import { useState, useRef, useEffect, useCallback } from 'react';
import { useApiCall } from '../utils/api';
import {
  generateFull,
  generateIncremental,
  generateSQLOnly,
  generateReact,
  cancelJob,
} from '../api/generation';
import useWebSocket from '../hooks/useWebSocket';

/* ── Generation type config ── */

const GEN_TYPES = [
  { key: 'full', label: 'Full', description: 'SQL + Java + React', fn: generateFull },
  { key: 'incremental', label: 'Incremental', description: 'Skip SQL', fn: generateIncremental },
  { key: 'sql', label: 'SQL Only', description: 'Skip Java', fn: generateSQLOnly },
  { key: 'react', label: 'React', description: 'Frontend only', fn: generateReact },
];

/* ── Log Viewer (terminal-like) ── */

function LogViewer({ lines }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [lines.length]);

  return (
    <div className="bg-gray-900 text-green-400 font-mono text-xs rounded-lg p-3 h-64 overflow-y-auto mt-3">
      {lines.length === 0 ? (
        <span className="text-gray-500 italic">Waiting for output…</span>
      ) : (
        lines.map((line, i) => (
          <div key={i} className="whitespace-pre-wrap leading-5">
            <span className="text-gray-600 select-none mr-2">{String(i + 1).padStart(3, ' ')}</span>
            {typeof line === 'string' ? line : line.line ?? line.message ?? JSON.stringify(line)}
          </div>
        ))
      )}
      <div ref={bottomRef} />
    </div>
  );
}

/* ── Completion Summary ── */

function CompletionSummary({ result }) {
  if (!result) return null;

  const files = result.files ?? result.generatedFiles ?? [];
  const status = result.status ?? (result.success ? 'completed' : 'failed');
  const isSuccess = status === 'completed' || result.success;

  return (
    <div className={`mt-3 rounded-lg p-3 text-sm ${isSuccess ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'}`}>
      <div className="flex items-center gap-2 mb-1">
        <span className={`text-lg ${isSuccess ? 'text-green-600' : 'text-red-600'}`}>
          {isSuccess ? '✓' : '✗'}
        </span>
        <span className={`font-semibold ${isSuccess ? 'text-green-800' : 'text-red-800'}`}>
          Generation {status}
        </span>
      </div>
      {files.length > 0 && (
        <p className="text-gray-600 ml-7">{files.length} file{files.length !== 1 ? 's' : ''} generated</p>
      )}
      {result.error && (
        <p className="text-red-700 ml-7 mt-1">{result.error}</p>
      )}
    </div>
  );
}


/* ── Main GenerationPanel Component ── */

export default function GenerationPanel({ appName }) {
  const [jobId, setJobId] = useState(null);
  const [running, setRunning] = useState(false);
  const [completionResult, setCompletionResult] = useState(null);
  const [logLines, setLogLines] = useState([]);
  const [activeType, setActiveType] = useState(null);

  // WebSocket URL for streaming job output
  const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const wsUrl = jobId
    ? `${wsProtocol}//${window.location.host}/ws/generate/${appName}/jobs/${jobId}/stream`
    : null;

  const { messages, connected, connect, disconnect, setMessages } = useWebSocket(wsUrl);

  // Append WebSocket messages to log lines
  useEffect(() => {
    if (messages.length === 0) return;
    const latest = messages[messages.length - 1];

    // Check for completion event
    if (latest?.type === 'completion' || latest?.type === 'job_complete' || latest?.status === 'completed' || latest?.status === 'failed') {
      setCompletionResult(latest);
      setRunning(false);
      disconnect();
      return;
    }

    // Append log line
    const line = latest?.line ?? latest?.message ?? (typeof latest === 'string' ? latest : null);
    if (line !== null) {
      setLogLines((prev) => [...prev, latest]);
    }
  }, [messages.length]); // eslint-disable-line react-hooks/exhaustive-deps

  // Start a generation job
  const startGeneration = useCallback(async (genType) => {
    // Reset state
    setLogLines([]);
    setCompletionResult(null);
    setMessages([]);
    setActiveType(genType.key);

    try {
      setRunning(true);
      const result = await genType.fn(appName);
      const id = result?.data?.jobId ?? result?.data?.job_id ?? result?.jobId ?? result?.job_id;

      if (id) {
        setJobId(id);
        // WebSocket will auto-connect once jobId is set and URL updates
      } else {
        // Synchronous result (no streaming job)
        setCompletionResult(result?.data ?? result);
        setRunning(false);
      }
    } catch (err) {
      const message = err.response?.data?.detail || err.message || 'Generation failed';
      setCompletionResult({ success: false, status: 'failed', error: message });
      setRunning(false);
    }
  }, [appName, setMessages]);

  // Connect WebSocket when jobId changes
  useEffect(() => {
    if (jobId && wsUrl) {
      connect();
    }
    return () => disconnect();
  }, [jobId]); // eslint-disable-line react-hooks/exhaustive-deps

  // Cancel the running job
  const handleCancel = useCallback(async () => {
    if (!jobId) return;
    try {
      await cancelJob(appName, jobId);
      setCompletionResult({ success: false, status: 'cancelled', error: 'Job cancelled by user' });
      setRunning(false);
      disconnect();
    } catch {
      // Best-effort cancel
    }
  }, [appName, jobId, disconnect]);

  return (
    <div className="mt-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-3">Code Generation</h3>

      {/* Generation buttons */}
      <div className="flex flex-wrap gap-2">
        {GEN_TYPES.map((gt) => (
          <button
            key={gt.key}
            onClick={() => startGeneration(gt)}
            disabled={running}
            className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
              running && activeType === gt.key
                ? 'bg-indigo-100 text-indigo-700 border border-indigo-300'
                : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50 hover:border-gray-400'
            } disabled:opacity-50 disabled:cursor-not-allowed`}
            title={gt.description}
          >
            {running && activeType === gt.key && (
              <span className="inline-block w-3 h-3 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin mr-2 align-middle" />
            )}
            {gt.label}
          </button>
        ))}

        {/* Cancel button */}
        {running && (
          <button
            onClick={handleCancel}
            className="px-4 py-2 text-sm font-medium text-red-700 bg-red-50 border border-red-200 rounded-lg hover:bg-red-100 transition-colors"
          >
            Cancel
          </button>
        )}
      </div>

      {/* WebSocket connection indicator */}
      {running && (
        <div className="flex items-center gap-2 mt-2 text-xs text-gray-500">
          <span className={`w-2 h-2 rounded-full ${connected ? 'bg-green-400' : 'bg-yellow-400 animate-pulse'}`} />
          {connected ? 'Connected — streaming output' : 'Connecting…'}
        </div>
      )}

      {/* Log viewer */}
      {(running || logLines.length > 0) && <LogViewer lines={logLines} />}

      {/* Completion summary */}
      <CompletionSummary result={completionResult} />
    </div>
  );
}
