import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllJobPostRequirement,
  getJobPostRequirementById,
  createJobPostRequirement as createJobPostRequirementApi,
  updateJobPostRequirement as updateJobPostRequirementApi,
  deleteJobPostRequirement as deleteJobPostRequirementApi,
} from '../../services/jobPostRequirementService';


export const fetchAllJobPostRequirement = createAsyncThunk(
  'jobPostRequirement/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllJobPostRequirement(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdJobPostRequirement = createAsyncThunk(
  'jobPostRequirement/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getJobPostRequirementById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createJobPostRequirement = createAsyncThunk(
  'jobPostRequirement/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createJobPostRequirementApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateJobPostRequirement = createAsyncThunk(
  'jobPostRequirement/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateJobPostRequirementApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeJobPostRequirement = createAsyncThunk(
  'jobPostRequirement/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteJobPostRequirementApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const jobPostRequirementSlice = createSlice({
  name: 'jobPostRequirement',
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
      .addCase(fetchAllJobPostRequirement.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllJobPostRequirement.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllJobPostRequirement.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdJobPostRequirement.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdJobPostRequirement.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdJobPostRequirement.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createJobPostRequirement.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createJobPostRequirement.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createJobPostRequirement.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateJobPostRequirement.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateJobPostRequirement.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.requirementId === action.payload.requirementId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateJobPostRequirement.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeJobPostRequirement.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeJobPostRequirement.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.requirementId !== action.meta.arg);
      })
      .addCase(removeJobPostRequirement.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = jobPostRequirementSlice.actions;
export default jobPostRequirementSlice.reducer;