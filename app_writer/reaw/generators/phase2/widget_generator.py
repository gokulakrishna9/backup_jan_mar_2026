"""Widget generator — produces shared widget component files for used widget types."""

import os
from typing import List

from models.react_definition_models import ReactAppDefinition
from templates.widget_templates import (
    FILE_UPLOAD_WIDGET,
    QUILL_EDITOR_WIDGET,
    MONACO_EDITOR_WIDGET,
    MARKDOWN_EDITOR_WIDGET,
)
from utils.file_writer import FileWriter

# Maps widget componentType to (output filename, template content)
WIDGET_TYPE_MAP = {
    "QuillEditor": ("QuillEditorWidget.jsx", QUILL_EDITOR_WIDGET),
    "MonacoEditor": ("MonacoEditorWidget.jsx", MONACO_EDITOR_WIDGET),
    "MarkdownEditor": ("MarkdownEditorWidget.jsx", MARKDOWN_EDITOR_WIDGET),
    "FileUpload": ("FileUploadWidget.jsx", FILE_UPLOAD_WIDGET),
}


class WidgetGenerator:
    @staticmethod
    def generate(react_def: ReactAppDefinition, output_dir: str) -> List[str]:
        """Generate shared widget component files for used widget types.

        Scans component_mappings for widget componentTypes.
        Only generates files for widgets actually used.
        Returns list of generated file paths.
        """
        used_widgets = set()
        for mapping in react_def.component_mappings:
            for field in mapping.fields:
                if field.componentType in WIDGET_TYPE_MAP:
                    used_widgets.add(field.componentType)

        if not used_widgets:
            return []

        widgets_dir = os.path.join(output_dir, "src", "components", "widgets")
        files = []

        for widget_type in sorted(used_widgets):
            filename, content = WIDGET_TYPE_MAP[widget_type]
            path = os.path.join(widgets_dir, filename)
            FileWriter.write_file(path, content)
            files.append(path)

        return files
