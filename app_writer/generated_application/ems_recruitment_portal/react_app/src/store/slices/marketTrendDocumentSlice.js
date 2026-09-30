import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllMarketTrendDocument,
  getMarketTrendDocumentById,
  createMarketTrendDocument as createMarketTrendDocumentApi,
  updateMarketTrendDocument as updateMarketTrendDocumentApi,
  deleteMarketTrendDocument as deleteMarketTrendDocumentApi,
} from '../../services/marketTrendDocumentService';


export const fetchAllMarketTrendDocument = createAsyncThunk(
  'marketTrendDocument/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllMarketTrendDocument(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdMarketTrendDocument = createAsyncThunk(
  'marketTrendDocument/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getMarketTrendDocumentById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createMarketTrendDocument = createAsyncThunk(
  'marketTrendDocument/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createMarketTrendDocumentApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateMarketTrendDocument = createAsyncThunk(
  'marketTrendDocument/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateMarketTrendDocumentApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeMarketTrendDocument = createAsyncThunk(
  'marketTrendDocument/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteMarketTrendDocumentApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const marketTrendDocumentSlice = createSlice({
  name: 'marketTrendDocument',
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
      .addCase(fetchAllMarketTrendDocument.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllMarketTrendDocument.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllMarketTrendDocument.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdMarketTrendDocument.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdMarketTrendDocument.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdMarketTrendDocument.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createMarketTrendDocument.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createMarketTrendDocument.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createMarketTrendDocument.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateMarketTrendDocument.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateMarketTrendDocument.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.documentId === action.payload.documentId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateMarketTrendDocument.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeMarketTrendDocument.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeMarketTrendDocument.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.documentId !== action.meta.arg);
      })
      .addCase(removeMarketTrendDocument.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = marketTrendDocumentSlice.actions;
export default marketTrendDocumentSlice.reducer;