import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllAiMarketTrendParameterGroup,
  getAiMarketTrendParameterGroupById,
  createAiMarketTrendParameterGroup as createAiMarketTrendParameterGroupApi,
  updateAiMarketTrendParameterGroup as updateAiMarketTrendParameterGroupApi,
  deleteAiMarketTrendParameterGroup as deleteAiMarketTrendParameterGroupApi,
} from '../../services/aiMarketTrendParameterGroupService';


export const fetchAllAiMarketTrendParameterGroup = createAsyncThunk(
  'aiMarketTrendParameterGroup/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllAiMarketTrendParameterGroup(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdAiMarketTrendParameterGroup = createAsyncThunk(
  'aiMarketTrendParameterGroup/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getAiMarketTrendParameterGroupById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createAiMarketTrendParameterGroup = createAsyncThunk(
  'aiMarketTrendParameterGroup/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createAiMarketTrendParameterGroupApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateAiMarketTrendParameterGroup = createAsyncThunk(
  'aiMarketTrendParameterGroup/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateAiMarketTrendParameterGroupApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeAiMarketTrendParameterGroup = createAsyncThunk(
  'aiMarketTrendParameterGroup/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteAiMarketTrendParameterGroupApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const aiMarketTrendParameterGroupSlice = createSlice({
  name: 'aiMarketTrendParameterGroup',
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
      .addCase(fetchAllAiMarketTrendParameterGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllAiMarketTrendParameterGroup.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllAiMarketTrendParameterGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdAiMarketTrendParameterGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdAiMarketTrendParameterGroup.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdAiMarketTrendParameterGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createAiMarketTrendParameterGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createAiMarketTrendParameterGroup.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createAiMarketTrendParameterGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateAiMarketTrendParameterGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateAiMarketTrendParameterGroup.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.groupId === action.payload.groupId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateAiMarketTrendParameterGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeAiMarketTrendParameterGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeAiMarketTrendParameterGroup.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.groupId !== action.meta.arg);
      })
      .addCase(removeAiMarketTrendParameterGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = aiMarketTrendParameterGroupSlice.actions;
export default aiMarketTrendParameterGroupSlice.reducer;