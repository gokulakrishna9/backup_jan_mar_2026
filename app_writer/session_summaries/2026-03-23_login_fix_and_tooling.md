# Session 2026-03-23: Login Fix & Tooling Updates

## DB Manager — `query` subcommand
- Wired up `query` subcommand in `db_manager/db_manager.py` `main()` with `--json` flag
- `query_database()` function was already implemented in prior session; this just connected it to the CLI

## Database Reload
- Old data had plain-text passwords (length 10) instead of BCrypt hashes (length 60)
- Dropped and recreated `ems_recruitment_portal` database via DB Manager
- Generated fresh dummy data (`ems_recruitment_portal_20260323_205854`) via Dummy Data Generator
- Loaded new data via DB Manager `execute` subcommand
- Activated admin user `stephentaylor` / `A1kNLTRw&4` (both `is_super_user=1`, `is_active=1`)

## React Login "Invalid Credentials" Fix
Two issues found and fixed:

1. **REAW template (`reaw/templates/auth_templates.py`)** — `LoginPage.jsx` expected `{ token, refreshToken, user }` but backend returns flat `{ token, userId, username, email, isSuperUser }`. Fixed `handleLogin` to destructure the flat response and build the user object client-side. `refreshToken` defaults to `null` since swfaw doesn't issue one yet.

2. **swfaw CORS config (`swfaw/templates/config_templates.py`)** — CORS was disabled by default (`cors.enabled: false`). Browser blocked cross-origin requests from `localhost:5173` → `localhost:8081`. Changed default to `cors.enabled: true` with `http://localhost:5173` as allowed origin, `allow-credentials: true`, and standard methods/headers.

Both apps regenerated with swfaw + REAW after template fixes. Backend validator confirms login HTTP 200.

## Steering Updates
- Added Rule 5: never use raw shell commands when a workspace tool exists
- Added Workspace Layout table mapping all folders to their purpose
- Added `query database` to phrase mapping table

## Known Gaps (for future)
- No `/api/auth/refresh` endpoint in swfaw — React `apiClient.js` interceptor calls it on 401 but it will 404. Refresh token support deferred (Option B from discussion).
- `LoginResponse` record in `auth_service_templates.py` has no `refreshToken` field — React handles this by defaulting to `null`.

## Tomorrow
- Debug React App Writer (REAW) issues
