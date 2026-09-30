# Issue 009: Soft-delete column mismatch — is_deleted vs deleted_at vs none

**Date:** 2026-04-02
**App:** job_portal
**Tool:** app_def_manager (scaffolder.py, crud.py), swfaw
**Severity:** Critical

## Symptom
`bad SQL grammar [SELECT * FROM user_profile WHERE ... AND deleted_at IS NULL]` — column doesn't exist.

## Root Cause
Three-way mismatch:
- Scaffolder created `is_deleted BOOLEAN` column
- swfaw entity/repository templates expected `deleted_at TIMESTAMP`
- DDL generator didn't add any soft-delete column

Meanwhile, the activity tracking system already handles deleted record backup via `deleted_record` table with full JSON recovery.

## Fix
Removed soft-delete entirely from the application definition layer:
- Scaffolder: no longer generates `is_deleted` field or `hasSoftDelete: true`
- CRUD: no longer adds `is_deleted` to entity/column/DTO definitions
- Existing job_portal definitions: set `hasSoftDelete: false` on all entities, removed `isDeleted` fields
- Tests: updated to not expect `is_deleted`

Delete flow now: service saves record JSON to `deleted_record` → hard-deletes from entity table.

## Verification
- 62 app_def_manager tests pass
- No `deleted_at` or `is_deleted` in generated SQL or Java code
