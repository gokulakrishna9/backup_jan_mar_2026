"""Storage abstraction layer for application definitions.

Provides interchangeable backends (JSON files or MySQL database)
that both produce the same objects the generators consume.
"""

from .base import DefinitionStore
from .json_store import JsonStore

# DbStore requires mysql-connector-python; import lazily to avoid
# crashing when only JSON storage is needed.
try:
    from .db_store import DbStore
except ImportError:
    DbStore = None

__all__ = [
    'DefinitionStore',
    'JsonStore',
    'DbStore',
]
