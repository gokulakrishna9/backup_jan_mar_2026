"""Generic JSON CRUD manager for layer definition files."""

import json
from pathlib import Path
from typing import Optional, Dict, Any, List, Union
from .definition_manager import DefinitionManager


class LayerManager:
    """Generic CRUD operations on JSON layer definition files (v2.3).
    
    This manager provides a flexible interface for manipulating any JSON file
    in the application_definitions directory using JSONPath-like queries.
    """
    
    # Layer file names
    LAYER_FILES = {
        "entity": "webflux_entity_layer.json",
        "repository": "webflux_repository_layer.json",
        "service": "webflux_service_layer.json",
        "controller": "webflux_controller_layer.json",
        "dto": "webflux_dto_layer.json",
        "security": "webflux_security_layer.json",
        "config": "webflux_config_layer.json",
        "exception": "webflux_exception_layer.json",
        "audit": "webflux_audit_logging_layer.json",
        "authorization": "webflux_authorization_layer.json",
        "custom_queries": "webflux_custom_queries_layer.json",
        "group_definition": "webflux_group_definition_layer.json",
        "manifest": "webflux_manifest.json",
        "project_metadata": "webflux_project_metadata.json",
        "entities": "webflux_entities.json",
        "relationships": "webflux_relationships.json"
    }
    
    def __init__(self, definition_manager: DefinitionManager):
        """Initialize the layer manager.
        
        Args:
            definition_manager: DefinitionManager instance
        """
        self.def_manager = definition_manager
        self.definitions_dir = definition_manager.definitions_dir
    
    def get(self, file_name: str, path: Optional[str] = None) -> Any:
        """Get data from a JSON file, optionally at a specific path.
        
        Args:
            file_name: Name of the file (with or without .json extension) or layer alias
            path: Dot-notation path to nested data (e.g., "jwt.expiration" or "entities[0].name")
            
        Returns:
            The data at the specified path, or entire file if no path given
            
        Examples:
            >>> manager.get("security_layer.json")  # Get entire file
            >>> manager.get("security", "jwt.expiration")  # Get nested value
            >>> manager.get("entities", "[0].name")  # Get array element
        """
        # Resolve file name
        resolved_file = self._resolve_file_name(file_name)
        file_path = self.definitions_dir / resolved_file
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # If no path specified, return entire data
        if path is None:
            return data
        
        # Navigate to the specified path
        return self._get_nested(data, path)
    
    def set(self, file_name: str, path: str, value: Any) -> None:
        """Set a value at a specific path in a JSON file.
        
        Args:
            file_name: Name of the file or layer alias
            path: Dot-notation path to the data (e.g., "jwt.expiration")
            value: Value to set
            
        Examples:
            >>> manager.set("security", "jwt.expiration", 3600000)
            >>> manager.set("entities", "[0].name", "NewName")
        """
        resolved_file = self._resolve_file_name(file_name)
        file_path = self.definitions_dir / resolved_file
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Set the value at the path
        self._set_nested(data, path, value)
        
        # Save the file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def update(self, file_name: str, path: Optional[str], updates: Dict[str, Any]) -> None:
        """Update multiple fields at a specific path in a JSON file.
        
        Args:
            file_name: Name of the file or layer alias
            path: Dot-notation path to the object to update (None for root)
            updates: Dictionary of fields to update
            
        Examples:
            >>> manager.update("security", "jwt", {"expiration": 3600000, "issuer": "my-company"})
            >>> manager.update("entities", None, {"version": "2.0"})
        """
        resolved_file = self._resolve_file_name(file_name)
        file_path = self.definitions_dir / resolved_file
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Get the target object
        if path is None:
            target = data
        else:
            target = self._get_nested(data, path)
        
        # Update the target
        if not isinstance(target, dict):
            raise ValueError(f"Target at path '{path}' is not a dictionary")
        
        target.update(updates)
        
        # Save the file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def delete(self, file_name: str, path: str) -> None:
        """Delete a value at a specific path in a JSON file.
        
        Args:
            file_name: Name of the file or layer alias
            path: Dot-notation path to the data to delete
            
        Examples:
            >>> manager.delete("security", "jwt.issuer")
            >>> manager.delete("entities", "[0]")
        """
        resolved_file = self._resolve_file_name(file_name)
        file_path = self.definitions_dir / resolved_file
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Delete the value at the path
        self._delete_nested(data, path)
        
        # Save the file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def append(self, file_name: str, path: str, value: Any) -> None:
        """Append a value to an array at a specific path.
        
        Args:
            file_name: Name of the file or layer alias
            path: Dot-notation path to the array
            value: Value to append
            
        Examples:
            >>> manager.append("entities", "tables", {"name": "new_table"})
        """
        resolved_file = self._resolve_file_name(file_name)
        file_path = self.definitions_dir / resolved_file
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Get the array
        target = self._get_nested(data, path)
        
        if not isinstance(target, list):
            raise ValueError(f"Target at path '{path}' is not an array")
        
        target.append(value)
        
        # Save the file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def find(self, file_name: str, path: str, predicate: Dict[str, Any]) -> Optional[Any]:
        """Find an item in an array that matches a predicate.
        
        Args:
            file_name: Name of the file or layer alias
            path: Dot-notation path to the array
            predicate: Dictionary of field-value pairs to match
            
        Returns:
            The first matching item, or None if not found
            
        Examples:
            >>> manager.find("entities", "tables", {"name": "users"})
        """
        array = self.get(file_name, path)
        
        if not isinstance(array, list):
            raise ValueError(f"Target at path '{path}' is not an array")
        
        for item in array:
            if isinstance(item, dict) and all(item.get(k) == v for k, v in predicate.items()):
                return item
        
        return None
    
    def filter(self, file_name: str, path: str, predicate: Dict[str, Any]) -> List[Any]:
        """Filter items in an array that match a predicate.
        
        Args:
            file_name: Name of the file or layer alias
            path: Dot-notation path to the array
            predicate: Dictionary of field-value pairs to match
            
        Returns:
            List of matching items
            
        Examples:
            >>> manager.filter("entities", "tables", {"type": "user_table"})
        """
        array = self.get(file_name, path)
        
        if not isinstance(array, list):
            raise ValueError(f"Target at path '{path}' is not an array")
        
        return [
            item for item in array
            if isinstance(item, dict) and all(item.get(k) == v for k, v in predicate.items())
        ]
    
    def exists(self, file_name: str, path: Optional[str] = None) -> bool:
        """Check if a file or path exists.
        
        Args:
            file_name: Name of the file or layer alias
            path: Optional dot-notation path to check
            
        Returns:
            True if exists, False otherwise
            
        Examples:
            >>> manager.exists("security")  # Check if file exists
            >>> manager.exists("security", "jwt.expiration")  # Check if path exists
        """
        try:
            resolved_file = self._resolve_file_name(file_name)
            file_path = self.definitions_dir / resolved_file
            
            if not file_path.exists():
                return False
            
            if path is None:
                return True
            
            # Check if path exists
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            try:
                self._get_nested(data, path)
                return True
            except (KeyError, IndexError, ValueError):
                return False
        except:
            return False
    
    def list_files(self) -> List[str]:
        """List all JSON files in the definitions directory.
        
        Returns:
            List of file names
        """
        if not self.definitions_dir.exists():
            return []
        
        return [f.name for f in self.definitions_dir.glob("*.json")]
    
    def list_layers(self) -> List[str]:
        """List all available layer aliases.
        
        Returns:
            List of layer names
        """
        return list(self.LAYER_FILES.keys())
    
    # Helper methods for path navigation
    
    def _resolve_file_name(self, file_name: str) -> str:
        """Resolve a file name or layer alias to actual file name.
        
        Args:
            file_name: File name or layer alias
            
        Returns:
            Actual file name with .json extension
        """
        # If it's a layer alias, resolve it
        if file_name in self.LAYER_FILES:
            return self.LAYER_FILES[file_name]
        
        # If it doesn't have .json extension, add it
        if not file_name.endswith('.json'):
            return f"{file_name}.json"
        
        return file_name
    
    def _get_nested(self, data: Any, path: str) -> Any:
        """Get a value from nested data using dot notation.
        
        Args:
            data: The data structure
            path: Dot-notation path (e.g., "jwt.expiration" or "[0].name")
            
        Returns:
            The value at the path
            
        Raises:
            KeyError: If path doesn't exist
            IndexError: If array index is out of range
            ValueError: If path is invalid
        """
        if not path:
            return data
        
        parts = self._parse_path(path)
        current = data
        
        for part in parts:
            if isinstance(part, int):
                # Array index
                if not isinstance(current, list):
                    raise ValueError(f"Cannot index non-array with [{part}]")
                current = current[part]
            else:
                # Object key
                if not isinstance(current, dict):
                    raise ValueError(f"Cannot access key '{part}' on non-object")
                current = current[part]
        
        return current
    
    def _set_nested(self, data: Any, path: str, value: Any) -> None:
        """Set a value in nested data using dot notation.
        
        Args:
            data: The data structure
            path: Dot-notation path
            value: Value to set
        """
        parts = self._parse_path(path)
        current = data
        
        # Navigate to parent
        for part in parts[:-1]:
            if isinstance(part, int):
                current = current[part]
            else:
                current = current[part]
        
        # Set the value
        last_part = parts[-1]
        if isinstance(last_part, int):
            current[last_part] = value
        else:
            current[last_part] = value
    
    def _delete_nested(self, data: Any, path: str) -> None:
        """Delete a value from nested data using dot notation.
        
        Args:
            data: The data structure
            path: Dot-notation path
        """
        parts = self._parse_path(path)
        current = data
        
        # Navigate to parent
        for part in parts[:-1]:
            if isinstance(part, int):
                current = current[part]
            else:
                current = current[part]
        
        # Delete the value
        last_part = parts[-1]
        if isinstance(last_part, int):
            if isinstance(current, list):
                del current[last_part]
            else:
                raise ValueError("Cannot delete array index from non-array")
        else:
            if isinstance(current, dict):
                del current[last_part]
            else:
                raise ValueError("Cannot delete key from non-object")
    
    def _parse_path(self, path: str) -> List[Union[str, int]]:
        """Parse a dot-notation path into parts.
        
        Args:
            path: Dot-notation path (e.g., "jwt.expiration" or "[0].name")
            
        Returns:
            List of path parts (strings for keys, ints for array indices)
        """
        parts = []
        current = ""
        in_bracket = False
        
        for char in path:
            if char == '[':
                if current:
                    parts.append(current)
                    current = ""
                in_bracket = True
            elif char == ']':
                if in_bracket and current:
                    parts.append(int(current))
                    current = ""
                in_bracket = False
            elif char == '.' and not in_bracket:
                if current:
                    parts.append(current)
                    current = ""
            else:
                current += char
        
        if current:
            if in_bracket:
                parts.append(int(current))
            else:
                parts.append(current)
        
        return parts
