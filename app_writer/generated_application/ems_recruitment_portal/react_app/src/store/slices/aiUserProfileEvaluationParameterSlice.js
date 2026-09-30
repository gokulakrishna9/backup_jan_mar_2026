import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllAiUserProfileEvaluationParameter,
  getAiUserProfileEvaluationParameterById,
  createAiUserProfileEvaluationParameter as createAiUserProfileEvaluationParameterApi,
  updateAiUserProfileEvaluationParameter as updateAiUserProfileEvaluationParameterApi,
  deleteAiUserProfileEvaluationParameter as deleteAiUserProfileEvaluationParameterApi,
} from '../../services/aiUserProfileEvaluationParameterService';


export const fetchAllAiUserProfileEvaluationParameter = createAsyncThunk(
  'aiUserProfileEvaluationParameter/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllAiUserProfileEvaluationParameter(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdAiUserProfileEvaluationParameter = createAsyncThunk(
  'aiUserProfileEvaluationParameter/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getAiUserProfileEvaluationParameterById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createAiUserProfileEvaluationParameter = createAsyncThunk(
  'aiUserProfileEvaluationParameter/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createAiUserProfileEvaluationParameterApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateAiUserProfileEvaluationParameter = createAsyncThunk(
  'aiUserProfileEvaluationParameter/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateAiUserProfileEvaluationParameterApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeAiUserProfileEvaluationParameter = createAsyncThunk(
  'aiUserProfileEvaluationParameter/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteAiUserProfileEvaluationParameterApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const aiUserProfileEvaluationParameterSlice = createSlice({
  name: 'aiUserProfileEvaluationParameter',
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
      .addCase(fetchAllAiUserProfileEvaluationParameter.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllAiUserProfileEvaluationParameter.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllAiUserProfileEvaluationParameter.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdAiUserProfileEvaluationParameter.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdAiUserProfileEvaluationParameter.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdAiUserProfileEvaluationParameter.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createAiUserProfileEvaluationParameter.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createAiUserProfileEvaluationParameter.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createAiUserProfileEvaluationParameter.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateAiUserProfileEvaluationParameter.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateAiUserProfileEvaluationParameter.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.parameterId === action.payload.parameterId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateAiUserProfileEvaluationParameter.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeAiUserProfileEvaluationParameter.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeAiUserProfileEvaluationParameter.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.parameterId !== action.meta.arg);
      })
      .addCase(removeAiUserProfileEvaluationParameter.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = aiUserProfileEvaluationParameterSlice.actions;
export default aiUserProfileEvaluationParameterSlice.reducer;