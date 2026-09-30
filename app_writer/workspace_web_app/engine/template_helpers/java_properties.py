"""Dedicated Python methods for Java code string construction.

These methods encapsulate the format rules and constraints for generating
Java code strings used by swfaw Jinja2 templates. Each method is independently
unit-testable without invoking the Jinja2 template engine.

Templates call these methods via the template context rather than containing
inline string construction logic. When a new generation rule is needed
(e.g., "enum fields generate @Enumerated annotation"), it is added to the
relevant method here — not as inline logic in the template.

Field dict contract (matches swfaw/models/layer_objects.py Field):
    {
        "fieldName": str,       # camelCase Java field name
        "javaType": str,        # Java type (String, Long, LocalDateTime, etc.)
        "columnName": str,      # snake_case DB column name
        "isPrimaryKey": bool,   # True if this is the @Id field
        "isNullable": bool,     # True if the column allows NULL
        "columnDefinition": str # Raw column definition (optional)
    }
"""

from typing import Optional


# ---------------------------------------------------------------------------
# Java type mapping helpers
# ---------------------------------------------------------------------------

# Types that use "is" prefix for boolean getters per JavaBean convention
_BOOLEAN_TYPES = frozenset({"boolean", "Boolean"})

# Primitive-to-wrapper mapping for generics / Optional usage
_PRIMITIVE_TO_WRAPPER = {
    "int": "Integer",
    "long": "Long",
    "double": "Double",
    "float": "Float",
    "boolean": "Boolean",
    "char": "Character",
    "byte": "Byte",
    "short": "Short",
}


def field_declaration(field: dict) -> str:
    """Generate a Java field declaration with optional annotations.

    Format rules:
    - Primary key fields are prefixed with ``@Id``.
    - All fields get ``@Column("column_name")`` annotation.
    - The declaration follows ``private <Type> <name>;`` convention.
    - Nullable reference types are NOT wrapped in Optional (Lombok @Data
      generates plain getters/setters; nullability is a DB concern).

    Args:
        field: A dict with keys ``fieldName``, ``javaType``, ``columnName``,
               ``isPrimaryKey``.

    Returns:
        A multi-line string containing annotations and the field declaration.

    Example::

        >>> field_declaration({"fieldName": "id", "javaType": "Long",
        ...     "columnName": "id", "isPrimaryKey": True, "isNullable": False})
        '@Id\\n    @Column("id")\\n    private Long id;'
    """
    lines: list[str] = []

    if field.get("isPrimaryKey"):
        lines.append("@Id")

    lines.append(f'@Column("{field["columnName"]}")')
    lines.append(f'private {field["javaType"]} {field["fieldName"]};')

    return "\n    ".join(lines)


def getter_signature(field: dict) -> str:
    """Generate a Java getter method signature (without body).

    Format rules:
    - Boolean fields (``boolean`` / ``Boolean``) use the ``is`` prefix
      per JavaBean specification.
    - All other types use the ``get`` prefix.
    - The field name's first character is uppercased after the prefix.
    - Return type matches ``field["javaType"]`` exactly.

    Args:
        field: A dict with keys ``fieldName``, ``javaType``.

    Returns:
        The getter method signature, e.g. ``public String getName()``.

    Example::

        >>> getter_signature({"fieldName": "active", "javaType": "boolean"})
        'public boolean isActive()'
        >>> getter_signature({"fieldName": "name", "javaType": "String"})
        'public String getName()'
    """
    java_type = field["javaType"]
    name = field["fieldName"]
    capitalized = name[0].upper() + name[1:] if name else ""

    prefix = "is" if java_type in _BOOLEAN_TYPES else "get"
    return f"public {java_type} {prefix}{capitalized}()"


def setter_signature(field: dict) -> str:
    """Generate a Java setter method signature (without body).

    Format rules:
    - Always uses the ``set`` prefix regardless of type.
    - The field name's first character is uppercased after the prefix.
    - Parameter type matches ``field["javaType"]`` exactly.
    - Parameter name matches ``field["fieldName"]`` exactly.

    Args:
        field: A dict with keys ``fieldName``, ``javaType``.

    Returns:
        The setter method signature,
        e.g. ``public void setName(String name)``.

    Example::

        >>> setter_signature({"fieldName": "name", "javaType": "String"})
        'public void setName(String name)'
    """
    java_type = field["javaType"]
    name = field["fieldName"]
    capitalized = name[0].upper() + name[1:] if name else ""

    return f"public void set{capitalized}({java_type} {name})"


def import_statement(class_name: str, package: str) -> str:
    """Generate a Java import statement.

    Format rules:
    - Follows ``import <package>.<ClassName>;`` format.
    - No wildcard imports — each class is imported explicitly.
    - The package should NOT include a trailing dot.
    - The class_name should be the simple (unqualified) class name.

    Args:
        class_name: Simple class name, e.g. ``"LocalDateTime"``.
        package: Fully qualified package, e.g. ``"java.time"``.

    Returns:
        A complete import statement string.

    Example::

        >>> import_statement("LocalDateTime", "java.time")
        'import java.time.LocalDateTime;'
    """
    return f"import {package}.{class_name};"


def annotation_string(annotation: str, params: Optional[dict] = None) -> str:
    """Generate a Java annotation string.

    Format rules:
    - Annotation name is prefixed with ``@`` if not already present.
    - When ``params`` is ``None`` or empty, produces ``@AnnotationName``.
    - When ``params`` has a single ``"value"`` key, uses shorthand:
      ``@AnnotationName(value)`` (no ``value =``).
    - When ``params`` has multiple keys, produces
      ``@AnnotationName(key1 = val1, key2 = val2)`` with alphabetical
      key ordering for deterministic output.
    - String parameter values are wrapped in double quotes.
    - Boolean and numeric values are rendered as-is.
    - ``None`` values are skipped.

    Args:
        annotation: Annotation name, e.g. ``"Column"`` or ``"@Column"``.
        params: Optional dict of annotation parameters.

    Returns:
        The annotation string.

    Examples::

        >>> annotation_string("Override")
        '@Override'
        >>> annotation_string("Column", {"nullable": False})
        '@Column(nullable = false)'
        >>> annotation_string("Query", {"value": "SELECT * FROM users"})
        '@Query("SELECT * FROM users")'
        >>> annotation_string("ApiResponse", {"responseCode": "200", "description": "OK"})
        '@ApiResponse(description = "OK", responseCode = "200")'
    """
    name = annotation if annotation.startswith("@") else f"@{annotation}"

    if not params:
        return name

    # Filter out None values
    filtered = {k: v for k, v in params.items() if v is not None}
    if not filtered:
        return name

    # Single "value" key uses shorthand
    if list(filtered.keys()) == ["value"]:
        return f"{name}({_format_annotation_value(filtered['value'])})"

    # Multiple params — alphabetical for deterministic output
    parts = []
    for key in sorted(filtered.keys()):
        parts.append(f"{key} = {_format_annotation_value(filtered[key])}")

    return f"{name}({', '.join(parts)})"


def _format_annotation_value(value) -> str:
    """Format a single annotation parameter value.

    - str → quoted with double quotes
    - bool → Java literal (true/false)
    - int/float → as-is
    - list → Java array literal {v1, v2, ...}
    """
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return f'"{value}"'
    if isinstance(value, list):
        items = ", ".join(_format_annotation_value(v) for v in value)
        return "{" + items + "}"
    return str(value)


def constructor_param(field: dict) -> str:
    """Generate a Java constructor parameter.

    Format rules:
    - Follows ``<Type> <name>`` format (no annotations).
    - Uses the wrapper type for primitives when the field is nullable
      (e.g., ``int`` → ``Integer`` when nullable).
    - Non-nullable primitives keep their primitive type.

    Args:
        field: A dict with keys ``fieldName``, ``javaType``, and
               optionally ``isNullable``.

    Returns:
        A constructor parameter string, e.g. ``String name``.

    Example::

        >>> constructor_param({"fieldName": "count", "javaType": "int",
        ...     "isNullable": True})
        'Integer count'
        >>> constructor_param({"fieldName": "name", "javaType": "String",
        ...     "isNullable": False})
        'String name'
    """
    java_type = field["javaType"]
    is_nullable = field.get("isNullable", True)

    # Promote primitives to wrappers when nullable
    if is_nullable and java_type in _PRIMITIVE_TO_WRAPPER:
        java_type = _PRIMITIVE_TO_WRAPPER[java_type]

    return f"{java_type} {field['fieldName']}"


def repository_method_signature(
    method_name: str,
    return_type: str,
    params: list[dict],
) -> str:
    """Generate a Spring Data repository method signature.

    Format rules:
    - Return type is a reactive type: ``Mono<T>`` or ``Flux<T>``.
    - Parameters follow ``<Type> <name>`` format, comma-separated.
    - No ``@Query`` annotation — that is handled separately by the
      template or by ``annotation_string()``.
    - Method name follows Spring Data naming conventions
      (``findBy...``, ``countBy...``, ``deleteBy...``).

    Args:
        method_name: The method name, e.g. ``"findByEmail"``.
        return_type: The full return type including reactive wrapper,
                     e.g. ``"Mono<User>"``, ``"Flux<User>"``,
                     ``"Mono<Long>"``.
        params: A list of dicts, each with ``"name"`` and ``"type"`` keys.

    Returns:
        The method signature string.

    Example::

        >>> repository_method_signature(
        ...     "findByEmail",
        ...     "Mono<User>",
        ...     [{"name": "email", "type": "String"}]
        ... )
        'Mono<User> findByEmail(String email);'
        >>> repository_method_signature(
        ...     "findAllPaged",
        ...     "Flux<User>",
        ...     [{"name": "size", "type": "int"}, {"name": "offset", "type": "long"}]
        ... )
        'Flux<User> findAllPaged(int size, long offset);'
    """
    param_strs = [f'{p["type"]} {p["name"]}' for p in params]
    return f"{return_type} {method_name}({', '.join(param_strs)});"
