import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllMarketTrendSkillDemand,
  getMarketTrendSkillDemandById,
  createMarketTrendSkillDemand as createMarketTrendSkillDemandApi,
  updateMarketTrendSkillDemand as updateMarketTrendSkillDemandApi,
  deleteMarketTrendSkillDemand as deleteMarketTrendSkillDemandApi,
} from '../../services/marketTrendSkillDemandService';


export const fetchAllMarketTrendSkillDemand = createAsyncThunk(
  'marketTrendSkillDemand/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllMarketTrendSkillDemand(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdMarketTrendSkillDemand = createAsyncThunk(
  'marketTrendSkillDemand/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getMarketTrendSkillDemandById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createMarketTrendSkillDemand = createAsyncThunk(
  'marketTrendSkillDemand/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createMarketTrendSkillDemandApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateMarketTrendSkillDemand = createAsyncThunk(
  'marketTrendSkillDemand/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateMarketTrendSkillDemandApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeMarketTrendSkillDemand = createAsyncThunk(
  'marketTrendSkillDemand/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteMarketTrendSkillDemandApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const marketTrendSkillDemandSlice = createSlice({
  name: 'marketTrendSkillDemand',
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
      .addCase(fetchAllMarketTrendSkillDemand.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllMarketTrendSkillDemand.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllMarketTrendSkillDemand.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdMarketTrendSkillDemand.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdMarketTrendSkillDemand.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdMarketTrendSkillDemand.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createMarketTrendSkillDemand.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createMarketTrendSkillDemand.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createMarketTrendSkillDemand.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateMarketTrendSkillDemand.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateMarketTrendSkillDemand.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.demandId === action.payload.demandId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateMarketTrendSkillDemand.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeMarketTrendSkillDemand.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeMarketTrendSkillDemand.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.demandId !== action.meta.arg);
      })
      .addCase(removeMarketTrendSkillDemand.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = marketTrendSkillDemandSlice.actions;
export default marketTrendSkillDemandSlice.reducer;