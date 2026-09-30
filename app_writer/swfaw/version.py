"""Version information for swfaw_v2."""

__version__ = "2.5.0"
__version_info__ = (2, 5, 0)

# Version history
# 2.5.0 - Removed dynamic SQL generation from authorization layer
# 2.4.0 - Query and filter layers for custom R2DBC queries
# 2.3.0 - Layer definitions with application-wide configurations
# 2.2.0 - Split definitions by layer (manifest, entities, relationships)
# 2.1.0 - Two-phase architecture
# 2.0.0 - Initial release

# Manifest version for application definitions
MANIFEST_VERSION = "2.5"

# Supported manifest versions for backward compatibility
SUPPORTED_MANIFEST_VERSIONS = ["2.2", "2.3", "2.4", "2.5"]
