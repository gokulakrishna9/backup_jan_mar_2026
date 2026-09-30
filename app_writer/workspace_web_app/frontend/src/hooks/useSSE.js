import { useState, useRef, useCallback, useEffect } from 'react';

/**
 * SSE hook for EventSource connections.
 * Usage: const { events, connected, connect, disconnect } = useSSE('/api/agent/stream');
 */
export default function useSSE(url) {
  const [events, setEvents] = useState([]);
  const [connected, setConnected] = useState(false);
  const [error, setError] = useState(null);
  const sourceRef = useRef(null);

  const connect = useCallback(() => {
    if (sourceRef.current) sourceRef.current.close();

    const es = new EventSource(url);
    sourceRef.current = es;

    es.onopen = () => {
      setConnected(true);
      setError(null);
    };

    es.onmessage = (event) => {
      try {
        const parsed = JSON.parse(event.data);
        setEvents((prev) => [...prev, parsed]);
      } catch {
        setEvents((prev) => [...prev, event.data]);
      }
    };

    es.onerror = () => {
      setConnected(false);
      setError('SSE connection lost');
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

  return { events, connected, error, connect, disconnect, setEvents };
}
