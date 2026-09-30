# Issue 002: React pages in wrong folder — blank pages

**Date:** 2026-04-01
**App:** job_portal
**Tool:** REAW (entity_page_generator.py, scaffold_generator.py)
**Severity:** Critical

## Symptom
All React routes show blank pages (`#root is empty`). Vite reports `Failed to resolve import "./pages/dashboard/DashboardPage"`.

## Root Cause
Two problems:
1. `EntityPageGenerator` hardcoded all pages into `pages/entitys/` but `App.jsx` imports from `pages/{pageFolder}/` (e.g. `pages/jobs/`, `pages/masters/`).
2. `DashboardPage` was referenced in routes but no generator created it (Dashboard is not an entity).

## Fix
1. **entity_page_generator.py** — Build a route lookup (`pageComponent → pageFolder`) from `react_def.routes` and use it to determine the output folder, falling back to `"entitys"`.
2. **scaffold_generator.py** — Added `DASHBOARD_PAGE` template and generation logic: if a route with `pageComponent == "DashboardPage"` exists, write a placeholder dashboard page to the correct folder.
3. **scaffold_templates.py** — Added `DASHBOARD_PAGE` template string.

## Verification
- Vite starts without import resolution errors
- Pages now exist in correct folders: `dashboard/`, `profiles/`, `resume/`, `jobs/`, `training/`, `learning/`, `masters/`
