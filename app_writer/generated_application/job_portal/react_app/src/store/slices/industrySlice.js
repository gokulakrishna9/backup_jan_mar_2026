import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllIndustry,
  getIndustryById,
  createIndustry as createIndustryApi,
  updateIndustry as updateIndustryApi,
  deleteIndustry as deleteIndustryApi,
} from '../../services/industryService';


export const fetchAllIndustry = createAsyncThunk(
  'industry/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllIndustry(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdIndustry = createAsyncThunk(
  'industry/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getIndustryById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createIndustry = createAsyncThunk(
  'industry/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createIndustryApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateIndustry = createAsyncThunk(
  'industry/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateIndustryApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeIndustry = createAsyncThunk(
  'industry/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteIndustryApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const industrySlice = createSlice({
  name: 'industry',
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
      .addCase(fetchAllIndustry.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllIndustry.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllIndustry.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdIndustry.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdIndustry.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdIndustry.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createIndustry.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createIndustry.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createIndustry.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateIndustry.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateIndustry.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.industryId === action.payload.industryId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateIndustry.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeIndustry.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeIndustry.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.industryId !== action.meta.arg);
      })
      .addCase(removeIndustry.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = industrySlice.actions;
export default industrySlice.reducer;