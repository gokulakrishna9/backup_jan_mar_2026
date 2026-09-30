# Issue 008: Repository SQL uses wrong table/column names — ems_ prefix and missing underscores

**Date:** 2026-04-02
**App:** job_portal
**Tool:** swfaw (repository_generator.py, layer_objects.py)
**Severity:** Critical

## Symptom
`bad SQL grammar [SELECT * FROM ems_user_profile WHERE userprofile_id IN ...]` — table doesn't exist.

## Root Cause
The repository generator derived table name as `ems_` + camelToSnake(entityName) and ID column as entityName.lower() + `_id`. But the actual tables (created by the scaffolder) use plain snake_case without `ems_` prefix, and ID columns use `{table_name}_id` with underscores.

## Fix
1. Added `tableName` and `idColumn` optional fields to `RepositoryLayerObject` in `layer_objects.py`
2. Updated `repository_generator.py` to use definition-provided values when available, falling back to legacy derivation
3. Updated `main.py` and `incremental_generator.py` to pass `tableName` and `idColumn` from the entity layer definition when constructing `RepositoryLayerObject`

## Verification
- Generated SQL now uses `user_profile` (not `ems_user_profile`) and `user_profile_id` (not `userprofile_id`)
- 124 swfaw tests pass
- Build succeeds
