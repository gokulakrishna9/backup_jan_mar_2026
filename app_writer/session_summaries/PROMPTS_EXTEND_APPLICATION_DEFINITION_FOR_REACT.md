# Prompts: Extend Application Definition JSON for React Scaffolding

## Overview
These prompts guide the extension of the existing `ApplicationDefinitionJSONGenerator` to add frontend-specific metadata that React scaffolding tools can use to generate UI components.

---

## Prompt 1: Add UI Metadata to Entity Definitions

**Goal:** Extend each entity with UI display information

**Task:**
Update `ApplicationDefinitionJSONGenerator._transform_table_to_entity()` to add a `ui` section to each entity with:

1. **Display Names**
   - `displayName`: Singular form (e.g., "Course")
   - `displayNamePlural`: Plural form (e.g., "Courses")

2. **Visual Identity**
   - `icon`: Material-UI icon name (e.g., "School", "Person", "Business")
   - `color`: Primary color for the entity (e.g., "#1976d2")

3. **List View Configuration**
   - `defaultColumns`: Array of field names to show in table (e.g., ["courseName", "courseCode", "credits"])
   - `sortableColumns`: Array of fields that can be sorted
   - `searchableColumns`: Array of fields that can be searched
   - `defaultSort`: Object with `field` and `order` ("asc" or "desc")
   - `pageSize`: Default number of items per page (e.g., 20)

4. **Detail View Configuration**
   - `layout`: "tabs" or "sections"
   - `sections`: Array of section objects with `name` and `fields`

5. **Form View Configuration**
   - `layout`: "single" or "stepper"
   - `steps`: Array of step objects with `name` and `fields` (for stepper layout)

**Example Output:**
```json
{
  "name": "Course",
  "tableName": "course",
  "isRootEntity": true,
  "fields": [...],
  "ui": {
    "displayName": "Course",
    "displayNamePlural": "Courses",
    "icon": "School",
    "color": "#1976d2",
    "listView": {
      "defaultColumns": ["courseName", "courseCode", "credits", "institutionId"],
      "sortableColumns": ["courseName", "courseCode", "credits"],
      "searchableColumns": ["courseName", "courseCode"],
      "defaultSort": { "field": "courseName", "order": "asc" },
      "pageSize": 20
    },
    "detailView": {
      "layout": "tabs",
      "sections": [
        { "name": "Details", "fields": ["courseName", "courseCode", "courseDescription", "credits"] },
        { "name": "Relationships", "fields": ["institutionId"] },
        { "name": "Audit", "fields": ["createdAt", "updatedAt"] }
      ]
    },
    "formView": {
      "layout": "single",
      "fields": ["courseName", "courseCode", "courseDescription", "credits", "institutionId"]
    }
  }
}
```

**Implementation Hints:**
- Use entity name to determine icon (map common names like "User" → "Person", "Course" → "School")
- Exclude audit fields (createdAt, updatedAt, deletedAt) from defaultColumns
- Include all non-audit fields in sortableColumns
- Include string fields in searchableColumns
- For detailView, group related fields into logical sections

---

## Prompt 2: Add UI Metadata to Field Definitions

**Goal:** Extend each field with UI input and display information

**Task:**
Update field transformation to add a `ui` section to each field with:

1. **Labels and Help**
   - `label`: Human-readable label (e.g., "Course Name")
   - `placeholder`: Placeholder text for inputs (e.g., "Enter course name")
   - `helpText`: Optional help text

2. **Input Configuration**
   - `inputType`: Type of input control (see list below)
   - `width`: "full", "half", "third", "quarter"
   - `order`: Display order in forms (1, 2, 3...)

3. **List Display**
   - `show`: Boolean - show in list view
   - `width`: Column width in pixels (e.g., 200)
   - `align`: "left", "center", "right"
   - `sortable`: Boolean
   - `filterable`: Boolean

4. **Form Display**
   - `show`: Boolean - show in forms
   - `required`: Boolean - based on nullable
   - `disabled`: Boolean
   - `readOnly`: Boolean

5. **Detail Display**
   - `show`: Boolean - show in detail view
   - `format`: Display format (see list below)
   - `copyable`: Boolean - show copy button

**Input Types:**
- `text`: VARCHAR, CHAR
- `textarea`: TEXT, LONGTEXT
- `number`: INT, BIGINT, DECIMAL
- `email`: VARCHAR with "email" in name
- `date`: DATE
- `datetime`: DATETIME, TIMESTAMP
- `select`: Foreign key fields
- `checkbox`: BOOLEAN, TINYINT(1)
- `password`: VARCHAR with "password" in name

**Display Formats:**
- `text`: Plain text
- `number`: Formatted number
- `date`: Formatted date
- `datetime`: Formatted date and time
- `email`: Email with mailto link
- `url`: URL with link
- `badge`: Colored badge (for codes, statuses)
- `boolean`: Yes/No or icon

**Example Output:**
```json
{
  "name": "courseName",
  "type": "VARCHAR(255)",
  "javaType": "String",
  "nullable": false,
  "ui": {
    "label": "Course Name",
    "placeholder": "Enter course name",
    "helpText": "The official name of the course",
    "inputType": "text",
    "width": "full",
    "order": 1,
    "listDisplay": {
      "show": true,
      "width": 200,
      "align": "left",
      "sortable": true,
      "filterable": true
    },
    "formDisplay": {
      "show": true,
      "required": true,
      "disabled": false,
      "readOnly": false
    },
    "detailDisplay": {
      "show": true,
      "format": "text",
      "copyable": false
    }
  }
}
```

**Implementation Hints:**
- Convert snake_case field names to Title Case for labels (course_name → "Course Name")
- Set `required` based on `nullable` field property
- Hide primary key fields in forms but show in detail view
- Set `copyable: true` for ID fields
- Use field name patterns to determine inputType (email, password, url, etc.)
- Set appropriate widths: full for text/textarea, half for numbers/dates

---

## Prompt 3: Add UI Metadata to Relationships

**Goal:** Extend relationships with UI rendering information

**Task:**
Update relationship definitions to add a `ui` section with:

1. **Display Configuration**
   - `displayName`: Human-readable name (e.g., "Institution")
   - `displayField`: Field to show from related entity (e.g., "institutionName")
   - `icon`: Material-UI icon for the relationship

2. **Form Display**
   - `inputType`: "select", "autocomplete", or "radio"
   - `searchFields`: Array of fields to search in autocomplete (e.g., ["institutionName", "institutionCode"])
   - `displayFormat`: Template for display (e.g., "{institutionName} ({institutionCode})")
   - `required`: Boolean
   - `allowCreate`: Boolean - allow creating new related entity

3. **List Display**
   - `show`: Boolean - show in list view
   - `format`: "text", "link", or "badge"
   - `navigateTo`: URL pattern for links (e.g., "/institutions/{id}")

4. **Detail Display**
   - `show`: Boolean - show in detail view
   - `format`: "card", "inline", or "link"
   - `fields`: Array of fields to show from related entity

5. **Inverse Relationship** (for one-to-many)
   - `name`: Name of inverse relationship (e.g., "enrollments")
   - `displayName`: Display name (e.g., "Enrollments")
   - `showInDetail`: Boolean - show in detail view
   - `displayFormat`: "table" or "list"
   - `columns`: Array of columns to show

**Example Output:**
```json
{
  "sourceEntity": "Course",
  "targetEntity": "Institution",
  "type": "many-to-one",
  "foreignKey": "institutionId",
  "ui": {
    "displayName": "Institution",
    "displayField": "institutionName",
    "icon": "Business",
    "formDisplay": {
      "inputType": "autocomplete",
      "searchFields": ["institutionName", "institutionCode"],
      "displayFormat": "{institutionName} ({institutionCode})",
      "required": true,
      "allowCreate": false
    },
    "listDisplay": {
      "show": true,
      "format": "link",
      "navigateTo": "/institutions/{id}"
    },
    "detailDisplay": {
      "show": true,
      "format": "card",
      "fields": ["institutionName", "institutionCode", "city"]
    }
  }
}
```

**For Inverse Relationships (one-to-many):**
```json
{
  "sourceEntity": "Institution",
  "targetEntity": "Course",
  "type": "one-to-many",
  "foreignKey": "institutionId",
  "ui": {
    "inverseRelationship": {
      "name": "courses",
      "displayName": "Courses",
      "showInDetail": true,
      "displayFormat": "table",
      "columns": ["courseName", "courseCode", "credits"]
    }
  }
}
```

**Implementation Hints:**
- For many-to-one: Use autocomplete for better UX
- For one-to-many: Show as table in detail view
- Use entity name to determine displayField (look for "name" field first)
- Set `required` based on foreign key nullable property

---

## Prompt 4: Add Page Definitions

**Goal:** Generate page definitions for each entity

**Task:**
Add a new method `_generate_page_definitions()` that creates page definitions for:

1. **List Page** - Shows all entities in a table
2. **Detail Page** - Shows single entity details
3. **Form Page** - Create/edit entity

**For Each Entity, Generate:**

```json
{
  "pages": [
    {
      "name": "CourseList",
      "path": "/courses",
      "type": "list",
      "entity": "Course",
      "title": "Courses",
      "icon": "School",
      "permissions": {
        "view": ["USER", "ADMIN", "SYSTEM_ADMIN"],
        "create": ["ADMIN", "SYSTEM_ADMIN"],
        "edit": ["ADMIN", "SYSTEM_ADMIN"],
        "delete": ["SYSTEM_ADMIN"]
      }
    },
    {
      "name": "CourseDetail",
      "path": "/courses/:id",
      "type": "detail",
      "entity": "Course",
      "title": "{courseName}",
      "permissions": {
        "view": ["USER", "ADMIN", "SYSTEM_ADMIN"]
      }
    },
    {
      "name": "CourseForm",
      "path": "/courses/:id?/edit",
      "type": "form",
      "entity": "Course",
      "title": "{id ? 'Edit Course' : 'New Course'}",
      "permissions": {
        "create": ["ADMIN", "SYSTEM_ADMIN"],
        "edit": ["ADMIN", "SYSTEM_ADMIN"]
      }
    }
  ]
}
```

**Implementation Hints:**
- Use entity displayNamePlural for list page title
- Use entity displayName for form page title
- For root entities: Restrict create/edit/delete to ADMIN roles
- For non-root entities: Allow all authenticated users
- Path should use lowercase plural (Course → /courses)

---

## Prompt 5: Add Navigation Structure

**Goal:** Generate navigation menu structure

**Task:**
Add a new method `_generate_navigation_structure()` that creates a sidebar navigation with:

1. **Dashboard Section** - Home/Dashboard link
2. **Entity Sections** - Group related entities
3. **Admin Section** - Admin-only links

**Example Output:**
```json
{
  "navigation": {
    "type": "sidebar",
    "items": [
      {
        "type": "section",
        "label": "Main",
        "items": [
          {
            "type": "link",
            "label": "Dashboard",
            "path": "/",
            "icon": "Dashboard",
            "permission": ["USER"]
          }
        ]
      },
      {
        "type": "section",
        "label": "Academic",
        "items": [
          {
            "type": "link",
            "label": "Institutions",
            "path": "/institutions",
            "icon": "Business",
            "permission": ["USER"]
          },
          {
            "type": "link",
            "label": "Courses",
            "path": "/courses",
            "icon": "School",
            "permission": ["USER"]
          },
          {
            "type": "link",
            "label": "Students",
            "path": "/students",
            "icon": "Person",
            "permission": ["USER"]
          }
        ]
      },
      {
        "type": "section",
        "label": "Administration",
        "permission": ["ADMIN"],
        "items": [
          {
            "type": "link",
            "label": "Users",
            "path": "/admin/users",
            "icon": "People",
            "permission": ["ADMIN"]
          },
          {
            "type": "link",
            "label": "Roles",
            "path": "/admin/roles",
            "icon": "Security",
            "permission": ["ADMIN"]
          }
        ]
      }
    ]
  }
}
```

**Implementation Hints:**
- Group entities by domain (Academic, HR, Finance, etc.)
- Use entity icon and displayNamePlural
- Add admin section for system entities (users, roles, settings)
- Order by importance or alphabetically

---

## Prompt 6: Add API Client Configuration

**Goal:** Add API client configuration for frontend

**Task:**
Add a new method `_generate_api_client_config()` that creates:

```json
{
  "apiClient": {
    "baseURL": "http://localhost:8080/api",
    "timeout": 30000,
    "authentication": {
      "type": "JWT",
      "tokenKey": "accessToken",
      "refreshTokenKey": "refreshToken",
      "headerName": "Authorization",
      "headerPrefix": "Bearer",
      "storage": "localStorage"
    },
    "endpoints": {
      "auth": {
        "login": "/auth/login",
        "register": "/auth/register",
        "refresh": "/auth/refresh"
      }
    }
  }
}
```

**Implementation Hints:**
- Use project metadata for baseURL
- Standard JWT configuration
- Include auth endpoints

---

## Prompt 7: Add Theme Configuration

**Goal:** Add theme configuration for Material-UI

**Task:**
Add a new method `_generate_theme_config()` that creates:

```json
{
  "theme": {
    "mode": "light",
    "primaryColor": "#1976d2",
    "secondaryColor": "#dc004e",
    "errorColor": "#f44336",
    "warningColor": "#ff9800",
    "infoColor": "#2196f3",
    "successColor": "#4caf50",
    "typography": {
      "fontFamily": "'Roboto', 'Helvetica', 'Arial', sans-serif",
      "fontSize": 14
    },
    "spacing": 8,
    "borderRadius": 4
  }
}
```

**Implementation Hints:**
- Use Material-UI default colors
- Standard spacing and border radius
- Can be customized later

---

## Prompt 8: Add Frontend Section to Root

**Goal:** Add top-level `frontend` section to application definition

**Task:**
Update `generate()` method to add a `frontend` section at the root level:

```json
{
  "version": "2.0",
  "projectMetadata": { ... },
  "entities": [ ... ],
  "relationships": [ ... ],
  "authentication": { ... },
  "authorization": { ... },
  "features": [ ... ],
  "technology": { ... },
  "statistics": { ... },
  
  "frontend": {
    "framework": "React",
    "version": "18.x",
    "stateManagement": "Redux Toolkit",
    "routing": "React Router v6",
    "uiLibrary": "Material-UI",
    "formLibrary": "React Hook Form",
    "apiClient": "Axios",
    
    "pages": [ ... ],
    "navigation": { ... },
    "theme": { ... },
    "apiClient": { ... }
  }
}
```

**Implementation:**
```python
def generate(self, db_definition: Dict, config: Dict = None) -> str:
    # ... existing code ...
    
    app_def = {
        "version": "2.0",
        "projectMetadata": metadata,
        "entities": entities,
        "relationships": relationships,
        "authentication": auth_info,
        "authorization": authz_info,
        "features": features,
        "technology": tech_stack,
        "statistics": stats,
        
        # NEW: Add frontend section
        "frontend": {
            "framework": "React",
            "version": "18.x",
            "stateManagement": "Redux Toolkit",
            "routing": "React Router v6",
            "uiLibrary": "Material-UI",
            "formLibrary": "React Hook Form",
            "apiClient": "Axios",
            
            "pages": self._generate_page_definitions(entities),
            "navigation": self._generate_navigation_structure(entities),
            "theme": self._generate_theme_config(),
            "apiClient": self._generate_api_client_config(metadata)
        }
    }
    
    return json.dumps(app_def, indent=2)
```

---

## Summary

These 8 prompts will extend the application definition JSON to include all metadata needed for React scaffolding:

1. ✅ Entity UI metadata (display names, icons, view configurations)
2. ✅ Field UI metadata (labels, input types, display formats)
3. ✅ Relationship UI metadata (form inputs, display formats)
4. ✅ Page definitions (list, detail, form pages)
5. ✅ Navigation structure (sidebar menu)
6. ✅ API client configuration (JWT, endpoints)
7. ✅ Theme configuration (colors, typography)
8. ✅ Frontend section (top-level integration)

The extended definition will be backward compatible with the backend generator and provide everything a React scaffolding tool needs to generate a complete UI.
