import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllJobApplication,
  getJobApplicationById,
  createJobApplication as createJobApplicationApi,
  updateJobApplication as updateJobApplicationApi,
  deleteJobApplication as deleteJobApplicationApi,
} from '../../services/jobApplicationService';


export const fetchAllJobApplication = createAsyncThunk(
  'jobApplication/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllJobApplication(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdJobApplication = createAsyncThunk(
  'jobApplication/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getJobApplicationById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createJobApplication = createAsyncThunk(
  'jobApplication/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createJobApplicationApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateJobApplication = createAsyncThunk(
  'jobApplication/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateJobApplicationApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeJobApplication = createAsyncThunk(
  'jobApplication/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteJobApplicationApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const jobApplicationSlice = createSlice({
  name: 'jobApplication',
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
      .addCase(fetchAllJobApplication.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllJobApplication.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllJobApplication.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdJobApplication.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdJobApplication.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdJobApplication.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createJobApplication.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createJobApplication.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createJobApplication.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateJobApplication.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateJobApplication.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.applicationId === action.payload.applicationId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateJobApplication.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeJobApplication.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeJobApplication.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.applicationId !== action.meta.arg);
      })
      .addCase(removeJobApplication.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = jobApplicationSlice.actions;
export default jobApplicationSlice.reducer;