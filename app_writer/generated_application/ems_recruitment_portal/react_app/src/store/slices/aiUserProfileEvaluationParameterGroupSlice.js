import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllAiUserProfileEvaluationParameterGroup,
  getAiUserProfileEvaluationParameterGroupById,
  createAiUserProfileEvaluationParameterGroup as createAiUserProfileEvaluationParameterGroupApi,
  updateAiUserProfileEvaluationParameterGroup as updateAiUserProfileEvaluationParameterGroupApi,
  deleteAiUserProfileEvaluationParameterGroup as deleteAiUserProfileEvaluationParameterGroupApi,
} from '../../services/aiUserProfileEvaluationParameterGroupService';


export const fetchAllAiUserProfileEvaluationParameterGroup = createAsyncThunk(
  'aiUserProfileEvaluationParameterGroup/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllAiUserProfileEvaluationParameterGroup(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdAiUserProfileEvaluationParameterGroup = createAsyncThunk(
  'aiUserProfileEvaluationParameterGroup/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getAiUserProfileEvaluationParameterGroupById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createAiUserProfileEvaluationParameterGroup = createAsyncThunk(
  'aiUserProfileEvaluationParameterGroup/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createAiUserProfileEvaluationParameterGroupApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateAiUserProfileEvaluationParameterGroup = createAsyncThunk(
  'aiUserProfileEvaluationParameterGroup/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateAiUserProfileEvaluationParameterGroupApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeAiUserProfileEvaluationParameterGroup = createAsyncThunk(
  'aiUserProfileEvaluationParameterGroup/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteAiUserProfileEvaluationParameterGroupApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const aiUserProfileEvaluationParameterGroupSlice = createSlice({
  name: 'aiUserProfileEvaluationParameterGroup',
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
      .addCase(fetchAllAiUserProfileEvaluationParameterGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllAiUserProfileEvaluationParameterGroup.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllAiUserProfileEvaluationParameterGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdAiUserProfileEvaluationParameterGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdAiUserProfileEvaluationParameterGroup.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdAiUserProfileEvaluationParameterGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createAiUserProfileEvaluationParameterGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createAiUserProfileEvaluationParameterGroup.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createAiUserProfileEvaluationParameterGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateAiUserProfileEvaluationParameterGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateAiUserProfileEvaluationParameterGroup.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.groupId === action.payload.groupId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateAiUserProfileEvaluationParameterGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeAiUserProfileEvaluationParameterGroup.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeAiUserProfileEvaluationParameterGroup.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.groupId !== action.meta.arg);
      })
      .addCase(removeAiUserProfileEvaluationParameterGroup.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = aiUserProfileEvaluationParameterGroupSlice.actions;
export default aiUserProfileEvaluationParameterGroupSlice.reducer;