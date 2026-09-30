import { useState, useRef, useEffect, useCallback } from 'react';
import useAppStore from '../store/appStore';
import { sendChatMessage, getHistory, clearHistory } from '../api/agent';

/* ── Session ID (stable per browser tab) ── */

const SESSION_ID = crypto.randomUUID?.() || Math.random().toString(36).slice(2);

/* ── SSE event type constants ── */

const EVENT_TYPES = {
  THINKING: 'thinking',
  TOOL_CALL: 'tool_call',
  TOOL_RESULT: 'tool_result',
  MESSAGE: 'message',
  ERROR: 'error',
};

/* ── Conversation cache key ── */

function contextKey(appName) {
  return appName || '_global';
}

/* ── Tool Invocation Card ── */

function ToolCard({ event }) {
  const [expanded, setExpanded] = useState(false);
  const isCall = event.type === EVENT_TYPES.TOOL_CALL;
  const title = isCall
    ? `🔧 ${event.data?.tool || event.data?.name || 'Tool call'}`
    : `📋 Result: ${event.data?.tool || event.data?.name || 'tool'}`;

  return (
    <div className="my-1 border border-gray-200 rounded-lg overflow-hidden text-xs">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center justify-between px-3 py-2 bg-gray-50 hover:bg-gray-100 transition-colors text-left"
      >
        <span className="font-medium text-gray-700 truncate">{title}</span>
        <svg
          className={`w-3.5 h-3.5 text-gray-400 transition-transform flex-shrink-0 ${expanded ? 'rotate-180' : ''}`}
          fill="none" stroke="currentColor" viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>
      {expanded && (
        <pre className="px-3 py-2 bg-white text-gray-600 overflow-x-auto whitespace-pre-wrap max-h-40 overflow-y-auto">
          {typeof event.data === 'string'
            ? event.data
            : JSON.stringify(event.data?.input ?? event.data?.output ?? event.data, null, 2)}
        </pre>
      )}
    </div>
  );
}

/* ── Single Message Bubble ── */

function MessageBubble({ msg }) {
  if (msg.role === 'system') {
    return (
      <div className="flex justify-center mb-3">
        <span className="text-xs text-gray-400 italic bg-gray-50 px-3 py-1 rounded-full">
          {msg.content}
        </span>
      </div>
    );
  }

  if (msg.role === 'user') {
    return (
      <div className="flex justify-end mb-3">
        <div className="max-w-[85%] bg-indigo-600 text-white rounded-2xl rounded-br-md px-4 py-2 text-sm whitespace-pre-wrap">
          {msg.content}
        </div>
      </div>
    );
  }

  // Agent message — may contain inline tool events
  return (
    <div className="flex justify-start mb-3">
      <div className="max-w-[85%]">
        {msg.events?.map((evt, i) => {
          if (evt.type === EVENT_TYPES.TOOL_CALL || evt.type === EVENT_TYPES.TOOL_RESULT) {
            return <ToolCard key={i} event={evt} />;
          }
          if (evt.type === EVENT_TYPES.THINKING) {
            return (
              <div key={i} className="text-xs text-gray-400 italic mb-1">
                {evt.data?.content || evt.data || 'Thinking…'}
              </div>
            );
          }
          return null;
        })}
        {msg.content && (
          <div className="bg-gray-100 text-gray-900 rounded-2xl rounded-bl-md px-4 py-2 text-sm whitespace-pre-wrap">
            {msg.content}
          </div>
        )}
      </div>
    </div>
  );
}

/* ── Streaming indicator ── */

function StreamingIndicator() {
  return (
    <div className="flex justify-start mb-3">
      <div className="bg-gray-100 rounded-2xl rounded-bl-md px-4 py-3">
        <div className="flex gap-1">
          <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
          <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
          <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
        </div>
      </div>
    </div>
  );
}

/* ── Model Switcher (placeholder) ── */

const PLACEHOLDER_MODELS = [
  { id: 'gpt-4', label: 'GPT-4', provider: 'OpenAI' },
  { id: 'claude-3-sonnet', label: 'Claude 3 Sonnet', provider: 'Anthropic' },
  { id: 'gemini/gemini-pro', label: 'Gemini Pro', provider: 'Google' },
  { id: 'ollama/llama3', label: 'Llama 3 (local)', provider: 'Ollama' },
];

function ModelSwitcher({ activeModel, onSwitch }) {
  const [open, setOpen] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    const handler = (e) => { if (ref.current && !ref.current.contains(e.target)) setOpen(false); };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  const current = PLACEHOLDER_MODELS.find((m) => m.id === activeModel) || PLACEHOLDER_MODELS[0];

  return (
    <div ref={ref} className="relative">
      <button
        onClick={() => setOpen(!open)}
        className="flex items-center gap-1.5 px-2 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
        title="Switch model"
      >
        <span className="w-1.5 h-1.5 rounded-full bg-green-400 flex-shrink-0" />
        <span className="text-gray-700 truncate max-w-[120px]">{current.label}</span>
        <svg className={`w-3 h-3 text-gray-400 transition-transform ${open ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>
      {open && (
        <div className="absolute right-0 top-full mt-1 w-56 bg-white border border-gray-200 rounded-lg shadow-lg z-50 py-1">
          {PLACEHOLDER_MODELS.map((m) => (
            <button
              key={m.id}
              onClick={() => { onSwitch(m.id); setOpen(false); }}
              className={`w-full text-left px-3 py-2 text-xs hover:bg-gray-50 flex items-center justify-between ${
                m.id === activeModel ? 'bg-indigo-50 text-indigo-700' : 'text-gray-700'
              }`}
            >
              <span>{m.label}</span>
              <span className="text-gray-400">{m.provider}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

/* ── Chat Panel Header ── */

function PanelHeader({ appName, activeModel, onModelSwitch, onClose, onClear, clearing }) {
  return (
    <div className="border-b border-gray-200 bg-white">
      {/* Top row: close, title, clear */}
      <div className="flex items-center justify-between px-4 py-3">
        <div className="flex items-center gap-2 min-w-0">
          <button
            onClick={onClose}
            className="p-1 rounded hover:bg-gray-100 transition-colors flex-shrink-0"
            aria-label="Close chat panel"
          >
            <svg className="w-5 h-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
          <div className="min-w-0">
            <h3 className="text-sm font-semibold text-gray-900 truncate">Agent Chat</h3>
            <p className="text-xs text-gray-500 truncate">
              {appName ? `App: ${appName}` : 'Global context'}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <ModelSwitcher activeModel={activeModel} onSwitch={onModelSwitch} />
          <button
            onClick={onClear}
            disabled={clearing}
            className="text-xs text-gray-400 hover:text-red-500 transition-colors disabled:opacity-50"
            title="Clear history"
          >
            {clearing ? '…' : 'Clear'}
          </button>
        </div>
      </div>
    </div>
  );
}

/* ── Message Input ── */

function MessageInput({ onSend, disabled }) {
  const [text, setText] = useState('');
  const inputRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    const trimmed = text.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setText('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  useEffect(() => {
    if (!disabled) inputRef.current?.focus();
  }, [disabled]);

  return (
    <form onSubmit={handleSubmit} className="border-t border-gray-200 p-3 bg-white">
      <div className="flex gap-2">
        <textarea
          ref={inputRef}
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={disabled}
          placeholder="Ask the agent…"
          rows={1}
          className="flex-1 resize-none rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent disabled:bg-gray-50 disabled:text-gray-400"
        />
        <button
          type="submit"
          disabled={disabled || !text.trim()}
          className="px-3 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex-shrink-0"
          aria-label="Send message"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
          </svg>
        </button>
      </div>
    </form>
  );
}

/* ── SSE stream reader ── */

async function readSSEStream(response, onEvent) {
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const raw = line.slice(6).trim();
          if (raw === '[DONE]') return;
          try {
            onEvent(JSON.parse(raw));
          } catch {
            // non-JSON data line — ignore
          }
        }
      }
    }
  } finally {
    reader.releaseLock();
  }
}

/* ══════════════════════════════════════════════
   Main ChatPanel Component
   ══════════════════════════════════════════════ */

export default function ChatPanel() {
  const selectedApp = useAppStore((s) => s.selectedApp);
  const appName = selectedApp?.name || selectedApp || '';

  // Panel open/close
  const [open, setOpen] = useState(false);

  // Per-app conversation cache: { [contextKey]: Message[] }
  const conversationsRef = useRef({});

  // Current conversation messages
  const [messages, setMessages] = useState([]);
  const [streaming, setStreaming] = useState(false);
  const [clearing, setClearing] = useState(false);
  const [activeModel, setActiveModel] = useState('gpt-4');

  const messagesEndRef = useRef(null);
  const prevAppRef = useRef(appName);

  // Scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, streaming]);

  // Save current conversation before switching
  const saveCurrentConversation = useCallback(() => {
    const key = contextKey(prevAppRef.current);
    conversationsRef.current[key] = messages;
  }, [messages]);

  // Load conversation for an app (from cache or server)
  const loadConversation = useCallback(async (name) => {
    const key = contextKey(name);

    // Check cache first
    if (conversationsRef.current[key]) {
      setMessages(conversationsRef.current[key]);
      return;
    }

    // Fetch from server
    try {
      const history = await getHistory(name);
      const loaded = Array.isArray(history?.messages) ? history.messages : [];
      conversationsRef.current[key] = loaded;
      setMessages(loaded);
    } catch {
      // No history — start fresh
      conversationsRef.current[key] = [];
      setMessages([]);
    }
  }, []);

  // When selectedApp changes, switch conversation context
  useEffect(() => {
    if (prevAppRef.current !== appName) {
      saveCurrentConversation();
      prevAppRef.current = appName;
      loadConversation(appName);
    }
  }, [appName, saveCurrentConversation, loadConversation]);

  // Load initial conversation when panel first opens
  useEffect(() => {
    if (open && messages.length === 0 && !conversationsRef.current[contextKey(appName)]) {
      loadConversation(appName);
    }
  }, [open, appName, messages.length, loadConversation]);

  // Send message and stream response via SSE
  const handleSend = useCallback(async (text) => {
    const userMsg = { role: 'user', content: text };
    setMessages((prev) => [...prev, userMsg]);
    setStreaming(true);

    // Prepare agent message accumulator
    let agentContent = '';
    const agentEvents = [];

    try {
      const response = await sendChatMessage(appName, text, SESSION_ID);

      await readSSEStream(response, (event) => {
        switch (event.type) {
          case EVENT_TYPES.MESSAGE:
            agentContent += event.data?.content || event.data || '';
            // Update in real-time
            setMessages((prev) => {
              const updated = [...prev];
              const lastIdx = updated.length - 1;
              if (lastIdx >= 0 && updated[lastIdx].role === 'assistant' && updated[lastIdx]._streaming) {
                updated[lastIdx] = { role: 'assistant', content: agentContent, events: [...agentEvents], _streaming: true };
              } else {
                updated.push({ role: 'assistant', content: agentContent, events: [...agentEvents], _streaming: true });
              }
              return updated;
            });
            break;

          case EVENT_TYPES.TOOL_CALL:
          case EVENT_TYPES.TOOL_RESULT:
            agentEvents.push(event);
            setMessages((prev) => {
              const updated = [...prev];
              const lastIdx = updated.length - 1;
              if (lastIdx >= 0 && updated[lastIdx].role === 'assistant' && updated[lastIdx]._streaming) {
                updated[lastIdx] = { role: 'assistant', content: agentContent, events: [...agentEvents], _streaming: true };
              } else {
                updated.push({ role: 'assistant', content: agentContent, events: [...agentEvents], _streaming: true });
              }
              return updated;
            });
            break;

          case EVENT_TYPES.THINKING:
            agentEvents.push(event);
            setMessages((prev) => {
              const updated = [...prev];
              const lastIdx = updated.length - 1;
              if (lastIdx >= 0 && updated[lastIdx].role === 'assistant' && updated[lastIdx]._streaming) {
                updated[lastIdx] = { role: 'assistant', content: agentContent, events: [...agentEvents], _streaming: true };
              } else {
                updated.push({ role: 'assistant', content: agentContent, events: [...agentEvents], _streaming: true });
              }
              return updated;
            });
            break;

          case EVENT_TYPES.ERROR:
            agentContent += `\n⚠️ ${event.data?.message || event.data || 'Error'}`;
            break;

          default:
            break;
        }
      });

      // Finalize: remove _streaming flag
      setMessages((prev) => {
        const updated = [...prev];
        const lastIdx = updated.length - 1;
        if (lastIdx >= 0 && updated[lastIdx]._streaming) {
          const { _streaming, ...final } = updated[lastIdx];
          updated[lastIdx] = { ...final, content: agentContent || '(No response)', events: agentEvents };
        }
        // Save to cache
        conversationsRef.current[contextKey(appName)] = updated;
        return updated;
      });
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: `⚠️ ${err.message || 'Failed to get response'}` },
      ]);
    } finally {
      setStreaming(false);
    }
  }, [appName]);

  // Clear conversation
  const handleClear = useCallback(async () => {
    setClearing(true);
    try {
      await clearHistory(appName);
    } catch {
      // Clear locally even if server fails
    }
    const key = contextKey(appName);
    conversationsRef.current[key] = [];
    setMessages([]);
    setClearing(false);
  }, [appName]);

  // Model switch (placeholder — adds system message)
  const handleModelSwitch = useCallback((modelId) => {
    const model = PLACEHOLDER_MODELS.find((m) => m.id === modelId);
    setActiveModel(modelId);
    setMessages((prev) => [
      ...prev,
      { role: 'system', content: `Switched to ${model?.label || modelId}` },
    ]);
  }, []);

  return (
    <>
      {/* ── Floating toggle button (always visible) ── */}
      {!open && (
        <button
          onClick={() => setOpen(true)}
          className="fixed bottom-6 right-6 z-50 w-14 h-14 bg-indigo-600 hover:bg-indigo-700 text-white rounded-full shadow-lg flex items-center justify-center transition-all hover:scale-105"
          aria-label="Open chat panel"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
        </button>
      )}

      {/* ── Slide-out panel ── */}
      {open && (
        <>
          {/* Backdrop */}
          <div
            className="fixed inset-0 bg-black/20 z-40 transition-opacity"
            onClick={() => setOpen(false)}
          />

          {/* Panel */}
          <div className="fixed top-0 right-0 h-full w-full sm:w-[420px] bg-white shadow-2xl z-50 flex flex-col animate-slide-in-right">
            <PanelHeader
              appName={appName}
              activeModel={activeModel}
              onModelSwitch={handleModelSwitch}
              onClose={() => setOpen(false)}
              onClear={handleClear}
              clearing={clearing}
            />

            {/* Message list */}
            <div className="flex-1 overflow-y-auto px-4 py-4">
              {messages.length === 0 && !streaming && (
                <div className="flex flex-col items-center justify-center h-full text-gray-400 text-sm">
                  <svg className="w-12 h-12 mb-3 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                  </svg>
                  <p>No messages yet</p>
                  <p className="text-xs mt-1">
                    {appName ? `Chatting about ${appName}` : 'Ask anything about your workspace'}
                  </p>
                </div>
              )}
              {messages.map((msg, i) => (
                <MessageBubble key={i} msg={msg} />
              ))}
              {streaming && !messages[messages.length - 1]?._streaming && <StreamingIndicator />}
              <div ref={messagesEndRef} />
            </div>

            <MessageInput onSend={handleSend} disabled={streaming} />
          </div>
        </>
      )}
    </>
  );
}
