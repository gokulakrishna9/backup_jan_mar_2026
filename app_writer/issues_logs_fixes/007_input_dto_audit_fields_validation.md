# Issue 007: Input DTO includes audit/soft-delete fields — 400 validation error

**Date:** 2026-04-02
**App:** job_portal
**Tool:** Application definitions (webflux_entity_layer.json)
**Severity:** Critical

## Symptom
`400 Bad Request` with `createdAt is required, isDeleted is required` when submitting form data.

## Root Cause
The scaffolder added `isDeleted` as an explicit field in `webflux_entity_layer.json`. The service generator's audit exclusion list includes `createdAt`, `updatedAt`, `deletedAt` but NOT `isDeleted`. So the service template generated `inputDTO.getIsDeleted()` — a method that doesn't exist on the Input DTO.

The entity template already adds `deletedAt` via `hasSoftDelete: true`, making the explicit `isDeleted` field redundant and harmful.

## Fix (definition layer)
Removed `isDeleted` from all 33 entity field lists in `webflux_entity_layer.json` and `is_deleted` columns from `webflux_entities.json`. The `hasSoftDelete: true` flag handles soft-delete generation.

However, the full fix requires that Phase 3's `generate_application` reads definitions from `application_definitions/` (source of truth) rather than `output_dir/application_definitions/` (legacy path). The legacy `generate_from_layer_definitions` function also expects fields (`isRootEntity`, `hasPublicFlag`, `corsConfig.maxAge`) that the App Def Manager scaffolder doesn't produce.

**Pending:** Need to either fix the scaffolder to produce all required fields, or fix Phase 3 to read from the correct directory. Both are swfaw changes.

## Verification
- Input DTOs no longer contain audit/soft-delete fields
- Services no longer reference `inputDTO.getIsDeleted()`
- Build succeeds, 124 swfaw tests pass
