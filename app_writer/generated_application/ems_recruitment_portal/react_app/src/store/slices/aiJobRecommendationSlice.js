import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllAiJobRecommendation,
  getAiJobRecommendationById,
  createAiJobRecommendation as createAiJobRecommendationApi,
  updateAiJobRecommendation as updateAiJobRecommendationApi,
  deleteAiJobRecommendation as deleteAiJobRecommendationApi,
} from '../../services/aiJobRecommendationService';


export const fetchAllAiJobRecommendation = createAsyncThunk(
  'aiJobRecommendation/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllAiJobRecommendation(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdAiJobRecommendation = createAsyncThunk(
  'aiJobRecommendation/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getAiJobRecommendationById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createAiJobRecommendation = createAsyncThunk(
  'aiJobRecommendation/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createAiJobRecommendationApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateAiJobRecommendation = createAsyncThunk(
  'aiJobRecommendation/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateAiJobRecommendationApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeAiJobRecommendation = createAsyncThunk(
  'aiJobRecommendation/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteAiJobRecommendationApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const aiJobRecommendationSlice = createSlice({
  name: 'aiJobRecommendation',
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
      .addCase(fetchAllAiJobRecommendation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllAiJobRecommendation.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllAiJobRecommendation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdAiJobRecommendation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdAiJobRecommendation.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdAiJobRecommendation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createAiJobRecommendation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createAiJobRecommendation.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createAiJobRecommendation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateAiJobRecommendation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateAiJobRecommendation.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.preferenceId === action.payload.preferenceId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateAiJobRecommendation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeAiJobRecommendation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeAiJobRecommendation.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.preferenceId !== action.meta.arg);
      })
      .addCase(removeAiJobRecommendation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = aiJobRecommendationSlice.actions;
export default aiJobRecommendationSlice.reducer;