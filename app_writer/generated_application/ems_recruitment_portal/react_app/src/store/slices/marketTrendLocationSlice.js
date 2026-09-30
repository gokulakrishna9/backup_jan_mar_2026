import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllMarketTrendLocation,
  getMarketTrendLocationById,
  createMarketTrendLocation as createMarketTrendLocationApi,
  updateMarketTrendLocation as updateMarketTrendLocationApi,
  deleteMarketTrendLocation as deleteMarketTrendLocationApi,
} from '../../services/marketTrendLocationService';


export const fetchAllMarketTrendLocation = createAsyncThunk(
  'marketTrendLocation/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllMarketTrendLocation(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdMarketTrendLocation = createAsyncThunk(
  'marketTrendLocation/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getMarketTrendLocationById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createMarketTrendLocation = createAsyncThunk(
  'marketTrendLocation/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createMarketTrendLocationApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateMarketTrendLocation = createAsyncThunk(
  'marketTrendLocation/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateMarketTrendLocationApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeMarketTrendLocation = createAsyncThunk(
  'marketTrendLocation/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteMarketTrendLocationApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const marketTrendLocationSlice = createSlice({
  name: 'marketTrendLocation',
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
      .addCase(fetchAllMarketTrendLocation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllMarketTrendLocation.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllMarketTrendLocation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdMarketTrendLocation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdMarketTrendLocation.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdMarketTrendLocation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createMarketTrendLocation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createMarketTrendLocation.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createMarketTrendLocation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateMarketTrendLocation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateMarketTrendLocation.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.locationId === action.payload.locationId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateMarketTrendLocation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeMarketTrendLocation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeMarketTrendLocation.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.locationId !== action.meta.arg);
      })
      .addCase(removeMarketTrendLocation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = marketTrendLocationSlice.actions;
export default marketTrendLocationSlice.reducer;