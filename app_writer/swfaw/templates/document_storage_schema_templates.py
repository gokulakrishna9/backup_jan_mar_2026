"""Document storage schema templates - SQL DDL for file_metadata and document collection tables."""


class DocumentStorageSchemaTemplates:
    """Templates for generating document storage database schema DDL."""

    @staticmethod
    def generate_file_metadata_ddl() -> str:
        """Generate DDL for the file_metadata table.

        Returns:
            SQL CREATE TABLE statement for file_metadata with all columns
            and an index on (entity_type, entity_id).
        """
        return """CREATE TABLE IF NOT EXISTS `file_metadata` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `file_name` VARCHAR(500) NOT NULL,
    `content_type` VARCHAR(255) NOT NULL,
    `file_size` BIGINT UNSIGNED NOT NULL,
    `storage_path` VARCHAR(1000) NOT NULL,
    `uploaded_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `entity_type` VARCHAR(255),
    `entity_id` BIGINT UNSIGNED,
    `uploaded_by_user_id` BIGINT UNSIGNED,
    PRIMARY KEY (`id`),
    INDEX `idx_file_metadata_entity` (`entity_type`, `entity_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;"""

    @staticmethod
    def generate_collection_table_ddl(table_name: str) -> str:
        """Generate DDL for a document collection table.

        Args:
            table_name: The MySQL table name for this collection.

        Returns:
            SQL CREATE TABLE statement with id, content JSON, created_at,
            and updated_at columns.
        """
        return f"""CREATE TABLE IF NOT EXISTS `{table_name}` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `content` JSON NOT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;"""
