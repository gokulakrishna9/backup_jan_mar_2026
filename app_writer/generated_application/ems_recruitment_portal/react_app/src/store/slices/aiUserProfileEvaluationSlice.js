import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllAiUserProfileEvaluation,
  getAiUserProfileEvaluationById,
  createAiUserProfileEvaluation as createAiUserProfileEvaluationApi,
  updateAiUserProfileEvaluation as updateAiUserProfileEvaluationApi,
  deleteAiUserProfileEvaluation as deleteAiUserProfileEvaluationApi,
} from '../../services/aiUserProfileEvaluationService';


export const fetchAllAiUserProfileEvaluation = createAsyncThunk(
  'aiUserProfileEvaluation/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllAiUserProfileEvaluation(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdAiUserProfileEvaluation = createAsyncThunk(
  'aiUserProfileEvaluation/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getAiUserProfileEvaluationById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createAiUserProfileEvaluation = createAsyncThunk(
  'aiUserProfileEvaluation/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createAiUserProfileEvaluationApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateAiUserProfileEvaluation = createAsyncThunk(
  'aiUserProfileEvaluation/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateAiUserProfileEvaluationApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeAiUserProfileEvaluation = createAsyncThunk(
  'aiUserProfileEvaluation/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteAiUserProfileEvaluationApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const aiUserProfileEvaluationSlice = createSlice({
  name: 'aiUserProfileEvaluation',
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
      .addCase(fetchAllAiUserProfileEvaluation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllAiUserProfileEvaluation.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllAiUserProfileEvaluation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdAiUserProfileEvaluation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdAiUserProfileEvaluation.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdAiUserProfileEvaluation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createAiUserProfileEvaluation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createAiUserProfileEvaluation.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createAiUserProfileEvaluation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateAiUserProfileEvaluation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateAiUserProfileEvaluation.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.evaluationId === action.payload.evaluationId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateAiUserProfileEvaluation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeAiUserProfileEvaluation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeAiUserProfileEvaluation.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.evaluationId !== action.meta.arg);
      })
      .addCase(removeAiUserProfileEvaluation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = aiUserProfileEvaluationSlice.actions;
export default aiUserProfileEvaluationSlice.reducer;