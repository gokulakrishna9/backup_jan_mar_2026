import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllJobInterview,
  getJobInterviewById,
  createJobInterview as createJobInterviewApi,
  updateJobInterview as updateJobInterviewApi,
  deleteJobInterview as deleteJobInterviewApi,
} from '../../services/jobInterviewService';


export const fetchAllJobInterview = createAsyncThunk(
  'jobInterview/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllJobInterview(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdJobInterview = createAsyncThunk(
  'jobInterview/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getJobInterviewById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createJobInterview = createAsyncThunk(
  'jobInterview/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createJobInterviewApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateJobInterview = createAsyncThunk(
  'jobInterview/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateJobInterviewApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeJobInterview = createAsyncThunk(
  'jobInterview/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteJobInterviewApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const jobInterviewSlice = createSlice({
  name: 'jobInterview',
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
      .addCase(fetchAllJobInterview.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllJobInterview.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllJobInterview.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdJobInterview.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdJobInterview.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdJobInterview.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createJobInterview.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createJobInterview.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createJobInterview.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateJobInterview.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateJobInterview.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.interviewId === action.payload.interviewId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateJobInterview.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeJobInterview.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeJobInterview.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.interviewId !== action.meta.arg);
      })
      .addCase(removeJobInterview.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = jobInterviewSlice.actions;
export default jobInterviewSlice.reducer;