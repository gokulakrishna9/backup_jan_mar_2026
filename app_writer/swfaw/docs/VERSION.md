# Version History

## Version 2.3.0 (Current)

**Release Date:** March 11, 2026  
**Status:** ✅ Production Ready

### New Features

#### Layer Definitions System
Complete control over code generation through customizable JSON configuration files.

**15 Definition Files Generated:**
- 4 core files (manifest, metadata, entities, relationships)
- 5 per-entity layers (entity, repository, service, controller, DTO)
- 6 application-wide layers (security, config, exception, audit, authorization, custom queries)

**Key Capabilities:**
- Customize validation messages per field
- Enable/disable endpoints per controller
- Configure JWT, OAuth2, CORS, password policies
- Configure database, server, logging settings
- Define custom exceptions and error messages
- Configure audit logging events and alerting
- Configure document-based access control
- Define custom authorization queries

**Benefits:**
- Intelligent defaults generated from SQL schema
- Review and modify before code generation
- Version control for application structure
- Team collaboration on configurations
- Fast regeneration without re-parsing SQL

### Changes from v2.2

1. **Phase 1 Output**: Now generates 15 files instead of 4
2. **Customization**: Users can modify layer definitions between Phase 1 and Phase 2
3. **Backward Compatible**: v2.2 applications continue to work (legacy mode)
4. **Version Management**: Centralized version.py file

### Files Modified

- `utils/layer_definition_generator.py` - Added 6 application-wide generators
- `utils/definition_splitter.py` - Updated to use centralized version
- `phase1_generate_definition.py` - Added version display
- `phase2_generate_code.py` - Added version display
- `main.py` - Fixed DTO field loading for layer definitions
- `version.py` - NEW: Centralized version management

### Documentation

- `docs/TWO_PHASE_ARCHITECTURE.md` - Updated with v2.3 layer definitions
- `docs/LAYER_DEFINITIONS_GUIDE.md` - NEW: Comprehensive guide (200+ lines)
- `docs/VERSION.md` - NEW: This file

---

## Version 2.2.0

**Release Date:** March 10, 2026  
**Status:** ✅ Production Ready

### Features

- Split application definitions by layer
- 4 definition files: manifest, metadata, entities, relationships
- Two-phase architecture (definition generation + code generation)
- Backward compatible with v2.1

### Files Generated

1. `manifest.json` - Version and file index
2. `project_metadata.json` - Project and database configuration
3. `entities.json` - All table definitions
4. `relationships.json` - Entity relationships

---

## Version 2.1.0

**Release Date:** February 2026

### Features

- Two-phase architecture introduced
- Phase 1: Generate application definition
- Phase 2: Generate code from definition
- Single `application_definition.json` file

---

## Version 2.0.0

**Release Date:** January 2026

### Features

- Initial release of swfaw_v2
- Spring WebFlux application generator
- R2DBC support
- JWT authentication
- Document-based authorization
- Audit logging
- Admin UI

---

## Version Compatibility

### Manifest Versions

- **2.3**: Layer definitions with application-wide configurations (current)
- **2.2**: Split definitions by layer (4 files)
- **2.1**: Single application_definition.json

### Backward Compatibility

Phase 2 automatically detects the manifest version and uses the appropriate generation mode:
- v2.3: Uses layer definitions (customizable)
- v2.2: Falls back to transformer-based generation (legacy mode)

### Migration Path

To upgrade from v2.2 to v2.3:
```bash
# Simply run Phase 1 again with your SQL schema
python phase1_generate_definition.py --input schema.sql --output ../generated_application/my_app
```

This generates the new layer definition files. Your existing v2.2 applications continue to work.

---

## Roadmap

### Version 2.4 (Planned)

- Generator updates to use additional layer definition properties
- Custom validation message support in DTO generator
- Endpoint enable/disable support in controller generator
- Custom query support in repository generator
- JSON schema validation for layer definitions

### Version 3.0 (Future)

- React frontend generator integration
- GraphQL API support
- Microservices architecture support
- Docker and Kubernetes deployment configs
- CI/CD pipeline generation

---

## Checking Your Version

### Command Line
```bash
cd emotisense-ai/swfaw_v2
python -c "from version import __version__; print(__version__)"
```

### In Code
```python
from version import __version__, MANIFEST_VERSION

print(f"swfaw_v2 version: {__version__}")
print(f"Manifest version: {MANIFEST_VERSION}")
```

### Generated Applications
Check the `manifest.json` file in `application_definitions/`:
```json
{
  "version": "2.3",
  "format": "split",
  ...
}
```

---

## Support

For issues, questions, or feature requests related to specific versions, please include:
- swfaw_v2 version (from `version.py`)
- Manifest version (from `manifest.json`)
- Python version
- Operating system

---

## License

swfaw_v2 is proprietary software. All rights reserved.
