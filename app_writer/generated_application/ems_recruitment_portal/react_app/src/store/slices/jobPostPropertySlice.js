import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllJobPostProperty,
  getJobPostPropertyById,
  createJobPostProperty as createJobPostPropertyApi,
  updateJobPostProperty as updateJobPostPropertyApi,
  deleteJobPostProperty as deleteJobPostPropertyApi,
} from '../../services/jobPostPropertyService';


export const fetchAllJobPostProperty = createAsyncThunk(
  'jobPostProperty/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllJobPostProperty(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdJobPostProperty = createAsyncThunk(
  'jobPostProperty/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getJobPostPropertyById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createJobPostProperty = createAsyncThunk(
  'jobPostProperty/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createJobPostPropertyApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateJobPostProperty = createAsyncThunk(
  'jobPostProperty/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateJobPostPropertyApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeJobPostProperty = createAsyncThunk(
  'jobPostProperty/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteJobPostPropertyApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const jobPostPropertySlice = createSlice({
  name: 'jobPostProperty',
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
      .addCase(fetchAllJobPostProperty.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllJobPostProperty.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllJobPostProperty.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdJobPostProperty.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdJobPostProperty.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdJobPostProperty.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createJobPostProperty.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createJobPostProperty.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createJobPostProperty.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateJobPostProperty.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateJobPostProperty.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.propertyId === action.payload.propertyId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateJobPostProperty.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeJobPostProperty.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeJobPostProperty.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.propertyId !== action.meta.arg);
      })
      .addCase(removeJobPostProperty.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = jobPostPropertySlice.actions;
export default jobPostPropertySlice.reducer;