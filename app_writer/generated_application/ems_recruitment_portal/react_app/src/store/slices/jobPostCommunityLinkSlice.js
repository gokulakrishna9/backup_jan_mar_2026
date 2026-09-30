import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllJobPostCommunityLink,
  getJobPostCommunityLinkById,
  createJobPostCommunityLink as createJobPostCommunityLinkApi,
  updateJobPostCommunityLink as updateJobPostCommunityLinkApi,
  deleteJobPostCommunityLink as deleteJobPostCommunityLinkApi,
} from '../../services/jobPostCommunityLinkService';


export const fetchAllJobPostCommunityLink = createAsyncThunk(
  'jobPostCommunityLink/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllJobPostCommunityLink(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdJobPostCommunityLink = createAsyncThunk(
  'jobPostCommunityLink/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getJobPostCommunityLinkById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createJobPostCommunityLink = createAsyncThunk(
  'jobPostCommunityLink/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createJobPostCommunityLinkApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateJobPostCommunityLink = createAsyncThunk(
  'jobPostCommunityLink/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateJobPostCommunityLinkApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeJobPostCommunityLink = createAsyncThunk(
  'jobPostCommunityLink/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteJobPostCommunityLinkApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const jobPostCommunityLinkSlice = createSlice({
  name: 'jobPostCommunityLink',
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
      .addCase(fetchAllJobPostCommunityLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllJobPostCommunityLink.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllJobPostCommunityLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdJobPostCommunityLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdJobPostCommunityLink.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdJobPostCommunityLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createJobPostCommunityLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createJobPostCommunityLink.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createJobPostCommunityLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateJobPostCommunityLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateJobPostCommunityLink.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.linkId === action.payload.linkId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateJobPostCommunityLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeJobPostCommunityLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeJobPostCommunityLink.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.linkId !== action.meta.arg);
      })
      .addCase(removeJobPostCommunityLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = jobPostCommunityLinkSlice.actions;
export default jobPostCommunityLinkSlice.reducer;