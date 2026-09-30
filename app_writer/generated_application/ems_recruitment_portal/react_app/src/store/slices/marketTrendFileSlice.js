import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllMarketTrendFile,
  getMarketTrendFileById,
  createMarketTrendFile as createMarketTrendFileApi,
  updateMarketTrendFile as updateMarketTrendFileApi,
  deleteMarketTrendFile as deleteMarketTrendFileApi,
} from '../../services/marketTrendFileService';


export const fetchAllMarketTrendFile = createAsyncThunk(
  'marketTrendFile/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllMarketTrendFile(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdMarketTrendFile = createAsyncThunk(
  'marketTrendFile/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getMarketTrendFileById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createMarketTrendFile = createAsyncThunk(
  'marketTrendFile/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createMarketTrendFileApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateMarketTrendFile = createAsyncThunk(
  'marketTrendFile/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateMarketTrendFileApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeMarketTrendFile = createAsyncThunk(
  'marketTrendFile/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteMarketTrendFileApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const marketTrendFileSlice = createSlice({
  name: 'marketTrendFile',
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
      .addCase(fetchAllMarketTrendFile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllMarketTrendFile.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllMarketTrendFile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdMarketTrendFile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdMarketTrendFile.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdMarketTrendFile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createMarketTrendFile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createMarketTrendFile.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createMarketTrendFile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateMarketTrendFile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateMarketTrendFile.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.fileId === action.payload.fileId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateMarketTrendFile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeMarketTrendFile.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeMarketTrendFile.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.fileId !== action.meta.arg);
      })
      .addCase(removeMarketTrendFile.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = marketTrendFileSlice.actions;
export default marketTrendFileSlice.reducer;