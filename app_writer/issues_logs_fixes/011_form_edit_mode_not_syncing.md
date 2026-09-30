# Issue 011: Form edit mode doesn't enable when selecting a record

**Date:** 2026-04-03
**App:** job_portal
**Tool:** REAW (entity_component_templates.py)
**Severity:** High

## Symptom
Clicking "Edit" on a DataTable row selects the record but the form stays disabled (view mode).

## Root Cause
`useState(mode === 'create')` only evaluates the initial value at mount time. When the parent page changes the `mode` prop from `'view'` to `'edit'`, React doesn't re-run `useState` — the form stays in its initial state.

## Fix
Added a `useEffect` that syncs `editMode` when the `mode` prop changes:
```jsx
useEffect(() => {
  setEditMode(mode === 'create' || mode === 'edit');
}, [mode]);
```

Added to the non-singleRecordPerUser path in the entity form template.

## Verification
- 18 REAW tests pass
- Form enables when "Edit" is clicked on a DataTable row
