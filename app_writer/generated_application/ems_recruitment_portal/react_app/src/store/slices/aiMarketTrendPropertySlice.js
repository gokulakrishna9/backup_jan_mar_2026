import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllAiMarketTrendProperty,
  getAiMarketTrendPropertyById,
  createAiMarketTrendProperty as createAiMarketTrendPropertyApi,
  updateAiMarketTrendProperty as updateAiMarketTrendPropertyApi,
  deleteAiMarketTrendProperty as deleteAiMarketTrendPropertyApi,
} from '../../services/aiMarketTrendPropertyService';


export const fetchAllAiMarketTrendProperty = createAsyncThunk(
  'aiMarketTrendProperty/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllAiMarketTrendProperty(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdAiMarketTrendProperty = createAsyncThunk(
  'aiMarketTrendProperty/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getAiMarketTrendPropertyById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createAiMarketTrendProperty = createAsyncThunk(
  'aiMarketTrendProperty/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createAiMarketTrendPropertyApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateAiMarketTrendProperty = createAsyncThunk(
  'aiMarketTrendProperty/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateAiMarketTrendPropertyApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeAiMarketTrendProperty = createAsyncThunk(
  'aiMarketTrendProperty/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteAiMarketTrendPropertyApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const aiMarketTrendPropertySlice = createSlice({
  name: 'aiMarketTrendProperty',
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
      .addCase(fetchAllAiMarketTrendProperty.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllAiMarketTrendProperty.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllAiMarketTrendProperty.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdAiMarketTrendProperty.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdAiMarketTrendProperty.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdAiMarketTrendProperty.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createAiMarketTrendProperty.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createAiMarketTrendProperty.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createAiMarketTrendProperty.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateAiMarketTrendProperty.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateAiMarketTrendProperty.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.trendId === action.payload.trendId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateAiMarketTrendProperty.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeAiMarketTrendProperty.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeAiMarketTrendProperty.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.trendId !== action.meta.arg);
      })
      .addCase(removeAiMarketTrendProperty.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = aiMarketTrendPropertySlice.actions;
export default aiMarketTrendPropertySlice.reducer;