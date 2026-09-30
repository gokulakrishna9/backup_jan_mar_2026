# Issue 003: Redux delete thunk key mismatch — missing removeEntity export

**Date:** 2026-04-01
**App:** job_portal
**Tool:** React definition builder script + REAW redux template
**Severity:** Critical

## Symptom
`The requested module '/src/store/slices/userProfileSlice.js' does not provide an export named 'removeUserProfile'` — causes blank pages on all routes.

## Root Cause
The builder script (`build_react_defs_phase2.py`) used `"remove": true` as the thunk key in `react_redux_store.json`, but the REAW Redux slice template checks `thunks['delete']`. The `remove` thunk was never generated.

## Fix
1. Fixed `react_redux_store.json` — renamed all `"remove": true` to `"delete": true`
2. Fixed `build_react_defs_phase2.py` — changed `thunks["remove"]` to `thunks["delete"]`

## Verification
- Redux slices now export `removeEntity` thunk for all 33 entities
- DataTable delete functionality works
