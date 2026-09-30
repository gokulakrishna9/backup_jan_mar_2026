"""Templates for AI React components.

Most templates use Python string.Template ($variable substitution) to avoid
conflicts between Jinja2 {{ }} delimiters and JavaScript object literals.
The AI_NAV_ENTRIES template uses Jinja2 for its loop construct.
"""

# ── AiChatPanel ─────────────────────────────────────────────────────────────

AI_CHAT_PANEL = r"""import React, { useState, useRef, useEffect, useCallback } from 'react';
import { InputTextarea } from 'primereact/inputtextarea';
import { Button } from 'primereact/button';
import { ProgressSpinner } from 'primereact/progressspinner';
import aiApiService from '../services/aiApiService';

const POSITION_STYLES = {
  sidebar: { position: 'fixed', right: 0, top: 0, width: '360px', height: '100vh', borderLeft: '1px solid #dee2e6' },
  floating: { position: 'fixed', bottom: '1.5rem', right: '1.5rem', width: '380px', height: '520px', borderRadius: '12px', boxShadow: '0 8px 32px rgba(0,0,0,0.15)' },
  fullpage: { width: '100%', height: '100%', maxWidth: '800px', margin: '0 auto' },
};

const AiChatPanel = ({ position = '$position', accentColor = '$accentColor', bubbleStyle = '$bubbleStyle', loadingAnimation = '$loadingAnimation', streamingEnabled = $streamingEnabled, defaultAssistant = '$defaultAssistant' }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => { messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages]);

  const sendMessage = useCallback(async () => {
    if (!input.trim() || loading) return;
    const userMsg = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      if (streamingEnabled) {
        let assistantContent = '';
        setMessages(prev => [...prev, { role: 'assistant', content: '' }]);
        await aiApiService.chatStream(
          { message: input, sessionId, assistant: defaultAssistant },
          (chunk) => {
            assistantContent += chunk;
            setMessages(prev => {
              const updated = [...prev];
              updated[updated.length - 1] = { role: 'assistant', content: assistantContent };
              return updated;
            });
          }
        );
      } else {
        const res = await aiApiService.chat({ message: input, sessionId, assistant: defaultAssistant });
        if (res.sessionId) setSessionId(res.sessionId);
        setMessages(prev => [...prev, { role: 'assistant', content: res.response }]);
      }
    } catch (err) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Error: ' + (err.message || 'Request failed') }]);
    } finally {
      setLoading(false);
    }
  }, [input, loading, sessionId, streamingEnabled, defaultAssistant]);

  const bubbleRadius = bubbleStyle === 'rounded' ? '16px' : '4px';

  const renderLoading = () => {
    if (loadingAnimation === 'spinner') return <ProgressSpinner style={{ width: '24px', height: '24px' }} />;
    if (loadingAnimation === 'pulse') return <span className="pi pi-ellipsis-h" style={{ animation: 'pulse 1.5s infinite' }} />;
    return <span>...</span>;
  };

  return (
    <div style={{ ...POSITION_STYLES[position], display: 'flex', flexDirection: 'column', background: '#fff', zIndex: 1000 }}>
      <div style={{ padding: '0.75rem 1rem', background: accentColor, color: '#fff', fontWeight: 600 }}>AI Chat</div>
      <div style={{ flex: 1, overflowY: 'auto', padding: '1rem' }}>
        {messages.map((msg, i) => (
          <div key={i} style={{ display: 'flex', justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start', marginBottom: '0.5rem' }}>
            <div style={{ maxWidth: '80%', padding: '0.5rem 0.75rem', borderRadius: bubbleRadius, background: msg.role === 'user' ? accentColor : '#f1f3f5', color: msg.role === 'user' ? '#fff' : '#333', whiteSpace: 'pre-wrap' }}>
              {msg.content}
            </div>
          </div>
        ))}
        {loading && <div style={{ textAlign: 'center', padding: '0.5rem' }}>{renderLoading()}</div>}
        <div ref={messagesEndRef} />
      </div>
      <div style={{ display: 'flex', gap: '0.5rem', padding: '0.75rem', borderTop: '1px solid #dee2e6' }}>
        <InputTextarea value={input} onChange={e => setInput(e.target.value)} onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); } }} rows={1} autoResize style={{ flex: 1 }} placeholder="Type a message..." />
        <Button icon="pi pi-send" onClick={sendMessage} disabled={loading || !input.trim()} style={{ background: accentColor, border: 'none' }} />
      </div>
    </div>
  );
};

export default AiChatPanel;
"""

# ── SmartSearchBar ──────────────────────────────────────────────────────────

SMART_SEARCH_BAR = r"""import React, { useState, useCallback } from 'react';
import { InputText } from 'primereact/inputtext';
import { Button } from 'primereact/button';
import aiApiService from '../../services/aiApiService';

const $componentName = ({ entityName = '$entityName', searchableFields = $searchableFields, onResults }) => {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);

  const handleSearch = useCallback(async () => {
    if (!query.trim()) return;
    setLoading(true);
    try {
      const res = await aiApiService.entitySearch('$entityNameLower', { query });
      setResults(res);
      if (onResults) onResults(res);
    } catch (err) {
      console.error('AI search failed:', err);
    } finally {
      setLoading(false);
    }
  }, [query, onResults]);

  return (
    <div className="flex align-items-center gap-2 mb-3">
      <span className="p-input-icon-left flex-1">
        <i className="pi pi-search" />
        <InputText value={query} onChange={e => setQuery(e.target.value)} onKeyDown={e => e.key === 'Enter' && handleSearch()} placeholder="AI search $entityName..." className="w-full" />
      </span>
      <Button icon="pi pi-bolt" label="AI Search" onClick={handleSearch} loading={loading} />
    </div>
  );
};

export default $componentName;
"""

# ── ContentGenerationButton ─────────────────────────────────────────────────

CONTENT_GENERATION_BUTTON = r"""import React, { useState, useCallback } from 'react';
import { Button } from 'primereact/button';
import { Dialog } from 'primereact/dialog';
import { InputTextarea } from 'primereact/inputtextarea';
import aiApiService from '../../services/aiApiService';

const $componentName = ({ entityName = '$entityName', fieldName = '$fieldName', buttonLabel = '$buttonLabel', onGenerated }) => {
  const [visible, setVisible] = useState(false);
  const [context, setContext] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState('');

  const handleGenerate = useCallback(async () => {
    setLoading(true);
    try {
      const res = await aiApiService.entityGenerate('$entityNameLower', { fieldName, context });
      setResult(res.response || res);
      if (onGenerated) onGenerated(res.response || res);
    } catch (err) {
      setResult('Error: ' + (err.message || 'Generation failed'));
    } finally {
      setLoading(false);
    }
  }, [context, fieldName, onGenerated]);

  return (
    <>
      <Button icon="pi pi-sparkles" label={buttonLabel} onClick={() => setVisible(true)} className="p-button-outlined p-button-sm" />
      <Dialog header={'Generate ' + fieldName} visible={visible} onHide={() => setVisible(false)} style={{ width: '500px' }}>
        <InputTextarea value={context} onChange={e => setContext(e.target.value)} rows={3} placeholder="Provide context..." className="w-full mb-3" />
        <Button label="Generate" icon="pi pi-sparkles" onClick={handleGenerate} loading={loading} className="mb-3" />
        {result && <div className="p-3 surface-100 border-round white-space-pre-wrap">{result}</div>}
      </Dialog>
    </>
  );
};

export default $componentName;
"""

# ── AiSuggestionWidget ──────────────────────────────────────────────────────

AI_SUGGESTION_WIDGET = r"""import React, { useState, useEffect, useCallback } from 'react';
import { Chip } from 'primereact/chip';
import aiApiService from '../../services/aiApiService';

const $componentName = ({ entityName = '$entityName', fieldName = '$fieldName', triggerOn = '$triggerOn', currentValue = '', onAccept }) => {
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchSuggestions = useCallback(async (value) => {
    if (!value || value.length < 3) { setSuggestions([]); return; }
    setLoading(true);
    try {
      const res = await aiApiService.entitySuggest('$entityNameLower', { fieldName, context: value });
      setSuggestions(Array.isArray(res) ? res : []);
    } catch (err) {
      console.error('AI suggestion failed:', err);
    } finally {
      setLoading(false);
    }
  }, [fieldName]);

  useEffect(() => {
    if (triggerOn === 'blur') return;
    const timer = setTimeout(() => fetchSuggestions(currentValue), 500);
    return () => clearTimeout(timer);
  }, [currentValue, triggerOn, fetchSuggestions]);

  const handleBlur = useCallback(() => {
    if (triggerOn === 'blur') fetchSuggestions(currentValue);
  }, [triggerOn, currentValue, fetchSuggestions]);

  return (
    <div onBlur={handleBlur}>
      {loading && <small className="text-500">Loading suggestions...</small>}
      {suggestions.length > 0 && (
        <div className="flex flex-wrap gap-1 mt-1">
          {suggestions.map((s, i) => (
            <Chip key={i} label={typeof s === 'string' ? s : s.text} onClick={() => onAccept && onAccept(s)} className="cursor-pointer" />
          ))}
        </div>
      )}
    </div>
  );
};

export default $componentName;
"""

# ── Standalone Pages ────────────────────────────────────────────────────────

STANDALONE_CHAT_PAGE = r"""import React, { useState, useRef, useEffect, useCallback } from 'react';
import { InputTextarea } from 'primereact/inputtextarea';
import { Button } from 'primereact/button';
import { Card } from 'primereact/card';
import aiApiService from '../services/aiApiService';

const $componentName = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const endRef = useRef(null);

  useEffect(() => { endRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages]);

  const send = useCallback(async () => {
    if (!input.trim() || loading) return;
    setMessages(prev => [...prev, { role: 'user', content: input }]);
    setInput('');
    setLoading(true);
    try {
      const res = await aiApiService.standaloneChat('$operationName', { message: input, sessionId });
      if (res.sessionId) setSessionId(res.sessionId);
      setMessages(prev => [...prev, { role: 'assistant', content: res.response }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Error: ' + (err.message || 'Failed') }]);
    } finally {
      setLoading(false);
    }
  }, [input, loading, sessionId]);

  return (
    <div className="p-4" style={{ maxWidth: '800px', margin: '0 auto' }}>
      <h2>$pageTitle</h2>
      <Card style={{ minHeight: '400px', display: 'flex', flexDirection: 'column' }}>
        <div style={{ flex: 1, overflowY: 'auto', marginBottom: '1rem' }}>
          {messages.map((m, i) => (
            <div key={i} className={'mb-2 p-2 border-round ' + (m.role === 'user' ? 'bg-primary-reverse text-right' : 'surface-100')}>
              <small className="text-500">{m.role}</small>
              <div className="white-space-pre-wrap">{m.content}</div>
            </div>
          ))}
          <div ref={endRef} />
        </div>
        <div className="flex gap-2">
          <InputTextarea value={input} onChange={e => setInput(e.target.value)} onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); } }} rows={1} autoResize className="flex-1" placeholder="Type a message..." />
          <Button icon="pi pi-send" onClick={send} disabled={loading || !input.trim()} />
        </div>
      </Card>
    </div>
  );
};

export default $componentName;
"""

STANDALONE_GENERATOR_PAGE = r"""import React, { useState, useCallback } from 'react';
import { InputTextarea } from 'primereact/inputtextarea';
import { Button } from 'primereact/button';
import { Card } from 'primereact/card';
import aiApiService from '../services/aiApiService';

const $componentName = () => {
  const [prompt, setPrompt] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const generate = useCallback(async () => {
    if (!prompt.trim() || loading) return;
    setLoading(true);
    try {
      const res = await aiApiService.standaloneGenerate('$operationName', { prompt });
      setResult(res.response || JSON.stringify(res, null, 2));
    } catch (err) {
      setResult('Error: ' + (err.message || 'Generation failed'));
    } finally {
      setLoading(false);
    }
  }, [prompt, loading]);

  return (
    <div className="p-4" style={{ maxWidth: '800px', margin: '0 auto' }}>
      <h2>$pageTitle</h2>
      <Card>
        <InputTextarea value={prompt} onChange={e => setPrompt(e.target.value)} rows={4} className="w-full mb-3" placeholder="Enter your prompt..." />
        <Button label="Generate" icon="pi pi-sparkles" onClick={generate} loading={loading} className="mb-3" />
        {result && <div className="p-3 surface-100 border-round white-space-pre-wrap">{result}</div>}
      </Card>
    </div>
  );
};

export default $componentName;
"""

STANDALONE_DASHBOARD_PAGE = r"""import React, { useState, useCallback } from 'react';
import { Card } from 'primereact/card';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { InputTextarea } from 'primereact/inputtextarea';
import { Button } from 'primereact/button';
import aiApiService from '../services/aiApiService';

const $componentName = () => {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const runQuery = useCallback(async () => {
    if (!query.trim() || loading) return;
    setLoading(true);
    try {
      const res = await aiApiService.standaloneQuery('$operationName', { query });
      setResult(res);
      setHistory(prev => [{ query, result: res, timestamp: new Date().toISOString() }, ...prev].slice(0, 20));
    } catch (err) {
      setResult({ error: err.message || 'Query failed' });
    } finally {
      setLoading(false);
    }
  }, [query, loading]);

  return (
    <div className="p-4" style={{ maxWidth: '1000px', margin: '0 auto' }}>
      <h2>$pageTitle</h2>
      <Card className="mb-3">
        <InputTextarea value={query} onChange={e => setQuery(e.target.value)} rows={3} className="w-full mb-3" placeholder="Enter your query..." />
        <Button label="Run Query" icon="pi pi-play" onClick={runQuery} loading={loading} />
      </Card>
      {result && (
        <Card title="Result" className="mb-3">
          <pre className="p-3 surface-100 border-round" style={{ whiteSpace: 'pre-wrap' }}>{JSON.stringify(result, null, 2)}</pre>
        </Card>
      )}
      {history.length > 0 && (
        <Card title="History">
          <DataTable value={history} size="small">
            <Column field="timestamp" header="Time" body={row => new Date(row.timestamp).toLocaleTimeString()} />
            <Column field="query" header="Query" style={{ maxWidth: '300px', overflow: 'hidden', textOverflow: 'ellipsis' }} />
          </DataTable>
        </Card>
      )}
    </div>
  );
};

export default $componentName;
"""

# ── RAG Admin ───────────────────────────────────────────────────────────────

RAG_ADMIN_PAGE = r"""import React, { useState, useEffect, useCallback } from 'react';
import { Card } from 'primereact/card';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Button } from 'primereact/button';
import { Badge } from 'primereact/badge';
import { ConfirmDialog, confirmDialog } from 'primereact/confirmdialog';
import aiApiService from '../services/aiApiService';

const RagAdminPage = () => {
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [reindexing, setReindexing] = useState({});

  const fetchSources = useCallback(async () => {
    setLoading(true);
    try {
      const res = await aiApiService.getRagSources();
      setSources(Array.isArray(res) ? res : []);
    } catch (err) {
      console.error('Failed to load RAG sources:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchSources(); }, [fetchSources]);

  const handleReindex = useCallback(async (sourceName) => {
    confirmDialog({
      message: 'Reindex source "' + sourceName + '"?',
      header: 'Confirm Reindex',
      icon: 'pi pi-refresh',
      accept: async () => {
        setReindexing(prev => ({ ...prev, [sourceName]: true }));
        try {
          await aiApiService.reindexRagSource(sourceName);
          await fetchSources();
        } catch (err) {
          console.error('Reindex failed:', err);
        } finally {
          setReindexing(prev => ({ ...prev, [sourceName]: false }));
        }
      },
    });
  }, [fetchSources]);

  const statusBody = (row) => {
    const severity = row.enabled ? (row.indexed ? 'success' : 'warning') : 'danger';
    const label = row.enabled ? (row.indexed ? 'Indexed' : 'Pending') : 'Disabled';
    return <Badge value={label} severity={severity} />;
  };

  const actionsBody = (row) => (
    <Button icon="pi pi-refresh" label="Reindex" className="p-button-sm p-button-outlined" onClick={() => handleReindex(row.name)} loading={reindexing[row.name]} disabled={!row.enabled} />
  );

  return (
    <div className="p-4">
      <ConfirmDialog />
      <h2>RAG Administration</h2>
      <Card>
        <DataTable value={sources} loading={loading} emptyMessage="No RAG sources configured.">
          <Column field="name" header="Source Name" sortable />
          <Column field="type" header="Type" sortable />
          <Column header="Status" body={statusBody} />
          <Column field="documentCount" header="Documents" />
          <Column header="Actions" body={actionsBody} />
        </DataTable>
      </Card>
    </div>
  );
};

export default RagAdminPage;
"""

# ── Evaluation Display ──────────────────────────────────────────────────────

EVALUATION_SCORE_BADGE = r"""import React from 'react';
import { Badge } from 'primereact/badge';
import { Tooltip } from 'primereact/tooltip';

const EvaluationScoreBadge = ({ score, type, badgeStyle = '$badgeStyle', passThreshold = $passThreshold, warnThreshold = $warnThreshold }) => {
  const severity = score >= passThreshold ? 'success' : score >= warnThreshold ? 'warning' : 'danger';
  const label = typeof score === 'number' ? score.toFixed(2) : score;
  const id = 'eval-badge-' + Math.random().toString(36).slice(2, 9);

  if (badgeStyle === 'tooltip') {
    return (
      <>
        <Tooltip target={'#' + id} content={type + ': ' + label} />
        <Badge id={id} value={label} severity={severity} />
      </>
    );
  }

  if (badgeStyle === 'expandable') {
    return (
      <span className="inline-flex align-items-center gap-1">
        <Badge value={label} severity={severity} />
        <small className="text-500">{type}</small>
      </span>
    );
  }

  return <Badge value={type + ': ' + label} severity={severity} />;
};

export default EvaluationScoreBadge;
"""

EVALUATION_DASHBOARD_PAGE = r"""import React, { useState, useEffect, useCallback } from 'react';
import { Card } from 'primereact/card';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Badge } from 'primereact/badge';
import aiApiService from '../services/aiApiService';
import EvaluationScoreBadge from '../components/ai/EvaluationScoreBadge';

const EvaluationDashboardPage = () => {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchResults = useCallback(async () => {
    setLoading(true);
    try {
      const res = await aiApiService.getEvaluationResults();
      setResults(Array.isArray(res) ? res : []);
    } catch (err) {
      console.error('Failed to load evaluations:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchResults(); }, [fetchResults]);

  const scoreBody = (row) => <EvaluationScoreBadge score={row.score} type={row.evaluatorType || row.type} />;
  const statusBody = (row) => <Badge value={row.status} severity={row.status === 'pass' ? 'success' : row.status === 'fail' ? 'danger' : 'info'} />;

  return (
    <div className="p-4">
      <h2>AI Evaluation Dashboard</h2>
      <Card>
        <DataTable value={results} loading={loading} paginator rows={20} emptyMessage="No evaluation results.">
          <Column field="evaluatorName" header="Evaluator" sortable />
          <Column field="operationName" header="Operation" sortable />
          <Column header="Score" body={scoreBody} sortable sortField="score" />
          <Column header="Status" body={statusBody} sortable sortField="status" />
          <Column field="category" header="Category" sortable />
          <Column field="createdAt" header="Date" sortable body={row => row.createdAt ? new Date(row.createdAt).toLocaleString() : ''} />
        </DataTable>
      </Card>
    </div>
  );
};

export default EvaluationDashboardPage;
"""

# ── Document UI ─────────────────────────────────────────────────────────────

DOCUMENT_UPLOAD_PANEL = r"""import React, { useState, useRef } from 'react';
import { FileUpload } from 'primereact/fileupload';
import { Message } from 'primereact/message';
import { ProgressBar } from 'primereact/progressbar';
import aiApiService from '../services/aiApiService';

const DocumentUploadPanel = () => {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const fileRef = useRef(null);

  const handleUpload = async (event) => {
    const file = event.files[0];
    if (!file) return;
    setUploading(true);
    setError(null);
    setSuccess(null);
    try {
      await aiApiService.uploadDocument(file);
      setSuccess('Uploaded: ' + file.name);
      if (fileRef.current) fileRef.current.clear();
    } catch (err) {
      setError(err.message || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="mb-3">
      <FileUpload ref={fileRef} mode="advanced" customUpload uploadHandler={handleUpload} chooseLabel="Choose Document" uploadLabel="Upload" cancelLabel="Cancel" maxFileSize={10000000} emptyTemplate={<p className="m-0">Drag and drop a document here.</p>} />
      {uploading && <ProgressBar mode="indeterminate" style={{ height: '6px', marginTop: '0.5rem' }} />}
      {error && <Message severity="error" text={error} className="mt-2 w-full" />}
      {success && <Message severity="success" text={success} className="mt-2 w-full" />}
    </div>
  );
};

export default DocumentUploadPanel;
"""

DOCUMENT_LIST_PANEL = r"""import React, { useState, useEffect, useCallback } from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Badge } from 'primereact/badge';
import aiApiService from '../services/aiApiService';

const DocumentListPanel = ({ onSelect }) => {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchDocuments = useCallback(async () => {
    setLoading(true);
    try {
      const res = await aiApiService.getDocuments();
      setDocuments(Array.isArray(res) ? res : []);
    } catch (err) {
      console.error('Failed to load documents:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchDocuments(); }, [fetchDocuments]);

  const statusBody = (row) => {
    const sev = row.extractionStatus === 'completed' ? 'success' : row.extractionStatus === 'failed' ? 'danger' : 'info';
    return <Badge value={row.extractionStatus || 'unknown'} severity={sev} />;
  };

  const sizeBody = (row) => {
    const kb = (row.fileSizeBytes || 0) / 1024;
    return kb > 1024 ? (kb / 1024).toFixed(1) + ' MB' : kb.toFixed(0) + ' KB';
  };

  return (
    <DataTable value={documents} loading={loading} paginator rows={10} selectionMode="single" onSelectionChange={e => onSelect && onSelect(e.value)} emptyMessage="No documents ingested.">
      <Column field="filename" header="Filename" sortable />
      <Column field="mimeType" header="Type" sortable />
      <Column header="Size" body={sizeBody} sortable sortField="fileSizeBytes" />
      <Column header="Status" body={statusBody} sortable sortField="extractionStatus" />
      <Column field="createdAt" header="Uploaded" sortable body={row => row.createdAt ? new Date(row.createdAt).toLocaleString() : ''} />
    </DataTable>
  );
};

export default DocumentListPanel;
"""

DOCUMENT_INGESTION_PAGE = r"""import React, { useState } from 'react';
import { Card } from 'primereact/card';
import { TabView, TabPanel } from 'primereact/tabview';
import DocumentUploadPanel from '../components/ai/DocumentUploadPanel';
import DocumentListPanel from '../components/ai/DocumentListPanel';

const DocumentIngestionPage = () => {
  const [selectedDoc, setSelectedDoc] = useState(null);

  return (
    <div className="p-4">
      <h2>Document Ingestion</h2>
      <TabView>
        <TabPanel header="Upload">
          <DocumentUploadPanel />
        </TabPanel>
        <TabPanel header="Documents">
          <DocumentListPanel onSelect={setSelectedDoc} />
          {selectedDoc && (
            <Card title={selectedDoc.filename} className="mt-3">
              <p><strong>MIME:</strong> {selectedDoc.mimeType}</p>
              <p><strong>Status:</strong> {selectedDoc.extractionStatus}</p>
              {selectedDoc.extractionError && <p className="text-red-500"><strong>Error:</strong> {selectedDoc.extractionError}</p>}
            </Card>
          )}
        </TabPanel>
      </TabView>
    </div>
  );
};

export default DocumentIngestionPage;
"""

DOCUMENT_TASK_PANEL = r"""import React, { useState, useCallback } from 'react';
import { Card } from 'primereact/card';
import { Dropdown } from 'primereact/dropdown';
import { InputTextarea } from 'primereact/inputtextarea';
import { Button } from 'primereact/button';
import { Badge } from 'primereact/badge';
import aiApiService from '../services/aiApiService';

const TASK_TYPES = [
  'summarization', 'composition', 'querying', 'translation',
  'key_info_extraction', 'sentiment_analysis', 'classification',
  'comparison', 'redaction_suggestions', 'action_item_extraction',
  'table_extraction', 'outline_generation',
];

const DocumentTaskPanel = ({ documentId, documentName }) => {
  const [taskType, setTaskType] = useState(null);
  const [instruction, setInstruction] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const runTask = useCallback(async () => {
    if (!taskType || !documentId) return;
    setLoading(true);
    try {
      const res = await aiApiService.runDocumentTask(documentId, { taskName: taskType, userInstruction: instruction });
      setResult(res);
    } catch (err) {
      setResult({ error: err.message || 'Task failed' });
    } finally {
      setLoading(false);
    }
  }, [taskType, documentId, instruction]);

  return (
    <Card title={'Process: ' + (documentName || documentId)} className="mb-3">
      <div className="flex flex-column gap-3">
        <Dropdown value={taskType} options={TASK_TYPES.map(t => ({ label: t.replace(/_/g, ' '), value: t }))} onChange={e => setTaskType(e.value)} placeholder="Select task type" className="w-full" />
        <InputTextarea value={instruction} onChange={e => setInstruction(e.target.value)} rows={2} placeholder="Optional instructions..." className="w-full" />
        <Button label="Run Task" icon="pi pi-play" onClick={runTask} loading={loading} disabled={!taskType} />
        {result && (
          <div className="p-3 surface-100 border-round">
            {result.error ? <span className="text-red-500">{result.error}</span> : (
              <>
                {result.status && <Badge value={result.status} severity={result.status === 'completed' ? 'success' : 'info'} className="mb-2" />}
                <pre className="white-space-pre-wrap mt-2">{result.outputText || JSON.stringify(result, null, 2)}</pre>
              </>
            )}
          </div>
        )}
      </div>
    </Card>
  );
};

export default DocumentTaskPanel;
"""

DOCUMENT_TASK_CHAIN_BUILDER = r"""import React, { useState, useCallback } from 'react';
import { Card } from 'primereact/card';
import { Dropdown } from 'primereact/dropdown';
import { Button } from 'primereact/button';
import { OrderList } from 'primereact/orderlist';
import { Badge } from 'primereact/badge';
import aiApiService from '../services/aiApiService';

const TASK_TYPES = [
  'summarization', 'composition', 'querying', 'translation',
  'key_info_extraction', 'sentiment_analysis', 'classification',
  'comparison', 'redaction_suggestions', 'action_item_extraction',
  'table_extraction', 'outline_generation',
];

const DocumentTaskChainBuilder = ({ documentId, documentName }) => {
  const [chain, setChain] = useState([]);
  const [selectedTask, setSelectedTask] = useState(null);
  const [results, setResults] = useState([]);
  const [running, setRunning] = useState(false);

  const addTask = useCallback(() => {
    if (!selectedTask) return;
    setChain(prev => [...prev, { taskName: selectedTask, id: Date.now() }]);
    setSelectedTask(null);
  }, [selectedTask]);

  const runChain = useCallback(async () => {
    if (!chain.length || !documentId) return;
    setRunning(true);
    setResults([]);
    const chainResults = [];
    for (const step of chain) {
      try {
        const res = await aiApiService.runDocumentTask(documentId, { taskName: step.taskName, chainedFromResultId: chainResults.length > 0 ? chainResults[chainResults.length - 1].id : undefined });
        chainResults.push({ ...res, taskName: step.taskName });
      } catch (err) {
        chainResults.push({ taskName: step.taskName, error: err.message || 'Failed' });
        break;
      }
    }
    setResults(chainResults);
    setRunning(false);
  }, [chain, documentId]);

  const itemTemplate = (item) => <span>{item.taskName.replace(/_/g, ' ')}</span>;

  return (
    <Card title={'Task Chain: ' + (documentName || documentId)}>
      <div className="flex gap-2 mb-3">
        <Dropdown value={selectedTask} options={TASK_TYPES.map(t => ({ label: t.replace(/_/g, ' '), value: t }))} onChange={e => setSelectedTask(e.value)} placeholder="Add task to chain" className="flex-1" />
        <Button icon="pi pi-plus" onClick={addTask} disabled={!selectedTask} />
      </div>
      {chain.length > 0 && <OrderList value={chain} onChange={e => setChain(e.value)} itemTemplate={itemTemplate} header="Task Chain" className="mb-3" />}
      <Button label="Run Chain" icon="pi pi-play" onClick={runChain} loading={running} disabled={!chain.length} className="mb-3" />
      {results.map((r, i) => (
        <div key={i} className="p-2 mb-2 surface-100 border-round">
          <div className="flex align-items-center gap-2 mb-1">
            <strong>{r.taskName ? r.taskName.replace(/_/g, ' ') : ''}</strong>
            <Badge value={r.error ? 'failed' : (r.status || 'done')} severity={r.error ? 'danger' : 'success'} />
          </div>
          {r.error ? <span className="text-red-500">{r.error}</span> : <pre className="white-space-pre-wrap">{r.outputText || JSON.stringify(r, null, 2)}</pre>}
        </div>
      ))}
    </Card>
  );
};

export default DocumentTaskChainBuilder;
"""

# ── AI API Service ──────────────────────────────────────────────────────────

AI_API_SERVICE = r"""import apiClient from './apiClient';

/**
 * Centralized AI API service for all AI endpoints.
 */
const aiApiService = {
  // Chat
  chat: async (data) => {
    const res = await apiClient.post('/api/ai/chat', data);
    return res.data;
  },

  chatStream: async (data, onChunk) => {
    const baseUrl = (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.VITE_API_URL) || '';
    const res = await fetch(
      baseUrl + '/api/ai/chat/stream',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: 'Bearer ' + (localStorage.getItem('token') || ''),
        },
        body: JSON.stringify(data),
      }
    );
    if (!res.ok) throw new Error('Chat stream failed: ' + res.status);
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';
      for (const line of lines) {
        if (line.startsWith('data:')) {
          const chunk = line.slice(5).trim();
          if (chunk && chunk !== '[DONE]') onChunk(chunk);
        }
      }
    }
  },

  // Entity AI
  entitySearch: async (entityName, data) => {
    const res = await apiClient.post('/api/' + entityName + '/ai/search', data);
    return res.data;
  },

  entityGenerate: async (entityName, data) => {
    const res = await apiClient.post('/api/' + entityName + '/ai/generate', data);
    return res.data;
  },

  entitySuggest: async (entityName, data) => {
    const res = await apiClient.post('/api/' + entityName + '/ai/suggest', data);
    return res.data;
  },

  // Standalone AI
  standaloneChat: async (operationName, data) => {
    const res = await apiClient.post('/api/ai/' + operationName + '/chat', data);
    return res.data;
  },

  standaloneGenerate: async (operationName, data) => {
    const res = await apiClient.post('/api/ai/' + operationName + '/generate', data);
    return res.data;
  },

  standaloneQuery: async (operationName, data) => {
    const res = await apiClient.post('/api/ai/' + operationName + '/query', data);
    return res.data;
  },

  // RAG
  getRagSources: async () => {
    const res = await apiClient.get('/api/ai/rag/sources');
    return res.data;
  },

  reindexRagSource: async (sourceName) => {
    const res = await apiClient.post('/api/ai/rag/sources/' + sourceName + '/reindex');
    return res.data;
  },

  // Evaluations
  getEvaluationResults: async (params) => {
    const res = await apiClient.get('/api/ai/evaluations', { params: params || {} });
    return res.data;
  },

  // Documents
  uploadDocument: async (file, metadata) => {
    const formData = new FormData();
    formData.append('file', file);
    if (metadata) {
      Object.entries(metadata).forEach(function(entry) { formData.append(entry[0], entry[1]); });
    }
    const res = await apiClient.post('/api/ai/documents/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return res.data;
  },

  getDocuments: async (params) => {
    const res = await apiClient.get('/api/ai/documents', { params: params || {} });
    return res.data;
  },

  runDocumentTask: async (documentId, data) => {
    const res = await apiClient.post('/api/ai/documents/' + documentId + '/tasks', data);
    return res.data;
  },
};

export default aiApiService;
"""

# ── Navigation Entries (uses Jinja2 for loop) ───────────────────────────────

AI_NAV_ENTRIES = """/**
 * AI section navigation entries.
 * Import and spread into your main nav config.
 */
const aiNavEntries = [
{% for entry in entries %}  {
    label: '{{ entry.label }}',
    icon: '{{ entry.icon }}',
    to: '{{ entry.to }}',
  },
{% endfor %}];

export default aiNavEntries;
"""
