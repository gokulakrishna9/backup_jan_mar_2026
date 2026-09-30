# Frontend Generator Implementation Guide

## Overview
This guide provides step-by-step instructions for implementing the React frontend generator based on the extended application definition.

## Phase 1: Extend Application Definition Generator

### Task 1.1: Update ApplicationDefinitionJSONGenerator

**File:** `src/generators/application_definition_json_generator.py`

**Changes:**
1. Add `_generate_frontend_config()` method
2. Add `_generate_entity_ui_metadata()` method
3. Add `_generate_field_ui_metadata()` method
4. Add `_generate_relationship_ui_metadata()` method
5. Add `_generate_page_definitions()` method
6. Add `_generate_navigation_structure()` method

**Example Implementation:**

```python
def _generate_frontend_config(self, db_definition: Dict) -> Dict:
    """Generate frontend configuration."""
    return {
        "framework": "React",
        "version": "18.x",
        "stateManagement": "Redux Toolkit",
        "routing": "React Router v6",
        "uiLibrary": "Material-UI",
        "formLibrary": "React Hook Form",
        "apiClient": "Axios",
        "authentication": "JWT",
        
        "pages": self._generate_page_definitions(db_definition),
        "navigation": self._generate_navigation_structure(db_definition),
        "theme": self._generate_theme_config(),
        "apiClient": self._generate_api_client_config()
    }

def _generate_entity_ui_metadata(self, entity: Dict) -> Dict:
    """Generate UI metadata for entity."""
    entity_name = entity['name']
    
    return {
        "displayName": entity_name,
        "displayNamePlural": self._pluralize(entity_name),
        "icon": self._get_entity_icon(entity_name),
        "color": self._get_entity_color(entity_name),
        "description": f"Manage {self._pluralize(entity_name).lower()}",
        
        "listView": self._generate_list_view_config(entity),
        "detailView": self._generate_detail_view_config(entity),
        "formView": self._generate_form_view_config(entity),
        "filterView": self._generate_filter_view_config(entity)
    }

def _generate_field_ui_metadata(self, field: Dict) -> Dict:
    """Generate UI metadata for field."""
    return {
        "label": self._to_title_case(field['name']),
        "placeholder": f"Enter {field['name'].lower()}",
        "helpText": f"The {field['name'].lower()} value",
        "inputType": self._get_input_type(field),
        "width": "full" if field['type'].startswith('TEXT') else "half",
        
        "listDisplay": {
            "show": not field.get('isPrimaryKey', False),
            "width": self._get_column_width(field),
            "sortable": field['type'] in ['VARCHAR', 'INT', 'BIGINT', 'DATE'],
            "filterable": True
        },
        
        "formDisplay": {
            "show": not field.get('isPrimaryKey', False),
            "required": not field.get('nullable', True),
            "disabled": False,
            "readOnly": False
        },
        
        "detailDisplay": {
            "show": True,
            "format": self._get_display_format(field),
            "copyable": field.get('isPrimaryKey', False)
        }
    }
```

---

## Phase 2: Create React Generator Framework

### Task 2.1: Create ReactAppGenerator

**File:** `src/generators/react_app_generator.py`

```python
"""
React Application Generator
Generates complete React application from extended definition.
"""

class ReactAppGenerator:
    def __init__(self, base_package: str = 'com.example'):
        self.base_package = base_package
        self.generators = {
            'api': APIClientGenerator(),
            'store': ReduxStoreGenerator(),
            'components': ComponentGenerator(),
            'routes': RouteGenerator(),
            'theme': ThemeGenerator()
        }
    
    def generate_all(self, extended_definition: Dict) -> List[Dict]:
        """Generate all React components."""
        components = []
        
        # 1. Generate package.json
        components.append(self._generate_package_json(extended_definition))
        
        # 2. Generate API clients
        components.extend(self.generators['api'].generate_all(extended_definition))
        
        # 3. Generate Redux store
        components.extend(self.generators['store'].generate_all(extended_definition))
        
        # 4. Generate React components
        components.extend(self.generators['components'].generate_all(extended_definition))
        
        # 5. Generate routes
        components.append(self.generators['routes'].generate(extended_definition))
        
        # 6. Generate theme
        components.append(self.generators['theme'].generate(extended_definition))
        
        # 7. Generate App.jsx
        components.append(self._generate_app_component(extended_definition))
        
        return components
```

---

## Phase 3: Implement Component Generators

### Task 3.1: API Client Generator

**File:** `src/generators/react/api_client_generator.py`

```python
class APIClientGenerator:
    def generate_all(self, definition: Dict) -> List[Dict]:
        """Generate API client files."""
        components = []
        
        # Base API client
        components.append(self._generate_base_client(definition))
        
        # Entity API clients
        for entity in definition['entities']:
            components.append(self._generate_entity_api(entity, definition))
        
        # Auth API client
        components.append(self._generate_auth_api(definition))
        
        return components
    
    def _generate_entity_api(self, entity: Dict, definition: Dict) -> Dict:
        """Generate API client for entity."""
        entity_name = entity['name']
        entity_name_lower = entity_name.lower()
        entity_name_plural = self._pluralize(entity_name_lower)
        
        code = f"""import client from './client';

const {entity_name}API = {{
  // Get all {entity_name_plural}
  getAll: async (params = {{}}) => {{
    const response = await client.get('/{entity_name_plural}', {{ params }});
    return response.data;
  }},
  
  // Get {entity_name} by ID
  getById: async (id) => {{
    const response = await client.get(`/{entity_name_plural}/${{id}}`);
    return response.data;
  }},
  
  // Create {entity_name}
  create: async (data) => {{
    const response = await client.post('/{entity_name_plural}', data);
    return response.data;
  }},
  
  // Update {entity_name}
  update: async (id, data) => {{
    const response = await client.put(`/{entity_name_plural}/${{id}}`, data);
    return response.data;
  }},
  
  // Delete {entity_name}
  delete: async (id) => {{
    await client.delete(`/{entity_name_plural}/${{id}}`);
  }}
}};

export default {entity_name}API;
"""
        
        return {
            'fileName': f'{entity_name_lower}Api.js',
            'code': code,
            'path': 'src/api'
        }
```

### Task 3.2: Redux Store Generator

**File:** `src/generators/react/redux_store_generator.py`

```python
class ReduxStoreGenerator:
    def generate_all(self, definition: Dict) -> List[Dict]:
        """Generate Redux store files."""
        components = []
        
        # Store configuration
        components.append(self._generate_store_config(definition))
        
        # Entity slices
        for entity in definition['entities']:
            components.append(self._generate_entity_slice(entity, definition))
        
        return components
    
    def _generate_entity_slice(self, entity: Dict, definition: Dict) -> Dict:
        """Generate Redux slice for entity."""
        entity_name = entity['name']
        entity_name_lower = entity_name.lower()
        entity_name_plural = self._pluralize(entity_name_lower)
        
        code = f"""import {{ createSlice, createAsyncThunk }} from '@reduxjs/toolkit';
import {entity_name}API from '../api/{entity_name_lower}Api';

// Async thunks
export const fetch{entity_name_plural} = createAsyncThunk(
  '{entity_name_lower}/fetchAll',
  async (params) => {{
    return await {entity_name}API.getAll(params);
  }}
);

export const fetch{entity_name}ById = createAsyncThunk(
  '{entity_name_lower}/fetchById',
  async (id) => {{
    return await {entity_name}API.getById(id);
  }}
);

export const create{entity_name} = createAsyncThunk(
  '{entity_name_lower}/create',
  async (data) => {{
    return await {entity_name}API.create(data);
  }}
);

export const update{entity_name} = createAsyncThunk(
  '{entity_name_lower}/update',
  async ({{ id, data }}) => {{
    return await {entity_name}API.update(id, data);
  }}
);

export const delete{entity_name} = createAsyncThunk(
  '{entity_name_lower}/delete',
  async (id) => {{
    await {entity_name}API.delete(id);
    return id;
  }}
);

// Slice
const {entity_name_lower}Slice = createSlice({{
  name: '{entity_name_lower}',
  initialState: {{
    items: [],
    currentItem: null,
    loading: false,
    error: null,
    totalCount: 0
  }},
  reducers: {{
    clearCurrent: (state) => {{
      state.currentItem = null;
    }}
  }},
  extraReducers: (builder) => {{
    builder
      // Fetch all
      .addCase(fetch{entity_name_plural}.pending, (state) => {{
        state.loading = true;
        state.error = null;
      }})
      .addCase(fetch{entity_name_plural}.fulfilled, (state, action) => {{
        state.loading = false;
        state.items = action.payload;
      }})
      .addCase(fetch{entity_name_plural}.rejected, (state, action) => {{
        state.loading = false;
        state.error = action.error.message;
      }})
      
      // Fetch by ID
      .addCase(fetch{entity_name}ById.fulfilled, (state, action) => {{
        state.currentItem = action.payload;
      }})
      
      // Create
      .addCase(create{entity_name}.fulfilled, (state, action) => {{
        state.items.push(action.payload);
      }})
      
      // Update
      .addCase(update{entity_name}.fulfilled, (state, action) => {{
        const index = state.items.findIndex(item => item.id === action.payload.id);
        if (index !== -1) {{
          state.items[index] = action.payload;
        }}
        state.currentItem = action.payload;
      }})
      
      // Delete
      .addCase(delete{entity_name}.fulfilled, (state, action) => {{
        state.items = state.items.filter(item => item.id !== action.payload);
      }});
  }}
}});

export const {{ clearCurrent }} = {entity_name_lower}Slice.actions;
export default {entity_name_lower}Slice.reducer;
"""
        
        return {
            'fileName': f'{entity_name_lower}Slice.js',
            'code': code,
            'path': 'src/store'
        }
```

### Task 3.3: Component Generator

**File:** `src/generators/react/component_generator.py`

```python
class ComponentGenerator:
    def generate_all(self, definition: Dict) -> List[Dict]:
        """Generate React components."""
        components = []
        
        for entity in definition['entities']:
            # List component
            components.append(self._generate_list_component(entity, definition))
            
            # Detail component
            components.append(self._generate_detail_component(entity, definition))
            
            # Form component
            components.append(self._generate_form_component(entity, definition))
            
            # Filter component
            components.append(self._generate_filter_component(entity, definition))
        
        # Layout components
        components.extend(self._generate_layout_components(definition))
        
        return components
```

---

## Phase 4: Testing Strategy

### Test Files to Create

1. `tests/test_react_app_generator.py`
2. `tests/test_api_client_generator.py`
3. `tests/test_redux_store_generator.py`
4. `tests/test_component_generator.py`

### Example Test

```python
def test_generate_entity_api(self):
    """Test API client generation."""
    entity = {
        'name': 'Course',
        'fields': [...]
    }
    
    generator = APIClientGenerator()
    api_client = generator._generate_entity_api(entity, {})
    
    self.assertIn('CourseAPI', api_client['code'])
    self.assertIn('getAll', api_client['code'])
    self.assertIn('getById', api_client['code'])
    self.assertIn('create', api_client['code'])
    self.assertIn('update', api_client['code'])
    self.assertIn('delete', api_client['code'])
```

---

## Phase 5: Demo Script

**File:** `demo_react_generation.py`

```python
"""
Demo: React Application Generation
Shows complete flow from extended definition to React app.
"""

from application_definition_json_generator import ApplicationDefinitionJSONGenerator
from react_app_generator import ReactAppGenerator

def main():
    # 1. Generate extended definition
    print("Step 1: Generating extended application definition...")
    app_def_generator = ApplicationDefinitionJSONGenerator()
    extended_def = app_def_generator.generate_with_frontend_extensions(db_definition)
    
    # 2. Generate React application
    print("Step 2: Generating React application...")
    react_generator = ReactAppGenerator()
    react_components = react_generator.generate_all(extended_def)
    
    # 3. Write files
    print("Step 3: Writing React files...")
    output_dir = 'output/frontend'
    react_generator.write_all_to_files(react_components, output_dir)
    
    print(f"✅ Generated {len(react_components)} React files")

if __name__ == '__main__':
    main()
```

---

## Implementation Checklist

### Phase 1: Extended Definition
- [ ] Update ApplicationDefinitionJSONGenerator
- [ ] Add frontend config generation
- [ ] Add entity UI metadata
- [ ] Add field UI metadata
- [ ] Add relationship UI metadata
- [ ] Add page definitions
- [ ] Add navigation structure
- [ ] Test extended definition generation

### Phase 2: React Framework
- [ ] Create ReactAppGenerator
- [ ] Create APIClientGenerator
- [ ] Create ReduxStoreGenerator
- [ ] Create ComponentGenerator
- [ ] Create RouteGenerator
- [ ] Create ThemeGenerator
- [ ] Test framework structure

### Phase 3: Component Generators
- [ ] Implement list component generator
- [ ] Implement detail component generator
- [ ] Implement form component generator
- [ ] Implement filter component generator
- [ ] Implement layout components
- [ ] Test all component generators

### Phase 4: Integration
- [ ] Create demo script
- [ ] Test end-to-end generation
- [ ] Verify generated React app runs
- [ ] Test API integration
- [ ] Test authentication flow
- [ ] Test CRUD operations

### Phase 5: Documentation
- [ ] Write usage guide
- [ ] Create examples
- [ ] Document customization options
- [ ] Add troubleshooting guide

---

## Expected Output

After running the generator, you should have:

```
output/frontend/
├── package.json
├── public/
│   └── index.html
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
│   │   ├── courses/
│   │   ├── institutions/
│   │   └── common/
│   ├── routes/
│   │   └── index.jsx
│   ├── theme/
│   │   └── index.js
│   ├── App.jsx
│   └── index.js
└── README.md
```

---

## Next Steps

1. Start with Phase 1: Extend the application definition generator
2. Create comprehensive tests for each phase
3. Build incrementally, testing each component
4. Generate a sample React app and verify it works
5. Iterate based on feedback
6. Add advanced features (TypeScript, Storybook, etc.)
