import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllInstitutionLocation,
  getInstitutionLocationById,
  createInstitutionLocation as createInstitutionLocationApi,
  updateInstitutionLocation as updateInstitutionLocationApi,
  deleteInstitutionLocation as deleteInstitutionLocationApi,
} from '../../services/institutionLocationService';


export const fetchAllInstitutionLocation = createAsyncThunk(
  'institutionLocation/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllInstitutionLocation(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdInstitutionLocation = createAsyncThunk(
  'institutionLocation/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getInstitutionLocationById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createInstitutionLocation = createAsyncThunk(
  'institutionLocation/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createInstitutionLocationApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateInstitutionLocation = createAsyncThunk(
  'institutionLocation/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateInstitutionLocationApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeInstitutionLocation = createAsyncThunk(
  'institutionLocation/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteInstitutionLocationApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const institutionLocationSlice = createSlice({
  name: 'institutionLocation',
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
      .addCase(fetchAllInstitutionLocation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllInstitutionLocation.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllInstitutionLocation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdInstitutionLocation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdInstitutionLocation.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdInstitutionLocation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createInstitutionLocation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createInstitutionLocation.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createInstitutionLocation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateInstitutionLocation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateInstitutionLocation.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.locationId === action.payload.locationId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateInstitutionLocation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeInstitutionLocation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeInstitutionLocation.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.locationId !== action.meta.arg);
      })
      .addCase(removeInstitutionLocation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = institutionLocationSlice.actions;
export default institutionLocationSlice.reducer;