"""Jinja2 templates for Redux store files."""

STORE_JS = """import { configureStore } from '@reduxjs/toolkit';
{% for entity in entities %}import {{ entity | camelCase }}Reducer from './slices/{{ entity | camelCase }}Slice';
{% endfor %}

export const store = configureStore({
  reducer: {
{% for entity in entities %}    {{ entity | camelCase }}: {{ entity | camelCase }}Reducer,
{% endfor %}  },
});
"""

STORE_INDEX = """export { store } from './store';
"""

ENTITY_SLICE = """import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
{% if thunks['fetchAll'] %}  getAll{{ entityNamePascal }},
{% endif %}{% if thunks['fetchById'] %}  get{{ entityNamePascal }}ById,
{% endif %}{% if thunks['create'] %}  create{{ entityNamePascal }} as create{{ entityNamePascal }}Api,
{% endif %}{% if thunks['update'] %}  update{{ entityNamePascal }} as update{{ entityNamePascal }}Api,
{% endif %}{% if thunks['delete'] %}  delete{{ entityNamePascal }} as delete{{ entityNamePascal }}Api,
{% endif %}} from '../../services/{{ entityNameCamel }}Service';

{% if thunks['fetchAll'] %}
export const fetchAll{{ entityNamePascal }} = createAsyncThunk(
  '{{ entityNameCamel }}/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAll{{ entityNamePascal }}(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);
{% endif %}

{% if thunks['fetchById'] %}
export const fetchById{{ entityNamePascal }} = createAsyncThunk(
  '{{ entityNameCamel }}/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await get{{ entityNamePascal }}ById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);
{% endif %}

{% if thunks['create'] %}
export const create{{ entityNamePascal }} = createAsyncThunk(
  '{{ entityNameCamel }}/create',
  async (data, { rejectWithValue }) => {
    try {
      return await create{{ entityNamePascal }}Api(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);
{% endif %}

{% if thunks['update'] %}
export const update{{ entityNamePascal }} = createAsyncThunk(
  '{{ entityNameCamel }}/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await update{{ entityNamePascal }}Api(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);
{% endif %}

{% if thunks['delete'] %}
export const remove{{ entityNamePascal }} = createAsyncThunk(
  '{{ entityNameCamel }}/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await delete{{ entityNamePascal }}Api(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);
{% endif %}

const {{ entityNameCamel }}Slice = createSlice({
  name: '{{ entityNameCamel }}',
  initialState: {
    items: [],
    selectedItem: null,
    loading: false,
    error: null,
{% if hasPagination %}    currentPage: 0,
    pageSize: {{ pageSize }},
    totalCount: 0,
{% endif %}  },
  reducers: {
    clearError: (state) => { state.error = null; },
    clearSelectedItem: (state) => { state.selectedItem = null; },
  },
  extraReducers: (builder) => {
{% if thunks['fetchAll'] %}    builder
      .addCase(fetchAll{{ entityNamePascal }}.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAll{{ entityNamePascal }}.fulfilled, (state, action) => {
        state.loading = false;
{% if hasPagination %}        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
{% else %}        state.items = action.payload;
{% endif %}      })
      .addCase(fetchAll{{ entityNamePascal }}.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
{% endif %}
{% if thunks['fetchById'] %}    builder
      .addCase(fetchById{{ entityNamePascal }}.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchById{{ entityNamePascal }}.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchById{{ entityNamePascal }}.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
{% endif %}
{% if thunks['create'] %}    builder
      .addCase(create{{ entityNamePascal }}.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(create{{ entityNamePascal }}.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(create{{ entityNamePascal }}.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
{% endif %}
{% if thunks['update'] %}    builder
      .addCase(update{{ entityNamePascal }}.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(update{{ entityNamePascal }}.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.{{ pkField }} === action.payload.{{ pkField }});
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(update{{ entityNamePascal }}.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
{% endif %}
{% if thunks['delete'] %}    builder
      .addCase(remove{{ entityNamePascal }}.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(remove{{ entityNamePascal }}.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.{{ pkField }} !== action.meta.arg);
      })
      .addCase(remove{{ entityNamePascal }}.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
{% endif %}  },
});

export const { clearError, clearSelectedItem } = {{ entityNameCamel }}Slice.actions;
export default {{ entityNameCamel }}Slice.reducer;
"""
