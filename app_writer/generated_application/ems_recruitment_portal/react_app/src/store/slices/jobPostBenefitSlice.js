import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllJobPostBenefit,
  getJobPostBenefitById,
  createJobPostBenefit as createJobPostBenefitApi,
  updateJobPostBenefit as updateJobPostBenefitApi,
  deleteJobPostBenefit as deleteJobPostBenefitApi,
} from '../../services/jobPostBenefitService';


export const fetchAllJobPostBenefit = createAsyncThunk(
  'jobPostBenefit/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllJobPostBenefit(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdJobPostBenefit = createAsyncThunk(
  'jobPostBenefit/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getJobPostBenefitById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createJobPostBenefit = createAsyncThunk(
  'jobPostBenefit/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createJobPostBenefitApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateJobPostBenefit = createAsyncThunk(
  'jobPostBenefit/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateJobPostBenefitApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeJobPostBenefit = createAsyncThunk(
  'jobPostBenefit/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteJobPostBenefitApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const jobPostBenefitSlice = createSlice({
  name: 'jobPostBenefit',
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
      .addCase(fetchAllJobPostBenefit.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllJobPostBenefit.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllJobPostBenefit.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdJobPostBenefit.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdJobPostBenefit.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdJobPostBenefit.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createJobPostBenefit.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createJobPostBenefit.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createJobPostBenefit.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateJobPostBenefit.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateJobPostBenefit.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.benefitId === action.payload.benefitId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateJobPostBenefit.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeJobPostBenefit.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeJobPostBenefit.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.benefitId !== action.meta.arg);
      })
      .addCase(removeJobPostBenefit.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = jobPostBenefitSlice.actions;
export default jobPostBenefitSlice.reducer;