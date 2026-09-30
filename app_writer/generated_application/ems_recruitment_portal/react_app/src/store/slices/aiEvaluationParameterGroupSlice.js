import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllAiEvaluationParameterGroup,
  getAiEvaluationParameterGroupById,
  createAiEvaluationParameterGroup as createAiEvaluationParameterGroupApi,
  updateAiEvaluationParameterGroup as updateAiEvaluationParameterGroupApi,
  deleteAiEvaluationParameterGroup as deleteAiEvaluationParameterGroupApi,
} from '../../services/aiEvaluationParameterGroupService';


export const fetchAllAiEvaluationParameterGroup = createAsyncThunk(
  'aiEvaluationParameterGroup/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllAiEvaluationParameterGroup(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdAiEvaluationParameterGroup = createAsyncThunk(
  'aiEvaluationParameterGroup/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getAiEvaluationParameterGroupById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createAiEvaluationParameterGroup = createAsyncThunk(
  'aiEvaluationParameterGroup/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createAiEvaluationParameterGroupApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateAiEvaluationParameterGroup = createAsyncThunk(
  'aiEvaluationParameterGroup/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateAiEvaluationParameterGroupApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeAiEvaluationParameterGroup = createAsyncThunk(
  'aiEvaluationParameterGroup/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteAiEvaluationParameterGroupApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const aiEvaluationParameterGroupSlice = createSlice({
  name: 'aiEvaluationParameterGroup',
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
      .addCase(fetchAllAiEvaluationParameterGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllAiEvaluationParameterGroup.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllAiEvaluationParameterGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdAiEvaluationParameterGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdAiEvaluationParameterGroup.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdAiEvaluationParameterGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createAiEvaluationParameterGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createAiEvaluationParameterGroup.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createAiEvaluationParameterGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateAiEvaluationParameterGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateAiEvaluationParameterGroup.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.groupId === action.payload.groupId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateAiEvaluationParameterGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeAiEvaluationParameterGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeAiEvaluationParameterGroup.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.groupId !== action.meta.arg);
      })
      .addCase(removeAiEvaluationParameterGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = aiEvaluationParameterGroupSlice.actions;
export default aiEvaluationParameterGroupSlice.reducer;