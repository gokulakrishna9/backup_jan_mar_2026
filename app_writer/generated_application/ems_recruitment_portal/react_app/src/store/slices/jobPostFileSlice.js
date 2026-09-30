import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllJobPostFile,
  getJobPostFileById,
  createJobPostFile as createJobPostFileApi,
  updateJobPostFile as updateJobPostFileApi,
  deleteJobPostFile as deleteJobPostFileApi,
} from '../../services/jobPostFileService';


export const fetchAllJobPostFile = createAsyncThunk(
  'jobPostFile/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllJobPostFile(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdJobPostFile = createAsyncThunk(
  'jobPostFile/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getJobPostFileById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createJobPostFile = createAsyncThunk(
  'jobPostFile/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createJobPostFileApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateJobPostFile = createAsyncThunk(
  'jobPostFile/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateJobPostFileApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeJobPostFile = createAsyncThunk(
  'jobPostFile/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteJobPostFileApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const jobPostFileSlice = createSlice({
  name: 'jobPostFile',
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
      .addCase(fetchAllJobPostFile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllJobPostFile.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllJobPostFile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdJobPostFile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdJobPostFile.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdJobPostFile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createJobPostFile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createJobPostFile.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createJobPostFile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateJobPostFile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateJobPostFile.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.fileId === action.payload.fileId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateJobPostFile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeJobPostFile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeJobPostFile.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.fileId !== action.meta.arg);
      })
      .addCase(removeJobPostFile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = jobPostFileSlice.actions;
export default jobPostFileSlice.reducer;