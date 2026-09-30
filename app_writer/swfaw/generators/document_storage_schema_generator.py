"""Document storage schema generator - generates DDL for file_metadata and document collection tables."""

from templates.document_storage_schema_templates import DocumentStorageSchemaTemplates


class DocumentStorageSchemaGenerator:
    """Generates DDL for file_metadata and document collection tables."""

    @staticmethod
    def generate(document_storage_layer: dict) -> str:
        """Generate SQL DDL for document storage tables.

        Args:
            document_storage_layer: Parsed webflux_document_storage_layer.json dict.

        Returns:
            SQL string with CREATE TABLE statements, or empty string if nothing to generate.
        """
        ddl_parts = []

        # file_metadata DDL when fileStorage is enabled
        file_storage = document_storage_layer.get("fileStorage", {})
        if file_storage.get("enabled", False):
            ddl_parts.append(DocumentStorageSchemaTemplates.generate_file_metadata_ddl())

        # Per-collection table DDL
        for collection in document_storage_layer.get("documentCollections", []):
            table_name = collection["tableName"]
            ddl_parts.append(DocumentStorageSchemaTemplates.generate_collection_table_ddl(table_name))

        if not ddl_parts:
            return ""

        return "\n\n".join(ddl_parts)
