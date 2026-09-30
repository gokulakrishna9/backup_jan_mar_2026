import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllInstitution,
  getInstitutionById,
  createInstitution as createInstitutionApi,
  updateInstitution as updateInstitutionApi,
  deleteInstitution as deleteInstitutionApi,
} from '../../services/institutionService';


export const fetchAllInstitution = createAsyncThunk(
  'institution/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllInstitution(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdInstitution = createAsyncThunk(
  'institution/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getInstitutionById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createInstitution = createAsyncThunk(
  'institution/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createInstitutionApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateInstitution = createAsyncThunk(
  'institution/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateInstitutionApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeInstitution = createAsyncThunk(
  'institution/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteInstitutionApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const institutionSlice = createSlice({
  name: 'institution',
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
      .addCase(fetchAllInstitution.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllInstitution.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllInstitution.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdInstitution.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdInstitution.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdInstitution.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createInstitution.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createInstitution.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createInstitution.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateInstitution.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateInstitution.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.institutionId === action.payload.institutionId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateInstitution.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeInstitution.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeInstitution.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.institutionId !== action.meta.arg);
      })
      .addCase(removeInstitution.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = institutionSlice.actions;
export default institutionSlice.reducer;