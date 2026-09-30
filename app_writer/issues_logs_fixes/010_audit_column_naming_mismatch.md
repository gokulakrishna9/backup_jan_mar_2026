# Issue 010: Audit column naming mismatch — created_by_id/created_on vs created_at

**Date:** 2026-04-02
**App:** job_portal
**Tool:** swfaw (entity_templates.py, service_templates.py, service_generator.py)
**Severity:** Critical

## Symptom
`bad SQL grammar [INSERT INTO user_profile (first_name, ..., created_by_id, updated_by_id, created_on, updated_on)]` — columns don't exist.

## Root Cause
swfaw entity/service templates generated `created_by_id`, `updated_by_id`, `created_on`, `updated_on` for audit fields. But the scaffolder creates `created_at`, `updated_at` only. The `created_by_id`/`updated_by_id` are redundant because `record_owner` tracks ownership and `crud_activity_log` tracks who did what.

## Fix
Updated swfaw templates to use `created_at`/`updated_at` matching the scaffolder:
- `entity_templates.py`: `@Column("created_at")` / `@Column("updated_at")` only
- `service_templates.py`: `.createdAt(LocalDateTime.now())` / `.updatedAt(LocalDateTime.now())` in create/update
- `service_generator.py`: added `isDeleted` to audit field exclusion list

## Verification
- 124 swfaw tests pass
- Build succeeds
- INSERT uses `created_at, updated_at` matching the database schema
