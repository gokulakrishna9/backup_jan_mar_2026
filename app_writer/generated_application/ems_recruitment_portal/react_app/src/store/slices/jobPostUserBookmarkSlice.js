import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllJobPostUserBookmark,
  getJobPostUserBookmarkById,
  createJobPostUserBookmark as createJobPostUserBookmarkApi,
  updateJobPostUserBookmark as updateJobPostUserBookmarkApi,
  deleteJobPostUserBookmark as deleteJobPostUserBookmarkApi,
} from '../../services/jobPostUserBookmarkService';


export const fetchAllJobPostUserBookmark = createAsyncThunk(
  'jobPostUserBookmark/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllJobPostUserBookmark(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdJobPostUserBookmark = createAsyncThunk(
  'jobPostUserBookmark/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getJobPostUserBookmarkById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createJobPostUserBookmark = createAsyncThunk(
  'jobPostUserBookmark/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createJobPostUserBookmarkApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateJobPostUserBookmark = createAsyncThunk(
  'jobPostUserBookmark/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateJobPostUserBookmarkApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeJobPostUserBookmark = createAsyncThunk(
  'jobPostUserBookmark/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteJobPostUserBookmarkApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const jobPostUserBookmarkSlice = createSlice({
  name: 'jobPostUserBookmark',
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
      .addCase(fetchAllJobPostUserBookmark.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllJobPostUserBookmark.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllJobPostUserBookmark.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdJobPostUserBookmark.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdJobPostUserBookmark.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdJobPostUserBookmark.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createJobPostUserBookmark.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createJobPostUserBookmark.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createJobPostUserBookmark.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateJobPostUserBookmark.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateJobPostUserBookmark.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.bookmarkId === action.payload.bookmarkId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateJobPostUserBookmark.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeJobPostUserBookmark.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeJobPostUserBookmark.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.bookmarkId !== action.meta.arg);
      })
      .addCase(removeJobPostUserBookmark.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = jobPostUserBookmarkSlice.actions;
export default jobPostUserBookmarkSlice.reducer;