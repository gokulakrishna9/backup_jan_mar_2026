# Definition Editor

Standalone JSON CRUD tool for editing `application_definitions/` files — works with both `webflux_*.json` (swfaw) and `react_*.json` (REAW) definitions.

No dependency on swfaw or reaw modules.

## Usage

```bash
py definition_editor/cli.py --dir <path_to_application_definitions> <command> [args]
```

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `list` | List definition files | `list --prefix react` |
| `aliases` | Show alias → filename mappings | `aliases --prefix rx` |
| `get` | Read a value (entire file or path) | `get rx:theme colorPalette.accent` |
| `set` | Set a value at a path | `set rx:theme colorPalette.accent '"#2563eb"'` |
| `update` | Merge updates into an object | `update wf:metadata - '{"applicationName":"My App"}'` |
| `delete` | Delete a value at a path | `delete rx:theme source` |
| `append` | Append to an array | `append rx:routes - '{"path":"/new"}'` |
| `find` | Find first match in array | `find wf:entities entities '{"name":"ems_users"}'` |
| `filter` | Filter matches in array | `filter rx:routes - '{"pageType":"entity"}'` |
| `exists` | Check if file/path exists | `exists rx:theme colorPalette` |
| `diff` | Compare with another definitions dir | `diff rx:theme colorPalette --other /other/defs` |
| `backup` | Create timestamped backup | `backup rx:theme` |
| `restore` | Restore from backup | `restore react_theme.20260323_120000.bak.json` |

Use `-` for root-level paths in `update`, `append`, `find`, `filter`.

## Aliases

### WebFlux (`wf:`)
| Alias | File |
|-------|------|
| `wf:entity` | `webflux_entity_layer.json` |
| `wf:repository` | `webflux_repository_layer.json` |
| `wf:service` | `webflux_service_layer.json` |
| `wf:controller` | `webflux_controller_layer.json` |
| `wf:dto` | `webflux_dto_layer.json` |
| `wf:security` | `webflux_security_layer.json` |
| `wf:config` | `webflux_config_layer.json` |
| `wf:exception` | `webflux_exception_layer.json` |
| `wf:audit` | `webflux_audit_logging_layer.json` |
| `wf:authorization` | `webflux_authorization_layer.json` |
| `wf:custom_queries` | `webflux_custom_queries_layer.json` |
| `wf:group_definition` | `webflux_group_definition_layer.json` |
| `wf:manifest` | `webflux_manifest.json` |
| `wf:metadata` | `webflux_project_metadata.json` |
| `wf:entities` | `webflux_entities.json` |
| `wf:relationships` | `webflux_relationships.json` |

### React (`rx:`)
| Alias | File |
|-------|------|
| `rx:routes` | `react_routes.json` |
| `rx:auth` | `react_auth_config.json` |
| `rx:layout` | `react_layout.json` |
| `rx:components` | `react_component_mappings.json` |
| `rx:pages` | `react_page_definitions.json` |
| `rx:api` | `react_api_services.json` |
| `rx:redux` | `react_redux_store.json` |
| `rx:theme` | `react_theme.json` |
| `rx:charts` | `react_charts.json` |
| `rx:manifest` | `react_manifest.json` |
| `rx:groupings` | `react_form_groupings.json` |

## Python API

```python
from definition_editor.editor import DefinitionEditor

editor = DefinitionEditor("generated_application/my_app/application_definitions")

# Read
theme = editor.get("rx:theme")
accent = editor.get("rx:theme", "colorPalette.accent")

# Write
editor.set("rx:theme", "colorPalette.accent", "#2563eb")
editor.update("rx:theme", "typography", {"fontSize": "16px"})

# Search
user_route = editor.find("rx:routes", "", {"entityName": "User"})
entity_pages = editor.filter("rx:routes", "", {"pageType": "entity"})

# Backup/restore
bak = editor.backup("rx:theme")
editor.restore(bak)
```

## Path Syntax

- Dot notation: `colorPalette.accent`
- Array access: `entities[0].name`
- Combined: `routes[0].path`
