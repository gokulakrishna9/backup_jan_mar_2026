import { useState, useCallback, useRef, useEffect } from 'react';

/**
 * Composable hook: wraps any async API function with loading/error/data state.
 * Usage: const { data, loading, error, execute } = useApiCall(fetchApps);
 */
export function useApiCall(apiFn) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const execute = useCallback(async (...args) => {
    setLoading(true);
    setError(null);
    try {
      const result = await apiFn(...args);
      setData(result.data ?? result);
      return result;
    } catch (err) {
      const message = err.response?.data?.detail || err.message || 'Request failed';
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [apiFn]);

  return { data, loading, error, execute, setData };
}

/**
 * Composable hook: SSE streaming with auto-reconnect.
 * Usage: const { data, error, connected } = useStreamingApi('/api/agent/chat');
 */
export function useStreamingApi(url) {
  const [data, setData] = useState([]);
  const [error, setError] = useState(null);
  const [connected, setConnected] = useState(false);
  const sourceRef = useRef(null);

  const connect = useCallback(() => {
    if (sourceRef.current) sourceRef.current.close();

    const es = new EventSource(url);
    sourceRef.current = es;

    es.onopen = () => setConnected(true);
    es.onmessage = (event) => {
      try {
        const parsed = JSON.parse(event.data);
        setData((prev) => [...prev, parsed]);
      } catch {
        setData((prev) => [...prev, event.data]);
      }
    };
    es.onerror = () => {
      setConnected(false);
      setError('Stream disconnected');
      es.close();
    };
  }, [url]);

  const disconnect = useCallback(() => {
    if (sourceRef.current) {
      sourceRef.current.close();
      sourceRef.current = null;
    }
    setConnected(false);
  }, []);

  useEffect(() => () => disconnect(), [disconnect]);

  return { data, error, connected, connect, disconnect, setData };
}
