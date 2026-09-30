import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllJobTitle,
  getJobTitleById,
  createJobTitle as createJobTitleApi,
  updateJobTitle as updateJobTitleApi,
  deleteJobTitle as deleteJobTitleApi,
} from '../../services/jobTitleService';


export const fetchAllJobTitle = createAsyncThunk(
  'jobTitle/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllJobTitle(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdJobTitle = createAsyncThunk(
  'jobTitle/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getJobTitleById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createJobTitle = createAsyncThunk(
  'jobTitle/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createJobTitleApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateJobTitle = createAsyncThunk(
  'jobTitle/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateJobTitleApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeJobTitle = createAsyncThunk(
  'jobTitle/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteJobTitleApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const jobTitleSlice = createSlice({
  name: 'jobTitle',
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
      .addCase(fetchAllJobTitle.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllJobTitle.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllJobTitle.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdJobTitle.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdJobTitle.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdJobTitle.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createJobTitle.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createJobTitle.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createJobTitle.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateJobTitle.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateJobTitle.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.jobTitleId === action.payload.jobTitleId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateJobTitle.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeJobTitle.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeJobTitle.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.jobTitleId !== action.meta.arg);
      })
      .addCase(removeJobTitle.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = jobTitleSlice.actions;
export default jobTitleSlice.reducer;