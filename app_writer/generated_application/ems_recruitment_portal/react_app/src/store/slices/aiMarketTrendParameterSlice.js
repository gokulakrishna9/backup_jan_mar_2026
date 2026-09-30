import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllAiMarketTrendParameter,
  getAiMarketTrendParameterById,
  createAiMarketTrendParameter as createAiMarketTrendParameterApi,
  updateAiMarketTrendParameter as updateAiMarketTrendParameterApi,
  deleteAiMarketTrendParameter as deleteAiMarketTrendParameterApi,
} from '../../services/aiMarketTrendParameterService';


export const fetchAllAiMarketTrendParameter = createAsyncThunk(
  'aiMarketTrendParameter/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllAiMarketTrendParameter(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdAiMarketTrendParameter = createAsyncThunk(
  'aiMarketTrendParameter/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getAiMarketTrendParameterById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createAiMarketTrendParameter = createAsyncThunk(
  'aiMarketTrendParameter/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createAiMarketTrendParameterApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateAiMarketTrendParameter = createAsyncThunk(
  'aiMarketTrendParameter/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateAiMarketTrendParameterApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeAiMarketTrendParameter = createAsyncThunk(
  'aiMarketTrendParameter/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteAiMarketTrendParameterApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const aiMarketTrendParameterSlice = createSlice({
  name: 'aiMarketTrendParameter',
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
      .addCase(fetchAllAiMarketTrendParameter.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllAiMarketTrendParameter.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllAiMarketTrendParameter.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdAiMarketTrendParameter.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdAiMarketTrendParameter.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdAiMarketTrendParameter.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createAiMarketTrendParameter.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createAiMarketTrendParameter.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createAiMarketTrendParameter.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateAiMarketTrendParameter.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateAiMarketTrendParameter.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.parameterId === action.payload.parameterId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateAiMarketTrendParameter.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeAiMarketTrendParameter.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeAiMarketTrendParameter.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.parameterId !== action.meta.arg);
      })
      .addCase(removeAiMarketTrendParameter.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = aiMarketTrendParameterSlice.actions;
export default aiMarketTrendParameterSlice.reducer;