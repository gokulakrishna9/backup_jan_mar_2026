"""String conversion utilities for naming conventions."""

import re


def to_camel_case(name: str) -> str:
    """Convert snake_case or PascalCase to camelCase.

    Examples:
        'user_roles' -> 'userRoles'
        'UserRoles'  -> 'userRoles'
        'user'       -> 'user'
    """
    if "_" in name:
        parts = name.split("_")
        return parts[0].lower() + "".join(p.capitalize() for p in parts[1:])
    if name and name[0].isupper():
        return name[0].lower() + name[1:]
    return name


def to_pascal_case(name: str) -> str:
    """Convert snake_case or camelCase to PascalCase.

    Examples:
        'user_roles' -> 'UserRoles'
        'userRoles'  -> 'UserRoles'
        'user'       -> 'User'
    """
    if "_" in name:
        return "".join(p.capitalize() for p in name.split("_"))
    if name:
        return name[0].upper() + name[1:]
    return name


def to_snake_case(name: str) -> str:
    """Convert camelCase or PascalCase to snake_case.

    Examples:
        'UserRoles'  -> 'user_roles'
        'userRoles'  -> 'user_roles'
        'user_roles' -> 'user_roles'
    """
    if "_" in name:
        return name.lower()
    result = re.sub(r"([A-Z])", r"_\1", name).lstrip("_").lower()
    return result


def to_kebab_case(name: str) -> str:
    """Convert snake_case, camelCase, or PascalCase to kebab-case.

    Examples:
        'user_roles' -> 'user-roles'
        'UserRoles'  -> 'user-roles'
        'userRoles'  -> 'user-roles'
    """
    return to_snake_case(name).replace("_", "-")


def to_display_label(name: str) -> str:
    """Convert a field name to a human-readable display label.

    Examples:
        'firstName'  -> 'First Name'
        'user_roles' -> 'User Roles'
        'email'      -> 'Email'
    """
    snake = to_snake_case(name)
    return " ".join(p.capitalize() for p in snake.split("_"))
