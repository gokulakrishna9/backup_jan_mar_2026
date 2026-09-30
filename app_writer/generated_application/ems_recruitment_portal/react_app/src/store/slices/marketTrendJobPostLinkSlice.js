import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllMarketTrendJobPostLink,
  getMarketTrendJobPostLinkById,
  createMarketTrendJobPostLink as createMarketTrendJobPostLinkApi,
  updateMarketTrendJobPostLink as updateMarketTrendJobPostLinkApi,
  deleteMarketTrendJobPostLink as deleteMarketTrendJobPostLinkApi,
} from '../../services/marketTrendJobPostLinkService';


export const fetchAllMarketTrendJobPostLink = createAsyncThunk(
  'marketTrendJobPostLink/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllMarketTrendJobPostLink(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdMarketTrendJobPostLink = createAsyncThunk(
  'marketTrendJobPostLink/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getMarketTrendJobPostLinkById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createMarketTrendJobPostLink = createAsyncThunk(
  'marketTrendJobPostLink/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createMarketTrendJobPostLinkApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateMarketTrendJobPostLink = createAsyncThunk(
  'marketTrendJobPostLink/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateMarketTrendJobPostLinkApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeMarketTrendJobPostLink = createAsyncThunk(
  'marketTrendJobPostLink/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteMarketTrendJobPostLinkApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const marketTrendJobPostLinkSlice = createSlice({
  name: 'marketTrendJobPostLink',
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
      .addCase(fetchAllMarketTrendJobPostLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllMarketTrendJobPostLink.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllMarketTrendJobPostLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdMarketTrendJobPostLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdMarketTrendJobPostLink.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdMarketTrendJobPostLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createMarketTrendJobPostLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createMarketTrendJobPostLink.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createMarketTrendJobPostLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateMarketTrendJobPostLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateMarketTrendJobPostLink.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.linkId === action.payload.linkId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateMarketTrendJobPostLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeMarketTrendJobPostLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeMarketTrendJobPostLink.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.linkId !== action.meta.arg);
      })
      .addCase(removeMarketTrendJobPostLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = marketTrendJobPostLinkSlice.actions;
export default marketTrendJobPostLinkSlice.reducer;