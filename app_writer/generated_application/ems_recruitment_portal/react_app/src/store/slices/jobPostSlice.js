import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllJobPost,
  getJobPostById,
  createJobPost as createJobPostApi,
  updateJobPost as updateJobPostApi,
  deleteJobPost as deleteJobPostApi,
} from '../../services/jobPostService';


export const fetchAllJobPost = createAsyncThunk(
  'jobPost/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllJobPost(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdJobPost = createAsyncThunk(
  'jobPost/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getJobPostById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createJobPost = createAsyncThunk(
  'jobPost/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createJobPostApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateJobPost = createAsyncThunk(
  'jobPost/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateJobPostApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeJobPost = createAsyncThunk(
  'jobPost/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteJobPostApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const jobPostSlice = createSlice({
  name: 'jobPost',
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
      .addCase(fetchAllJobPost.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllJobPost.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllJobPost.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdJobPost.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdJobPost.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdJobPost.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createJobPost.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createJobPost.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createJobPost.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateJobPost.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateJobPost.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.jobPostId === action.payload.jobPostId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateJobPost.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeJobPost.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeJobPost.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.jobPostId !== action.meta.arg);
      })
      .addCase(removeJobPost.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = jobPostSlice.actions;
export default jobPostSlice.reducer;