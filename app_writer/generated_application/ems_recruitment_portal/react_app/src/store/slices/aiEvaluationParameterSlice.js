import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllAiEvaluationParameter,
  getAiEvaluationParameterById,
  createAiEvaluationParameter as createAiEvaluationParameterApi,
  updateAiEvaluationParameter as updateAiEvaluationParameterApi,
  deleteAiEvaluationParameter as deleteAiEvaluationParameterApi,
} from '../../services/aiEvaluationParameterService';


export const fetchAllAiEvaluationParameter = createAsyncThunk(
  'aiEvaluationParameter/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllAiEvaluationParameter(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdAiEvaluationParameter = createAsyncThunk(
  'aiEvaluationParameter/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getAiEvaluationParameterById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createAiEvaluationParameter = createAsyncThunk(
  'aiEvaluationParameter/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createAiEvaluationParameterApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateAiEvaluationParameter = createAsyncThunk(
  'aiEvaluationParameter/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateAiEvaluationParameterApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeAiEvaluationParameter = createAsyncThunk(
  'aiEvaluationParameter/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteAiEvaluationParameterApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const aiEvaluationParameterSlice = createSlice({
  name: 'aiEvaluationParameter',
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
      .addCase(fetchAllAiEvaluationParameter.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllAiEvaluationParameter.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllAiEvaluationParameter.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdAiEvaluationParameter.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdAiEvaluationParameter.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdAiEvaluationParameter.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createAiEvaluationParameter.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createAiEvaluationParameter.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createAiEvaluationParameter.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateAiEvaluationParameter.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateAiEvaluationParameter.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.parameterId === action.payload.parameterId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateAiEvaluationParameter.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeAiEvaluationParameter.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeAiEvaluationParameter.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.parameterId !== action.meta.arg);
      })
      .addCase(removeAiEvaluationParameter.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = aiEvaluationParameterSlice.actions;
export default aiEvaluationParameterSlice.reducer;