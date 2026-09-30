"""Abstract storage backend for application definitions."""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from models.database_definition import DatabaseDefinition


class DefinitionStore(ABC):
    """Abstract interface that both JSON and DB backends implement.

    Both backends produce the same two objects the generators consume:
      1. DatabaseDefinition (Pydantic model)
      2. layer_definitions dict (or None)
    """

    @abstractmethod
    def save(self, db_def: DatabaseDefinition, output_dir: str) -> str:
        """Save a complete application definition.

        Args:
            db_def: The parsed database definition
            output_dir: Output directory for the generated application

        Returns:
            Identifier string (manifest path for JSON, app_id for DB)
        """

    @abstractmethod
    def load(self, identifier: str) -> DatabaseDefinition:
        """Load a DatabaseDefinition from storage.

        Args:
            identifier: output_dir for JSON, app_id for DB

        Returns:
            Reconstructed DatabaseDefinition
        """

    @abstractmethod
    def load_layer_definitions(self, identifier: str) -> Optional[Dict[str, Any]]:
        """Load layer definition data for code generation.

        Returns:
            Dict with keys like 'entity_layer', 'repository_layer', etc.
            or None if layer definitions are not available.
        """

    @abstractmethod
    def list_apps(self) -> List[Dict[str, Any]]:
        """List available application definitions."""

    @abstractmethod
    def delete(self, identifier: str) -> bool:
        """Delete an application definition."""
