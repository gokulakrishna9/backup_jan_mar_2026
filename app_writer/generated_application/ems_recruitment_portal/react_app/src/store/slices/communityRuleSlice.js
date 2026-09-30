import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllCommunityRule,
  getCommunityRuleById,
  createCommunityRule as createCommunityRuleApi,
  updateCommunityRule as updateCommunityRuleApi,
  deleteCommunityRule as deleteCommunityRuleApi,
} from '../../services/communityRuleService';


export const fetchAllCommunityRule = createAsyncThunk(
  'communityRule/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllCommunityRule(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdCommunityRule = createAsyncThunk(
  'communityRule/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getCommunityRuleById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createCommunityRule = createAsyncThunk(
  'communityRule/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createCommunityRuleApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateCommunityRule = createAsyncThunk(
  'communityRule/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateCommunityRuleApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeCommunityRule = createAsyncThunk(
  'communityRule/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteCommunityRuleApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const communityRuleSlice = createSlice({
  name: 'communityRule',
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
      .addCase(fetchAllCommunityRule.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllCommunityRule.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllCommunityRule.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdCommunityRule.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdCommunityRule.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdCommunityRule.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createCommunityRule.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createCommunityRule.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createCommunityRule.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateCommunityRule.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateCommunityRule.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.ruleId === action.payload.ruleId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateCommunityRule.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeCommunityRule.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeCommunityRule.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.ruleId !== action.meta.arg);
      })
      .addCase(removeCommunityRule.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = communityRuleSlice.actions;
export default communityRuleSlice.reducer;