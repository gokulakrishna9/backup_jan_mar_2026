"""Dedicated Python methods for React code string construction.

These methods encapsulate the format rules and constraints for generating
React/JSX code strings used by REAW Jinja2 templates. Each method is
independently unit-testable without invoking the Jinja2 template engine.

Templates call these methods via the template context rather than containing
inline string construction logic. When a new generation rule is needed
(e.g., "date fields render a Calendar component"), it is added to the
relevant method here — not as inline logic in the template.

Field dict contract (matches REAW component field structure):
    {
        "fieldName": str,           # camelCase field name
        "fieldLabel": str,          # Human-readable label
        "componentType": str,       # PrimeReact component (InputText, InputNumber, etc.)
        "javaType": str,            # Backend Java type for prop type mapping
        "validation": dict | None,  # {required, minLength, maxLength, email, pattern, ...}
        "isRelationshipField": bool # True if this is a FK/autocomplete field
    }
"""

from typing import Optional


# ---------------------------------------------------------------------------
# Java type → JS PropTypes mapping
# ---------------------------------------------------------------------------

_JAVA_TO_PROPTYPE = {
    "String": "string",
    "Long": "number",
    "Integer": "number",
    "int": "number",
    "long": "number",
    "Double": "number",
    "Float": "number",
    "double": "number",
    "float": "number",
    "BigDecimal": "number",
    "Boolean": "bool",
    "boolean": "bool",
    "LocalDateTime": "string",
    "LocalDate": "string",
    "UUID": "string",
}

# Component types that should span full width in grid layouts
_FULL_WIDTH_COMPONENTS = frozenset({
    "InputTextarea",
    "QuillEditor",
    "MonacoEditor",
    "MarkdownEditor",
    "FileUpload",
})


def jsx_element(
    tag: str,
    props: dict,
    children: Optional[str] = None,
) -> str:
    """Generate a JSX element string.

    Format rules:
    - Self-closing syntax when ``children`` is ``None`` or empty.
    - Props are rendered as ``key="value"`` for strings, ``key={value}``
      for non-strings (booleans, numbers, expressions).
    - Boolean ``True`` props render as bare attributes (e.g., ``disabled``).
    - Boolean ``False`` props are omitted entirely.
    - ``None`` prop values are omitted.
    - Props are rendered in insertion order (dict order).
    - ``className`` is always rendered with quotes.

    Args:
        tag: The JSX tag name, e.g. ``"InputText"``, ``"div"``.
        props: Dict of prop name → value.
        children: Optional inner content string.

    Returns:
        A JSX element string.

    Examples::

        >>> jsx_element("InputText", {"id": "name", "disabled": True})
        '<InputText id="name" disabled />'
        >>> jsx_element("div", {"className": "card"}, "Hello")
        '<div className="card">Hello</div>'
        >>> jsx_element("Button", {"label": "Save", "onClick": "{handleSave}"})
        '<Button label="Save" onClick={handleSave} />'
    """
    prop_parts: list[str] = []

    for key, value in props.items():
        if value is None:
            continue
        if isinstance(value, bool):
            if value:
                prop_parts.append(key)
            # False booleans are omitted
            continue
        if isinstance(value, str):
            # Expression syntax: "{expression}" → key={expression}
            if value.startswith("{") and value.endswith("}"):
                prop_parts.append(f"{key}={value}")
            else:
                prop_parts.append(f'{key}="{value}"')
        elif isinstance(value, (int, float)):
            prop_parts.append(f"{key}={{{value}}}")
        else:
            prop_parts.append(f"{key}={{{value}}}")

    props_str = " ".join(prop_parts)
    space = " " if props_str else ""

    if children:
        return f"<{tag}{space}{props_str}>{children}</{tag}>"
    return f"<{tag}{space}{props_str} />"


def prop_type_declaration(
    name: str,
    type_str: str,
    required: bool = True,
) -> str:
    """Generate a PropTypes declaration line.

    Format rules:
    - Uses ``PropTypes.<type>`` syntax.
    - Appends ``.isRequired`` when ``required`` is ``True``.
    - Supported type strings: ``string``, ``number``, ``bool``, ``func``,
      ``object``, ``array``, ``node``, ``element``, ``any``.
    - For complex shapes, ``type_str`` can be a raw expression like
      ``"shape({ id: PropTypes.number })"``.

    Args:
        name: The prop name, e.g. ``"onSave"``.
        type_str: The PropTypes type, e.g. ``"func"``, ``"string"``.
        required: Whether to append ``.isRequired``.

    Returns:
        A single PropTypes declaration line.

    Examples::

        >>> prop_type_declaration("onSave", "func")
        'onSave: PropTypes.func.isRequired,'
        >>> prop_type_declaration("data", "object", required=False)
        'data: PropTypes.object,'
    """
    suffix = ".isRequired" if required else ""
    return f"{name}: PropTypes.{type_str}{suffix},"


def form_input(field: dict) -> str:
    """Generate a PrimeReact form input JSX string for a field.

    Format rules:
    - Wraps the input in a ``<div className="field">`` container with a
      ``<label>`` element.
    - Required fields show a red asterisk after the label.
    - Component type is determined by ``field["componentType"]``:
      ``InputText``, ``InputNumber``, ``InputTextarea``, ``Calendar``,
      ``Checkbox``, ``Dropdown``, ``AutoComplete``.
    - All inputs get ``id``, ``disabled={isDisabled}``, and error class
      binding via ``className={getErrorMessage(...) ? 'p-invalid' : ''}``.
    - ``InputTextarea`` gets ``rows={3}``.
    - ``Calendar`` with datetime mode gets ``showTime``.
    - Error message is rendered in a ``<small>`` tag below the input.

    Args:
        field: A dict with keys ``fieldName``, ``fieldLabel``,
               ``componentType``, and optionally ``validation``.

    Returns:
        A JSX string for the form field.

    Example::

        >>> result = form_input({
        ...     "fieldName": "email",
        ...     "fieldLabel": "Email",
        ...     "componentType": "InputText",
        ...     "validation": {"required": True}
        ... })
        >>> "label htmlFor" in result
        True
        >>> "InputText" in result
        True
    """
    name = field["fieldName"]
    label = field["fieldLabel"]
    comp = field["componentType"]
    validation = field.get("validation") or {}
    is_required = validation.get("required", False)

    # Label with optional required asterisk
    asterisk = ' <span className="p-error">*</span>' if is_required else ""
    label_jsx = f'<label htmlFor="{name}">{label}{asterisk}</label>'

    # Build the input component
    error_class = f"className={{getErrorMessage('{name}') ? 'p-invalid' : ''}}"

    if comp == "InputText":
        input_jsx = (
            f'<InputText id="{name}" {{...f}} value={{f.value || \'\'}} '
            f'disabled={{isDisabled}} {error_class} />'
        )
    elif comp == "InputNumber":
        input_jsx = (
            f'<InputNumber id="{name}" value={{f.value}} '
            f'onValueChange={{(e) => f.onChange(e.value)}} '
            f'disabled={{isDisabled}} {error_class} />'
        )
    elif comp == "InputTextarea":
        input_jsx = (
            f'<InputTextarea id="{name}" {{...f}} value={{f.value || \'\'}} '
            f'disabled={{isDisabled}} rows={{3}} {error_class} />'
        )
    elif comp == "Calendar":
        input_jsx = (
            f'<Calendar id="{name}" '
            f'value={{f.value ? new Date(f.value) : null}} '
            f'onChange={{(e) => f.onChange(e.value)}} '
            f'disabled={{isDisabled}} {error_class} />'
        )
    elif comp == "Checkbox":
        input_jsx = (
            f'<Checkbox id="{name}" checked={{!!f.value}} '
            f'onChange={{(e) => f.onChange(e.checked)}} '
            f'disabled={{isDisabled}} {error_class} />'
        )
    elif comp == "Dropdown":
        input_jsx = (
            f'<Dropdown id="{name}" value={{f.value}} options={{[]}} '
            f'onChange={{(e) => f.onChange(e.value)}} '
            f'disabled={{isDisabled}} {error_class} />'
        )
    elif comp == "AutoComplete":
        input_jsx = (
            f'<AutoComplete id="{name}" value={{f.value}} '
            f'suggestions={{[]}} completeMethod={{() => {{}}}} '
            f'onChange={{(e) => f.onChange(e.value)}} '
            f'disabled={{isDisabled}} {error_class} />'
        )
    else:
        # Fallback to InputText for unknown component types
        input_jsx = (
            f'<InputText id="{name}" {{...f}} value={{f.value || \'\'}} '
            f'disabled={{isDisabled}} {error_class} />'
        )

    # Error message
    error_jsx = (
        f"{{getErrorMessage('{name}') && "
        f'<small className="p-error">{{getErrorMessage(\'{name}\')}}</small>}}'
    )

    return (
        f'<div className="field">\n'
        f"  {label_jsx}\n"
        f"  {input_jsx}\n"
        f"  {error_jsx}\n"
        f"</div>"
    )


def api_endpoint_path(entity: str, action: str) -> str:
    """Generate a REST API endpoint path for an entity action.

    Format rules:
    - Base path is ``/api/<entity_lowercase>``.
    - ``getAll`` / ``create`` → base path only.
    - ``getById`` / ``update`` / ``delete`` → ``base_path/${id}``.
    - ``me`` (single-record-per-user) → ``base_path/me``.
    - Entity name is lowercased for the URL segment.
    - Custom actions append ``/<action>`` to the base path.

    Args:
        entity: The entity name, e.g. ``"UserProfile"``.
        action: The CRUD action: ``"create"``, ``"getAll"``, ``"getById"``,
                ``"update"``, ``"delete"``, ``"me"``, or a custom action name.

    Returns:
        The API endpoint path string.

    Examples::

        >>> api_endpoint_path("UserProfile", "getAll")
        '/api/userprofile'
        >>> api_endpoint_path("UserProfile", "getById")
        '/api/userprofile/${id}'
        >>> api_endpoint_path("UserProfile", "me")
        '/api/userprofile/me'
    """
    base = f"/api/{entity.lower()}"

    if action in ("getAll", "create"):
        return base
    if action in ("getById", "update", "delete"):
        return f"{base}/${{id}}"
    if action == "me":
        return f"{base}/me"
    # Custom action
    return f"{base}/{action}"


def column_header(field: dict) -> str:
    """Generate a PrimeReact DataTable Column header string.

    Format rules:
    - Uses ``field["fieldLabel"]`` if present.
    - Falls back to converting ``field["fieldName"]`` from camelCase to
      Title Case (e.g., ``"firstName"`` → ``"First Name"``).
    - Primary key fields are labeled as ``"ID"`` when no explicit label
      is provided and the field name ends with ``"id"`` (case-insensitive).

    Args:
        field: A dict with keys ``fieldName`` and optionally ``fieldLabel``,
               ``isPrimaryKey``.

    Returns:
        The column header string.

    Examples::

        >>> column_header({"fieldName": "firstName"})
        'First Name'
        >>> column_header({"fieldName": "id", "isPrimaryKey": True})
        'ID'
        >>> column_header({"fieldName": "email", "fieldLabel": "Email Address"})
        'Email Address'
    """
    # Explicit label takes priority
    if field.get("fieldLabel"):
        return field["fieldLabel"]

    name = field["fieldName"]

    # PK fields ending in "id"
    if field.get("isPrimaryKey") and name.lower().endswith("id"):
        return "ID"

    # camelCase → Title Case
    return _camel_to_title(name)


def route_path(entity: str) -> str:
    """Generate a React Router path for an entity page.

    Format rules:
    - Path is ``/<entity_lowercase>``.
    - Entity name is lowercased and used as-is (no pluralization — that
      is the responsibility of the route configuration, not this helper).
    - Detail routes append ``/:id``.

    Args:
        entity: The entity name, e.g. ``"UserProfile"``.

    Returns:
        The route path string for the entity's list page.

    Examples::

        >>> route_path("UserProfile")
        '/userprofile'
        >>> route_path("JobApplication")
        '/jobapplication'
    """
    return f"/{entity.lower()}"


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _camel_to_title(name: str) -> str:
    """Convert a camelCase string to Title Case with spaces.

    Examples::

        >>> _camel_to_title("firstName")
        'First Name'
        >>> _camel_to_title("createdAt")
        'Created At'
        >>> _camel_to_title("id")
        'Id'
    """
    if not name:
        return ""

    result: list[str] = [name[0].upper()]
    for char in name[1:]:
        if char.isupper():
            result.append(" ")
        result.append(char)

    return "".join(result)
