"""Quick verification of widget_templates.py content."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from templates.widget_templates import (
    FILE_UPLOAD_WIDGET, QUILL_EDITOR_WIDGET,
    MONACO_EDITOR_WIDGET, MARKDOWN_EDITOR_WIDGET,
)

# FileUpload checks
assert 'mode="advanced"' in FILE_UPLOAD_WIDGET, "missing mode=advanced"
assert "customUpload" in FILE_UPLOAD_WIDGET, "missing customUpload"
assert "/api/files/upload" in FILE_UPLOAD_WIDGET, "missing upload endpoint"
assert "inlineUrl" in FILE_UPLOAD_WIDGET, "missing inlineUrl"
assert "ProgressBar" in FILE_UPLOAD_WIDGET, "missing ProgressBar"
assert "Message" in FILE_UPLOAD_WIDGET, "missing Message"
assert "FormData" in FILE_UPLOAD_WIDGET, "missing FormData"
assert "entityType" in FILE_UPLOAD_WIDGET, "missing entityType prop"
assert "entityId" in FILE_UPLOAD_WIDGET, "missing entityId prop"
print("FILE_UPLOAD_WIDGET: OK")

# QuillEditor checks
assert "react-quill-new" in QUILL_EDITOR_WIDGET, "missing react-quill-new"
assert "quill.snow.css" in QUILL_EDITOR_WIDGET, "missing quill.snow.css"
assert "katex" in QUILL_EDITOR_WIDGET, "missing katex"
assert "window.katex" in QUILL_EDITOR_WIDGET, "missing window.katex"
assert "formula: true" in QUILL_EDITOR_WIDGET, "missing formula module"
assert "bold" in QUILL_EDITOR_WIDGET, "missing bold toolbar"
assert "code-block" in QUILL_EDITOR_WIDGET, "missing code-block"
assert "/api/files/upload" in QUILL_EDITOR_WIDGET, "missing image upload"
assert "console.error" in QUILL_EDITOR_WIDGET, "missing error logging"
assert "insertEmbed" in QUILL_EDITOR_WIDGET, "missing insertEmbed"
print("QUILL_EDITOR_WIDGET: OK")

# MonacoEditor checks
assert "@monaco-editor/react" in MONACO_EDITOR_WIDGET, "missing monaco import"
assert "minimap: { enabled: false }" in MONACO_EDITOR_WIDGET, "missing minimap"
assert "vs-dark" in MONACO_EDITOR_WIDGET, "missing vs-dark theme"
assert "readOnly" in MONACO_EDITOR_WIDGET, "missing readOnly"
assert "...options" in MONACO_EDITOR_WIDGET, "missing options merge"
assert "language" in MONACO_EDITOR_WIDGET, "missing language prop"
assert "300px" in MONACO_EDITOR_WIDGET, "missing default height"
print("MONACO_EDITOR_WIDGET: OK")

# MarkdownEditor checks
assert "@monaco-editor/react" in MARKDOWN_EDITOR_WIDGET, "missing monaco import"
assert "marked" in MARKDOWN_EDITOR_WIDGET, "missing marked"
assert "DOMPurify" in MARKDOWN_EDITOR_WIDGET, "missing DOMPurify"
assert "TabView" in MARKDOWN_EDITOR_WIDGET, "missing TabView"
assert "TabPanel" in MARKDOWN_EDITOR_WIDGET, "missing TabPanel"
assert "400px" in MARKDOWN_EDITOR_WIDGET, "missing default height"
assert "dangerouslySetInnerHTML" in MARKDOWN_EDITOR_WIDGET, "missing preview render"
assert 'language="markdown"' in MARKDOWN_EDITOR_WIDGET, "missing markdown language"
print("MARKDOWN_EDITOR_WIDGET: OK")

print("\nAll 4 widget templates verified successfully!")
