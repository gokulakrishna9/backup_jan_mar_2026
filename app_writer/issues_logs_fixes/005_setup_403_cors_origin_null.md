# Issue 005: POST /setup returns 403 from browser — CORS Origin: null

**Date:** 2026-04-01
**App:** job_portal
**Tool:** swfaw (security_templates.py, auth_service_templates.py, config_templates.py)
**Severity:** Critical

## Symptom
Browser form submission to POST `/setup` returns 403 Forbidden. Python requests work fine.

## Root Cause
Three compounding issues:

1. **WebFilter double-registration:** `JwtAuthenticationFilter` and `AuthorizationWebFilter` were annotated with `@Component` AND added to the security chain via `addFilterAt/addFilterAfter`. Spring WebFlux auto-registered them as global WebFilters, so they ran twice — once before Spring Security's `permitAll()` rules.

2. **CORS Origin: null:** Browsers send `Origin: null` for same-origin form submissions over HTTP. The CORS config only allowed `http://localhost:5173`, so `Origin: null` was rejected with 403.

3. **Redirect URL encoding:** The setup success redirect had unencoded spaces: `/login?message=Setup completed successfully. Please login.`

## Fix
1. Removed `@Component` from both `JwtAuthenticationFilter` and `AuthorizationWebFilter` templates. Created them as `@Bean` methods in `SecurityConfig` instead.
2. Added `"null"` and `"http://localhost:{port}"` to the default CORS allowed-origins in `config_templates.py`.
3. URL-encoded the redirect message in `setup_templates.py`.

**Files changed:**
- `swfaw/templates/auth_service_templates.py` — removed `@Component` from JwtAuthenticationFilter
- `swfaw/templates/authorization_service_templates.py` — removed `@Component` from AuthorizationWebFilter
- `swfaw/templates/security_templates.py` — added `@Bean` methods for both filters, added service/repository/auth package imports
- `swfaw/generators/security_generator.py` — added `servicePackage`, `repositoryPackage`, `authPackage` to template context
- `swfaw/templates/config_templates.py` — added `"null"` and backend origin to CORS allowed-origins
- `swfaw/templates/setup_templates.py` — URL-encoded redirect messages

## Verification
- Headless browser: POST /setup → 303 → /login with success message
- Swagger UI: still working (302 → 200)
- All 204 existing tests pass
