import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllCommunity,
  getCommunityById,
  createCommunity as createCommunityApi,
  updateCommunity as updateCommunityApi,
  deleteCommunity as deleteCommunityApi,
} from '../../services/communityService';


export const fetchAllCommunity = createAsyncThunk(
  'community/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllCommunity(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdCommunity = createAsyncThunk(
  'community/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getCommunityById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createCommunity = createAsyncThunk(
  'community/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createCommunityApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateCommunity = createAsyncThunk(
  'community/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateCommunityApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeCommunity = createAsyncThunk(
  'community/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteCommunityApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const communitySlice = createSlice({
  name: 'community',
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
      .addCase(fetchAllCommunity.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllCommunity.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllCommunity.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdCommunity.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdCommunity.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdCommunity.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createCommunity.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createCommunity.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createCommunity.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateCommunity.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateCommunity.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.communityId === action.payload.communityId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateCommunity.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeCommunity.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeCommunity.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.communityId !== action.meta.arg);
      })
      .addCase(removeCommunity.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = communitySlice.actions;
export default communitySlice.reducer;