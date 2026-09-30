# Issue 012: Service NPE — user.getRoles() returns null

**Date:** 2026-04-03
**App:** job_portal
**Tool:** swfaw (auth_service_templates.py — JwtAuthenticationFilter)
**Severity:** Critical

## Symptom
`GET /api/education_levels` → 500: `Cannot invoke "java.util.List.contains(Object)" because "roles" is null`

## Root Cause
The `AuthUser` entity has a transient `roles` field, but the `JwtAuthenticationFilter` didn't populate it from the JWT. The service's `findAllPaged` called `user.getRoles()` which returned null.

## Fix
Updated the `JwtAuthenticationFilter` template to extract roles from the JWT token and set them on the `AuthUser` object before creating the authentication principal. Added `java.util.Map` import.

## Verification
- SUPER_ADMIN user can now GET and POST to all endpoints (200)
- 124 swfaw tests pass
