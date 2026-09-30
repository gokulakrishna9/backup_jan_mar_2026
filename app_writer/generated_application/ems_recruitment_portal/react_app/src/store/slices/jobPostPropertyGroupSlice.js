import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllJobPostPropertyGroup,
  getJobPostPropertyGroupById,
  createJobPostPropertyGroup as createJobPostPropertyGroupApi,
  updateJobPostPropertyGroup as updateJobPostPropertyGroupApi,
  deleteJobPostPropertyGroup as deleteJobPostPropertyGroupApi,
} from '../../services/jobPostPropertyGroupService';


export const fetchAllJobPostPropertyGroup = createAsyncThunk(
  'jobPostPropertyGroup/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllJobPostPropertyGroup(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdJobPostPropertyGroup = createAsyncThunk(
  'jobPostPropertyGroup/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getJobPostPropertyGroupById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createJobPostPropertyGroup = createAsyncThunk(
  'jobPostPropertyGroup/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createJobPostPropertyGroupApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateJobPostPropertyGroup = createAsyncThunk(
  'jobPostPropertyGroup/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateJobPostPropertyGroupApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeJobPostPropertyGroup = createAsyncThunk(
  'jobPostPropertyGroup/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteJobPostPropertyGroupApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const jobPostPropertyGroupSlice = createSlice({
  name: 'jobPostPropertyGroup',
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
      .addCase(fetchAllJobPostPropertyGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllJobPostPropertyGroup.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllJobPostPropertyGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdJobPostPropertyGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdJobPostPropertyGroup.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdJobPostPropertyGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createJobPostPropertyGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createJobPostPropertyGroup.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createJobPostPropertyGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateJobPostPropertyGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateJobPostPropertyGroup.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.groupId === action.payload.groupId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateJobPostPropertyGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeJobPostPropertyGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeJobPostPropertyGroup.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.groupId !== action.meta.arg);
      })
      .addCase(removeJobPostPropertyGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = jobPostPropertyGroupSlice.actions;
export default jobPostPropertyGroupSlice.reducer;