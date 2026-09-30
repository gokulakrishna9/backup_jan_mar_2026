"""Java/SQL type to React component mapping."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ComponentMapping:
    """Result of mapping a Java/SQL type to a PrimeReact component."""
    component_type: str
    prime_react_import: str
    mode: Optional[str] = None


# Java/SQL type → PrimeReact component mapping
_TYPE_MAP = {
    # String types
    "String": ComponentMapping("InputText", "primereact/inputtext"),
    "VARCHAR": ComponentMapping("InputText", "primereact/inputtext"),
    # Numeric types
    "Long": ComponentMapping("InputNumber", "primereact/inputnumber", "decimal"),
    "Integer": ComponentMapping("InputNumber", "primereact/inputnumber", "decimal"),
    "int": ComponentMapping("InputNumber", "primereact/inputnumber", "decimal"),
    "BigDecimal": ComponentMapping("InputNumber", "primereact/inputnumber", "decimal"),
    "DECIMAL": ComponentMapping("InputNumber", "primereact/inputnumber", "decimal"),
    "INT": ComponentMapping("InputNumber", "primereact/inputnumber", "decimal"),
    "BIGINT": ComponentMapping("InputNumber", "primereact/inputnumber", "decimal"),
    "Float": ComponentMapping("InputNumber", "primereact/inputnumber", "decimal"),
    "Double": ComponentMapping("InputNumber", "primereact/inputnumber", "decimal"),
    # Date types
    "LocalDate": ComponentMapping("Calendar", "primereact/calendar", "date"),
    "DATE": ComponentMapping("Calendar", "primereact/calendar", "date"),
    "LocalDateTime": ComponentMapping("Calendar", "primereact/calendar", "datetime"),
    "TIMESTAMP": ComponentMapping("Calendar", "primereact/calendar", "datetime"),
    # Boolean types
    "Boolean": ComponentMapping("Checkbox", "primereact/checkbox"),
    "boolean": ComponentMapping("Checkbox", "primereact/checkbox"),
    "TINYINT(1)": ComponentMapping("Checkbox", "primereact/checkbox"),
    "Byte": ComponentMapping("Checkbox", "primereact/checkbox"),
    # Text types
    "TEXT": ComponentMapping("InputTextarea", "primereact/inputtextarea"),
}


class TypeMapper:
    """Maps Java/SQL types to PrimeReact components."""

    @staticmethod
    def map_to_component(
        java_type: str,
        column_definition: str = "",
        relationship_type: Optional[str] = None,
        is_link_entity: bool = False,
    ) -> ComponentMapping:
        """Map a Java/SQL type to its corresponding PrimeReact component.

        Args:
            java_type: The Java type (e.g., 'String', 'Long', 'LocalDate').
            column_definition: The SQL column definition for ENUM detection.
            relationship_type: If set, indicates this is a FK field
                ('MANY_TO_ONE', 'ONE_TO_MANY', 'MANY_TO_MANY').
            is_link_entity: True if the related entity is a link (m2m) entity.

        Returns:
            ComponentMapping with component_type, prime_react_import, and mode.
        """
        # Foreign key fields → AutoComplete
        if relationship_type in ("ManyToOne", "OneToMany", "ManyToMany",
                                 "MANY_TO_ONE", "ONE_TO_MANY", "MANY_TO_MANY") or is_link_entity:
            mode = "multiple" if is_link_entity or relationship_type in ("ManyToMany", "MANY_TO_MANY") else "single"
            return ComponentMapping("AutoComplete", "primereact/autocomplete", mode)

        # ENUM detection from column definition
        if column_definition and "ENUM" in column_definition.upper():
            return ComponentMapping("Dropdown", "primereact/dropdown", "enum")

        # Direct type lookup
        if java_type in _TYPE_MAP:
            return _TYPE_MAP[java_type]

        # Fallback: check column_definition for SQL types
        col_upper = column_definition.upper().strip()
        for sql_type, mapping in _TYPE_MAP.items():
            if col_upper.startswith(sql_type.upper()):
                return mapping

        # Default to InputText
        return ComponentMapping("InputText", "primereact/inputtext")
