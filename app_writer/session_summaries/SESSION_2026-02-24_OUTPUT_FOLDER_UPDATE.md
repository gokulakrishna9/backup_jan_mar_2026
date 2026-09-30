# Output Folder Configuration Update

**Date:** 2026-02-24  
**Purpose:** Update default output folder to use workspace-relative path

---

## Changes Made

### Old Default Output Folder
```
../generated_application/<application_name>/backend/
```

### New Default Output Folder
```
emotisense-ai/generated_application/<database_name>_backend/
```

---

## Key Changes

### 1. Path Structure
- **Old**: Relative path outside workspace (`../generated_application/`)
- **New**: Workspace-relative path (`emotisense-ai/generated_application/`)

### 2. Naming Convention
- **Old**: `<application_name>/backend/`
- **New**: `<database_name>_backend/`

### 3. Benefits
- Generated applications stay within the workspace
- Easier to find and manage generated code
- Consistent with workspace structure
- Better integration with version control

---

## Updated Files

### 1. OUTPUT_FOLDER_SPECIFICATION.md
**Location:** `emotisense-ai/prompts/code_generators/OUTPUT_FOLDER_SPECIFICATION.md`

**Changes:**
- Updated default pattern from `../generated_application/<name>/backend/` to `emotisense-ai/generated_application/<database_name>_backend/`
- Updated all examples to use new path structure
- Updated implementation logic to use `database.name` instead of `projectMetadata.name`
- Updated directory structure diagrams
- Added workspace integration benefits

### 2. 01_PROJECT_SETUP.md
**Location:** `emotisense-ai/prompts/code_generators/01_PROJECT_SETUP.md`

**Changes:**
- Updated default output in Key Principles section
- Updated `__init__` method to construct workspace-relative path
- Changed path construction to navigate to workspace root and build path from there

### 3. TWO_PHASE_WORKFLOW.md
**Location:** `emotisense-ai/prompts/code_generators/TWO_PHASE_WORKFLOW.md`

**Changes:**
- Updated example `outputFolder` values in JSON examples
- Updated output messages to show new path structure

---

## Implementation Details

### Default Path Construction

**Old Logic:**
```python
if output_dir is None:
    base_dir = Path(__file__).parent.parent / "generated_application"
    output_dir = base_dir / f"{database_name}_backend"
```

**New Logic:**
```python
if output_dir is None:
    # Default: emotisense-ai/generated_application/{database_name}_backend/
    workspace_root = Path(__file__).parent.parent.parent  # Navigate to workspace root
    output_dir = workspace_root / "emotisense-ai" / "generated_application" / f"{database_name}_backend"
```

### Priority System (Unchanged)

The three-tier priority system remains the same:

1. **Command-line flag** (highest priority)
   ```bash
   python main.py --input db.json --output ./custom-folder
   ```

2. **Metadata field** (medium priority)
   ```json
   {
     "projectMetadata": {
       "outputFolder": "custom/path/"
     }
   }
   ```

3. **Default pattern** (lowest priority)
   ```
   emotisense-ai/generated_application/<database_name>_backend/
   ```

---

## Example Outputs

### Example 1: Database named "course_db"
**Default output:**
```
emotisense-ai/generated_application/course_db_backend/
├── pom.xml
├── authentication_authorization_schema.sql
└── src/
```

### Example 2: Database named "user_management"
**Default output:**
```
emotisense-ai/generated_application/user_management_backend/
├── pom.xml
├── authentication_authorization_schema.sql
└── src/
```

### Example 3: Database named "inventory_system"
**Default output:**
```
emotisense-ai/generated_application/inventory_system_backend/
├── pom.xml
├── authentication_authorization_schema.sql
└── src/
```

---

## Workspace Structure

### Before (Old Structure)
```
project-root/
├── swfaw_v2/                    # Generator code
├── database_definitions/        # Input files
└── generated_application/       # Generated apps (outside workspace)
    └── course-api/
        └── backend/
```

### After (New Structure)
```
emotisense-ai/
├── prompts/
│   └── code_generators/
├── generated_application/       # Generated apps (inside workspace)
│   ├── course_db_backend/
│   ├── user_db_backend/
│   └── inventory_db_backend/
└── session_summaries/
```

---

## Migration Notes

### For Existing Projects

If you have existing generated applications in the old location, you can:

1. **Move them manually:**
   ```bash
   mv ../generated_application/my-app/backend emotisense-ai/generated_application/my_app_backend
   ```

2. **Regenerate with new structure:**
   ```bash
   python main.py --input my_db.json
   # Will generate to: emotisense-ai/generated_application/my_db_backend/
   ```

3. **Use custom output flag:**
   ```bash
   python main.py --input my_db.json --output ../generated_application/my-app/backend
   # Keeps old location if needed
   ```

### For New Projects

New projects will automatically use the new structure:
```bash
python main.py --input new_db.json
# Generates to: emotisense-ai/generated_application/new_db_backend/
```

---

## SQL Parser Behavior

The SQL parser now generates the new path format:

**Old:**
```json
{
  "projectMetadata": {
    "outputFolder": "../generated_application/course-db/backend/"
  }
}
```

**New:**
```json
{
  "projectMetadata": {
    "outputFolder": "emotisense-ai/generated_application/course_db_backend/"
  }
}
```

---

## Validation

The output folder validation remains the same:
- Check for empty paths
- Check for invalid characters
- Warn if path doesn't end with `/`
- Create directory if it doesn't exist

---

## Benefits of New Structure

### 1. Workspace Integration
- Generated code stays within the workspace
- Easier to manage with version control
- Consistent with workspace guidelines

### 2. Simplified Paths
- No need to navigate outside workspace (`../`)
- Clear, absolute-like paths from workspace root
- Easier to understand and document

### 3. Better Organization
- All generated applications in one location
- Easy to find: `emotisense-ai/generated_application/`
- Consistent naming: `<database_name>_backend/`

### 4. Future-Proof
- Room for frontend generation: `<database_name>_frontend/`
- Room for other artifacts: `<database_name>_docs/`
- Scalable structure for multiple projects

---

## Summary

**What changed:**
- Default output folder moved from `../generated_application/` to `emotisense-ai/generated_application/`
- Naming changed from `<app_name>/backend/` to `<database_name>_backend/`
- Path construction updated to use workspace root

**What stayed the same:**
- Three-tier priority system (command-line > metadata > default)
- Override capability with `--output` flag
- Metadata field `outputFolder` still works
- Validation and directory creation logic

**Impact:**
- New projects automatically use new structure
- Existing projects can continue using old structure with `--output` flag
- Better workspace integration and organization

