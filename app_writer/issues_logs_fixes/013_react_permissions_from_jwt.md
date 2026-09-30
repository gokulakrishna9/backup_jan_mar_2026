# Issue 013: React usePermissions returns false for all — blocks view/edit/delete

**Date:** 2026-04-03
**App:** job_portal
**Tool:** REAW (permission_templates.py)
**Severity:** Critical

## Symptom
All permission checks (canView, canUpdate, canCreate, canDelete) return false. DataTable action menu shows no options. Form edit doesn't work.

## Root Cause
The `usePermissions` hook relied on `allowedApiList` from `AuthContext`, which was fetched from `/api/auth/permissions`. This endpoint returned empty/wrong data, so all permissions were false.

## Fix
Replaced the `allowedApiList`-based permission check with JWT claim decoding:
- Decode JWT from localStorage
- Extract `roles` and `tableAccess` claims
- SUPER_ADMIN: full access to everything
- TABLE_ADMIN: check `tableAccess` map for the specific table
- USER: allow all operations (backend service layer handles record-level filtering)

No more dependency on `/api/auth/permissions` endpoint.

## Verification
- 18 REAW tests pass
- SUPER_ADMIN user sees all action buttons (View, Edit, Delete)
- Form edit mode works when clicking Edit
