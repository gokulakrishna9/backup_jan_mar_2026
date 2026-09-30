"""File writing utilities with automatic directory creation."""

import json
import os


class FileWriter:
    """Writes files to disk, creating parent directories as needed."""

    @staticmethod
    def write_file(path: str, content: str) -> str:
        """Write text content to a file.

        Args:
            path: Absolute or relative file path.
            content: Text content to write.

        Returns:
            The absolute path of the written file.
        """
        abs_path = os.path.abspath(path)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(content)
        return abs_path

    @staticmethod
    def write_json(path: str, data, indent: int = 2) -> str:
        """Write data as pretty-printed JSON to a file.

        Args:
            path: Absolute or relative file path.
            data: JSON-serializable data (dict, list, or Pydantic model).
            indent: Indentation level (default 2 spaces).

        Returns:
            The absolute path of the written file.
        """
        abs_path = os.path.abspath(path)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)

        # Handle Pydantic models
        if hasattr(data, "model_dump"):
            data = data.model_dump(by_alias=True)
        elif hasattr(data, "dict"):
            data = data.dict(by_alias=True)

        with open(abs_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
            f.write("\n")
        return abs_path
