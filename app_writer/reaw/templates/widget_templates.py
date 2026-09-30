"""Static JSX templates for shared widget components.

These are complete, self-contained React functional components.
No Jinja2 variables — they are shared across all entities.
"""

FILE_UPLOAD_WIDGET = """import React, { useState, useRef } from 'react';
import { FileUpload } from 'primereact/fileupload';
import { Message } from 'primereact/message';
import { ProgressBar } from 'primereact/progressbar';

const FileUploadWidget = ({ onChange, entityType, entityId, accept, disabled, id }) => {
  const [uploadedFile, setUploadedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const fileUploadRef = useRef(null);

  const customUploader = async (event) => {
    const file = event.files[0];
    if (!file) return;

    setUploading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);
    if (entityType) formData.append('entityType', entityType);
    if (entityId) formData.append('entityId', String(entityId));

    try {
      const response = await fetch('/api/files/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      setUploadedFile(data);
      if (onChange) {
        onChange({ id: data.id, fileName: data.fileName, inlineUrl: data.inlineUrl });
      }
    } catch (err) {
      setError(err.message || 'Upload failed');
    } finally {
      setUploading(false);
      if (fileUploadRef.current) {
        fileUploadRef.current.clear();
      }
    }
  };

  return (
    <div className="file-upload-widget">
      <FileUpload
        ref={fileUploadRef}
        id={id}
        mode="advanced"
        customUpload
        uploadHandler={customUploader}
        accept={accept || undefined}
        disabled={disabled || uploading}
        chooseLabel="Choose File"
        uploadLabel="Upload"
        cancelLabel="Cancel"
        maxFileSize={10000000}
        emptyTemplate={<p className="m-0">Drag and drop a file here to upload.</p>}
      />
      {uploading && <ProgressBar mode="indeterminate" style={{ height: '6px', marginTop: '0.5rem' }} />}
      {error && <Message severity="error" text={error} style={{ marginTop: '0.5rem', width: '100%' }} />}
      {uploadedFile && (
        <div className="mt-2">
          <i className="pi pi-file mr-2" />
          <a href={uploadedFile.inlineUrl} target="_blank" rel="noopener noreferrer">
            {uploadedFile.fileName}
          </a>
        </div>
      )}
    </div>
  );
};

export default FileUploadWidget;
"""

QUILL_EDITOR_WIDGET = """import React, { useRef, useMemo, useCallback } from 'react';
import ReactQuill from 'react-quill-new';
import 'react-quill-new/dist/quill.snow.css';
import katex from 'katex';
import 'katex/dist/katex.min.css';

window.katex = katex;

const QuillEditorWidget = ({ value, onChange, disabled, entityType, entityId, className, id }) => {
  const quillRef = useRef(null);

  const imageHandler = useCallback(() => {
    const input = document.createElement('input');
    input.setAttribute('type', 'file');
    input.setAttribute('accept', 'image/*');
    input.click();

    input.onchange = async () => {
      const file = input.files[0];
      if (!file) return;

      const formData = new FormData();
      formData.append('file', file);
      if (entityType) formData.append('entityType', entityType);
      if (entityId) formData.append('entityId', String(entityId));

      try {
        const response = await fetch('/api/files/upload', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          throw new Error(`Image upload failed: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        const quill = quillRef.current?.getEditor();
        if (quill) {
          const range = quill.getSelection(true);
          quill.insertEmbed(range.index, 'image', data.inlineUrl);
          quill.setSelection(range.index + 1);
        }
      } catch (err) {
        console.error('Image upload failed:', err);
        const quill = quillRef.current?.getEditor();
        if (quill) {
          const range = quill.getSelection(true);
          quill.insertText(range.index, '[Image upload failed]', { color: 'red' });
        }
      }
    };
  }, [entityType, entityId]);

  const modules = useMemo(() => ({
    toolbar: {
      container: [
        ['bold', 'italic', 'underline', 'strike'],
        [{ header: 1 }, { header: 2 }, { header: 3 }],
        [{ list: 'ordered' }, { list: 'bullet' }],
        ['blockquote', 'code-block'],
        ['link', 'image', 'formula'],
        ['clean'],
      ],
      handlers: {
        image: imageHandler,
      },
    },
    formula: true,
  }), [imageHandler]);

  const formats = [
    'bold', 'italic', 'underline', 'strike',
    'header',
    'list', 'bullet',
    'blockquote', 'code-block',
    'link', 'image', 'formula',
  ];

  return (
    <div className={`quill-editor-widget ${className || ''}`} id={id}>
      <ReactQuill
        ref={quillRef}
        theme="snow"
        value={value || ''}
        onChange={onChange}
        modules={modules}
        formats={formats}
        readOnly={disabled}
        placeholder="Enter content..."
      />
    </div>
  );
};

export default QuillEditorWidget;
"""

MONACO_EDITOR_WIDGET = """import React, { useCallback, useMemo } from 'react';
import Editor from '@monaco-editor/react';

const MonacoEditorWidget = ({ value, onChange, disabled, language = 'javascript', height = '300px', className, options, id }) => {
  const detectTheme = useCallback(() => {
    if (typeof document !== 'undefined') {
      const isDark = document.documentElement.classList.contains('dark') ||
        document.body.classList.contains('dark') ||
        window.matchMedia?.('(prefers-color-scheme: dark)').matches;
      return isDark ? 'vs-dark' : 'light';
    }
    return 'vs-dark';
  }, []);

  const mergedOptions = useMemo(() => ({
    minimap: { enabled: false },
    readOnly: !!disabled,
    scrollBeyondLastLine: false,
    wordWrap: 'on',
    automaticLayout: true,
    ...options,
  }), [disabled, options]);

  const handleChange = useCallback((val) => {
    if (onChange) {
      onChange(val);
    }
  }, [onChange]);

  return (
    <div className={`monaco-editor-widget ${className || ''}`} id={id}>
      <Editor
        height={height}
        language={language}
        value={value || ''}
        theme={detectTheme()}
        options={mergedOptions}
        onChange={handleChange}
      />
    </div>
  );
};

export default MonacoEditorWidget;
"""

MARKDOWN_EDITOR_WIDGET = """import React, { useMemo, useState, useEffect } from 'react';
import Editor from '@monaco-editor/react';
import { marked } from 'marked';
import DOMPurify from 'dompurify';
import { TabView, TabPanel } from 'primereact/tabview';

const MarkdownEditorWidget = ({ value, onChange, disabled, height = '400px', className, id }) => {
  const [activeTab, setActiveTab] = useState(0);
  const [windowWidth, setWindowWidth] = useState(typeof window !== 'undefined' ? window.innerWidth : 1024);

  useEffect(() => {
    const handleResize = () => setWindowWidth(window.innerWidth);
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const renderedHtml = useMemo(() => {
    if (!value) return '';
    const raw = marked(value, { breaks: true, gfm: true });
    return DOMPurify.sanitize(raw);
  }, [value]);

  const detectTheme = () => {
    if (typeof document !== 'undefined') {
      const isDark = document.documentElement.classList.contains('dark') ||
        document.body.classList.contains('dark') ||
        window.matchMedia?.('(prefers-color-scheme: dark)').matches;
      return isDark ? 'vs-dark' : 'light';
    }
    return 'vs-dark';
  };

  const editorOptions = useMemo(() => ({
    minimap: { enabled: false },
    readOnly: !!disabled,
    scrollBeyondLastLine: false,
    wordWrap: 'on',
    automaticLayout: true,
  }), [disabled]);

  const previewPanel = (
    <div
      className="markdown-preview"
      style={{
        height,
        overflow: 'auto',
        padding: '1rem',
        border: '1px solid var(--surface-border, #dee2e6)',
        borderRadius: 'var(--border-radius, 6px)',
        backgroundColor: 'var(--surface-ground, #ffffff)',
      }}
      dangerouslySetInnerHTML={{ __html: renderedHtml }}
    />
  );

  if (disabled) {
    return (
      <div className={`markdown-editor-widget ${className || ''}`} id={id}>
        {previewPanel}
      </div>
    );
  }

  const isSmallScreen = windowWidth < 768;

  if (isSmallScreen) {
    return (
      <div className={`markdown-editor-widget ${className || ''}`} id={id}>
        <TabView activeIndex={activeTab} onTabChange={(e) => setActiveTab(e.index)}>
          <TabPanel header="Edit">
            <Editor
              height={height}
              language="markdown"
              value={value || ''}
              theme={detectTheme()}
              options={editorOptions}
              onChange={onChange}
            />
          </TabPanel>
          <TabPanel header="Preview">
            {previewPanel}
          </TabPanel>
        </TabView>
      </div>
    );
  }

  return (
    <div className={`markdown-editor-widget ${className || ''}`} id={id}>
      <div style={{ display: 'flex', gap: '1rem', height }}>
        <div style={{ flex: 1 }}>
          <Editor
            height={height}
            language="markdown"
            value={value || ''}
            theme={detectTheme()}
            options={editorOptions}
            onChange={onChange}
          />
        </div>
        <div style={{ flex: 1 }}>
          {previewPanel}
        </div>
      </div>
    </div>
  );
};

export default MarkdownEditorWidget;
"""
