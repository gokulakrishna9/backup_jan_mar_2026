# Issue 004: AppLayout — headerCollapsed/footerCollapsed not defined

**Date:** 2026-04-01
**App:** job_portal
**Tool:** REAW (grid_layout_templates.py)
**Severity:** Critical

## Symptom
`headerCollapsed is not defined` error in AppLayout.jsx — causes blank pages on all authenticated routes.

## Root Cause
The `APP_LAYOUT_JSX` template conditionally declares `headerCollapsed` state only when `header.collapsible` is true, but the className expression always references `headerCollapsed` unconditionally. When `header.collapsible: false`, the variable is never declared but still used.

## Fix
Made the className expression conditional — only include `${headerCollapsed ? ...}`, `${leftNavCollapsed ? ...}`, `${footerCollapsed ? ...}` when the corresponding region is collapsible.

**File changed:** `reaw/templates/grid_layout_templates.py`

## Verification
- AppLayout renders without JS errors
- All 6 tested routes pass frontend validation
