import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {
  getAllCommunityPostLink,
  getCommunityPostLinkById,
  createCommunityPostLink as createCommunityPostLinkApi,
  updateCommunityPostLink as updateCommunityPostLinkApi,
  deleteCommunityPostLink as deleteCommunityPostLinkApi,
} from '../../services/communityPostLinkService';


export const fetchAllCommunityPostLink = createAsyncThunk(
  'communityPostLink/fetchAll',
  async (params, { rejectWithValue }) => {
    try {
      return await getAllCommunityPostLink(params);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const fetchByIdCommunityPostLink = createAsyncThunk(
  'communityPostLink/fetchById',
  async (id, { rejectWithValue }) => {
    try {
      return await getCommunityPostLinkById(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const createCommunityPostLink = createAsyncThunk(
  'communityPostLink/create',
  async (data, { rejectWithValue }) => {
    try {
      return await createCommunityPostLinkApi(data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const updateCommunityPostLink = createAsyncThunk(
  'communityPostLink/update',
  async ({ id, data }, { rejectWithValue }) => {
    try {
      return await updateCommunityPostLinkApi(id, data);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);



export const removeCommunityPostLink = createAsyncThunk(
  'communityPostLink/delete',
  async (id, { rejectWithValue }) => {
    try {
      return await deleteCommunityPostLinkApi(id);
    } catch (error) {
      return rejectWithValue(error.response?.data || error.message);
    }
  }
);


const communityPostLinkSlice = createSlice({
  name: 'communityPostLink',
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
      .addCase(fetchAllCommunityPostLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchAllCommunityPostLink.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.content || action.payload;
        state.totalCount = action.payload.totalElements || 0;
        state.currentPage = action.payload.number || 0;
      })
      .addCase(fetchAllCommunityPostLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(fetchByIdCommunityPostLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(fetchByIdCommunityPostLink.fulfilled, (state, action) => { state.loading = false; state.selectedItem = action.payload; })
      .addCase(fetchByIdCommunityPostLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(createCommunityPostLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(createCommunityPostLink.fulfilled, (state, action) => { state.loading = false; state.items.push(action.payload); })
      .addCase(createCommunityPostLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(updateCommunityPostLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(updateCommunityPostLink.fulfilled, (state, action) => {
        state.loading = false;
        const idx = state.items.findIndex((i) => i.linkId === action.payload.linkId);
        if (idx !== -1) state.items[idx] = action.payload;
        state.selectedItem = action.payload;
      })
      .addCase(updateCommunityPostLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });

    builder
      .addCase(removeCommunityPostLink.pending, (state) => { state.loading = true; state.error = null; })
      .addCase(removeCommunityPostLink.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter((i) => i.linkId !== action.meta.arg);
      })
      .addCase(removeCommunityPostLink.rejected, (state, action) => { state.loading = false; state.error = action.payload; });
  },
});

export const { clearError, clearSelectedItem } = communityPostLinkSlice.actions;
export default communityPostLinkSlice.reducer;