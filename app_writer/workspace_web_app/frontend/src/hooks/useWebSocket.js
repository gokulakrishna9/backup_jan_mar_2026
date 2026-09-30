import { useState, useRef, useCallback, useEffect } from 'react';

/**
 * WebSocket hook with auto-reconnect.
 * Usage: const { messages, connected, send, connect, disconnect } = useWebSocket(url);
 */
export default function useWebSocket(url, { autoConnect = false, reconnectDelay = 3000 } = {}) {
  const [messages, setMessages] = useState([]);
  const [connected, setConnected] = useState(false);
  const wsRef = useRef(null);
  const reconnectTimer = useRef(null);
  const urlRef = useRef(url);
  urlRef.current = url;

  const clearReconnect = () => {
    if (reconnectTimer.current) {
      clearTimeout(reconnectTimer.current);
      reconnectTimer.current = null;
    }
  };

  const connect = useCallback(() => {
    clearReconnect();
    if (wsRef.current) wsRef.current.close();

    const ws = new WebSocket(urlRef.current);
    wsRef.current = ws;

    ws.onopen = () => setConnected(true);

    ws.onmessage = (event) => {
      try {
        const parsed = JSON.parse(event.data);
        setMessages((prev) => [...prev, parsed]);
      } catch {
        setMessages((prev) => [...prev, event.data]);
      }
    };

    ws.onclose = () => {
      setConnected(false);
      reconnectTimer.current = setTimeout(connect, reconnectDelay);
    };

    ws.onerror = () => ws.close();
  }, [reconnectDelay]);

  const disconnect = useCallback(() => {
    clearReconnect();
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
    setConnected(false);
  }, []);

  const send = useCallback((data) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(typeof data === 'string' ? data : JSON.stringify(data));
    }
  }, []);

  useEffect(() => {
    if (autoConnect) connect();
    return () => disconnect();
  }, [autoConnect, connect, disconnect]);

  return { messages, connected, send, connect, disconnect, setMessages };
}
