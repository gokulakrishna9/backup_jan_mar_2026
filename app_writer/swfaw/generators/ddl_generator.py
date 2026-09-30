"""DDL Generator - generates MySQL CREATE TABLE DDL from application definition JSON.

Reads entity_layer, relationships, and project_metadata to produce a complete
SQL schema including CREATE DATABASE, CREATE TABLE statements with columns,
PRIMARY KEY, NOT NULL, AUTO_INCREMENT, FOREIGN KEY, and INDEX constraints.

Appends auth schema DDL and activity tracking schema DDL at the end.
All CREATE statements use IF NOT EXISTS for idempotent execution.
"""

import warnings

from generators.auth_schema_generator import AuthSchemaGenerator
from generators.activity_tracking_schema_generator import ActivityTrackingSchemaGenerator


class DDLGenerator:
    """Generates SQL DDL from application definition JSON."""

    JAVA_TO_SQL_FALLBACK: dict[str, str] = {
        "Long": "BIGINT UNSIGNED",
        "Integer": "INT",
        "Short": "SMALLINT",
        "Byte": "TINYINT",
        "String": "VARCHAR(255)",
        "Boolean": "BOOLEAN",
        "LocalDate": "DATE",
        "LocalDateTime": "TIMESTAMP",
        "LocalTime": "TIME",
        "BigDecimal": "DECIMAL(19,4)",
        "Float": "FLOAT",
        "Double": "DOUBLE",
        "byte[]": "BLOB",
        "UUID": "VARCHAR(36)",
    }

    def generate_schema(self, entity_layer: dict,
                        relationships: dict,
                        project_metadata: dict) -> str:
        """Generate complete SQL DDL string.

        Args:
            entity_layer: Parsed webflux_entity_layer.json with "entities" list.
            relationships: Parsed webflux_relationships.json with "relationships" list.
            project_metadata: Parsed webflux_project_metadata.json.

        Returns:
            Complete SQL DDL string with database preamble, entity tables,
            auth schema, and activity tracking schema.
        """
        db_name = project_metadata["projectMetadata"]["database"]["name"]

        parts: list[str] = []
        parts.append(f"CREATE DATABASE IF NOT EXISTS `{db_name}`;")
        parts.append(f"USE `{db_name}`;")
        parts.append("")

        # Group relationships by sourceTable for fast lookup
        rels_by_source: dict[str, list[dict]] = {}
        for rel in relationships.get("relationships", []):
            src = rel.get("sourceTable", "")
            rels_by_source.setdefault(src, []).append(rel)

        entities = entity_layer.get("entities", [])
        if not entities:
            print("WARNING: entity_layer has an empty entities list. "
                  "Generating auth-only schema DDL.")

        for entity_def in entities:
            table_name = entity_def["tableName"]
            table_rels = rels_by_source.get(table_name, [])
            parts.append(self._generate_create_table(entity_def, table_rels))
            parts.append("")

        # Append auth schema DDL
        parts.append(AuthSchemaGenerator.generate())
        parts.append("")

        # Append activity tracking schema DDL
        parts.append(ActivityTrackingSchemaGenerator.generate())

        return "\n".join(parts)

    def _generate_create_table(self, entity_def: dict,
                               relationships: list[dict]) -> str:
        """Generate CREATE TABLE statement for a single entity.

        Args:
            entity_def: Single entity dict from entity_layer["entities"].
            relationships: List of relationship dicts where sourceTable matches.

        Returns:
            SQL CREATE TABLE IF NOT EXISTS statement string.
        """
        table_name = entity_def["tableName"]
        fields = entity_def.get("fields", [])

        lines: list[str] = []
        pk_columns: list[str] = []

        for field in fields:
            col_name = field["columnName"]
            sql_type = self._resolve_sql_type(field)
            parts: list[str] = [f"    `{col_name}` {sql_type}"]

            is_pk = field.get("isPrimaryKey", False)
            is_nullable = field.get("isNullable", True)

            if is_pk or not is_nullable:
                parts.append("NOT NULL")

            # AUTO_INCREMENT for BIGINT primary keys
            if is_pk and sql_type.upper().startswith("BIGINT"):
                parts.append("AUTO_INCREMENT")

            # DEFAULT CURRENT_TIMESTAMP for created_at/updated_at TIMESTAMP columns
            if sql_type.upper() == "TIMESTAMP":
                if col_name in ("created_at", "updated_at"):
                    parts.append("DEFAULT CURRENT_TIMESTAMP")
                if col_name == "updated_at":
                    parts.append("ON UPDATE CURRENT_TIMESTAMP")

            if is_pk:
                pk_columns.append(col_name)

            lines.append(" ".join(parts))

        # PRIMARY KEY constraint
        if pk_columns:
            pk_cols = ", ".join(f"`{c}`" for c in pk_columns)
            lines.append(f"    PRIMARY KEY ({pk_cols})")

        # FOREIGN KEY and INDEX constraints
        fk_lines = self._generate_foreign_keys(table_name, relationships)
        lines.extend(fk_lines)

        columns_sql = ",\n".join(lines)
        return (
            f"CREATE TABLE IF NOT EXISTS `{table_name}` (\n"
            f"{columns_sql}\n"
            f") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 "
            f"COLLATE=utf8mb4_unicode_ci;"
        )

    def _resolve_sql_type(self, field: dict) -> str:
        """Resolve SQL column type from field definition.

        Priority:
        1. columnDefinition verbatim (when non-empty string)
        2. JAVA_TO_SQL_FALLBACK[javaType]
        3. VARCHAR(255) with warning for unknown types

        Args:
            field: Field dict with columnDefinition, javaType, columnName.

        Returns:
            SQL type string.
        """
        col_def = field.get("columnDefinition", "")
        if col_def and isinstance(col_def, str) and col_def.strip():
            return col_def.strip()

        java_type = field.get("javaType", "")
        if java_type in self.JAVA_TO_SQL_FALLBACK:
            return self.JAVA_TO_SQL_FALLBACK[java_type]

        col_name = field.get("columnName", "unknown")
        field_name = field.get("fieldName", "unknown")
        print(f"WARNING: Unknown javaType '{java_type}' for field "
              f"'{field_name}' (column '{col_name}'). "
              f"Using VARCHAR(255) as default.")
        return "VARCHAR(255)"

    def _generate_foreign_keys(self, table_name: str,
                               relationships: list[dict]) -> list[str]:
        """Generate FOREIGN KEY and INDEX constraint lines for a table.

        Args:
            table_name: The source table name.
            relationships: List of relationship dicts for this table.

        Returns:
            List of SQL constraint line strings (with leading indent).
        """
        lines: list[str] = []
        for rel in relationships:
            fk_col = rel.get("foreignKey")
            if not fk_col:
                continue

            target_table = rel.get("targetTable", "")
            # Convention: FK references the primary key of the target table.
            # We use the FK column name as the reference column on the target
            # unless it's a standard pattern where the target PK is the FK name.
            # Standard convention: FK column on source references PK on target.
            # The target PK column name isn't stored in relationships, so we
            # reference the FK column name on the target (common pattern).
            fk_name = f"fk_{table_name}_{fk_col}"
            idx_name = f"idx_{table_name}_{fk_col}"

            lines.append(
                f"    CONSTRAINT `{fk_name}` "
                f"FOREIGN KEY (`{fk_col}`) "
                f"REFERENCES `{target_table}` (`{fk_col}`)"
            )
            lines.append(
                f"    INDEX `{idx_name}` (`{fk_col}`)"
            )

        return lines
