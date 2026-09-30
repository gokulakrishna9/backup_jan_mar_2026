"""Integration tests for widget feature backward compatibility and mixed fields.

**Validates: Requirements 6.1, 6.7, 12.1, 12.2, 12.3, 12.4**
"""

import os
import sys
import tempfile
from pathlib import Path

import pytest
from jinja2 import Template

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from models.definition_models import (
    DtoFieldDef, DtoLayerEntry, DtoLayerDef,
    EntityLayerEntry, EntityLayerDef, RelationshipsDef,
)
from models.react_definition_models import (
    ComponentMapping, FieldMapping, ReactAppDefinition,
)
from transformers.phase1.component_mapping_transformer import ComponentMappingTransformer
from transformers.phase2.scaffold_transformer import ScaffoldTransformer
from generators.phase2.widget_generator import WidgetGenerator
from templates.entity_component_templates import ENTITY_FORM


# ---------------------------------------------------------------------------
# 14.1: No-widget backward compatibility
# ---------------------------------------------------------------------------

class TestNoWidgetBackwardCompatibility:
    """Verify that apps with zero fieldWidget properties produce identical output."""

    def test_no_widget_fields_no_widget_files_generated(self):
        """No widget files generated when no fieldWidget properties exist."""
        react_def = ReactAppDefinition(
            component_mappings=[ComponentMapping(
                entityName="User",
                fields=[
                    FieldMapping(fieldName="name", componentType="InputText", javaType="String", includeInDTO=True),
                    FieldMapping(fieldName="age", componentType="InputNumber", javaType="Integer", includeInDTO=True),
                    FieldMapping(fieldName="active", componentType="Checkbox", javaType="Boolean", includeInDTO=True),
                ],
            )],
        )

        with tempfile.TemporaryDirectory() as tmp:
            result = WidgetGenerator.generate(react_def, tmp)
            assert result == [], "No widget files should be generated"

            widgets_dir = os.path.join(tmp, "src", "components", "widgets")
            assert not os.path.exists(widgets_dir), "widgets/ directory should not exist"

    def test_no_widget_fields_no_widget_imports_in_form(self):
        """No widget imports in form when no widget componentTypes used."""
        from models.property_objects import EntityFormProperties, FormFieldProperties

        fields = [
            FormFieldProperties(fieldName="name", fieldLabel="Name", componentType="InputText", javaType="String"),
            FormFieldProperties(fieldName="email", fieldLabel="Email", componentType="InputText", javaType="String"),
            FormFieldProperties(fieldName="age", fieldLabel="Age", componentType="InputNumber", javaType="Integer"),
        ]
        form_props = EntityFormProperties(
            entityName="User", entityNamePascal="User", entityNameCamel="user",
            basePath="/api/user", pkField="id", fields=fields,
            isRootEntity=True, hasCreateEndpoint=True, hasUpdateEndpoint=True,
            hasDeleteEndpoint=False,
        )

        output = Template(ENTITY_FORM).render(**form_props.model_dump())

        assert "QuillEditorWidget" not in output
        assert "MonacoEditorWidget" not in output
        assert "MarkdownEditorWidget" not in output
        assert "FileUploadWidget" not in output

    def test_no_widget_fields_no_widget_npm_deps(self):
        """No widget npm deps when no widget componentTypes used."""
        react_def = ReactAppDefinition(
            component_mappings=[ComponentMapping(
                entityName="User",
                fields=[
                    FieldMapping(fieldName="name", componentType="InputText", javaType="String", includeInDTO=True),
                ],
            )],
        )
        scaffold, _ = ScaffoldTransformer.transform(react_def)
        assert scaffold.widgetDependencies == {}

    def test_component_mapping_without_field_widget_uses_type_mapper(self):
        """Fields without fieldWidget use TypeMapper (standard behavior)."""
        dto_layer = DtoLayerDef(dtos=[
            DtoLayerEntry(
                entityName="User", dtoType="Input", className="UserInputDTO",
                packageName="com.example.dto",
                fields=[
                    DtoFieldDef(fieldName="name", javaType="String", includeInDTO=True),
                    DtoFieldDef(fieldName="age", javaType="Integer", includeInDTO=True),
                    DtoFieldDef(fieldName="active", javaType="Boolean", includeInDTO=True),
                ],
            ),
        ])
        entity_layer = EntityLayerDef(entities=[
            EntityLayerEntry(tableName="user", className="User"),
        ])
        rels = RelationshipsDef(relationships=[])

        mappings = ComponentMappingTransformer.transform(dto_layer, rels, entity_layer)
        assert len(mappings) == 1

        types = {f.componentType for f in mappings[0].fields}
        assert "QuillEditor" not in types
        assert "MonacoEditor" not in types
        assert "MarkdownEditor" not in types
        # Standard types should be present
        assert "InputText" in types
        assert "InputNumber" in types
        assert "Checkbox" in types


# ---------------------------------------------------------------------------
# 14.2: Mixed widget and standard fields
# ---------------------------------------------------------------------------

class TestMixedWidgetAndStandardFields:
    """Verify correct output when entity has both standard and widget fields."""

    def test_mixed_fields_component_mapping(self):
        """Standard fields use TypeMapper, widget fields use widget componentType."""
        dto_layer = DtoLayerDef(dtos=[
            DtoLayerEntry(
                entityName="Article", dtoType="Input", className="ArticleInputDTO",
                packageName="com.example.dto",
                fields=[
                    DtoFieldDef(fieldName="title", javaType="String", includeInDTO=True),
                    DtoFieldDef(fieldName="publishDate", javaType="LocalDate", includeInDTO=True),
                    DtoFieldDef(fieldName="content", javaType="String", includeInDTO=True,
                                fieldWidget="richText"),
                    DtoFieldDef(fieldName="sourceCode", javaType="String", includeInDTO=True,
                                fieldWidget="codeEditor", language="java"),
                ],
            ),
        ])
        entity_layer = EntityLayerDef(entities=[
            EntityLayerEntry(tableName="article", className="Article"),
        ])
        rels = RelationshipsDef(relationships=[])

        mappings = ComponentMappingTransformer.transform(dto_layer, rels, entity_layer)
        assert len(mappings) == 1

        field_map = {f.fieldName: f for f in mappings[0].fields}

        # Standard fields
        assert field_map["title"].componentType == "InputText"
        assert field_map["publishDate"].componentType == "Calendar"

        # Widget fields
        assert field_map["content"].componentType == "QuillEditor"
        assert field_map["content"].props.get("fieldWidget") == "richText"

        assert field_map["sourceCode"].componentType == "MonacoEditor"
        assert field_map["sourceCode"].props.get("language") == "java"
        assert field_map["sourceCode"].props.get("fieldWidget") == "codeEditor"

    def test_mixed_fields_form_has_only_used_widget_imports(self):
        """Form with QuillEditor and MonacoEditor imports only those two widgets."""
        from models.property_objects import EntityFormProperties, FormFieldProperties

        fields = [
            FormFieldProperties(fieldName="title", fieldLabel="Title", componentType="InputText", javaType="String"),
            FormFieldProperties(fieldName="content", fieldLabel="Content", componentType="QuillEditor",
                                javaType="String", props={"fieldWidget": "richText"}),
            FormFieldProperties(fieldName="code", fieldLabel="Code", componentType="MonacoEditor",
                                javaType="String", props={"fieldWidget": "codeEditor", "language": "java"}),
        ]
        form_props = EntityFormProperties(
            entityName="Article", entityNamePascal="Article", entityNameCamel="article",
            basePath="/api/article", pkField="id", fields=fields,
            isRootEntity=True, hasCreateEndpoint=True, hasUpdateEndpoint=True,
            hasDeleteEndpoint=False,
        )

        output = Template(ENTITY_FORM).render(**form_props.model_dump())

        # Used widgets should be imported
        assert "import QuillEditorWidget from" in output
        assert "import MonacoEditorWidget from" in output

        # Unused widgets should NOT be imported
        assert "import MarkdownEditorWidget from" not in output
        assert "import FileUploadWidget from" not in output

        # Standard components still render
        assert "<InputText" in output

        # Widget components render
        assert "<QuillEditorWidget" in output
        assert "<MonacoEditorWidget" in output

    def test_mixed_fields_widget_generator_only_generates_used(self):
        """WidgetGenerator only generates files for QuillEditor and MonacoEditor."""
        react_def = ReactAppDefinition(
            component_mappings=[ComponentMapping(
                entityName="Article",
                fields=[
                    FieldMapping(fieldName="title", componentType="InputText", javaType="String", includeInDTO=True),
                    FieldMapping(fieldName="content", componentType="QuillEditor", javaType="String",
                                 props={"fieldWidget": "richText"}, includeInDTO=True),
                    FieldMapping(fieldName="code", componentType="MonacoEditor", javaType="String",
                                 props={"fieldWidget": "codeEditor", "language": "java"}, includeInDTO=True),
                ],
            )],
        )

        with tempfile.TemporaryDirectory() as tmp:
            result = WidgetGenerator.generate(react_def, tmp)
            filenames = {os.path.basename(p) for p in result}

            assert "QuillEditorWidget.jsx" in filenames
            assert "MonacoEditorWidget.jsx" in filenames
            assert "MarkdownEditorWidget.jsx" not in filenames
            assert "FileUploadWidget.jsx" not in filenames

    def test_mixed_fields_scaffold_deps_only_for_used_widgets(self):
        """ScaffoldTransformer adds deps only for QuillEditor and MonacoEditor."""
        react_def = ReactAppDefinition(
            component_mappings=[ComponentMapping(
                entityName="Article",
                fields=[
                    FieldMapping(fieldName="title", componentType="InputText", javaType="String", includeInDTO=True),
                    FieldMapping(fieldName="content", componentType="QuillEditor", javaType="String", includeInDTO=True),
                    FieldMapping(fieldName="code", componentType="MonacoEditor", javaType="String", includeInDTO=True),
                ],
            )],
        )

        scaffold, _ = ScaffoldTransformer.transform(react_def)
        deps = scaffold.widgetDependencies

        # Quill deps
        assert "quill" in deps
        assert "react-quill-new" in deps
        assert "katex" in deps

        # Monaco deps
        assert "@monaco-editor/react" in deps
        assert "monaco-editor" in deps

        # Markdown-only deps should NOT be present
        assert "marked" not in deps
        assert "dompurify" not in deps
