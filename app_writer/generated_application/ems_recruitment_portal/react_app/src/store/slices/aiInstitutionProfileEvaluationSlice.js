import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllAiInstitutionProfileEvaluation,
  getAiInstitutionProfileEvaluationById,
  createAiInstitutionProfileEvaluation as createAiInstitutionProfileEvaluationApi,
  updateAiInstitutionProfileEvaluation as updateAiInstitutionProfileEvaluationApi,
  deleteAiInstitutionProfileEvaluation as deleteAiInstitutionProfileEvaluationApi,
} from '../../services/aiInstitutionProfileEvaluationService';


export const fetchAllAiInstitutionProfileEvaluation = createAsyncThunk(
  'aiInstitutionProfileEvaluation/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllAiInstitutionProfileEvaluation(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdAiInstitutionProfileEvaluation = createAsyncThunk(
  'aiInstitutionProfileEvaluation/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getAiInstitutionProfileEvaluationById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createAiInstitutionProfileEvaluation = createAsyncThunk(
  'aiInstitutionProfileEvaluation/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createAiInstitutionProfileEvaluationApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateAiInstitutionProfileEvaluation = createAsyncThunk(
  'aiInstitutionProfileEvaluation/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateAiInstitutionProfileEvaluationApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeAiInstitutionProfileEvaluation = createAsyncThunk(
  'aiInstitutionProfileEvaluation/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteAiInstitutionProfileEvaluationApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const aiInstitutionProfileEvaluationSlice = createSlice({
  name: 'aiInstitutionProfileEvaluation',
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
      .addCase(fetchAllAiInstitutionProfileEvaluation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllAiInstitutionProfileEvaluation.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllAiInstitutionProfileEvaluation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdAiInstitutionProfileEvaluation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdAiInstitutionProfileEvaluation.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdAiInstitutionProfileEvaluation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createAiInstitutionProfileEvaluation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createAiInstitutionProfileEvaluation.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createAiInstitutionProfileEvaluation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateAiInstitutionProfileEvaluation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateAiInstitutionProfileEvaluation.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.evaluationId === action.payload.evaluationId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateAiInstitutionProfileEvaluation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeAiInstitutionProfileEvaluation.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeAiInstitutionProfileEvaluation.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.evaluationId !== action.meta.arg);
      })
      .addCase(removeAiInstitutionProfileEvaluation.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = aiInstitutionProfileEvaluationSlice.actions;
export default aiInstitutionProfileEvaluationSlice.reducer;