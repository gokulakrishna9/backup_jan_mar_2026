import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllMarketTrendIndustry,
  getMarketTrendIndustryById,
  createMarketTrendIndustry as createMarketTrendIndustryApi,
  updateMarketTrendIndustry as updateMarketTrendIndustryApi,
  deleteMarketTrendIndustry as deleteMarketTrendIndustryApi,
} from '../../services/marketTrendIndustryService';


export const fetchAllMarketTrendIndustry = createAsyncThunk(
  'marketTrendIndustry/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllMarketTrendIndustry(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdMarketTrendIndustry = createAsyncThunk(
  'marketTrendIndustry/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getMarketTrendIndustryById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createMarketTrendIndustry = createAsyncThunk(
  'marketTrendIndustry/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createMarketTrendIndustryApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateMarketTrendIndustry = createAsyncThunk(
  'marketTrendIndustry/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateMarketTrendIndustryApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeMarketTrendIndustry = createAsyncThunk(
  'marketTrendIndustry/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteMarketTrendIndustryApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const marketTrendIndustrySlice = createSlice({
  name: 'marketTrendIndustry',
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
      .addCase(fetchAllMarketTrendIndustry.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllMarketTrendIndustry.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllMarketTrendIndustry.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdMarketTrendIndustry.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdMarketTrendIndustry.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdMarketTrendIndustry.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createMarketTrendIndustry.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createMarketTrendIndustry.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createMarketTrendIndustry.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateMarketTrendIndustry.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateMarketTrendIndustry.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.industryId === action.payload.industryId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateMarketTrendIndustry.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeMarketTrendIndustry.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeMarketTrendIndustry.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.industryId !== action.meta.arg);
      })
      .addCase(removeMarketTrendIndustry.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = marketTrendIndustrySlice.actions;
export default marketTrendIndustrySlice.reducer;