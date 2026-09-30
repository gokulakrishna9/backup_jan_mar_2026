import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllAiCommunityPostEvaluation,
  getAiCommunityPostEvaluationById,
  createAiCommunityPostEvaluation as createAiCommunityPostEvaluationApi,
  updateAiCommunityPostEvaluation as updateAiCommunityPostEvaluationApi,
  deleteAiCommunityPostEvaluation as deleteAiCommunityPostEvaluationApi,
} from '../../services/aiCommunityPostEvaluationService';


export const fetchAllAiCommunityPostEvaluation = createAsyncThunk(
  'aiCommunityPostEvaluation/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllAiCommunityPostEvaluation(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdAiCommunityPostEvaluation = createAsyncThunk(
  'aiCommunityPostEvaluation/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getAiCommunityPostEvaluationById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createAiCommunityPostEvaluation = createAsyncThunk(
  'aiCommunityPostEvaluation/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createAiCommunityPostEvaluationApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateAiCommunityPostEvaluation = createAsyncThunk(
  'aiCommunityPostEvaluation/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateAiCommunityPostEvaluationApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeAiCommunityPostEvaluation = createAsyncThunk(
  'aiCommunityPostEvaluation/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteAiCommunityPostEvaluationApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const aiCommunityPostEvaluationSlice = createSlice({
  name: 'aiCommunityPostEvaluation',
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
      .addCase(fetchAllAiCommunityPostEvaluation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllAiCommunityPostEvaluation.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllAiCommunityPostEvaluation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdAiCommunityPostEvaluation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdAiCommunityPostEvaluation.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdAiCommunityPostEvaluation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createAiCommunityPostEvaluation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createAiCommunityPostEvaluation.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createAiCommunityPostEvaluation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateAiCommunityPostEvaluation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateAiCommunityPostEvaluation.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.evaluationId === action.payload.evaluationId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateAiCommunityPostEvaluation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeAiCommunityPostEvaluation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeAiCommunityPostEvaluation.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.evaluationId !== action.meta.arg);
      })
      .addCase(removeAiCommunityPostEvaluation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = aiCommunityPostEvaluationSlice.actions;
export default aiCommunityPostEvaluationSlice.reducer;