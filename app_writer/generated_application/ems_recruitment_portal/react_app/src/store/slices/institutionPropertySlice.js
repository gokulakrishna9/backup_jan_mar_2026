import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllInstitutionProperty,
  getInstitutionPropertyById,
  createInstitutionProperty as createInstitutionPropertyApi,
  updateInstitutionProperty as updateInstitutionPropertyApi,
  deleteInstitutionProperty as deleteInstitutionPropertyApi,
} from '../../services/institutionPropertyService';


export const fetchAllInstitutionProperty = createAsyncThunk(
  'institutionProperty/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllInstitutionProperty(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdInstitutionProperty = createAsyncThunk(
  'institutionProperty/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getInstitutionPropertyById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createInstitutionProperty = createAsyncThunk(
  'institutionProperty/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createInstitutionPropertyApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateInstitutionProperty = createAsyncThunk(
  'institutionProperty/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateInstitutionPropertyApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeInstitutionProperty = createAsyncThunk(
  'institutionProperty/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteInstitutionPropertyApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const institutionPropertySlice = createSlice({
  name: 'institutionProperty',
  initialState: {
    items: [],
    selectedItem: null,
    loading: false,
    error: null,
    currentPage: 0,
    pageSize: 20,
    totalCount: 0,
  },
  reducers: {
    clearError: (state) => { state.error = null; },
    clearSelectedItem: (state) => { state.selectedItem = null; },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchAllInstitutionProperty.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllInstitutionProperty.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllInstitutionProperty.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdInstitutionProperty.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdInstitutionProperty.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdInstitutionProperty.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createInstitutionProperty.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createInstitutionProperty.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createInstitutionProperty.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateInstitutionProperty.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateInstitutionProperty.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.propertyId === action.payload.propertyId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateInstitutionProperty.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeInstitutionProperty.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeInstitutionProperty.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.propertyId !== action.meta.arg);
      })
      .addCase(removeInstitutionProperty.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = institutionPropertySlice.actions;
export default institutionPropertySlice.reducer;