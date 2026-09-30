import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from generators.phase2.widget_generator import WidgetGenerator, WIDGET_TYPE_MAP

print("Import OK")
print("WIDGET_TYPE_MAP keys:", sorted(WIDGET_TYPE_MAP.keys()))
print("generate is static:", isinstance(
    WidgetGenerator.__dict__["generate"], staticmethod
))

# Quick functional test with empty component_mappings
from models.react_definition_models import ReactAppDefinition
rd = ReactAppDefinition()
result = WidgetGenerator.generate(rd, "/tmp/test_out")
print("Empty mappings -> files:", result)
assert result == [], f"Expected empty list, got {result}"

# Test with a widget componentType present
from models.react_definition_models import ComponentMapping, FieldMapping
rd2 = ReactAppDefinition(component_mappings=[
    ComponentMapping(entityName="Article", fields=[
        FieldMapping(fieldName="content", componentType="QuillEditor", javaType="String"),
        FieldMapping(fieldName="title", componentType="InputText", javaType="String"),
    ])
])
import tempfile, os
with tempfile.TemporaryDirectory() as td:
    files = WidgetGenerator.generate(rd2, td)
    print("QuillEditor only -> files:", [os.path.basename(f) for f in files])
    assert len(files) == 1
    assert files[0].endswith("QuillEditorWidget.jsx")
    assert os.path.exists(files[0])

# Test with multiple widget types
rd3 = ReactAppDefinition(component_mappings=[
    ComponentMapping(entityName="Article", fields=[
        FieldMapping(fieldName="content", componentType="QuillEditor", javaType="String"),
        FieldMapping(fieldName="code", componentType="MonacoEditor", javaType="String"),
    ]),
    ComponentMapping(entityName="Doc", fields=[
        FieldMapping(fieldName="body", componentType="MarkdownEditor", javaType="String"),
        FieldMapping(fieldName="code", componentType="MonacoEditor", javaType="String"),
    ]),
])
with tempfile.TemporaryDirectory() as td:
    files = WidgetGenerator.generate(rd3, td)
    basenames = [os.path.basename(f) for f in files]
    print("Multiple widgets -> files:", basenames)
    assert len(files) == 3  # QuillEditor, MonacoEditor, MarkdownEditor (deduplicated)
    assert "QuillEditorWidget.jsx" in basenames
    assert "MonacoEditorWidget.jsx" in basenames
    assert "MarkdownEditorWidget.jsx" in basenames

print("\nAll checks passed!")
