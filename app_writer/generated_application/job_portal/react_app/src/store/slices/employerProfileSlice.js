import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllEmployerProfile,
  getEmployerProfileById,
  createEmployerProfile as createEmployerProfileApi,
  updateEmployerProfile as updateEmployerProfileApi,
  deleteEmployerProfile as deleteEmployerProfileApi,
} from '../../services/employerProfileService';


export const fetchAllEmployerProfile = createAsyncThunk(
  'employerProfile/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllEmployerProfile(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdEmployerProfile = createAsyncThunk(
  'employerProfile/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getEmployerProfileById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createEmployerProfile = createAsyncThunk(
  'employerProfile/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createEmployerProfileApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateEmployerProfile = createAsyncThunk(
  'employerProfile/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateEmployerProfileApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeEmployerProfile = createAsyncThunk(
  'employerProfile/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteEmployerProfileApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const employerProfileSlice = createSlice({
  name: 'employerProfile',
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
      .addCase(fetchAllEmployerProfile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllEmployerProfile.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllEmployerProfile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdEmployerProfile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdEmployerProfile.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdEmployerProfile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createEmployerProfile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createEmployerProfile.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createEmployerProfile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateEmployerProfile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateEmployerProfile.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.employerProfileId === action.payload.employerProfileId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateEmployerProfile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeEmployerProfile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeEmployerProfile.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.employerProfileId !== action.meta.arg);
      })
      .addCase(removeEmployerProfile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = employerProfileSlice.actions;
export default employerProfileSlice.reducer;