# Frontend Application Definition Extension

## Overview
This document defines the extended application definition schema for React frontend scaffolding. The extension adds UI-specific metadata to the existing backend application definition, enabling automatic generation of React components, forms, views, and routing.

## Purpose
Enable a React code generator to automatically create:
- API client services
- CRUD forms with validation
- List/table views with filtering
- Detail views
- Navigation and routing
- Role-based UI components
- Relationship visualizations

## Extended Schema Structure

```json
{
  "version": "2.0",
  "projectMetadata": { /* existing */ },
  "entities": [ /* existing with extensions */ ],
  "relationships": [ /* existing */ ],
  "authentication": { /* existing */ },
  "authorization": { /* existing */ },
  "features": [ /* existing */ ],
  "technology": { /* existing */ },
  "statistics": { /* existing */ },
  
  // NEW: Frontend-specific extensions
  "frontend": {
    "framework": "React",
    "version": "18.x",
    "stateManagement": "Redux Toolkit",
    "routing": "React Router v6",
    "uiLibrary": "Material-UI",
    "formLibrary": "React Hook Form",
    "apiClient": "Axios",
    "authentication": "JWT",
    
    "pages": [ /* page definitions */ ],
    "navigation": { /* navigation structure */ },
    "theme": { /* theme configuration */ },
    "layouts": [ /* layout definitions */ ]
  }
}
```

---

## Entity Extensions for Frontend

Each entity gets extended with UI-specific metadata:

```json
{
  "name": "Course",
  "tableName": "course",
  "isRootEntity": true,
  "fields": [ /* existing fields */ ],
  
  // NEW: UI Extensions
  "ui": {
    "displayName": "Course",
    "displayNamePlural": "Courses",
    "icon": "School",
    "color": "#1976d2",
    "description": "Manage courses and curriculum",
    
    "listView": {
      "defaultColumns": ["courseName", "courseCode", "credits", "institutionId"],
      "sortableColumns": ["courseName", "courseCode", "credits"],
      "searchableColumns": ["courseName", "courseCode"],
      "defaultSort": { "field": "courseName", "order": "asc" },
      "pageSize": 20,
      "enableExport": true,
      "enableBulkActions": true
    },

    
    "detailView": {
      "layout": "tabs",
      "tabs": [
        {
          "name": "Details",
          "fields": ["courseName", "courseCode", "courseDescription", "credits"]
        },
        {
          "name": "Relationships",
          "relationships": ["institution", "enrollments"]
        },
        {
          "name": "Audit",
          "fields": ["createdAt", "updatedAt"]
        }
      ]
    },
    
    "formView": {
      "layout": "stepper",
      "steps": [
        {
          "name": "Basic Information",
          "fields": ["courseName", "courseCode", "courseDescription"]
        },
        {
          "name": "Details",
          "fields": ["credits", "institutionId"]
        }
      ],
      "validation": {
        "courseName": {
          "required": true,
          "minLength": 3,
          "maxLength": 255,
          "message": "Course name is required (3-255 characters)"
        },
        "courseCode": {
          "required": true,
          "pattern": "^[A-Z]{2,4}[0-9]{3,4}$",
          "message": "Course code must be in format: CS101"
        },
        "credits": {
          "required": true,
          "min": 1,
          "max": 10,
          "message": "Credits must be between 1 and 10"
        }
      }
    },
    
    "filterView": {
      "filters": [
        {
          "field": "courseName",
          "type": "text",
          "operator": "contains",
          "label": "Course Name"
        },
        {
          "field": "courseCode",
          "type": "text",
          "operator": "equals",
          "label": "Course Code"
        },
        {
          "field": "credits",
          "type": "number",
          "operator": "range",
          "label": "Credits"
        },
        {
          "field": "institutionId",
          "type": "select",
          "operator": "equals",
          "label": "Institution",
          "dataSource": "institutions"
        },
        {
          "field": "createdAt",
          "type": "dateRange",
          "operator": "between",
          "label": "Created Date"
        }
      ],
      "quickFilters": [
        {
          "name": "Recent",
          "filter": { "createdAt": { "gte": "now-7d" } }
        },
        {
          "name": "High Credits",
          "filter": { "credits": { "gte": 4 } }
        }
      ]
    }
  }
}
```

---

## Field Extensions for Frontend

Each field gets UI-specific metadata:

```json
{
  "name": "courseName",
  "type": "VARCHAR(255)",
  "javaType": "String",
  "nullable": false,
  
  // NEW: UI Extensions
  "ui": {
    "label": "Course Name",
    "placeholder": "Enter course name",
    "helpText": "The official name of the course",
    "inputType": "text",
    "displayFormat": "text",
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
      "copyable": true
    }
  }
}
```

### Field Input Types

```json
{
  "inputTypes": {
    "text": "Single-line text input",
    "textarea": "Multi-line text input",
    "number": "Number input with +/- controls",
    "email": "Email input with validation",
    "password": "Password input (masked)",
    "date": "Date picker",
    "datetime": "Date and time picker",
    "time": "Time picker",
    "select": "Dropdown select",
    "multiselect": "Multi-select dropdown",
    "autocomplete": "Autocomplete search",
    "radio": "Radio button group",
    "checkbox": "Single checkbox",
    "checkboxGroup": "Multiple checkboxes",
    "switch": "Toggle switch",
    "slider": "Range slider",
    "file": "File upload",
    "image": "Image upload with preview",
    "richtext": "Rich text editor",
    "color": "Color picker",
    "rating": "Star rating"
  }
}
```

---

## Relationship Extensions for Frontend

```json
{
  "sourceEntity": "Course",
  "targetEntity": "Institution",
  "type": "many-to-one",
  "foreignKey": "institutionId",
  
  // NEW: UI Extensions
  "ui": {
    "displayName": "Institution",
    "displayField": "institutionName",
    "icon": "Business",
    
    "listDisplay": {
      "show": true,
      "format": "link",
      "navigateTo": "/institutions/{id}"
    },
    
    "formDisplay": {
      "inputType": "autocomplete",
      "searchFields": ["institutionName", "institutionCode"],
      "displayFormat": "{institutionName} ({institutionCode})",
      "allowCreate": false,
      "required": true
    },
    
    "detailDisplay": {
      "show": true,
      "format": "card",
      "fields": ["institutionName", "institutionCode", "city"]
    },
    
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

---

## Page Definitions

```json
{
  "pages": [
    {
      "name": "CourseList",
      "path": "/courses",
      "type": "list",
      "entity": "Course",
      "title": "Courses",
      "description": "Manage all courses",
      "icon": "School",
      
      "permissions": {
        "view": ["USER", "ADMIN", "SYSTEM_ADMIN"],
        "create": ["ADMIN", "SYSTEM_ADMIN"],
        "edit": ["ADMIN", "SYSTEM_ADMIN"],
        "delete": ["SYSTEM_ADMIN"]
      },
      
      "components": [
        {
          "type": "header",
          "title": "Courses",
          "actions": [
            {
              "type": "button",
              "label": "Add Course",
              "icon": "Add",
              "action": "navigate",
              "target": "/courses/new",
              "permission": "create"
            },
            {
              "type": "button",
              "label": "Export",
              "icon": "Download",
              "action": "export",
              "format": "csv"
            }
          ]
        },
        {
          "type": "filters",
          "position": "top",
          "collapsible": true,
          "defaultExpanded": false
        },
        {
          "type": "table",
          "columns": ["courseName", "courseCode", "credits", "institution"],
          "actions": ["view", "edit", "delete"],
          "bulkActions": ["delete", "export"],
          "pagination": true,
          "sorting": true,
          "selection": true
        }
      ]
    },
    
    {
      "name": "CourseDetail",
      "path": "/courses/:id",
      "type": "detail",
      "entity": "Course",
      "title": "{courseName}",
      
      "permissions": {
        "view": ["USER", "ADMIN", "SYSTEM_ADMIN"]
      },
      
      "components": [
        {
          "type": "header",
          "breadcrumbs": true,
          "actions": [
            {
              "type": "button",
              "label": "Edit",
              "icon": "Edit",
              "action": "navigate",
              "target": "/courses/{id}/edit",
              "permission": "edit"
            },
            {
              "type": "button",
              "label": "Delete",
              "icon": "Delete",
              "action": "delete",
              "confirm": true,
              "permission": "delete"
            }
          ]
        },
        {
          "type": "tabs",
          "tabs": [
            {
              "name": "Details",
              "component": "detailView"
            },
            {
              "name": "Enrollments",
              "component": "relationshipTable",
              "relationship": "enrollments"
            },
            {
              "name": "Audit",
              "component": "auditView"
            }
          ]
        }
      ]
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
      },
      
      "components": [
        {
          "type": "header",
          "breadcrumbs": true
        },
        {
          "type": "form",
          "layout": "stepper",
          "submitLabel": "{id ? 'Update' : 'Create'}",
          "cancelLabel": "Cancel",
          "onSuccess": "navigate",
          "successTarget": "/courses/{id}"
        }
      ]
    }
  ]
}
```

---

## Navigation Structure

```json
{
  "navigation": {
    "type": "sidebar",
    "position": "left",
    "collapsible": true,
    "width": 240,
    
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
            "permission": ["USER"],
            "badge": {
              "type": "count",
              "source": "institutions"
            }
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
          },
          {
            "type": "link",
            "label": "Enrollments",
            "path": "/enrollments",
            "icon": "Assignment",
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
          },
          {
            "type": "link",
            "label": "Settings",
            "path": "/admin/settings",
            "icon": "Settings",
            "permission": ["SYSTEM_ADMIN"]
          }
        ]
      }
    ]
  }
}
```

---

## API Client Configuration

```json
{
  "apiClient": {
    "baseURL": "http://localhost:8080/api",
    "timeout": 30000,
    "headers": {
      "Content-Type": "application/json"
    },
    
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
        "refresh": "/auth/refresh",
        "logout": "/auth/logout"
      }
    },
    
    "errorHandling": {
      "401": "redirect:/login",
      "403": "show:AccessDenied",
      "404": "show:NotFound",
      "500": "show:ServerError"
    },
    
    "retryPolicy": {
      "enabled": true,
      "maxRetries": 3,
      "retryDelay": 1000,
      "retryOn": [408, 429, 500, 502, 503, 504]
    }
  }
}
```

---

## Theme Configuration

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
      "fontSize": 14,
      "h1": { "fontSize": 32, "fontWeight": 500 },
      "h2": { "fontSize": 28, "fontWeight": 500 },
      "h3": { "fontSize": 24, "fontWeight": 500 },
      "h4": { "fontSize": 20, "fontWeight": 500 },
      "h5": { "fontSize": 18, "fontWeight": 500 },
      "h6": { "fontSize": 16, "fontWeight": 500 }
    },
    
    "spacing": 8,
    "borderRadius": 4,
    "shadows": true
  }
}
```

---

## Layout Definitions

```json
{
  "layouts": [
    {
      "name": "MainLayout",
      "type": "dashboard",
      "components": {
        "header": {
          "show": true,
          "height": 64,
          "components": ["logo", "search", "notifications", "userMenu"]
        },
        "sidebar": {
          "show": true,
          "width": 240,
          "collapsible": true,
          "component": "navigation"
        },
        "content": {
          "padding": 24,
          "maxWidth": 1200
        },
        "footer": {
          "show": true,
          "height": 48,
          "text": "© 2026 Course Management System"
        }
      }
    },
    {
      "name": "AuthLayout",
      "type": "centered",
      "components": {
        "content": {
          "maxWidth": 400,
          "centered": true
        }
      }
    }
  ]
}
```


---

## Complete Example: Extended Application Definition

```json
{
  "version": "2.0",
  "projectMetadata": {
    "name": "Course Management System",
    "groupId": "com.university",
    "artifactId": "course-management",
    "version": "1.0.0",
    "description": "A comprehensive course management system",
    "database": {
      "name": "course_management",
      "type": "MySQL"
    }
  },
  
  "entities": [
    {
      "name": "Course",
      "tableName": "course",
      "isRootEntity": true,
      "description": "Academic courses offered by institutions",
      
      "fields": [
        {
          "name": "courseId",
          "type": "BIGINT",
          "javaType": "Long",
          "isPrimaryKey": true,
          "autoIncrement": true,
          "ui": {
            "label": "ID",
            "listDisplay": { "show": true, "width": 80 },
            "formDisplay": { "show": false },
            "detailDisplay": { "show": true, "copyable": true }
          }
        },
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
            "listDisplay": { "show": true, "width": 200, "sortable": true },
            "formDisplay": { "show": true, "required": true },
            "detailDisplay": { "show": true, "format": "text" }
          }
        },
        {
          "name": "courseCode",
          "type": "VARCHAR(50)",
          "javaType": "String",
          "nullable": false,
          "unique": true,
          "ui": {
            "label": "Course Code",
            "placeholder": "e.g., CS101",
            "helpText": "Unique course identifier",
            "inputType": "text",
            "width": "half",
            "order": 2,
            "listDisplay": { "show": true, "width": 120, "sortable": true },
            "formDisplay": { "show": true, "required": true },
            "detailDisplay": { "show": true, "format": "badge" }
          }
        },
        {
          "name": "courseDescription",
          "type": "TEXT",
          "javaType": "String",
          "nullable": true,
          "ui": {
            "label": "Description",
            "placeholder": "Enter course description",
            "inputType": "textarea",
            "rows": 4,
            "width": "full",
            "order": 3,
            "listDisplay": { "show": false },
            "formDisplay": { "show": true, "required": false },
            "detailDisplay": { "show": true, "format": "markdown" }
          }
        },
        {
          "name": "credits",
          "type": "INT",
          "javaType": "Integer",
          "nullable": false,
          "ui": {
            "label": "Credits",
            "placeholder": "Enter credits",
            "helpText": "Number of credit hours",
            "inputType": "number",
            "min": 1,
            "max": 10,
            "width": "half",
            "order": 4,
            "listDisplay": { "show": true, "width": 100, "sortable": true },
            "formDisplay": { "show": true, "required": true },
            "detailDisplay": { "show": true, "format": "number" }
          }
        },
        {
          "name": "institutionId",
          "type": "BIGINT",
          "javaType": "Long",
          "nullable": false,
          "isForeignKey": true,
          "referencedTable": "institution",
          "referencedColumn": "institutionId",
          "ui": {
            "label": "Institution",
            "inputType": "autocomplete",
            "width": "full",
            "order": 5,
            "listDisplay": { "show": true, "width": 150, "format": "lookup" },
            "formDisplay": { "show": true, "required": true },
            "detailDisplay": { "show": true, "format": "link" }
          }
        }
      ],
      
      "ui": {
        "displayName": "Course",
        "displayNamePlural": "Courses",
        "icon": "School",
        "color": "#1976d2",
        "description": "Manage courses and curriculum",
        
        "listView": {
          "defaultColumns": ["courseName", "courseCode", "credits", "institutionId"],
          "sortableColumns": ["courseName", "courseCode", "credits"],
          "searchableColumns": ["courseName", "courseCode"],
          "defaultSort": { "field": "courseName", "order": "asc" },
          "pageSize": 20,
          "enableExport": true,
          "enableBulkActions": true
        },
        
        "detailView": {
          "layout": "tabs",
          "tabs": [
            {
              "name": "Details",
              "fields": ["courseName", "courseCode", "courseDescription", "credits", "institutionId"]
            },
            {
              "name": "Enrollments",
              "relationship": "enrollments",
              "displayFormat": "table"
            },
            {
              "name": "Audit",
              "fields": ["createdAt", "updatedAt"]
            }
          ]
        },
        
        "formView": {
          "layout": "stepper",
          "steps": [
            {
              "name": "Basic Information",
              "fields": ["courseName", "courseCode", "courseDescription"]
            },
            {
              "name": "Details",
              "fields": ["credits", "institutionId"]
            }
          ]
        },
        
        "filterView": {
          "filters": [
            {
              "field": "courseName",
              "type": "text",
              "operator": "contains",
              "label": "Course Name"
            },
            {
              "field": "courseCode",
              "type": "text",
              "operator": "equals",
              "label": "Course Code"
            },
            {
              "field": "credits",
              "type": "number",
              "operator": "range",
              "label": "Credits"
            },
            {
              "field": "institutionId",
              "type": "select",
              "operator": "equals",
              "label": "Institution",
              "dataSource": "institutions"
            }
          ]
        }
      }
    }
  ],
  
  "relationships": [
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
          "required": true
        },
        "detailDisplay": {
          "format": "card",
          "fields": ["institutionName", "institutionCode", "city"]
        }
      }
    },
    {
      "sourceEntity": "Enrollment",
      "targetEntity": "Course",
      "type": "many-to-one",
      "foreignKey": "courseId",
      "ui": {
        "displayName": "Course",
        "displayField": "courseName",
        "inverseRelationship": {
          "name": "enrollments",
          "displayName": "Enrollments",
          "showInDetail": true,
          "displayFormat": "table",
          "columns": ["student", "enrollmentDate", "grade"]
        }
      }
    }
  ],
  
  "frontend": {
    "framework": "React",
    "version": "18.x",
    "stateManagement": "Redux Toolkit",
    "routing": "React Router v6",
    "uiLibrary": "Material-UI",
    "formLibrary": "React Hook Form",
    "apiClient": "Axios",
    
    "pages": [
      {
        "name": "CourseList",
        "path": "/courses",
        "type": "list",
        "entity": "Course",
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
        "permissions": {
          "view": ["USER", "ADMIN", "SYSTEM_ADMIN"]
        }
      },
      {
        "name": "CourseForm",
        "path": "/courses/:id?/edit",
        "type": "form",
        "entity": "Course",
        "permissions": {
          "create": ["ADMIN", "SYSTEM_ADMIN"],
          "edit": ["ADMIN", "SYSTEM_ADMIN"]
        }
      }
    ],
    
    "navigation": {
      "type": "sidebar",
      "items": [
        {
          "type": "section",
          "label": "Academic",
          "items": [
            {
              "label": "Courses",
              "path": "/courses",
              "icon": "School",
              "permission": ["USER"]
            }
          ]
        }
      ]
    },
    
    "apiClient": {
      "baseURL": "http://localhost:8080/api",
      "authentication": {
        "type": "JWT",
        "tokenKey": "accessToken"
      }
    },
    
    "theme": {
      "mode": "light",
      "primaryColor": "#1976d2",
      "secondaryColor": "#dc004e"
    }
  }
}
```

---

## Generator Prompts

### Prompt 1: Extend Application Definition Generator

```
Update the ApplicationDefinitionJSONGenerator to include frontend extensions:

1. Add frontend configuration section
2. Extend entity definitions with UI metadata
3. Extend field definitions with UI display options
4. Extend relationship definitions with UI rendering options
5. Add page definitions for each entity (list, detail, form)
6. Add navigation structure
7. Add API client configuration
8. Add theme configuration

The extended definition should be backward compatible with the backend generator.
Use the schema defined in FRONTEND_APPLICATION_DEFINITION_EXTENSION.md.
```

### Prompt 2: React Component Generator

```
Create a React component generator that reads the extended application definition and generates:

1. API Client Services
   - Axios-based API client
   - CRUD operations for each entity
   - Authentication interceptors
   - Error handling

2. Redux Store
   - Slices for each entity
   - Async thunks for API calls
   - Selectors for data access

3. React Components
   - List views with tables, filtering, sorting, pagination
   - Detail views with tabs and relationships
   - Form views with validation and stepper
   - Layout components (header, sidebar, footer)

4. React Router Configuration
   - Routes for all pages
   - Protected routes with role-based access
   - Navigation guards

5. Material-UI Theme
   - Theme configuration from definition
   - Custom components
   - Responsive design

Use the extended application definition as the single source of truth.
```

### Prompt 3: Form Generator

```
Create a form generator that generates React Hook Form components:

1. Read field definitions from extended application definition
2. Generate form fields based on inputType
3. Add validation rules from field metadata
4. Generate stepper forms for multi-step processes
5. Handle relationship fields with autocomplete
6. Add file upload handling
7. Generate form submission logic
8. Add success/error handling

Support all input types defined in the schema.
```

### Prompt 4: Table/List Generator

```
Create a table/list generator that generates Material-UI DataGrid components:

1. Read listView configuration from entity UI metadata
2. Generate columns from defaultColumns
3. Add sorting for sortableColumns
4. Add filtering for searchableColumns
5. Add pagination with configurable page size
6. Add bulk actions (delete, export)
7. Add row actions (view, edit, delete)
8. Add export functionality (CSV, Excel)
9. Add search bar for quick filtering
10. Handle relationship columns with lookups

Generate responsive tables that work on mobile devices.
```

---

## Usage Example

### Step 1: Generate Extended Definition

```bash
python generate_extended_definition.py \
  --input examples/sample_schema.sql \
  --output output/application_definition_extended.json
```

### Step 2: Generate React Application

```bash
python generate_react_app.py \
  --definition output/application_definition_extended.json \
  --output frontend/
```

### Step 3: Generated Structure

```
frontend/
├── package.json
├── public/
├── src/
│   ├── api/
│   │   ├── client.js
│   │   ├── courseApi.js
│   │   ├── institutionApi.js
│   │   └── authApi.js
│   ├── store/
│   │   ├── index.js
│   │   ├── courseSlice.js
│   │   └── institutionSlice.js
│   ├── components/
│   │   ├── layout/
│   │   │   ├── MainLayout.jsx
│   │   │   ├── Header.jsx
│   │   │   └── Sidebar.jsx
│   │   ├── courses/
│   │   │   ├── CourseList.jsx
│   │   │   ├── CourseDetail.jsx
│   │   │   ├── CourseForm.jsx
│   │   │   └── CourseFilters.jsx
│   │   └── common/
│   │       ├── DataTable.jsx
│   │       ├── FormField.jsx
│   │       └── ConfirmDialog.jsx
│   ├── routes/
│   │   └── index.jsx
│   ├── theme/
│   │   └── index.js
│   └── App.jsx
└── README.md
```

---

## Benefits

1. **Single Source of Truth**: One definition for both backend and frontend
2. **Consistency**: UI matches backend API structure
3. **Rapid Development**: Generate complete CRUD interfaces automatically
4. **Type Safety**: Field types and validations match backend
5. **Role-Based Access**: UI respects backend authorization
6. **Maintainability**: Update definition, regenerate code
7. **Best Practices**: Generated code follows React best practices
8. **Customizable**: Extend generated components as needed

---

## Next Steps

1. Implement extended application definition generator
2. Create React component generators
3. Add TypeScript support
4. Add Storybook for component documentation
5. Add E2E tests with Cypress
6. Add mobile-responsive layouts
7. Add dark mode support
8. Add internationalization (i18n)
