import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllMarketTrendInstitutionLink,
  getMarketTrendInstitutionLinkById,
  createMarketTrendInstitutionLink as createMarketTrendInstitutionLinkApi,
  updateMarketTrendInstitutionLink as updateMarketTrendInstitutionLinkApi,
  deleteMarketTrendInstitutionLink as deleteMarketTrendInstitutionLinkApi,
} from '../../services/marketTrendInstitutionLinkService';


export const fetchAllMarketTrendInstitutionLink = createAsyncThunk(
  'marketTrendInstitutionLink/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllMarketTrendInstitutionLink(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdMarketTrendInstitutionLink = createAsyncThunk(
  'marketTrendInstitutionLink/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getMarketTrendInstitutionLinkById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createMarketTrendInstitutionLink = createAsyncThunk(
  'marketTrendInstitutionLink/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createMarketTrendInstitutionLinkApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateMarketTrendInstitutionLink = createAsyncThunk(
  'marketTrendInstitutionLink/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateMarketTrendInstitutionLinkApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeMarketTrendInstitutionLink = createAsyncThunk(
  'marketTrendInstitutionLink/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteMarketTrendInstitutionLinkApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const marketTrendInstitutionLinkSlice = createSlice({
  name: 'marketTrendInstitutionLink',
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
      .addCase(fetchAllMarketTrendInstitutionLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllMarketTrendInstitutionLink.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllMarketTrendInstitutionLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdMarketTrendInstitutionLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdMarketTrendInstitutionLink.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdMarketTrendInstitutionLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createMarketTrendInstitutionLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createMarketTrendInstitutionLink.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createMarketTrendInstitutionLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateMarketTrendInstitutionLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateMarketTrendInstitutionLink.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.linkId === action.payload.linkId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateMarketTrendInstitutionLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeMarketTrendInstitutionLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeMarketTrendInstitutionLink.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.linkId !== action.meta.arg);
      })
      .addCase(removeMarketTrendInstitutionLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = marketTrendInstitutionLinkSlice.actions;
export default marketTrendInstitutionLinkSlice.reducer;