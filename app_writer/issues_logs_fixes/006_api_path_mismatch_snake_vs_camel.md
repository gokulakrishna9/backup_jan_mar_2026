# Issue 006: API path mismatch — React uses snake_case, backend uses camelCase

**Date:** 2026-04-02
**App:** job_portal
**Tool:** swfaw controller generator + React definition builder
**Severity:** Critical

## Symptom
`404 NOT_FOUND "No static resource api/user_profiles."` when React app calls backend API.

## Root Cause
The scaffolder generates `basePath` in snake_case (`/api/user_profiles`) in `webflux_controller_layer.json`. But the swfaw controller generator strips underscores when generating Java code, producing `@RequestMapping("/api/userprofiles")`. The React API services used the definition paths (snake_case), causing a mismatch.

## Fix (data-level)
Updated `react_api_services.json` basePaths to match the actual generated controller paths (no underscores). 28 paths updated.

## Root cause fix needed (task #27)
The swfaw controller generator or scaffolder needs to be aligned so the definition basePath matches what gets generated. Either:
- Scaffolder should generate camelCase paths to match the controller output
- Or the controller generator should preserve the basePath as-is from the definition

## Verification
- React services now call `/api/userprofiles` matching the backend
- All 33 entity API paths aligned
