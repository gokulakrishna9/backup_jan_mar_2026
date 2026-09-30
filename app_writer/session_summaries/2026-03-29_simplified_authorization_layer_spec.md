# Session 2026-03-29 — Simplified Authorization Layer Spec (Tasks 1–8)

## Spec

`.kiro/specs/simplified-authorization-layer/` — Replaces swfaw's complex document-group-based authorization system (13+ tables, 9 group types, 8 ACL boolean flags) with a simplified role-based model (8 auth tables, 3 roles, JWT-embedded claims, annotation-based WebFilter).

## Completed Tasks

| Task | What Changed |
|------|-------------|
| 1.1 | Rewrote `auth_schema_templates.py` — removed 13 old table DDLs + `is_super_user` column, added 6 new tables (user_role, record_owner, query_group, query_group_query, query_group_member, query_group_record) |
| 1.2 | Rewrote `auth_schema_generator.py` — removed 7 old INSERT methods, simplified `generate()` to static DDL |
| 1.3 | Created `swfaw/tests/test_auth_schema_properties.py` — 4 hypothesis tests (Properties 1, 2) |
| 2 | Checkpoint passed — 4/4 tests |
| 3.1 | Rewrote `auth_entity_templates.py` — removed 13 old entity templates + `isSuperUser`, added 6 new entity templates |
| 3.2 | Rewrote `auth_entity_generator.py` — removed old methods, added 6 new generate methods |
| 4.1 | Rewrote `auth_repository_templates.py` — removed 13 old repo templates + `findByIsSuperUser`, added 6 new repo templates |
| 4.2 | Rewrote `auth_repository_generator.py` — removed old methods, added 6 new generate methods |
| 5 | Checkpoint passed — 4/4 tests |
| 6.1 | Replaced `authorization_service_templates.py` — removed 5 old templates, added ROLE_AUTHORIZATION_SERVICE, AUTHORIZATION_WEB_FILTER, 3 annotation templates |
| 6.2 | Rewrote `authorization_service_generator.py` — removed 5 old methods, added 5 new generate methods |
| 6.3 | Added to `swfaw/tests/test_authorization_service_properties.py` — 11 tests (Properties 4, 5) |
| 6.4 | Added to same test file — 26 tests (Properties 7, 14, 15) |
| 7.1 | Updated `jwt_templates.py` — generateToken now accepts roles/tableAccess/queryGroupMemberships, added 3 extract methods |
| 7.2 | Created `swfaw/tests/test_jwt_properties.py` — 21 tests (Property 3) |
| 8 | Checkpoint passed — 62/62 tests |

## Resume Point

**Next task: 9** — Update controller templates with authorization annotations (@EntityTable, @TableAccess, @QueryAccess).

Remaining tasks: 9–18 (controller templates, service templates, permissions, audit logging, security config, auth service registration, main pipeline wiring, final checkpoint).

## Files Modified

- `swfaw/templates/auth_schema_templates.py`
- `swfaw/generators/auth_schema_generator.py`
- `swfaw/templates/auth_entity_templates.py`
- `swfaw/generators/auth_entity_generator.py`
- `swfaw/templates/auth_repository_templates.py`
- `swfaw/generators/auth_repository_generator.py`
- `swfaw/templates/authorization_service_templates.py`
- `swfaw/generators/authorization_service_generator.py`
- `swfaw/templates/jwt_templates.py`

## Files Created

- `swfaw/tests/test_auth_schema_properties.py` (4 tests)
- `swfaw/tests/test_authorization_service_properties.py` (37 tests)
- `swfaw/tests/test_jwt_properties.py` (21 tests)

## Notes

- `main.py` still references old generator methods — will be fixed in Task 17.1
- `auth_service_templates.py` still uses old 2-arg `generateToken` signature — will be fixed in Task 15.1
- All property tests use `hypothesis` with `@settings(max_examples=100)` and direct `importlib` imports to avoid pypika dependency issues
- Python command is `python` (not `py`) on this machine
