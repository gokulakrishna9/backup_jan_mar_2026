import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllJobPosting,
  getJobPostingById,
  createJobPosting as createJobPostingApi,
  updateJobPosting as updateJobPostingApi,
  deleteJobPosting as deleteJobPostingApi,
} from '../../services/jobPostingService';


export const fetchAllJobPosting = createAsyncThunk(
  'jobPosting/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllJobPosting(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdJobPosting = createAsyncThunk(
  'jobPosting/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getJobPostingById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createJobPosting = createAsyncThunk(
  'jobPosting/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createJobPostingApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateJobPosting = createAsyncThunk(
  'jobPosting/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateJobPostingApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeJobPosting = createAsyncThunk(
  'jobPosting/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteJobPostingApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const jobPostingSlice = createSlice({
  name: 'jobPosting',
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
      .addCase(fetchAllJobPosting.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllJobPosting.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllJobPosting.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdJobPosting.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdJobPosting.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdJobPosting.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createJobPosting.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createJobPosting.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createJobPosting.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateJobPosting.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateJobPosting.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.jobPostingId === action.payload.jobPostingId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateJobPosting.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeJobPosting.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeJobPosting.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.jobPostingId !== action.meta.arg);
      })
      .addCase(removeJobPosting.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = jobPostingSlice.actions;
export default jobPostingSlice.reducer;